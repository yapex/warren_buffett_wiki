#!/usr/bin/env python3
"""
清理股东大会 summary 文件，移除机械的"原文预览"部分。
保留 frontmatter、基本信息、核心要点（如有）。
"""

import re
from pathlib import Path

def clean_summary(content: str) -> tuple[str, int]:
    """
    清理 summary 文件内容。
    返回 (清理后内容, 删除的行数)
    """
    lines = content.split('\n')
    result = []
    removed = 0
    skip_section = False
    skip_until_marker = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测"原文预览"部分 - 开始跳过
        if '原文预览' in line or '原文预览（前' in line:
            # 从上一行如果是 ``` 也要跳过
            if result and result[-1].strip() == '```':
                result.pop()
                removed += 1
            skip_section = True
            removed += 1
            i += 1
            continue
            
        # 如果跳过了，检查是否遇到下一个 ## 或 --- 结束
        if skip_section:
            if line.startswith('##') or line.startswith('---'):
                skip_section = False
                result.append(line)
            else:
                removed += 1
            i += 1
            continue
            
        # 检测内嵌的原文内容（以#开头的重复标题）
        if (line.startswith('#') and 
            ('年伯克希尔' in line or '年股东大会' in line)):
            # 检查是否是标题重复（后面跟着 ... 或 数字）
            if i + 1 < len(lines) and re.search(r'\.{3,}', lines[i+1]):
                # 跳过这个标题和后面的省略号行
                removed += 1
                i += 1
                while i < len(lines) and re.search(r'\.{3,}', lines[i]):
                    removed += 1
                    i += 1
                continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result).strip() + '\n', removed


def main():
    base = Path('wiki/shareholders_meeting')
    total_removed = 0
    files_changed = 0
    
    for summary_file in sorted(base.glob('*_summary.md')):
        content = summary_file.read_text(encoding='utf-8')
        cleaned, count = clean_summary(content)
        
        if count > 0:
            summary_file.write_text(cleaned, encoding='utf-8')
            print(f"  ✓ {summary_file.name}: 删除 {count} 行")
            total_removed += count
            files_changed += 1
        else:
            # 检查是否还有"原文预览"残留
            if '原文预览' in content:
                print(f"  ⚠ {summary_file.name}: 有'原文预览'但未检测到")
    
    print(f"\n共处理 {files_changed} 个文件，删除 {total_removed} 行")


if __name__ == '__main__':
    main()
