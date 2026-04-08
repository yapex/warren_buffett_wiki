#!/usr/bin/env python3
"""
RAG 查询脚本
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config import search

def main():
    if len(sys.argv) > 1:
        # 命令行模式
        question = " ".join(sys.argv[1:])
        results = search(question, top_k=3)
        
        print(f"\n🔍 问题: {question}")
        print("=" * 60)
        
        for i, r in enumerate(results, 1):
            print(f"\n📄 文档 {i}: {r['source']}")
            print(f"   相关度: {r['score']:.0f} 个匹配词")
            if r['chunks']:
                print(f"   片段: {r['chunks'][0][:200]}...")
    else:
        # 交互模式
        print("\n📚 Buffett Wiki RAG 查询")
        print("=" * 60)
        print("输入问题，按 Enter 查询，按 q 退出")
        print("=" * 60)
        
        while True:
            try:
                question = input("\n问题: ").strip()
                if not question:
                    continue
                if question.lower() in ('q', 'quit', 'exit'):
                    break
                
                results = search(question, top_k=3)
                
                print("\n" + "-" * 60)
                for i, r in enumerate(results, 1):
                    print(f"\n📄 文档 {i}: {r['source']}")
                    print(f"   相关度: {r['score']:.0f} 个匹配词")
                    if r['chunks']:
                        print(f"   {r['chunks'][0][:150]}...")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 再见!")
                break

if __name__ == "__main__":
    main()
