#!/usr/bin/env python3
"""
批量生成概念原文引用时间线
"""
import sys
import json
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config import get_concept_quote_timeline, search_concept_timeline

# 核心概念列表（中文）
CORE_CONCEPTS = [
    "内在价值",
    "安全边际",
    "护城河",
    "市场先生",
    "浮存金",
    "经济商誉",
    "所有者收益",
    "透视盈余",
    "能力圈",
    "集中投资",
    "长期持有",
    "有效市场",
    "通货膨胀",
    "管理层",
    "资本配置",
    "回购",
    "留存收益",
    "复利",
    "账面价值",
    "股东回报",
    "套利",
    "保险业",
    "银行业",
    "衍生品",
    "特许经营权"
]

def extract_key_sentence(text: str, max_len: int = 150) -> str:
    """提取关键句子"""
    # 找到第一个完整句子
    sentences = re.split(r'(?<=[。！？.!?])', text)
    for s in sentences:
        s = s.strip()
        if len(s) >= 20:  # 至少20个字符
            return s[:max_len] + "..." if len(s) > max_len else s
    return text[:max_len] + "..." if len(text) > max_len else text

def format_timeline_markdown(concept: str, timeline: list) -> str:
    """格式化时间线为 Markdown"""
    lines = []
    
    lines.append(f"## 原文引用时间线\n")
    
    if not timeline:
        lines.append("*暂无原文引用*")
        return "\n".join(lines)
    
    # 按年份分组
    by_year = {}
    for item in timeline:
        year = item.get("year", "N/A")
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(item)
    
    # 输出时间线
    for year in sorted(by_year.keys(), reverse=True):
        lines.append(f"### {year} 年")
        lines.append("")
        for item in by_year[year]:
            quote = extract_key_sentence(item.get("quote", ""))
            jump = item.get("jump_link", "")
            lines.append(f"> {quote}")
            lines.append(f"> — [📄 原文](./{jump})")
            lines.append("")
    
    return "\n".join(lines)

def format_timeline_json(concept: str, timeline: list) -> dict:
    """格式化时间线为 JSON"""
    return {
        "concept": concept,
        "quotes": [
            {
                "year": item.get("year"),
                "quote": extract_key_sentence(item.get("quote", "")),
                "source": item.get("source"),
                "jump_link": item.get("jump_link")
            }
            for item in timeline
        ]
    }

def generate_all_timelines(output_dir: Path = None):
    """生成所有概念的时间线"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "wiki" / "concepts"
    
    results = []
    
    for concept in CORE_CONCEPTS:
        print(f"📊 处理概念: {concept}")
        try:
            timeline = get_concept_quote_timeline(concept)
            
            # 生成 JSON 数据
            json_data = format_timeline_json(concept, timeline)
            
            # 保存 JSON 文件
            json_file = output_dir / f".{concept}_timeline.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            # 生成 Markdown 片段
            md_content = format_timeline_markdown(concept, timeline)
            md_file = output_dir / f".{concept}_timeline.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            results.append({
                "concept": concept,
                "quote_count": len(timeline),
                "years": [t.get("year") for t in timeline if t.get("year")]
            })
            
            print(f"   ✅ 生成 {len(timeline)} 条引用")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    
    return results

def update_concept_file(concept_file: Path, timeline_md: str):
    """更新概念文件，添加时间线"""
    if not concept_file.exists():
        return False
    
    with open(concept_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有时间线部分
    if "## 原文引用时间线" in content:
        # 替换现有时间线
        pattern = r'## 原文引用时间线[\s\S]*?(?=\n## |\n# |\Z)'
        content = re.sub(pattern, timeline_md + "\n", content)
    else:
        # 在文件末尾添加时间线
        content += "\n\n" + timeline_md
    
    with open(concept_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def export_summary_json(results: list, output_file: Path):
    """导出汇总 JSON"""
    summary = {
        "generated_at": "2024-04-08",
        "total_concepts": len(results),
        "concepts": results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"💾 汇总已保存到: {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="批量生成概念原文引用时间线")
    parser.add_argument("--output", "-o", type=str, help="输出目录")
    parser.add_argument("--concept", "-c", type=str, help="只处理指定概念")
    parser.add_argument("--summary", "-s", action="store_true", help="生成汇总文件")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output) if args.output else None
    
    if args.concept:
        # 处理单个概念
        concept = args.concept
        print(f"📊 处理概念: {concept}")
        timeline = get_concept_quote_timeline(concept)
        json_data = format_timeline_json(concept, timeline)
        md_content = format_timeline_markdown(concept, timeline)
        
        print(f"\n📝 Markdown 时间线:\n")
        print(md_content)
        
        if args.summary:
            print(f"\n📋 JSON 数据:\n")
            print(json.dumps(json_data, ensure_ascii=False, indent=2))
    else:
        # 批量处理所有概念
        print("🚀 开始批量生成概念时间线...")
        results = generate_all_timelines(output_dir)
        
        print(f"\n✅ 完成! 已处理 {len(results)} 个概念")
        
        if args.summary and output_dir:
            export_summary_json(results, output_dir / "timeline_summary.json")

if __name__ == "__main__":
    main()
