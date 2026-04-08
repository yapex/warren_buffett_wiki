#!/usr/bin/env python3
"""
编译中文信件为 Wiki 格式 - 美化版
遵循 Karpathy LLM Wiki 精神
"""
import re
from pathlib import Path
from datetime import datetime

RAW_ZH_DIR = Path("raw/berkshire/zh")
RAW_EN_DIR = Path("raw/berkshire/en")
WIKI_DIR = Path("wiki/letters")

# 已知公司关键词
COMPANIES = [
    "伯克希尔", "盖可", "GEICO", "可口可乐", "美国运通", "喜诗糖果",
    "吉列", "富国银行", "华盛顿邮报", "国民保险", "BNSF", "苹果",
    "西方石油", "迪士尼", "IBM", "沃尔玛", "美国银行", "摩根"
]

# 已知人物关键词
PEOPLE = [
    "巴菲特", "芒格", "查理", "格雷厄姆", "阿吉特", "阿贝尔",
    "杰克", "汤姆", "凯瑟琳"
]

def extract_year(filename: str) -> int:
    """从文件名提取年份"""
    match = re.match(r'(\d{4})', filename)
    return int(match.group(1)) if match else 0

def split_paragraphs(content: str) -> list:
    """将内容分割为段落"""
    # 按句子分割，保留句子边界
    paragraphs = []
    current = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            if current:
                paragraphs.append(' '.join(current))
                current = []
        else:
            current.append(line)
    
    if current:
        paragraphs.append(' '.join(current))
    
    return [p for p in paragraphs if len(p) > 50]

def extract_entities(content: str) -> tuple:
    """提取涉及的公司和人物"""
    companies = set()
    people = set()
    
    for company in COMPANIES:
        if company in content:
            companies.add(company)
    
    for person in PEOPLE:
        if person in content:
            people.add(person)
    
    return companies, people

def extract_themes(content: str, year: int) -> list:
    """提取关键主题"""
    themes = []
    content_lower = content.lower()
    
    # 基于关键词识别主题
    if any(w in content_lower for w in ['内在价值', '估值', '市价']):
        themes.append("内在价值与市场估值")
    if any(w in content_lower for w in ['保险', '浮存金', '承保', '综合比率']):
        themes.append("保险业务与浮存金")
    if any(w in content_lower for w in ['收购', '并购', '收购']):
        themes.append("收购与资本配置")
    if any(w in content_lower for w in ['铁路', 'bnsf']):
        themes.append("铁路业务")
    if any(w in content_lower for w in ['分红', '回购', '股息']):
        themes.append("股东回报")
    if any(w in content_lower for w in ['经济', '衰退', '危机', '恐慌']):
        themes.append("经济环境")
    if year >= 2020 and any(w in content_lower for w in ['新冠', '疫情', ' pandemic']):
        themes.append("新冠疫情影响")
    
    return themes[:5]  # 最多5个主题

def format_paragraphs(paragraphs: list) -> str:
    """格式化段落，每段适当宽度"""
    formatted = []
    for para in paragraphs:
        # 跳过标题行
        if '致股东信' in para and len(para) < 50:
            continue
        
        # 每段最大宽度 80 字符
        if len(para) > 80:
            words = para.split()
            lines = []
            current_line = []
            current_len = 0
            
            for word in words:
                if current_len + len(word) + 1 <= 80:
                    current_line.append(word)
                    current_len += len(word) + 1
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_len = len(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            para = '\n'.join(lines)
        
        formatted.append(para)
    
    return '\n\n'.join(formatted)

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
    
    # 提取实体和主题
    companies, people = extract_entities(zh_content)
    themes = extract_themes(zh_content, year)
    
    # 清理内容 - 移除标题行
    lines = []
    for line in zh_content.split('\n'):
        line = line.strip()
        # 跳过重复的标题行
        if line and not (
            line.startswith('股东信') or 
            re.match(r'^\d{4}巴菲特致股东信$', line) or
            line.startswith('=')
        ):
            lines.append(line)
    
    # 分割为段落
    paragraphs = split_paragraphs('\n'.join(lines))
    formatted_content = format_paragraphs(paragraphs)
    
    # 构建 Wiki 页面
    en_link = f"[EN](../../raw/berkshire/en/{year}-letter-en.md)" if en_file.exists() else ""
    
    # 生成涉及实体
    entities_parts = []
    if companies:
        companies_list = ', '.join([f'[{c}](../companies/{c}.md)' for c in sorted(companies)])
        entities_parts.append(f"- **公司**: {companies_list}")
    if people:
        # 去重并过滤掉太短的
        people_filtered = [p for p in people if len(p) >= 2]
        if people_filtered:
            people_list = ', '.join([f'[{p}](../people/{p}.md)' for p in sorted(people_filtered)])
            entities_parts.append(f"- **人物**: {people_list}")
    
    entities_section = '\n'.join(entities_parts) if entities_parts else "- （待提取）"
    
    # 生成关键主题
    themes_section = '\n'.join([f"- {t}" for t in themes]) if themes else "- （待提取）"
    
    wiki_content = f"""---
source: ../../raw/berkshire/zh/{year}-letter-zh.md
year: {year}
compiled: {datetime.now().strftime('%Y-%m-%d')}
---

# {year} 巴菲特致股东信

> [!原文]
> {en_link}

## 概要

本信回顾了伯克希尔 {year} 年的经营成果和投资理念。

## 关键主题

{themes_section}

## 涉及实体

{entities_section}

---

## 全文

{formatted_content}

---

*本页面由 LLM 编译，原始中文文本见 [{year}-letter-zh.md](../../raw/berkshire/zh/{year}-letter-zh.md)*
"""
    
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    with open(wiki_file, 'w', encoding='utf-8') as f:
        f.write(wiki_content)
    
    print(f"✅ {year} 已编译")
    return True

def main():
    print("📚 编译巴菲特信件为 Wiki（美化版）")
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
