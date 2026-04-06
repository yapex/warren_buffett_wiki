# Buffett Shareholder Letters Wiki — Schema

> This document defines the structure, conventions, and workflows for this LLM Wiki.
> It is the key configuration file that makes the LLM a disciplined wiki maintainer.

---

## Project Overview

A bilingual (Chinese/English) knowledge base built from Warren Buffett's shareholder letters, following the [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

The vault itself is the wiki. Open it in Obsidian, enable the `bilingual-reading` CSS Snippet, and use Graph View / Backlinks / Full-text Search to navigate.

**Principles:**
- The wiki is a persistent, compounding artifact — knowledge is compiled once and kept current.
- Every claim links back to its source document.
- Bilingual: Chinese and English content are co-located for easy comparison.
- `raw/` is the only non-wiki directory — it holds immutable source material.
- All wiki pages (letters, concepts, companies, people, analysis) live at the vault root.

---

## Data Sources

| Source | URL | Coverage | Format | Role |
|--------|-----|----------|--------|------|
| juliuschun/eco-moat-ai | https://github.com/juliuschun/eco-moat-ai | 1977–2024 | Markdown (EN) | **Primary English source** |
| buffett-letters-eir | https://buffett-letters-eir.pages.dev | 1956–2024 | HTML (ZH) | **Primary Chinese source** |
| fenwii/WarrenBuffettLetter | https://github.com/fenwii/WarrenBuffettLetter | 1957–2024 | PDF (ZH+EN) | PDF archive, fallback |
| Berkshire Hathaway (official) | https://www.berkshirehathaway.com/letters/ | 1977–2024 | PDF/HTML | Official, some early years 404 |

---

## Directory Structure

```
warren_buffett_wiki/            ← Obsidian vault
├── raw/                        ← IMMUTABLE source material (not wiki)
│   ├── berkshire/
│   │   ├── YYYY-letter-en.md   #   English source (from juliuschun)
│   │   └── YYYY-letter-zh.txt  #   Chinese source (from buffett-letters-eir)
│   ├── partnership/            #   Partnership letter sources
│   └── other/                  #   Speeches, interviews, etc.
│
├── letters/                    ← Wiki: bilingual letters + summaries
│   ├── YYYY-letter.md          #   Bilingual paragraph-aligned letter
│   └── YYYY-summary.md         #   Per-letter summary
├── concepts/                   ← Wiki: investment concepts
├── companies/                  ← Wiki: companies mentioned
├── people/                     ← Wiki: key people
├── analysis/                   ← Wiki: deep-dive analyses
├── assets/                     ← Images, charts
├── index.md                    ← Master index
├── log.md                      ← Append-only changelog
├── SCHEMA.md                   ← This file
└── .obsidian/snippets/
    └── bilingual-reading.css   ← CSS for paragraph-aligned reading
```

---

## Bilingual Letter Format (`letters/YYYY-letter.md`)

The core wiki artifact. Uses Obsidian callout syntax for paragraph-aligned reading:

```markdown
> [!zh] 🇨🇳
> 中文段落……
>
> 多段用空行分隔……

> [!en] 🇺🇸
> English paragraph...
>
> Multiple paragraphs separated by blank lines...
```

**Conventions:**
- `> [!zh] 🇨🇳` and `> [!en] 🇺🇸` alternate, forming aligned pairs
- Entity names are wrapped in `[[wikilinks]]`: `[可口可乐](companies/可口可乐.md)`, `[查理·芒格](people/查理·芒格.md)`, `[内在价值](concepts/内在价值.md)`
- These links make Obsidian's Graph View and Backlinks work — each letter becomes a hub connecting to concept/company/person pages
- Styled via `bilingual-reading.css`: Chinese = blue tint 15px, English = gray tint 14px

---

## Page Template & Frontmatter

Every wiki page (concepts, companies, people, summaries, analysis) uses:

```yaml
---
type: concept | company | person | letter-summary | analysis
title_zh: "内在价值"
title_en: "Intrinsic Value"
aliases: [IV, 真实价值]
sources:
  - "[1989-letter](letters/1989-letter.md)"
related:
  - "[[账面价值]]"
  - "[[安全边际]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | reviewed | mature
---
```

