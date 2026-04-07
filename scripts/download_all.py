#!/usr/bin/env python3
"""
一键下载所有巴菲特信件
"""
import subprocess
import sys

def run_script(name: str, script: str):
    print(f"\n{'='*60}")
    print(f"📦 {name}")
    print('='*60)
    result = subprocess.run([sys.executable, script], capture_output=False)
    return result.returncode == 0

def main():
    scripts = [
        ("伯克希尔中文信件 (1965-2024)", "download_berkshire_zh.py"),
        ("伯克希尔英文信件 (1977-2024)", "download_berkshire_en.py"),
        ("合伙人中文信件 (1956-1970)", "download_partnership_zh.py"),
    ]
    
    for name, script in scripts:
        run_script(name, f"scripts/{script}")
    
    print(f"\n{'='*60}")
    print("🎉 下载完成!")
    print('='*60)

if __name__ == "__main__":
    main()
