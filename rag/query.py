#!/usr/bin/env python3
"""
Buffett Wiki 统一查询 CLI

基于 Meilisearch 搜索引擎，提供：
- 段落级搜索
- 概念时间线
- 文档内搜索
- 高级过滤
- 分面统计

用法:
    buffett-wiki search <查询>       - 搜索段落
    buffett-wiki timeline <概念>     - 概念时间线
    buffett-wiki doc <概念> <文档>   - 文档内搜索
    buffett-wiki filter <查询> [...] - 带过滤搜索
    buffett-wiki facets [字段]       - 分面统计
    buffett-wiki rebuild             - 重建索引
    buffett-wiki benchmark           - 性能测试
"""
import sys
import json
from pathlib import Path

# 确保能导入 rag 模块
sys.path.insert(0, str(Path(__file__).parent))

from meilisearch_search import (
    search_paragraphs,
    search_concept_timeline,
    search_concept_in_doc,
    get_concept_quote_timeline,
    search_with_filters,
    get_facets,
    benchmark,
)


def format_results(results: list, verbose: bool = False):
    """格式化搜索结果"""
    for i, r in enumerate(results, 1):
        year_info = f"[{r.get('year', '')}]" if r.get('year') else ""
        doc_type = r.get('doc_type', '')
        title = r.get('title', '')
        print(f"\n📄 结果 {i}: {year_info} [{doc_type}] {title or r.get('doc_id', '')}")
        print(f"   匹配度：{r.get('score', 'N/A')}")
        if r.get('matched_tokens'):
            print(f"   匹配字段：{', '.join(r['matched_tokens'][:5])}")
        if r.get('tags'):
            print(f"   标签：{', '.join(r['tags'][:5])}")
        content = r.get('content', '')
        print(f"   内容：{content[:200]}...")
        if verbose:
            print(f"   跳转：{r.get('jump_url', '')}")


def show_timeline(results: list):
    """格式化时间线结果"""
    print("\n📅 概念时间线:")
    print("=" * 60)
    for r in results:
        year = r.get('year', 'N/A')
        title = r.get('title', '')
        content_preview = r.get('content', '')[:100].replace('\n', ' ')
        print(f"\n[{year}] {title}")
        print(f"  {content_preview}...")
        print(f"  🔗 {r.get('jump_url', '')}")


def show_doc_results(results: list, doc_id: str):
    """格式化文档内搜索结果"""
    print(f"\n📖 在 {doc_id} 中搜索结果:")
    print("=" * 60)
    for i, r in enumerate(results, 1):
        print(f"\n段落 {i} (索引：{r.get('para_index', i)}):")
        print(f"  {r.get('content', '')[:150]}...")
        print(f"  🔗 {r.get('jump_url', '')}")


def cmd_rebuild(args: list[str] = None):
    """重建索引"""
    rebuild_index()


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


def cmd_search(args: list[str]):
    """普通搜索"""
    query = " ".join(args) if args else input("输入查询：")
    results = search_paragraphs(query, top_k=10)
    print(f"\n🔍 搜索：{query}")
    print("=" * 60)
    if not results:
        print("   无结果")
        return
    format_results(results, verbose=True)
    print(f"\n共 {len(results)} 条结果")


def cmd_timeline(args: list[str]):
    """概念时间线"""
    concept = " ".join(args) if args else input("输入概念：")
    results = search_concept_timeline(concept, top_k=20)
    print(f"\n📅 概念时间线：{concept}")
    if not results:
        print("   无结果")
        return
    show_timeline(results)
    print(f"\n共 {len(results)} 条时间线")


def cmd_doc(args: list[str]):
    """文档内搜索"""
    if len(args) < 2:
        print("用法：buffett-wiki doc <概念> <文档 ID>")
        print("示例：buffett-wiki doc 安全边际 wiki/concepts/安全边际.md")
        return
    concept = args[0]
    doc_id = args[1]
    results = search_concept_in_doc(concept, doc_id, top_k=5)
    if not results:
        print(f"   在 {doc_id} 中未找到 '{concept}'")
        return
    show_doc_results(results, doc_id)


