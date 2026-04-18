#!/usr/bin/env python3
"""
Step 5: 完整测试验证

测试内容：
1. 基本搜索
2. 时间线排序
3. 过滤搜索
4. 文档内搜索
5. 性能基准
6. 分面统计
7. 同义词测试
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "rag"))

from meilisearch_search import (
    search_paragraphs,
    search_concept_timeline,
    search_concept_in_doc,
    search_with_filters,
    get_facets,
    benchmark,
)

PASSED = 0
FAILED = 0


def test(name, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  ✅ {name}")
    else:
        FAILED += 1
        print(f"  ❌ {name}: {detail}")


def run_tests():
    global PASSED, FAILED
    PASSED = 0
    FAILED = 0

    print("=" * 60)
    print("Step 5: 测试验证")
    print("=" * 60)

    # === 1. 基本搜索 ===
    print("\n📝 1. 基本搜索测试")
    
    results = search_paragraphs("安全边际", top_k=5)
    test("搜索返回结果", len(results) > 0, "结果为空")
    test("top1 是安全边际概念", "安全边际" in results[0].get("title", ""), f"实际: {results[0].get('title', '')}")
    test("结果包含 jump_url", all(r.get("jump_url") for r in results), "缺少 jump_url")
    test("结果包含 doc_type", all(r.get("doc_type") for r in results), "缺少 doc_type")
    
    results = search_paragraphs("可口可乐", top_k=5)
    test("可口可乐搜索有结果", len(results) > 0)
    
    results = search_paragraphs("Berkshire", top_k=5)
    test("英文搜索有结果", len(results) > 0)

    # === 2. 时间线 ===
    print("\n📝 2. 时间线测试")
    
    timeline = search_concept_timeline("护城河", top_k=10)
    test("时间线有结果", len(timeline) > 0)
    test("时间线按年份排序", len(timeline) <= 1 or all(
        (timeline[i].get("year", "") <= timeline[i+1].get("year", ""))
        for i in range(len(timeline)-1)
    ), "年份未正确排序")
    
    timeline = search_concept_timeline("安全边际", top_k=15)
    test("安全边际时间线有结果", len(timeline) > 0)

    # === 3. 过滤搜索 ===
    print("\n📝 3. 过滤搜索测试")
    
    results = search_with_filters("可口可乐", doc_type="letters", top_k=5)
    test("按类型过滤有结果", len(results) > 0)
    if results:
        test("结果都是 letters 类型", all(r.get("doc_type") == "letters" for r in results),
             f"混合类型: {[r.get('doc_type') for r in results]}")
    
    results = search_with_filters("巴菲特", year_from="1990", year_to="2000", top_k=5)
    test("年份范围过滤有结果", len(results) > 0)

    # === 4. 文档内搜索 ===
    print("\n📝 4. 文档内搜索测试")
    
    results = search_concept_in_doc("安全边际", "wiki/concepts/安全边际.md", top_k=3)
    test("文档内搜索有结果", len(results) > 0)

    # === 5. 性能基准 ===
    print("\n📝 5. 性能基准测试")
    
    stats = benchmark()
    test(f"平均查询时间 < 10ms ({stats['avg_ms']}ms)", stats["avg_ms"] < 10)
    test(f"最大查询时间 < 15ms ({stats['max_ms']}ms)", stats["max_ms"] < 15)
    test(f"所有查询返回结果", all(
        info["total_hits"] > 0 for info in stats["queries"].values()
    ))
    print(f"\n  📊 平均: {stats['avg_ms']}ms, 最快: {stats['min_ms']}ms, 最慢: {stats['max_ms']}ms")

    # === 6. 分面统计 ===
    print("\n📝 6. 分面统计测试")
    
    facets = get_facets("doc_type")
    test("分面统计有数据", len(facets) > 0)
    test("concepts 类型数量正确", facets.get("concepts", 0) >= 100, f"实际: {facets.get('concepts', 0)}")
    test("letters 类型存在", "letters" in facets)
    print(f"\n  📊 文档类型: {facets}")

    # === 7. 总文档数 ===
    print("\n📝 7. 索引完整性测试")
    
    # 搜索所有
    results = search_paragraphs("", top_k=1)
    import meilisearch
    client = meilisearch.Client("http://127.0.0.1:7700", "meilisearch-buffett-wiki-key")
    idx = client.get_index("buffett-wiki")
    stats_idx = idx.get_stats()
    test(f"文档数 >= 430 ({stats_idx.number_of_documents})", stats_idx.number_of_documents >= 430)
    
    # === 结果 ===
    print(f"\n{'=' * 60}")
    print(f"测试结果: ✅ {PASSED} 通过, ❌ {FAILED} 失败")
    if FAILED == 0:
        print("🎉 所有测试通过！")
    print(f"{'=' * 60}")
    
    return FAILED == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
