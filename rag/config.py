"""
增强 RAG 配置 - 段落级检索 + 概念时间线 + 跳转链接
"""
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Optional

# 路径配置
PACKAGE_DIR = Path(__file__).parent  # rag/
PROJECT_ROOT = PACKAGE_DIR.parent     # 项目根目录
INDEX_DIR = PROJECT_ROOT / ".rag"     # .rag/ (隐藏，存储索引)
RAW_ZH_DIR = PROJECT_ROOT / "raw/berkshire/zh"
RAW_EN_DIR = PROJECT_ROOT / "raw/berkshire/en"
RAW_PARTNERSHIP_DIR = PROJECT_ROOT / "raw/partnership/zh"
WIKI_DIR = PROJECT_ROOT / "wiki"

# 全局索引
PARAGRAPHS = {}  # {para_id: {"doc_id": str, "index": int, "content": str, "tokens": set}}
PARA_BY_DOC = defaultdict(list)  # {doc_id: [para_id]}
INVERTED_INDEX = defaultdict(list)  # {word: [para_id]}
DOCUMENTS = {}  # {doc_id: {"source": str, "type": str, "year": Optional[int]}}
DOC_TYPE_PATTERNS = {
    "wiki": ("wiki", None)
}

def tokenize(text: str) -> list[str]:
    """中文分词（简单版）"""
    tokens = re.findall(r'[\w]+', text.lower())
    chinese = re.findall(r'[\u4e00-\u9fff]+', text)
    for chars in chinese:
        tokens.extend(list(chars))
    return tokens

def extract_year(filename: str, doc_type: str) -> Optional[int]:
    """从文件名提取年份"""
    if doc_type == "wiki":
        match = re.search(r'(\d{4})', filename)
        if match:
            return int(match.group(1))
    return None

def split_paragraphs(content: str) -> list[str]:
    """将文本分割为段落，保持段落完整性"""
    # 先按双换行分割
    blocks = content.split('\n\n')
    paragraphs = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # 如果段落太长，进一步分割
        if len(block) > 800:
            # 按单换行或句子分割
            sentences = re.split(r'(?<=[。！？.!?])\s+', block)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) > 600:
                    if current:
                        paragraphs.append(current.strip())
                    current = sent
                else:
                    current += sent if not current else " " + sent
            if current.strip():
                paragraphs.append(current.strip())
        else:
            paragraphs.append(block)
    return paragraphs

def build_paragraph_index():
    """构建段落级索引"""
    global PARAGRAPHS, PARA_BY_DOC, INVERTED_INDEX, DOCUMENTS
    
    PARAGRAPHS.clear()
    PARA_BY_DOC.clear()
    INVERTED_INDEX.clear()
    DOCUMENTS.clear()
    
    para_counter = 0
    
    def index_file(filepath: Path, doc_type: str) -> None:
        """索引单个文件"""
        nonlocal para_counter
        doc_id = f"{doc_type}/{filepath.name}"
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取纯文本内容（去掉 HTML 标签）
        if filepath.suffix == '.html':
            content = re.sub(r'<[^>]+>', ' ', content)
        
        year = extract_year(filepath.name, doc_type)
        DOCUMENTS[doc_id] = {
            "source": str(filepath),
            "type": doc_type,
            "year": year,
            "content": content
        }
        
        # 段落级索引
        paragraphs = split_paragraphs(content)
        para_ids = []
        for idx, para in enumerate(paragraphs):
            if len(para) < 20:  # 跳过太短的段落
                continue
            para_id = f"{doc_id}#p{idx}"
            tokens = set(tokenize(para))
            PARAGRAPHS[para_id] = {
                "doc_id": doc_id,
                "index": idx,
                "content": para,
                "tokens": tokens,
                "year": year
            }
            para_ids.append(para_id)
            
            # 倒排索引
            for token in tokens:
                if len(token) >= 1:  # 包含单字
                    INVERTED_INDEX[token].append(para_id)
            
            para_counter += 1
        
        PARA_BY_DOC[doc_id] = para_ids
    
    # 索引 Wiki 页面（raw/ 不直接索引，需先编译为 wiki 页面）
    for f in WIKI_DIR.glob("**/*.md"):
        index_file(f, "wiki")
    
    print(f"✅ 已索引 {len(DOCUMENTS)} 个文档, {para_counter} 个段落")

