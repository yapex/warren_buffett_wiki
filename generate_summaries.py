#!/usr/bin/env python3
"""
为股东大会 summary 生成真正有价值的核心要点。

策略：
1. 清理残留的废弃内容（代码块、多余标题行）
2. 从原文提取关键信息，生成"核心要点"部分
3. 添加"金句"部分（精选巴菲特/芒格的经典语录）
"""

import re
from pathlib import Path


def extract_key_info_from_source(year: int) -> tuple[list[str], list[str]]:
    """
    从原文提取关键信息，返回 (要点列表, 金句列表)
    这是一个简化的实现，实际需要更智能的提取
    """
    source_file = Path(f'wiki/shareholders_meeting/{year}-股东大会.md')
    if not source_file.exists():
        return [], []
    
    content = source_file.read_text(encoding='utf-8')
    
    # 提取开场白/第一段（通常包含关键统计）
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    key_points = []
    quotes = []
    
    # 简单启发式：包含数字和关键词的行可能是要点
    keywords = ['巴菲特', '芒格', '伯克希尔', '收购', '投资', '亿元', '亿美元', 
                 '参会', '股东', '董事', '参会人数', '销售', '保险']
    
    for line in lines[:100]:  # 只看前100行
        # 提取包含关键词且较长的句子作为潜在金句
        if any(kw in line for kw in ['说：', '表示：', '认为：']):
            if len(line) > 30 and len(line) < 200:
                # 清理格式
                clean = re.sub(r'^\w+：', '', line)
                if clean not in quotes and len(quotes) < 3:
                    quotes.append(clean[:150])
        
        # 提取统计信息
        if any(kw in line for kw in keywords):
            if any(c.isdigit() for c in line) and len(line) < 100:
                if line not in key_points and len(key_points) < 4:
                    key_points.append(line[:100])
    
    return key_points, quotes


def generate_summary_content(year: int, old_content: str) -> str:
    """生成新的 summary 内容，保留 frontmatter。"""
    
    # 解析旧的 frontmatter
    if old_content.startswith('---'):
        end = old_content.find('---', 3)
        frontmatter = old_content[3:end]
        body = old_content[end+3:]
    else:
        frontmatter = f'type: interview\nyear: {year}\nsubtype: annual_meeting\nvenue: 伯克希尔股东大会\ndate: {year}\ntags: [股东大会, 伯克希尔]\n'
        body = old_content
    
    # 清理 body：只保留 ## 完整原文 和 ## 相关 部分
    sections = {
        'intro': '',
        'keypoints': '',
        'quotes': '',
        'original': '',
        'related': ''
    }
    
    current_section = 'intro'
    lines = body.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('## 核心要点'):
            current_section = 'keypoints'
            i += 1
            continue
        elif line.startswith('## 金句'):
            current_section = 'quotes'
            i += 1
            continue
        elif line.startswith('## 完整原文'):
            current_section = 'original'
            sections[current_section] += line + '\n'
            i += 1
            continue
        elif line.startswith('## 相关'):
            current_section = 'related'
            sections[current_section] += line + '\n'
            i += 1
            continue
        elif line.startswith('##'):
            current_section = 'intro'
        
        sections[current_section] += line + '\n'
        i += 1
    
    # 如果没有核心要点，尝试从原文提取
    if not sections['keypoints'].strip() and year >= 1994:
        points, quotes = extract_key_info_from_source(year)
        if points or quotes:
            sections['keypoints'] = '## 核心要点\n\n'
            for i, p in enumerate(points, 1):
                sections['keypoints'] += f'{i}. {p}\n'
            sections['keypoints'] += '\n'
            
            if quotes:
                sections['quotes'] = '## 金句\n\n'
                for q in quotes:
                    sections['quotes'] += f'> {q}\n'
                sections['quotes'] += '\n'
    
    # 重新组装
    new_body = sections['intro'].strip()
    if sections['keypoints']:
        new_body += '\n\n' + sections['keypoints'].strip()
    if sections['quotes']:
        new_body += '\n\n' + sections['quotes'].strip()
    if sections['original']:
        new_body += '\n\n' + sections['original'].strip()
    if sections['related']:
        new_body += '\n\n' + sections['related'].strip()
    
    return f'---\n{frontmatter}---\n\n{new_body}\n'


def main():
    base = Path('wiki/shareholders_meeting')
    
    for summary_file in sorted(base.glob('*_summary.md')):
        # 跳过已有核心要点的（2023-2025）
        if summary_file.name.startswith(('2023', '2024', '2025')):
            continue
        
        content = summary_file.read_text(encoding='utf-8')
        
        # 检查是否已有核心要点
        if '## 核心要点' in content:
            print(f'  - {summary_file.name}: 已有核心要点')
            continue
        
        # 生成新内容
        year = int(summary_file.name[:4])
        new_content = generate_summary_content(year, content)
        
        if new_content != content:
            summary_file.write_text(new_content, encoding='utf-8')
            print(f'  ✓ {summary_file.name}: 生成核心要点')
        else:
            print(f'  · {summary_file.name}: 无变化')


if __name__ == '__main__':
    main()
