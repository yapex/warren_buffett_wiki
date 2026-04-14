"""
Meilisearch 搜索封装 — 替代 buffett-rag 倒排索引

提供与 rag/config.py 兼容的搜索接口：
- search_paragraphs(): 段落级搜索
- search_concept_timeline(): 概念时间线
- search_concept_in_doc(): 文档内搜索
"""
import os
import re
import time
from pathlib import Path
from typing import Optional

import meilisearch

# 配置（从 .env.meilisearch 读取）
_MEILI_URL = os.environ.get("MEILI_URL", "http://127.0.0.1:7700")
_MEILI_KEY = os.environ.get("MEILI_MASTER_KEY", "meilisearch-buffett-wiki-key")
_INDEX_UID = os.environ.get("MEILI_INDEX_UID", "buffett-wiki")

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
WIKI_DIR = PROJECT_ROOT / "wiki"


def _get_client() -> meilisearch.Client:
    return meilisearch.Client(_MEILI_URL, _MEILI_KEY)


def _get_index():
    return _get_client().get_index(_INDEX_UID)


def _normalize_path(path_or_doc_id: str) -> str:
    """标准化文档路径/ID，去掉 wiki/ 前缀"""
    if path_or_doc_id.startswith("wiki/"):
        path_or_doc_id = path_or_doc_id[5:]
    return path_or_doc_id


def search_paragraphs(query: str, top_k: int = 10, doc_filter: Optional[str] = None) -> list[dict]:
    """
    搜索 Wiki 文档（兼容 rag/config.py 接口）

    Args:
        query: 搜索关键词
        top_k: 返回结果数量
        doc_filter: 文档类型过滤（如 "letters", "concepts"）

    Returns:
        [{"para_id", "doc_id", "content", "year", "score", "matched_tokens", "jump_url", "source"}]
    """
    index = _get_index()

    params = {
        "hitsPerPage": top_k,
        "attributesToCrop": ["content"],
        "cropLength": 500,
        "attributesToHighlight": ["title", "content"],
        "showMatchesPosition": True,
    }

    # 过滤
    filters = []
    if doc_filter:
        filters.append(f"doc_type = '{doc_filter}'")
    if filters:
        params["filter"] = " AND ".join(filters)

    results = index.search(query, params)

    output = []
    for hit in results["hits"]:
        doc_path = hit.get("path", "")
        doc_type = hit.get("doc_type", "")

        # 生成跳转链接
        jump_url = f"./wiki/{doc_path}"

        # 提取格式化内容（带高亮）
        formatted = hit.get("_formatted", {})
        content = formatted.get("content", hit.get("content", ""))[:500]

        # 提取匹配位置
        matches_info = hit.get("_matchesPosition", {})
        matched_fields = list(matches_info.keys())

        output.append({
            "para_id": hit["id"],
            "doc_id": f"wiki/{doc_path}",
            "content": content,
            "year": hit.get("year", ""),
            "score": hit.get("_rankingScore", 0),
            "matched_tokens": matched_fields,
            "jump_url": jump_url,
            "source": str(WIKI_DIR / doc_path),
            "title": hit.get("title", ""),
            "doc_type": doc_type,
            "tags": hit.get("tags", []),
        })

    return output


def search_concept_timeline(concept: str, top_k: int = 20) -> list[dict]:
    """
    概念时间线搜索（按年份排序）

    Args:
        concept: 概念名称（如"内在价值"、"安全边际"）
        top_k: 返回结果数量

    Returns:
        [{"year", "doc_id", "para_id", "content", "jump_url", "matched_tokens"}]
    """
    index = _get_index()

    # 扩大搜索范围，然后按年份排序
    results = index.search(
        concept,
        {
            "sort": ["year_sort:asc"],
            "hitsPerPage": min(top_k * 3, 100),  # 扩大范围
            "attributesToCrop": ["content"],
            "cropLength": 300,
        },
    )

    # 客户端按 year_sort 排序（Meilisearch 的 sort 只是 tiebreaker）
    sorted_hits = sorted(
        results["hits"],
        key=lambda h: h.get("year_sort") or 9999
    )

    # 按年份去重（同一年只取最相关的）
    timeline = []
    seen_years = set()
    for hit in sorted_hits:
        year = hit.get("year", "")
        if year and year not in seen_years:
            seen_years.add(year)
            doc_path = hit.get("path", "")
            timeline.append({
                "year": year,
                "doc_id": f"wiki/{doc_path}",
                "para_id": hit["id"],
                "content": hit.get("content", "")[:300],
                "jump_url": f"./wiki/{doc_path}",
                "matched_tokens": [concept],
                "title": hit.get("title", ""),
                "doc_type": hit.get("doc_type", ""),
            })

    return timeline[:top_k]


