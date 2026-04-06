# Buffett Shareholder Letters Wiki

A bilingual (中文/English) knowledge base built from Warren Buffett's shareholder letters, following the [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

An Obsidian vault that doubles as an LLM-readable wiki — every claim links back to its source, entities are cross-referenced via `[[wikilinks]]`, and knowledge compounds over time.

## Quick Start (for LLM agents)

1. **Read [`SCHEMA.md`](SCHEMA.md) first.** It defines all operational conventions, templates, and workflows.
2. **Read [`index.md`](index.md)** to understand what's already ingested (letters, concepts, companies, people).
3. **To ingest a new letter** — follow the Ingest workflow in SCHEMA.md.
4. **To query** — read index.md, navigate to relevant pages, synthesize answers with `[[source-links]]`.
5. **To lint** — run the Lint workflow in SCHEMA.md.

## Directory Structure

```
warren_buffett_wiki/            ← Obsidian vault
├── SCHEMA.md                   # ⚙️  Operational rules for LLM agents
├── index.md                    # Master index with stats
├── log.md                      # Append-only changelog
├── raw/                        # Immutable source material (not wiki)
│   ├── berkshire/
│   │   ├── YYYY-letter-en.md   #   English source
│   │   └── YYYY-letter-zh.txt  #   Chinese source
│   ├── partnership/            # Partnership letter sources
│   └── other/                  # Speeches, interviews, etc.
├── letters/                    # Bilingual paragraph-aligned letters + summaries
│   ├── YYYY-letter.md
│   └── YYYY-summary.md
├── concepts/                   # Investment concepts (内在价值, 烟蒂投资法, ...)
├── companies/                  # Companies mentioned (可口可乐, 盖可保险, ...)
├── people/                     # Key people (查理·芒格, B夫人, ...)
├── analysis/                   # Deep-dive analyses
└── assets/                     # Images, charts
```

## Data Sources

| Source | URL | Coverage | Role |
|--------|-----|----------|------|
| juliuschun/eco-moat-ai | https://github.com/juliuschun/eco-moat-ai | 1977–2024 | **Primary English source** (Markdown) |
| buffett-letters-eir | https://buffett-letters-eir.pages.dev | 1956–2024 | **Primary Chinese source** (HTML) |
| fenwii/WarrenBuffettLetter | https://github.com/fenwii/WarrenBuffettLetter | 1957–2024 | PDF archive, fallback |
| Berkshire Hathaway (official) | https://www.berkshirehathaway.com/letters/ | 1977–2024 | Official, some early years 404 |

## Key Principles

- **Source-backed**: every fact links to its origin letter
- **Bilingual**: Chinese and English co-located, paragraph-aligned via Obsidian callouts
- **Cross-linked**: `[[wikilinks]]` connect letters ↔ concepts ↔ companies ↔ people
- **Compounding**: wiki pages are updated as new letters are ingested, building an evolving knowledge graph
- **No dangling links**: all `[[wikilinks]]` must resolve to existing `.md` files
- **`raw/` is immutable**: holds original source material, never modified

## Page Types

### Concept pages (`concepts/`)
- 概念解析 / Definition
- 核心要义 / Key Principles
- 实践应用 / Practical Application
- 巴菲特原话精选 / Buffett Quotes
- 思想演变 / Evolution of Thought (updated as more letters are ingested)
- 🔗 Related

### Company pages (`companies/`)
- 公司简介 / Company Overview
- 伯克希尔的关系 / Berkshire's Relationship
- 关键事件时间线 / Key Events Timeline
- 巴菲特原话精选 / Buffett Quotes
- 🔗 Related

### Person pages (`people/`)
- 人物简介 / Biography
- 与巴菲特的关系 / Relationship with Buffett
- 在股东信中的出现 / Appearances in Letters
- 🔗 Related

### Letter pages (`letters/`)
- `YYYY-letter.md` — Bilingual paragraph-aligned text with embedded `[[entity links]]`
- `YYYY-summary.md` — Structured summary: overview, themes, figures, entities, excerpts

### Analysis pages (`analysis/`)
- 分析主题 / Topic
- 核心论点 / Thesis
- 论据与原文引用 / Evidence with Source Links
- 结论 / Conclusion
- 🔗 Related

## Current Progress

- Letters ingested: **3** (1977, 1978, 1989) out of ~99
- Concepts: **14** · Companies: **19** · People: **16**

## For Humans

Open this directory in [Obsidian](https://obsidian.md/). Enable the `bilingual-reading` CSS snippet for styled paragraph-aligned reading. Use Graph View, Backlinks, and Full-text Search to navigate.