def save_paragraph_index():
    """保存段落索引"""
    # 保存文档元数据
    doc_meta = {
        doc_id: {
            "source": doc["source"],
            "type": doc["type"],
            "year": doc.get("year")
        }
        for doc_id, doc in DOCUMENTS.items()
    }
    with open(INDEX_DIR / "docs.json", 'w', encoding='utf-8') as f:
        json.dump(doc_meta, f, ensure_ascii=False)
    
    # 保存段落元数据（不包含content，节省空间）
    para_meta = {
        para_id: {
            "doc_id": p["doc_id"],
            "index": p["index"],
            "year": p.get("year")
        }
        for para_id, p in PARAGRAPHS.items()
    }
    with open(INDEX_DIR / "paragraphs_meta.json", 'w', encoding='utf-8') as f:
        json.dump(para_meta, f, ensure_ascii=False)
    
    # 保存段落内容
    para_content = {
        para_id: p["content"]
        for para_id, p in PARAGRAPHS.items()
    }
    with open(INDEX_DIR / "paragraphs_content.json", 'w', encoding='utf-8') as f:
        json.dump(para_content, f, ensure_ascii=False)
    
    # 保存倒排索引
    inv_index = {k: list(set(v)) for k, v in INVERTED_INDEX.items()}
    with open(INDEX_DIR / "inverted_index.json", 'w', encoding='utf-8') as f:
        json.dump(inv_index, f, ensure_ascii=False)
    
    print(f"💾 已保存索引到磁盘")

def load_paragraph_index() -> bool:
    """加载段落索引"""
    global PARAGRAPHS, DOCUMENTS, INVERTED_INDEX
    
    docs_file = INDEX_DIR / "docs.json"
    para_meta_file = INDEX_DIR / "paragraphs_meta.json"
    para_content_file = INDEX_DIR / "paragraphs_content.json"
    inv_file = INDEX_DIR / "inverted_index.json"
    
    if not all(f.exists() for f in [docs_file, para_meta_file, para_content_file, inv_file]):
        return False
    
    try:
        with open(docs_file, 'r', encoding='utf-8') as f:
            DOCUMENTS = json.load(f)
        
        with open(para_meta_file, 'r', encoding='utf-8') as f:
            para_meta = json.load(f)
        
        with open(para_content_file, 'r', encoding='utf-8') as f:
            para_content = json.load(f)
        
        with open(inv_file, 'r', encoding='utf-8') as f:
            INVERTED_INDEX = defaultdict(list, json.load(f))
        
        # 重建段落索引
        for para_id, meta in para_meta.items():
            PARAGRAPHS[para_id] = {
                "doc_id": meta["doc_id"],
                "index": meta["index"],
                "year": meta.get("year"),
                "content": para_content.get(para_id, ""),
                "tokens": set(tokenize(para_content.get(para_id, "")))
            }
        
        print(f"📂 已加载 {len(DOCUMENTS)} 个文档, {len(PARAGRAPHS)} 个段落")
        return True
    except Exception as e:
        print(f"⚠️ 加载索引失败: {e}")
        return False

def search_paragraphs(query: str, top_k: int = 10, doc_filter: Optional[str] = None) -> list[dict]:
    """
    段落级搜索
    
    Args:
        query: 查询文本
        top_k: 返回前 k 个结果
        doc_filter: 可选，限定搜索的文档类型 (wiki, 等)
    
    Returns:
        [{"para_id": str, "doc_id": str, "content": str, "year": int, "score": float, "jump_url": str}]
    """
    global PARAGRAPHS, INVERTED_INDEX, DOCUMENTS
    
    if not PARAGRAPHS:
        if not load_paragraph_index():
            build_paragraph_index()
    
    query_tokens = set(tokenize(query))
    
    # 找出包含查询词的段落
    para_scores = defaultdict(lambda: {"score": 0, "matched_tokens": set()})
    for token in query_tokens:
        for para_id in INVERTED_INDEX.get(token, []):
            p = PARAGRAPHS.get(para_id)
            if not p:
                continue
            # 文档类型过滤
            if doc_filter:
                doc_id = p["doc_id"]
                if not doc_id.startswith(doc_filter):
                    continue
            para_scores[para_id]["score"] += 1
            para_scores[para_id]["matched_tokens"].add(token)
    
    # 排序并返回 top_k
    results = []
    for para_id, data in sorted(para_scores.items(), key=lambda x: -x[1]["score"])[:top_k]:
        p = PARAGRAPHS[para_id]
        doc_id = p["doc_id"]
        doc = DOCUMENTS.get(doc_id, {})
        
        # 生成跳转链接
        jump_url = generate_jump_link(doc_id, p["index"], doc.get("type", ""))
        
        results.append({
            "para_id": para_id,
            "doc_id": doc_id,
            "content": p["content"][:500],  # 截取前500字符
            "year": p.get("year"),
            "score": data["score"],
            "matched_tokens": list(data["matched_tokens"]),
            "jump_url": jump_url,
            "source": doc.get("source", "")
        })
    
    return results