| Field | Required | Description |
|-------|----------|-------------|
| `type` | ✅ | Page category |
| `title_zh` | ✅ | Chinese title |
| `title_en` | ✅ | English title |
| `aliases` | No | Alternative names for search |
| `sources` | ✅ | Source letters this page draws from |
| `related` | No | Links to related wiki pages |
| `created` | ✅ | Date first created |
| `updated` | ✅ | Date last modified |
| `status` | ✅ | `draft` → `reviewed` → `mature` |

### Bilingual conventions (for concept/company/person/summary pages)

- Chinese section first, English section second
- Quotes: Chinese translation + original English in blockquote, with `[[source-link]]`
- Related links: `[[账面价值 / Book Value]]`

---

## Linking Conventions

| Target | Link format | Example |
|--------|-------------|---------|
| Bilingual letter | `[[YYYY-letter]]` | `[1989-letter](letters/1989-letter.md)` |
| Letter summary | `[[YYYY-summary]]` | `[1989-summary](letters/1989-summary.md)` |
| Concept | `[[title_zh]]` | `[内在价值](concepts/内在价值.md)` |
| Company | `[[title_zh]]` | `[可口可乐](companies/可口可乐.md)` |
| Person | `[[title_zh]]` | `[查理·芒格](people/查理·芒格.md)` |

### File naming

| Category | Pattern | Example |
|----------|---------|---------|
| Raw English | `YYYY-letter-en.md` | `1989-letter-en.md` |
| Raw Chinese | `YYYY-letter-zh.txt` | `1989-letter-zh.txt` |
| Bilingual letter | `YYYY-letter.md` | `1989-letter.md` |
| Letter summary | `YYYY-summary.md` | `1989-summary.md` |
| Concept | `title_zh.md` | `内在价值.md` |
| Company | `title_zh.md` | `可口可乐.md` |
| Person | `title_zh.md` | `查理·芒格.md` |
| Analysis | `descriptive-name.md` | `收购哲学的演变.md` |

---

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

---

## Operations

### Ingest

1. **Fetch raw sources**: English → `raw/berkshire/YYYY-letter-en.md`, Chinese → `raw/berkshire/YYYY-letter-zh.txt`
2. **Align paragraphs**: LLM aligns ZH/EN paragraphs, outputs `letters/YYYY-letter.md` with callout pairs and `[[entity links]]`
3. **Write summary**: Create `letters/YYYY-summary.md`
4. **Extract entities**: Identify concepts, companies, people
5. **Update/create wiki pages**: For each entity, create or update the corresponding page, add quotes, update evolution/timeline
6. **Verify links (REQUIRED)**: Before updating indexes, run link integrity check on all new and updated pages:
   - Every `[[wikilink]]` in new/updated files must resolve to an existing `.md` file
   - If a `[[link]]` in `related:` or `🔗 Related` points to a page that doesn't exist yet, either create that page or remove the link — **no dangling links allowed**
   - Use the shell check: `grep -oE '\[\[[^]]+\]\]' file.md | sed 's/|.*//' | while read link; do find . -name "${link}.md" ...; done`
   - Fix all broken links before proceeding
7. **Update `index.md`**: Add new entries, update stats
8. **Append to `log.md`**: Record what was done (include link verification result)

### Query

1. Read `index.md` to find relevant pages
2. Read the relevant wiki pages
3. Synthesize answer with `[[source-links]]`
4. If substantial, offer to save as `analysis/` page

### Lint

Periodically:
- **Broken `[[wikilinks]]`**: Every `[[link]]` must resolve to an existing `.md` file. Scan all wiki pages (excluding `raw/` and `.obsidian/`) and report orphans.
- **Dangling `related:` references**: Frontmatter `related:` and `🔗 Related` sections must not contain links to nonexistent pages.
- Orphan pages with no inbound links
- Missing cross-references
- Concepts mentioned in letters but lacking their own page
- Stale claims superseded by newer sources

---

## Changelog Format (`log.md`)

Append-only:

```
## [YYYY-MM-DD] ingest | 1989 Berkshire Shareholder Letter
- Created: [1989-letter](letters/1989-letter.md), [1989-summary](letters/1989-summary.md)
- Created concepts: [内在价值](concepts/内在价值.md), [透视收益](concepts/透视收益.md), [烟蒂投资法](concepts/烟蒂投资法.md), ...
- Created companies: [可口可乐](companies/可口可乐.md), [波仙珠宝](companies/波仙珠宝.md), ...
- Created people: [查理·芒格](people/查理·芒格.md), [B夫人](people/B夫人.md), ...
- New pages: 16
- Updated pages: 0
```
