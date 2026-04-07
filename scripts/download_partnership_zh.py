#!/usr/bin/env python3
"""
下载巴菲特合伙人时期中文信件到 raw/partnership/zh/
"""
import httpx
from selectolax.parser import HTMLParser
from pathlib import Path
import asyncio

BASE_URL = "https://buffett-letters-eir.pages.dev"
OUTPUT_DIR = Path("raw/partnership/zh")

# 合伙人时期信件列表
LETTERS = [
    "1956-有限合伙协议",
    "1957-巴菲特致合伙人信",
    "1958-巴菲特致合伙人信",
    "1959-巴菲特致合伙人信",
    "1960-巴菲特致合伙人信",
    "1961-巴菲特致合伙人信",
    "1961年中-巴菲特致合伙人信",
    "1962-巴菲特致合伙人信",
    "1962年11月-巴菲特致合伙人信",
    "1962年12月-巴菲特致合伙人信",
    "1962年中-巴菲特致合伙人信",
    "1963-巴菲特致合伙人信",
    "1963年11月-巴菲特致合伙人信",
    "1963年12月-巴菲特致合伙人信",
    "1963年中-巴菲特致合伙人信",
    "1964-巴菲特致合伙人信",
    "1964年中-巴菲特致合伙人信",
    "1965-巴菲特致合伙人信",
    "1965年11月-巴菲特致合伙人信",
    "1965年中-巴菲特致合伙人信",
    "1966-巴菲特致合伙人信",
    "1966年11月-巴菲特致合伙人信",
    "1966年中-巴菲特致合伙人信",
    "1967-巴菲特致合伙人信",
    "1967年10月-巴菲特致合伙人信",
    "1967年11月-巴菲特致合伙人信",
    "1967年中-巴菲特致合伙人信",
    "1968-巴菲特致合伙人信",
    "1968年11月-巴菲特致合伙人信",
    "1968年中-巴菲特致合伙人信",
    "1969年10月-巴菲特致合伙人信",
    "1969年12月-巴菲特致合伙人信",
    "1969年12月26日-巴菲特致合伙人信",
    "1969年5月-巴菲特致合伙人信",
    "1970年2月-巴菲特致合伙人信",
]

async def download_letter(name: str) -> bool:
    """下载单封信件"""
    # 生成文件名
    safe_name = name.replace("/", "-").replace(":", "-")
    output_file = OUTPUT_DIR / f"{safe_name}.md"
    
    if output_file.exists():
        print(f"⏭️  {name} 已存在")
        return True
    
    try:
        print(f"📥 下载 {name}...")
        url = f"{BASE_URL}/partnership/{name}"
        
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
        
        tree = HTMLParser(resp.text)
        main = tree.css_first("article, .content, main")
        content = main.text() if main else tree.text()
        
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        content = '\n'.join(lines)
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {name} ({len(content)} chars)")
        return True
    except Exception as e:
        print(f"❌ {name} 失败: {e}")
        return False

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📊 待下载: {len(LETTERS)} 封")
    print("-" * 50)
    
    for name in LETTERS:
        await download_letter(name)
        await asyncio.sleep(0.3)
    
    print("-" * 50)
    print(f"✅ 完成!")

if __name__ == "__main__":
    asyncio.run(main())
