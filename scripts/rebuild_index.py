#!/usr/bin/env python3
"""
Meilisearch 索引全量重建

用途：
- 首次初始化索引
- 定期维护（如每周一次）
- 修复索引数据问题

用法：
    uv run python scripts/rebuild_index.py
"""
import hashlib
import re
import json
import time
from pathlib import Path

import meilisearch

# 配置
MEILI_URL = "http://127.0.0.1:7700"
MEILI_KEY = "meilisearch-buffett-wiki-key"
INDEX_UID = "buffett-wiki"
WIKI_DIR = Path("/Users/yapex/workspace/warren_buffett_wiki/wiki")

def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    fm = {}
    if not content.startswith("---"):
        return fm
    parts = content.split("---", 2)
    if len(parts) < 3:
        return fm
    yaml_text = parts[1].strip()
    for line in yaml_text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # 解析 YAML 列表（简单版：tags: [a, b, c]）
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",") if v.strip()]
            fm[key] = value
        elif line.startswith("- ") and fm:
            # 多行列表项，追加到最后一个 key
            last_key = list(fm.keys())[-1]
            val = line[2:].strip().strip('"').strip("'")
            if isinstance(fm[last_key], list):
                fm[last_key].append(val)
            else:
                fm[last_key] = [fm[last_key], val]
    return fm


def extract_title(content: str) -> str:
    """提取第一个 H1 标题"""
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_year_from_frontmatter(fm: dict) -> str:
    """从 frontmatter 提取年份"""
    # 优先使用 year 字段
    year = fm.get("year", "")
    if year:
        # 可能是范围如 "1962-1965"，取第一个年份
        match = re.search(r'(\d{4})', str(year))
        return match.group(1) if match else str(year)
    # 其次使用 first_appeared
    first = fm.get("first_appeared", "")
    if first:
        match = re.search(r'(\d{4})', str(first))
        return match.group(1) if match else str(first)
    return ""


def extract_year_from_path(filepath: Path) -> str:
    """从文件路径/文件名中提取年份"""
    match = re.search(r'(\d{4})', filepath.name)
    return match.group(1) if match else ""


def get_doc_type(filepath: Path, wiki_dir: Path) -> str:
    """确定文档类型（基于 wiki/ 下的子目录）"""
    rel = filepath.relative_to(wiki_dir)
    parts = rel.parts
    if len(parts) >= 2:
        top_dir = parts[0]
        # research/cases -> cases
        if top_dir == "research" and len(parts) >= 3:
            return parts[1]  # e.g., "cases"
        return top_dir  # e.g., "companies", "concepts", "letters"
    return "unknown"


def load_wiki_documents() -> list[dict]:
    """加载所有 Wiki 文档"""
    documents = []

    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        if md_file.name == "index.md":
            continue

        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        title = extract_title(content)
        year = extract_year_from_frontmatter(fm) or extract_year_from_path(md_file)
        doc_type = get_doc_type(md_file, WIKI_DIR)

        # 相对路径（相对于 wiki/）
        file_path = str(md_file.relative_to(WIKI_DIR))

        # 生成唯一 ID（基于路径的 MD5，避免中文问题）
        doc_id = hashlib.md5(file_path.encode("utf-8")).hexdigest()[:16]

        # 处理 tags
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        # year_sort: 数字类型，用于排序（取年份范围的起始年）
        year_sort = None
        if year:
            m = re.search(r'(\d{4})', str(year))
            if m:
                year_sort = int(m.group(1))

        # 构建文档
        doc = {
            "id": doc_id,
            "title": title,
            "content": content,
            "year": year,
            "year_sort": year_sort,
            "doc_type": doc_type,
            "tags": tags,
            "path": file_path,
            "created_at": int(md_file.stat().st_mtime),
        }
        documents.append(doc)

    return documents


def migrate():
    """执行迁移"""
    print("=" * 60)
    print("Step 3: 数据迁移")
    print("=" * 60)

    # 连接 Meilisearch
    client = meilisearch.Client(MEILI_URL, MEILI_KEY)
    health = client.health()
    print(f"\n✅ Meilisearch 连接成功：{health['status']}")

    index = client.get_index(INDEX_UID)

    # 加载文档
    print(f"\n📂 加载 Wiki 文档...")
    documents = load_wiki_documents()
    print(f"   加载了 {len(documents)} 个文档")

    # 统计
    type_counts = {}
    for doc in documents:
        dt = doc["doc_type"]
        type_counts[dt] = type_counts.get(dt, 0) + 1
    print(f"\n   文档类型分布:")
    for dt, count in sorted(type_counts.items()):
        print(f"     {dt}: {count}")

    # 清除旧数据（全量重建）
    print(f"\n🗑️  清除旧数据...")
    task = index.delete_all_documents()
    client.wait_for_task(task.task_uid)
    print(f"   ✅ 旧数据已清除")

    # 分批索引
    print(f"\n📤 索引文档...")
    batch_size = 50
    total_batches = (len(documents) + batch_size - 1) // batch_size
    last_task = None

    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        batch_num = i // batch_size + 1
        task = index.add_documents(batch)
        last_task = task
        print(f"   批次 {batch_num}/{total_batches}: {len(batch)} 个文档 (task_uid={task.task_uid})")

    # 等待最后一个批次完成
    if last_task:
        print(f"\n⏳ 等待索引完成...")
        result = client.wait_for_task(last_task.task_uid)
        if result.status == "succeeded":
            print(f"   ✅ 索引完成")
        else:
            print(f"   ❌ 索引失败: {result.error}")
            return

    # 验证
    print(f"\n📊 验证索引...")
    stats = index.get_stats()
    print(f"   文档数: {stats.number_of_documents}")
    print(f"   索引已完成: {not stats.is_indexing}")

    # 快速搜索测试
    print(f"\n🔍 快速搜索测试...")
    test_queries = ["安全边际", "护城河", "可口可乐", "巴菲特"]
    for query in test_queries:
        results = index.search(query, {"hitsPerPage": 3})
        top = results["hits"][0]["title"] if results["hits"] else "无结果"
        total = results.get('estimatedTotalHits', results.get('totalHits', len(results['hits'])))
        print(f"   '{query}': {total} 个结果, top1 = {top}")

    print(f"\n{'=' * 60}")
    print(f"✅ Step 3 完成！{len(documents)} 个文档已成功迁移")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    migrate()
