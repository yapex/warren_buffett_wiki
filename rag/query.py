#!/usr/bin/env python3
"""
增强 RAG 查询脚本 - 支持段落级检索、概念时间线、跳转链接
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    search_paragraphs,
    search_concept_timeline,
    search_concept_in_doc,
    get_concept_quote_timeline,
    DOCUMENTS,
    PARAGRAPHS,
    build_paragraph_index,
    save_paragraph_index
)

def format_results(results: list, verbose: bool = False):
    """格式化搜索结果"""
    for i, r in enumerate(results, 1):
        year_info = f"[{r['year']}]" if r.get('year') else ""
        print(f"\n📄 结果 {i}: {year_info} {r['doc_id']}")
        print(f"   匹配度: {r['score']} 个词")
        if r.get('matched_tokens'):
            print(f"   匹配词: {', '.join(r['matched_tokens'][:5])}")
        print(f"   内容: {r['content'][:200]}...")
        if verbose:
            print(f"   跳转: {r['jump_url']}")

def show_timeline(results: list):
    """格式化时间线结果"""
    print("\n📅 概念时间线:")
    print("=" * 60)
    for r in results:
        year = r.get('year', 'N/A')
        content_preview = r['content'][:100].replace('\n', ' ')
        print(f"\n[{year}]")
        print(f"  {content_preview}...")
        print(f"  🔗 {r['jump_url']}")

def show_doc_results(results: list, doc_id: str):
    """格式化文档内搜索结果"""
    print(f"\n📖 在 {doc_id} 中搜索结果:")
    print("=" * 60)
    for i, r in enumerate(results, 1):
        print(f"\n段落 {i} (索引: {r['para_index']}):")
        print(f"  {r['content'][:150]}...")
        print(f"  🔗 {r['jump_url']}")

def rebuild_index():
    """重建索引"""
    print("🔨 正在重建段落索引...")
    build_paragraph_index()
    save_paragraph_index()
    print("✅ 索引重建完成")

def export_timeline_json(concept: str, output_file: str = None):
    """导出概念时间线为 JSON"""
    timeline = get_concept_quote_timeline(concept)
    output = {
        "concept": concept,
        "timeline": timeline
    }
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"💾 已导出到 {output_file}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) < 2:
        usage()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "search" or cmd == "s":
        # 普通搜索
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else input("输入查询: ")
        results = search_paragraphs(query, top_k=5)
        print(f"\n🔍 搜索: {query}")
        print("=" * 60)
        format_results(results, verbose=True)
    
    elif cmd == "timeline" or cmd == "t":
        # 概念时间线搜索
        concept = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else input("输入概念: ")
        results = search_concept_timeline(concept, top_k=20)
        print(f"\n📅 概念时间线: {concept}")
        show_timeline(results)
    
    elif cmd == "doc" or cmd == "d":
        # 文档内搜索
        if len(sys.argv) < 4:
            print("用法: query.py doc <概念> <文档ID>")
            print("示例: query.py doc 安全边际 berkshire_zh/1988-letter-zh.md")
            return
        concept = sys.argv[2]
        doc_id = sys.argv[3]
        results = search_concept_in_doc(concept, doc_id, top_k=5)
        show_doc_results(results, doc_id)
    
    elif cmd == "export" or cmd == "e":
        # 导出时间线为 JSON
        if len(sys.argv) < 3:
            print("用法: query.py export <概念> [输出文件]")
            return
        concept = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        export_timeline_json(concept, output)
    
    elif cmd == "rebuild" or cmd == "r":
        # 重建索引
        rebuild_index()
    
    elif cmd in ("help", "h", "--help"):
        usage()
    
    else:
        # 默认当作搜索
        query = " ".join(sys.argv[1:])
        results = search_paragraphs(query, top_k=5)
        print(f"\n🔍 搜索: {query}")
        format_results(results)

def usage():
    print("""
📚 Buffett Wiki RAG 查询 (增强版)

用法:
    python query.py <命令> [参数]

命令:
    search, s <查询>      - 段落级搜索
    timeline, t <概念>    - 搜索概念在所有信件中的时间线
    doc <概念> <文档ID>   - 在指定文档中搜索概念
    export <概念> [文件]  - 导出概念时间线为 JSON
    rebuild, r           - 重建索引
    help, h              - 显示帮助

示例:
    # 搜索段落
    python query.py search 安全边际
    python query.py s 内在价值
    
    # 概念时间线
    python query.py timeline 内在价值
    python query.py t 护城河
    
    # 文档内搜索
    python query.py doc 安全边际 berkshire_zh/1988-letter-zh.md
    
    # 导出为 JSON
    python query.py export 内在价值
    
    # 重建索引
    python query.py rebuild
""")

if __name__ == "__main__":
    main()
