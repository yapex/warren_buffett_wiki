#!/usr/bin/env python3
"""
CNBC 巴菲特股东大会文字稿爬取脚本
测试：2022 年股东大会
"""

import json
from pathlib import Path

# 2022 年股东大会 URL
URLS = {
    "morning": "https://buffett.cnbc.com/video/2022/05/02/morning-session---2022-meeting.html",
    "afternoon": "https://buffett.cnbc.com/video/2022/05/02/afternoon-session---2022-meeting.html"
}

def extract_transcript_from_page(html_content: str) -> list[dict]:
    """
    从页面 HTML 中提取文字稿
    返回格式：[{speaker: str, text: str, chapter: str}, ...]
    """
    # 这个函数将在浏览器控制台中执行 JavaScript 来提取数据
    # 这里只是占位，实际提取用 browser_console
    pass

def save_to_markdown(transcript: list[dict], output_path: str):
    """保存为 Markdown 格式"""
    content = []
    content.append("# 2022 年伯克希尔股东大会\n")
    content.append("来源：CNBC Warren Buffett Archive\n")
    content.append("日期：2022 年 4 月 30 日\n")
    content.append("---\n")
    
    current_chapter = None
    for item in transcript:
        if item.get('chapter') and item['chapter'] != current_chapter:
            current_chapter = item['chapter']
            content.append(f"\n## {current_chapter}\n")
        
        speaker = item.get('speaker', '')
        text = item.get('text', '')
        if speaker:
            content.append(f"**{speaker}**: {text}\n")
        else:
            content.append(f"{text}\n")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ 保存到：{output_path}")

if __name__ == "__main__":
    print("🐸 2022 年股东大会文字稿爬取脚本")
    print("注意：此脚本需要通过 browser_console 工具执行 JavaScript 来提取数据")
    print("下一步：使用 browser_console 提取页面数据")
