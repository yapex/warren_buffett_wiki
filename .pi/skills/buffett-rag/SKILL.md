---
name: buffett-rag
description: Search and query the Buffett Wiki knowledge base using RAG. Use when the user asks questions about Buffett's letters, investment philosophy, market views, specific concepts, companies, or people mentioned in the letters. Also use when you need to find cross-letter connections, trace how a concept evolved over time, or locate specific quotes across decades of shareholder and partnership letters.
---

# Buffett RAG Query

## Quick Start

```bash
# Default search — cross-document paragraph-level search
uv run python .rag/query.py "巴菲特如何看待保险浮存金"

# Concept timeline — trace a concept across all letters
uv run python .rag/query.py timeline 安全边际
uv run python .rag/query.py t 护城河

# Search within a specific letter
uv run python .rag/query.py doc 安全边际 berkshire_zh/1988-letter-zh.md

# Export timeline as JSON
uv run python .rag/query.py export 内在价值

# Rebuild index (after adding/modifying files)
uv run python .rag/query.py rebuild
```

All commands must run from the project root directory.

## Query Strategy: Iterate, Don't Guess

RAG is an iterative process. Complex questions need multiple rounds:

```
Round 1: Broad query → understand the landscape, discover keywords
  ↓
Round 2: Use specific keywords/names/years from Round 1 to narrow in
  ↓
Round 3: Fill gaps — find counterexamples, missing years, alternative phrasings
  ↓
If needed: Use doc mode to deep-dive into a specific letter
```

**Example: researching "Buffett's market predictions"**

```bash
# Round 1: Broad
uv run python .rag/query.py "巴菲特对市场未来走势的预测"

# Round 2: Precise follow-up based on Round 1 findings
uv run python .rag/query.py "未来十年标普500回报 股市预言家"
uv run python .rag/query.py "投资者预期过于乐观 市场剧烈调整"

# Round 3: Fill gaps from early partnership letters
uv run python .rag/query.py "道指年均收益率 股票比债券合适 看好股票"

# Deep dive into one letter
uv run python .rag/query.py doc 预测 berkshire_zh/1999-letter-zh.md
```

## When to Use RAG vs Other Tools

| Scenario | Use |
|----------|-----|
| Search a concept across all letters | ✅ RAG |
| Find the original source of a quote | ✅ RAG |
| Cross-letter comparisons and connections | ✅ RAG |
| Known file path, need full content | Direct `read` |
| Verify RAG results are complete | Direct `read` source file |
| List what files exist in a directory | `bash ls/find` |

## Data Coverage

| Source | Type ID | Content |
|--------|---------|---------|
| `raw/berkshire/zh/` | `berkshire_zh` | Berkshire shareholder letters 1965-2024 |
| `raw/berkshire/en/` | `berkshire_en` | English originals |
| `raw/partnership/zh/` | `partnership_zh` | Partnership letters 1956-1969 |
| `wiki/` | `wiki` | All wiki pages |

## After Adding or Modifying Files

```bash
uv run python .rag/query.py rebuild
```
