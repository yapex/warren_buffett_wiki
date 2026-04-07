"""
快速 RAG 配置 - 使用关键词搜索
"""
import json
import re
from pathlib import Path
from collections import defaultdict

# 路径配置
WORKING_DIR = Path("rag")
WIKI_DIR = Path("wiki/letters")
RAW_ZH_DIR = Path("raw/berkshire/zh")
RAW_EN_DIR = Path("raw/berkshire/en")

# 倒排索引
INVERTED_INDEX = defaultdict(list)  # {word: [(doc_id, position)]}
DOCUMENTS = {}  # {doc_id: {"source": str, "content": str}}

def tokenize(text: str) -> list[str]:
    """中文分词（简单版）"""
    # 中英文分词
    tokens = re.findall(r'[\w]+', text.lower())
    # 中文单字
    chinese = re.findall(r'[\u4e00-\u9fff]+', text)
    for chars in chinese:
        tokens.extend(list(chars))
    return tokens

def build_index():
    """构建索引"""
    global DOCUMENTS, INVERTED_INDEX
    
    DOCS = {}
    
    # 索引 Wiki 信件
    for letter_file in WIKI_DIR.glob("*.md"):
        doc_id = f"wiki/{letter_file.name}"
        with open(letter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tokens = tokenize(content)
        DOCS[doc_id] = {
            "source": str(letter_file),
            "content": content,
            "tokens": set(tokens),
            "token_count": len(tokens)
        }
        
        # 倒排索引
        for token in set(tokens):
            INVERTED_INDEX[token].append(doc_id)
    
    DOCUMENTS = DOCS
    
    # 保存索引
    save_index()
    print(f"✅ 已索引 {len(DOCS)} 个文档")

def save_index():
    """保存索引"""
    # 只保存元数据
    meta = {
        doc_id: {
            "source": doc["source"],
            "token_count": doc["token_count"]
        }
        for doc_id, doc in DOCUMENTS.items()
    }
    
    with open(WORKING_DIR / "index.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False)
    
    # 保存倒排索引
    inv_index = {k: list(set(v)) for k, v in INVERTED_INDEX.items()}
    with open(WORKING_DIR / "inverted_index.json", 'w', encoding='utf-8') as f:
        json.dump(inv_index, f, ensure_ascii=False)

def load_index():
    """加载索引"""
    global DOCUMENTS, INVERTED_INDEX
    
    meta_file = WORKING_DIR / "index.json"
    inv_file = WORKING_DIR / "inverted_index.json"
    
    if not meta_file.exists() or not inv_file.exists():
        return False
    
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    with open(inv_file, 'r', encoding='utf-8') as f:
        INVERTED_INDEX = defaultdict(list, json.load(f))
    
    # 重新加载文档内容
    for doc_id, info in meta.items():
        source = Path(info["source"])
        if source.exists():
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            DOCUMENTS[doc_id] = {
                "source": str(source),
                "content": content,
                "tokens": set(tokenize(content)),
                "token_count": info["token_count"]
            }
    
    return len(DOCUMENTS) > 0

def search(query: str, top_k: int = 5) -> list[dict]:
    """搜索"""
    global DOCUMENTS, INVERTED_INDEX
    
    if not DOCUMENTS:
        if not load_index():
            build_index()
    
    query_tokens = set(tokenize(query))
    
    # 找出包含查询词的文档
    doc_scores = defaultdict(float)
    for token in query_tokens:
        for doc_id in INVERTED_INDEX.get(token, []):
            # 词频作为分数
            if doc_id in DOCUMENTS:
                doc_scores[doc_id] += 1
    
    # 排序
    results = []
    for doc_id, score in sorted(doc_scores.items(), key=lambda x: -x[1])[:top_k]:
        doc = DOCUMENTS[doc_id]
        # 提取片段
        chunks = [c.strip() for c in doc["content"].split('\n\n') if c.strip()]
        relevant = []
        for chunk in chunks:
            if any(t in chunk for t in query_tokens):
                relevant.append(chunk[:300])
                if len(relevant) >= 2:
                    break
        
        results.append({
            "doc_id": doc_id,
            "source": doc["source"],
            "score": score,
            "chunks": relevant
        })
    
    return results

# 初始化
if not load_index():
    build_index()