def search_concept_in_doc(concept: str, doc_id: str, top_k: int = 5) -> list[dict]:
    """
    在指定文档中搜索概念

    Args:
        concept: 概念名称
        doc_id: 文档ID（如 "wiki/concepts/安全边际.md"）
        top_k: 返回结果数量

    Returns:
        [{"para_id", "content", "para_index", "score", "matched_tokens", "jump_url"}]
    """
    index = _get_index()

    # 标准化 doc_id -> path
    path = _normalize_path(doc_id)
    # doc_id 可能是 "wiki/filename.md" 格式，但 path 字段是相对 wiki/ 的
    # 也可能是 "wiki/research/cases/xxx.md" 格式

    # 尝试用文件名匹配
    filename = Path(path).name

    # 先尝试精确 path 过滤
    results = index.search(
        concept,
        {
            "filter": f"path = '{path}'",
            "hitsPerPage": top_k,
            "attributesToCrop": ["content"],
            "cropLength": 500,
            "showMatchesPosition": True,
        },
    )

    # 如果没找到，尝试用文件名匹配
    if not results["hits"] and "/" in path:
        results = index.search(
            concept,
            {
                "filter": f"path = '{filename}'",
                "hitsPerPage": top_k,
                "attributesToCrop": ["content"],
                "cropLength": 500,
            },
        )

    # 如果还没找到，只用文件名做 path ends with 匹配
    if not results["hits"]:
        results = index.search(
            concept,
            {
                "filter": f"path ENDS WITH '{filename}'",
                "hitsPerPage": top_k,
                "attributesToCrop": ["content"],
                "cropLength": 500,
            },
        )

    output = []
    for i, hit in enumerate(results["hits"]):
        doc_path = hit.get("path", "")
        output.append({
            "para_id": hit["id"],
            "content": hit.get("_formatted", {}).get("content", hit.get("content", ""))[:500],
            "para_index": i,
            "score": hit.get("_rankingScore", 0),
            "matched_tokens": [concept],
            "jump_url": f"./wiki/{doc_path}",
        })

    return output[:top_k]


def get_concept_quote_timeline(concept: str) -> list[dict]:
    """
    获取概念的原文引用时间线（用于批量生成）

    Returns:
        [{"year", "quote", "source", "jump_link"}]
    """
    timeline = search_concept_timeline(concept, top_k=50)
    quotes = []

    for item in timeline:
        content = item["content"]
        # 找到句号截断
        sentences = re.split(r'(?<=[。！？.!?])', content)
        quote = sentences[0][:200] if sentences else content[:200]

        quotes.append({
            "year": item["year"],
            "quote": quote,
            "source": item["doc_id"],
            "jump_link": item["jump_url"],
        })

    return quotes


# ============ 高级功能 ============

def search_with_filters(
    query: str,
    year_from: Optional[str] = None,
    year_to: Optional[str] = None,
    doc_type: Optional[str] = None,
    tags: Optional[list[str]] = None,
    top_k: int = 10,
) -> list[dict]:
    """
    带过滤的搜索（Meilisearch 独有功能）

    Args:
        query: 搜索关键词
        year_from: 起始年份
        year_to: 结束年份
        doc_type: 文档类型 (companies/concepts/cases/letters/people)
        tags: 标签过滤
        top_k: 返回结果数量
    """
    index = _get_index()

    filters = []
    if year_from:
        filters.append(f"year >= '{year_from}'")
    if year_to:
        filters.append(f"year <= '{year_to}'")
    if doc_type:
        filters.append(f"doc_type = '{doc_type}'")
    if tags:
        tag_filters = [f"tags = '{tag}'" for tag in tags]
        filters.append(f"[{' AND '.join(tag_filters)}]")

    params = {
        "hitsPerPage": top_k,
        "attributesToCrop": ["content"],
        "cropLength": 500,
        "attributesToHighlight": ["title", "content"],
    }
    if filters:
        params["filter"] = " AND ".join(filters)

    results = index.search(query, params)

    output = []
    for hit in results["hits"]:
        doc_path = hit.get("path", "")
        output.append({
            "para_id": hit["id"],
            "doc_id": f"wiki/{doc_path}",
            "content": hit.get("_formatted", {}).get("content", hit.get("content", ""))[:500],
            "year": hit.get("year", ""),
            "score": hit.get("_rankingScore", 0),
            "jump_url": f"./wiki/{doc_path}",
            "title": hit.get("title", ""),
            "doc_type": hit.get("doc_type", ""),
            "tags": hit.get("tags", []),
        })

    return output


def get_facets(field: str = "doc_type") -> dict:
    """
    获取分面统计（Meilisearch 独有功能）

    Args:
        field: 分面字段 (doc_type, year, tags)

    Returns:
        {value: count}
    """
    index = _get_index()
    results = index.search("", {
        "facets": [field],
        "hitsPerPage": 0,
    })
    return results.get("facetDistribution", {}).get(field, {})


def benchmark(queries: list[str] = None) -> dict:
    """
    性能基准测试
    """
    if queries is None:
        queries = ["安全边际", "护城河", "可口可乐", "巴菲特", "内在价值",
                    "Berkshire", "保险浮存金", "能力圈"]

    index = _get_index()
    times = []
    results_summary = {}

    for query in queries:
        start = time.time()
        results = index.search(query, {"hitsPerPage": 10})
        elapsed_ms = (time.time() - start) * 1000
        times.append(elapsed_ms)
        total = results.get('estimatedTotalHits', len(results['hits']))
        results_summary[query] = {
            "time_ms": round(elapsed_ms, 2),
            "total_hits": total,
        }

    avg = sum(times) / len(times)
    max_t = max(times)
    min_t = min(times)

    return {
        "queries": results_summary,
        "avg_ms": round(avg, 2),
        "max_ms": round(max_t, 2),
        "min_ms": round(min_t, 2),
        "total_queries": len(queries),
    }
