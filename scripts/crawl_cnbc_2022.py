#!/usr/bin/env python3
"""
从 CNBC 爬取 2022 年巴菲特股东大会完整文字稿
使用方法：
1. 在浏览器中打开上午场和下午场页面
2. 在控制台运行提取脚本
3. 保存结果到 raw/shareholders_meeting/en/
"""

from pathlib import Path

OUTPUT_DIR = Path("/Users/yapex/workspace/warren_buffett_wiki/raw/shareholders_meeting/en")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 提取 JavaScript 代码（在 browser_console 中运行）
EXTRACT_JS = """
// 提取完整的页面文本内容
const text = document.body.innerText;

// 清理多余空白
const cleaned = text
    .split('\\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
    .join('\\n');

return cleaned;
"""

print("🐸 CNBC 2022 年股东大会爬取指南")
print("=" * 60)
print("\n步骤 1: 在浏览器中打开以下两个页面:")
print("  上午场：https://buffett.cnbc.com/video/2022/05/02/morning-session---2022-meeting.html")
print("  下午场：https://buffett.cnbc.com/video/2022/05/02/afternoon-session---2022-meeting.html")
print("\n步骤 2: 在每个页面按 F12 打开控制台")
print("\n步骤 3: 运行以下 JavaScript 代码:")
print("-" * 60)
print(EXTRACT_JS)
print("-" * 60)
print("\n步骤 4: 将输出保存到:")
print(f"  {OUTPUT_DIR / '2022-morning-raw.txt'}")
print(f"  {OUTPUT_DIR / '2022-afternoon-raw.txt'}")
print("\n✅ 完成!")
