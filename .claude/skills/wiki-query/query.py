#!/usr/bin/env python3
"""
Buffett Wiki Query Tool

封装 RAG 查询功能，支持：
- 全文搜索
- 概念时间线
- 文档内搜索
- 引用时间线
"""

import sys
import json
import argparse
from pathlib import Path

# 添加 .rag 目录到路径
rag_dir = Path(__file__).parent.parent.parent / '.rag'
sys.path.insert(0, str(rag_dir))

from config import (
    search_paragraphs,
    search_concept_timeline,
    search_concept_in_doc,
    get_concept_quote_timeline,
    DOCUMENTS,
    PARAGRAPHS,
)

# 颜色定义
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def format_results(results: list, verbose: bool = False, limit: int = 5):
    """格式化搜索结果"""
    if not results:
        print(f'{Colors.YELLOW}未找到匹配结果{Colors.RESET}')
        return
    
    print(f'\n{Colors.BOLD}🔍 搜索结果{Colors.RESET}')
    print(f'{Colors.CYAN}{"=" * 60}{Colors.RESET}')
    
    display_count = min(len(results), limit)
    for i, r in enumerate(results[:display_count], 1):
        year_info = f"[{r['year']}]" if r.get('year') else ""
        print(f'\n{Colors.GREEN}📄 结果 {i}:{Colors.RESET} {year_info} {r["doc_id"]}')
        print(f'   匹配度：{Colors.YELLOW}{r["score"]}{Colors.RESET} 个词')
        
        if r.get('matched_tokens'):
            tokens = ', '.join(r['matched_tokens'][:5])
            print(f'   匹配词：{Colors.BLUE}{tokens}{Colors.RESET}')
        
        content = r['content'][:200].replace('\n', ' ')
        print(f'   内容：{content}...')
        
        if verbose:
            print(f'   🔗 {r["jump_url"]}')
    
    if len(results) > limit:
        print(f'\n{Colors.CYAN}ℹ️ 共找到 {len(results)} 个结果，显示前 {limit} 个{Colors.RESET}')
    else:
        print(f'\n{Colors.CYAN}ℹ️ 共找到 {len(results)} 个结果{Colors.RESET}')

def show_timeline(results: list):
    """格式化时间线结果"""
    if not results:
        print(f'{Colors.YELLOW}未找到时间线数据{Colors.RESET}')
        return
    
    print(f'\n{Colors.BOLD}📅 概念时间线{Colors.RESET}')
    print(f'{Colors.CYAN}{"=" * 60}{Colors.RESET}')
    
    # 按年份排序
    sorted_results = sorted(results, key=lambda x: x.get('year', '0000'))
    
    for r in sorted_results:
        year = r.get('year', 'N/A')
        content_preview = r['content'][:150].replace('\n', ' ')
        print(f'\n{Colors.GREEN}[{year}]{Colors.RESET}')
        print(f'  {content_preview}...')
        print(f'  {Colors.BLUE}🔗 {r["jump_url"]}{Colors.RESET}')
    
    print(f'\n{Colors.CYAN}ℹ️ 共 {len(sorted_results)} 个时间点{Colors.RESET}')

def show_doc_results(results: list, doc_id: str):
    """格式化文档内搜索结果"""
    if not results:
        print(f'{Colors.YELLOW}在 {doc_id} 中未找到匹配结果{Colors.RESET}')
        return
    
    print(f'\n{Colors.BOLD}📖 在 {doc_id} 中搜索结果{Colors.RESET}')
    print(f'{Colors.CYAN}{"=" * 60}{Colors.RESET}')
    
    for i, r in enumerate(results, 1):
        print(f'\n{Colors.GREEN}段落 {i}{Colors.RESET} (索引：{r["para_index"]}):')
        content = r['content'][:200].replace('\n', ' ')
        print(f'  {content}...')
        print(f'  {Colors.BLUE}🔗 {r["jump_url"]}{Colors.RESET}')
    
    print(f'\n{Colors.CYAN}ℹ️ 共找到 {len(results)} 个匹配段落{Colors.RESET}')

def show_quote_timeline(results: list):
    """格式化引用时间线"""
    if not results:
        print(f'{Colors.YELLOW}未找到引用时间线{Colors.RESET}')
        return
    
    print(f'\n{Colors.BOLD}💬 引用时间线{Colors.RESET}')
    print(f'{Colors.CYAN}{"=" * 60}{Colors.RESET}')
    
    sorted_results = sorted(results, key=lambda x: x.get('year', '0000'))
    
    for r in sorted_results:
        year = r.get('year', 'N/A')
        quote = r.get('quote', r['content'][:100])
        print(f'\n{Colors.GREEN}[{year}]{Colors.RESET}')
        print(f'  "{quote}"')
        print(f'  {Colors.BLUE}🔗 {r["jump_url"]}{Colors.RESET}')

def query_wiki(query: str, **kwargs):
    """执行查询"""
    limit = kwargs.get('limit', 5)
    verbose = kwargs.get('verbose', False)
    year_range = kwargs.get('year')
    doc_type = kwargs.get('type')
    
    # 基础搜索
    results = search_paragraphs(query, limit=limit * 2)
    
    # 按年份过滤
    if year_range:
        try:
            start, end = year_range.split('-')
            results = [r for r in results if r.get('year') and 
                      int(start) <= int(r['year']) <= int(end)]
        except:
            pass
    
    # 按文档类型过滤
    if doc_type:
        type_map = {
            'letters': ['letter'],
            'companies': ['company'],
            'concepts': ['concept'],
            'people': ['person'],
            'cases': ['case_study'],
        }
        types = type_map.get(doc_type, [])
        if types:
            results = [r for r in results if r.get('type') in types]
    
    format_results(results, verbose=verbose, limit=limit)

def query_timeline(concept: str):
    """查询概念时间线"""
    results = search_concept_timeline(concept)
    show_timeline(results)

def query_in_doc(query: str, doc_id: str):
    """在文档内搜索"""
    results = search_concept_in_doc(query, doc_id)
    show_doc_results(results, doc_id)

def query_quotes(concept: str):
    """查询引用时间线"""
    results = get_concept_quote_timeline(concept)
    show_quote_timeline(results)

def main():
    parser = argparse.ArgumentParser(description='Buffett Wiki Query Tool')
    parser.add_argument('query', help='搜索查询词')
    parser.add_argument('--timeline', '-t', action='store_true', 
                       help='查询概念时间线')
    parser.add_argument('--in-doc', '-d', help='在指定文档中搜索')
    parser.add_argument('--quotes', '-q', action='store_true',
                       help='查询引用时间线')
    parser.add_argument('--limit', '-l', type=int, default=5,
                       help='限制结果数量（默认：5）')
    parser.add_argument('--year', '-y', help='年份范围（如：1965-1975）')
    parser.add_argument('--type', help='文档类型（letters/companies/concepts/people/cases）')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细信息（包括链接）')
    
    args = parser.parse_args()
    
    print(f'{Colors.BOLD}🔍 查询："{args.query}"{Colors.RESET}\n')
    
    if args.timeline:
        query_timeline(args.query)
    elif args.in_doc:
        query_in_doc(args.query, args.in_doc)
    elif args.quotes:
        query_quotes(args.query)
    else:
        query_wiki(args.query, 
                  limit=args.limit,
                  verbose=args.verbose,
                  year_range=args.year,
                  doc_type=args.type)

if __name__ == '__main__':
    main()
