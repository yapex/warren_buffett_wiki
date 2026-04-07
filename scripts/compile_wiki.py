#!/usr/bin/env python3
"""
编译中文信件为 Wiki 格式
"""
import re
from pathlib import Path
from datetime import datetime

RAW_ZH_DIR = Path("raw/berkshire/zh")
RAW_EN_DIR = Path("raw/berkshire/en")
WIKI_DIR = Path("wiki/letters")

def extract_year(filename: str) -> int:
    """从文件名提取年份"""
    match = re.match(r'(\d{4})', filename)
    return int(match.group(1)) if match else 0

def compile_letter(year: int) -> bool:
    """编译单封信件"""
    zh_file = RAW_ZH_DIR / f"{year}-letter-zh.md"
    en_file = RAW_EN_DIR / f"{year}-letter-en.md"
    wiki_file = WIKI_DIR / f"{year}-letter.md"
    
    if not zh_file.exists():
        print(f"❌ {year} 中文原文不存在")
        return False
    
    # 读取中文原文
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_content = f.read()
    
    # 清理内容
    lines = [l.strip() for l in zh_content.split('\n') if l.strip()]
    content = '\n'.join(lines)
    
    # 构建 Wiki 页面
    en_link = f"[EN](../../raw/berkshire/en/{year}-letter-en.md)" if en_file.exists() else ""
    
    wiki_content = f"""---
source: ../../raw/berkshire/zh/{year}-letter-zh.md
year: {year}
compiled: {datetime.now().strftime('%Y-%m-%d')}
---

# {year} 巴菲特致股东信

> [!原文]
> {en_link}

## 全文

{content}

---

*本页面由 LLM 编译，原始中文文本见 [{year}-letter-zh.md](../../raw/berkshire/zh/{year}-letter-zh.md)*
"""
    
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    with open(wiki_file, 'w', encoding='utf-8') as f:
        f.write(wiki_content)
    
    print(f"✅ {year} 已编译")
    return True

def main():
    print("📚 编译巴菲特信件为 Wiki")
    print("-" * 50)
    
    # 编译所有中文信件
    zh_files = list(RAW_ZH_DIR.glob("*-letter-zh.md"))
    
    for zh_file in zh_files:
        year = extract_year(zh_file.name)
        if year:
            compile_letter(year)
    
    print("-" * 50)
    print(f"✅ 完成! 共编译 {len(zh_files)} 封")

if __name__ == "__main__":
    main()
