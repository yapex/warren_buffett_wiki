#!/usr/bin/env python3
"""
下载巴菲特伯克希尔时期中文信件到 raw/berkshire/zh/
"""
import httpx
from selectolax.parser import HTMLParser
from pathlib import Path
import asyncio

BASE_URL = "https://buffett-letters-eir.pages.dev"
OUTPUT_DIR = Path("raw/berkshire/zh")

# 伯克希尔时期: 1965-2024
YEARS = list(range(1965, 2025))

async def download_letter(year: int) -> bool:
    """下载并提取单封信件内容"""
    output_file = OUTPUT_DIR / f"{year}-letter-zh.md"
    
    if output_file.exists():
        print(f"⏭️  {year} 已存在")
        return True
    
    try:
        print(f"📥 下载 {year}...")
        # URL 不带 .html
        url = f"{BASE_URL}/berkshire/{year}-巴菲特致股东信"
        
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
        
        # 解析 HTML
        tree = HTMLParser(resp.text)
        
        # 提取主要内容
        main = tree.css_first("article, .content, main")
        if main:
            content = main.text()
        else:
            content = tree.text()
        
        # 清理空白
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        content = '\n'.join(lines)
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {year} 已保存 ({len(content)} chars)")
        return True
    except Exception as e:
        print(f"❌ {year} 失败: {e}")
        return False

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📊 待下载: {len(YEARS)} 封 ({YEARS[0]}-{YEARS[-1]})")
    print("-" * 50)
    
    for year in YEARS:
        await download_letter(year)
        await asyncio.sleep(0.3)
    
    print("-" * 50)
    print(f"✅ 完成!")

if __name__ == "__main__":
    asyncio.run(main())
