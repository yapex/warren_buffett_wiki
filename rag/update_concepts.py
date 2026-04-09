#!/usr/bin/env python3
"""
更新概念文件，添加原文引用时间线
"""
import json
import re
from pathlib import Path

CONCEPTS_DIR = Path(__file__).parent.parent / "wiki" / "concepts"

# 核心概念列表
CORE_CONCEPTS = [
    "内在价值", "安全边际", "护城河", "市场先生", "浮存金",
    "经济商誉", "所有者收益", "透视盈余", "能力圈", "集中投资",
    "长期持有", "有效市场", "通货膨胀", "管理层", "资本配置",
    "回购", "留存收益", "复利", "账面价值", "股东回报",
    "套利", "保险业", "银行业", "衍生品", "特许经营权"
]

def extract_key_sentence(text: str, max_len: int = 200) -> str:
    """提取关键句子"""
    # 清理文本
    text = text.replace('\n', ' ').strip()
    
    # 找到第一个完整句子
    sentences = re.split(r'(?<=[。！？.!?])', text)
    for s in sentences:
        s = s.strip()
        if len(s) >= 30:  # 至少30个字符
            return s[:max_len] + "..." if len(s) > max_len else s
    
    return text[:max_len] + "..." if len(text) > max_len else text

def generate_timeline_section(concept: str, quotes: list) -> str:
    """生成时间线 Markdown 片段"""
    lines = []
    
    lines.append(f"\n\n## 原文引用时间线\n")
    
    if not quotes:
        lines.append("*暂无原文引用*")
        return "".join(lines)
    
    # 按年份分组
    by_year = {}
    for item in quotes:
        year = item.get("year")
        if year:
            year = int(year)
            if year not in by_year:
                by_year[year] = []
            by_year[year].append(item)
    
    # 输出时间线（从新到旧）
    for year in sorted(by_year.keys(), reverse=True):
        lines.append(f"### {year} 年\n")
        for item in by_year[year]:
            quote = extract_key_sentence(item.get("quote", ""))
            jump = item.get("jump_link", "")
            
            # 修复跳转链接路径
            if jump.startswith("./wiki/"):
                jump = jump[2:]  # 移除 "./"
            
            lines.append(f"> {quote}\n")
            lines.append(f"> — [📄 原文](./{jump})\n\n")
    
    return "".join(lines)

def update_concept_file(concept: str) -> bool:
    """更新单个概念文件"""
    concept_file = CONCEPTS_DIR / f"{concept}.md"
    timeline_file = CONCEPTS_DIR / f".{concept}_timeline.json"
    
    if not concept_file.exists():
        print(f"  ⚠️ 文件不存在: {concept_file}")
        return False
    
    # 读取时间线数据
    if timeline_file.exists():
        with open(timeline_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        quotes = data.get("quotes", [])
    else:
        print(f"  ⚠️ 时间线文件不存在: {timeline_file}")
        return False
    
    # 读取概念文件
    with open(concept_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新的时间线部分
    new_timeline = generate_timeline_section(concept, quotes)
    
    # 检查是否已有时间线部分
    if "## 原文引用时间线" in content:
        # 替换现有时间线
        pattern = r'\n*## 原文引用时间线\n[\s\S]*?(?=\n## |\n# |\Z)'
        content = re.sub(pattern, new_timeline, content)
    else:
        # 在文件末尾添加时间线
        content += new_timeline
    
    # 写回文件
    with open(concept_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("🔄 开始更新概念文件...")
    print(f"📁 目录: {CONCEPTS_DIR}")
    
    updated = 0
    failed = 0
    
    for concept in CORE_CONCEPTS:
        print(f"📝 更新: {concept}")
        if update_concept_file(concept):
            updated += 1
            print(f"  ✅ 完成")
        else:
            failed += 1
            print(f"  ❌ 失败")
    
    print(f"\n✅ 完成! 更新 {updated} 个文件，失败 {failed} 个")

if __name__ == "__main__":
    main()