def cmd_filter(args: list[str]):
    """带过滤的搜索"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--type", "-t", help="文档类型 (letters/companies/concepts 等)")
    parser.add_argument("--from", dest="year_from", help="起始年份")
    parser.add_argument("--to", dest="year_to", help="结束年份")
    parser.add_argument("--limit", "-l", type=int, default=10, help="结果数量")
    
    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return
    
    results = search_with_filters(
        parsed.query,
        year_from=parsed.year_from,
        year_to=parsed.year_to,
        doc_type=parsed.type,
        top_k=parsed.limit,
    )
    
    print(f"\n🔍 过滤搜索：{parsed.query}")
    if parsed.type:
        print(f"   类型：{parsed.type}")
    if parsed.year_from:
        print(f"   年份：{parsed.year_from} - {parsed.year_to or '至今'}")
    print("=" * 60)
    if not results:
        print("   无结果")
        return
    format_results(results)


def cmd_facets(args: list[str]):
    """分面统计"""
    field = args[0] if args else "doc_type"
    facets = get_facets(field)
    print(f"\n📊 分面统计：{field}")
    print("=" * 60)
    for value, count in sorted(facets.items(), key=lambda x: -x[1]):
        print(f"   {value}: {count}")
    print(f"\n共 {len(facets)} 个值")


def cmd_benchmark(args: list[str]):
    """性能测试"""
    print("\n⚡ 性能基准测试")
    print("=" * 60)
    perf = benchmark()
    print(f"平均查询时间：{perf['avg_ms']}ms")
    print(f"最快：{perf['min_ms']}ms | 最慢：{perf['max_ms']}ms")
    print(f"\n详细结果:")
    for query, stats in perf['queries'].items():
        print(f"  {query}: {stats['time_ms']}ms ({stats['total_hits']} 条结果)")


def cmd_export(args: list[str]):
    """导出时间线 JSON"""
    if len(args) < 1:
        print("用法：buffett-wiki export <概念> [输出文件]")
        return
    concept = args[0]
    output = args[1] if len(args) > 1 else None
    export_timeline_json(concept, output)


def main():
    if len(sys.argv) < 2:
        usage()
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "search": cmd_search,
        "s": cmd_search,
        "timeline": cmd_timeline,
        "t": cmd_timeline,
        "doc": cmd_doc,
        "d": cmd_doc,
        "filter": cmd_filter,
        "f": cmd_filter,
        "facets": cmd_facets,
        "export": cmd_export,
        "e": cmd_export,
        "rebuild": cmd_rebuild,
        "r": cmd_rebuild,
        "benchmark": cmd_benchmark,
        "b": cmd_benchmark,
    }
    
    if cmd in ("help", "h", "--help"):
        usage()
    elif cmd in commands:
        commands[cmd](args)
    else:
        # 默认当搜索
        cmd_search([cmd] + args)


def usage():
    print("""
📚 Buffett Wiki 查询 CLI

用法:
    buffett-wiki <命令> [参数]

命令:
    search, s <查询>           - 段落级搜索
    timeline, t <概念>         - 概念时间线
    doc, d <概念> <文档 ID>     - 文档内搜索
    filter, f <查询> [选项]     - 带过滤搜索
    facets <字段>              - 分面统计
    export, e <概念> [文件]     - 导出时间线 JSON
    rebuild, r                 - 重建索引
    benchmark, b               - 性能测试
    help, h                    - 显示帮助

示例:
    # 搜索段落
    buffett-wiki search 安全边际
    buffett-wiki s 内在价值
    
    # 概念时间线
    buffett-wiki timeline 护城河
    buffett-wiki t 浮存金
    
    # 文档内搜索
    buffett-wiki doc 安全边际 wiki/concepts/安全边际.md
    
    # 带过滤搜索
    buffett-wiki filter 投资 --type letters --from 1980
    buffett-wiki f 可口可乐 --type companies
    
    # 分面统计
    buffett-wiki facets doc_type
    buffett-wiki facets year
    
    # 导出时间线
    buffett-wiki export 安全边际 timeline.json
    
    # 重建索引
    buffett-wiki rebuild
    
    # 性能测试
    buffett-wiki benchmark
""")


if __name__ == "__main__":
    main()