def generate_jump_link(doc_id: str, para_index: int, doc_type: str) -> str:
    """
    生成跳转链接
    
    Args:
        doc_id: 文档ID，格式 "type/filename"
        para_index: 段落索引
        doc_type: 文档类型
    
    Returns:
        跳转链接字符串，格式为 "#year-para-N" 或带文件路径的链接
    """
    # 从 doc_id 提取年份信息
    year_match = re.search(r'(\d{4})', doc_id)
    year = year_match.group(1) if year_match else ""
    
    # 现在只有 wiki 类型
    if doc_type == "wiki":
        filename = doc_id.split("/")[-1]
        return f"./wiki/{filename}#p{para_index}"
    else:
        return f"{doc_id}#p{para_index}"

def search_concept_timeline(concept: str, top_k: int = 20) -> list[dict]:
    """
    搜索概念在所有信件中的时间线
    
    Args:
        concept: 概念名称（如"内在价值"、"安全边际"）
        top_k: 返回结果数量
    
    Returns:
        [{"year": int, "doc_id": str, "para_id": str, "content": str, "jump_url": str}]
    """
    results = search_paragraphs(concept, top_k=top_k * 2, doc_filter=None)
    
    # 按年份分组并排序
    timeline = []
    seen = set()  # 去重
    
    for r in results:
        year = r.get("year")
        if year and r["doc_id"] not in seen:
            seen.add(r["doc_id"])
            timeline.append({
                "year": year,
                "doc_id": r["doc_id"],
                "para_id": r["para_id"],
                "content": r["content"][:300],
                "jump_url": r["jump_url"],
                "matched_tokens": r["matched_tokens"]
            })
    
    # 按年份排序
    timeline.sort(key=lambda x: x["year"])
    return timeline[:top_k]

def search_concept_in_doc(concept: str, doc_id: str, top_k: int = 5) -> list[dict]:
    """
    在指定文档中搜索概念
    
    Args:
        concept: 概念名称
        doc_id: 文档ID，格式 "type/filename"
        top_k: 返回结果数量
    
    Returns:
        [{"para_id": str, "content": str, "para_index": int, "jump_url": str}]
    """
    global PARAGRAPHS, DOCUMENTS
    
    if not PARAGRAPHS:
        if not load_paragraph_index():
            build_paragraph_index()
    
    if doc_id not in DOCUMENTS:
        return []
    
    query_tokens = set(tokenize(concept))
    results = []
    
    # 搜索该文档中的所有段落
    for para_id, p in PARAGRAPHS.items():
        if p["doc_id"] != doc_id:
            continue
        
        # 计算匹配分数
        matched = p["tokens"] & query_tokens
        if matched:
            results.append({
                "para_id": para_id,
                "content": p["content"][:500],
                "para_index": p["index"],
                "score": len(matched),
                "matched_tokens": list(matched),
                "jump_url": generate_jump_link(doc_id, p["index"], DOCUMENTS[doc_id].get("type", ""))
            })
    
    # 按分数排序
    results.sort(key=lambda x: -x["score"])
    return results[:top_k]

def get_concept_quote_timeline(concept: str) -> list[dict]:
    """
    获取概念的原文引用时间线（用于批量生成）
    
    Returns:
        [{"year": int, "quote": str, "source": str, "jump_link": str}]
    """
    timeline = search_concept_timeline(concept, top_k=50)
    quotes = []
    
    for item in timeline:
        # 提取关键引用（取前200字符）
        content = item["content"]
        # 找到句号或合适的位置截断
        sentences = re.split(r'(?<=[。！？.!?])', content)
        quote = sentences[0][:200] if sentences else content[:200]
        
        quotes.append({
            "year": item["year"],
            "quote": quote,
            "source": item["doc_id"],
            "jump_link": item["jump_url"]
        })
    
    return quotes

# 初始化
if not load_paragraph_index():
    build_paragraph_index()
    save_paragraph_index()
