#!/usr/bin/env python3
"""
下载巴菲特伯克希尔英文信件到 raw/berkshire/en/
从 Berkshire Hathaway 官网下载
"""
import httpx
from selectolax.parser import HTMLParser
from pathlib import Path
import asyncio

BASE_URL = "https://www.berkshirehathaway.com/letters"
OUTPUT_DIR = Path("raw/berkshire/en")

# 伯克希尔时期: 1977-2024
YEARS = list(range(1977, 2025))

async def download_letter(year: int) -> bool:
    """下载并提取单封信件"""
    output_file = OUTPUT_DIR / f"{year}-letter-en.md"
    
    if output_file.exists():
        return None  # 跳过
    
    try:
        print(f"📥 下载 {year}...")
        url = f"{BASE_URL}/{year}.html"
        
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            resp = await client.get(url)
            
            if resp.status_code == 404:
                print(f"⏭️  {year} 官网无 HTML")
                return False
            
            resp.raise_for_status()
        
        tree = HTMLParser(resp.text)
        main = tree.css_first("body")
        content = main.text() if main else tree.text()
        
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        content = '\n'.join(lines)
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {year} ({len(content)} chars)")
        return True
    except Exception as e:
        print(f"❌ {year} 失败: {e}")
        return False

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 检查已有文件
    existing = set()
    for f in OUTPUT_DIR.glob("*-letter-en.md"):
        yr = int(f.name[:4])
        existing.add(yr)
    
    years_to_download = [y for y in YEARS if y not in existing]
    
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📊 已下载: {len(existing)} 封")
    print(f"📊 待下载: {len(years_to_download)} 封")
    print("-" * 50)
    
    for year in years_to_download:
        await download_letter(year)
        await asyncio.sleep(0.5)
    
    print("-" * 50)
    print(f"✅ 完成!")

if __name__ == "__main__":
    asyncio.run(main())
