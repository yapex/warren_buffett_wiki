# Buffett Shareholder Letters Wiki — Schema

> Operational rules for LLM agents maintaining this wiki. Project overview and reference info are in [README.md](README.md).

---

## Frontmatter Template

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

## Bilingual Letter Format (`letters/YYYY-letter.md`)

Uses Obsidian callout syntax for paragraph-aligned reading:

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

**Rules:**
- `> [!zh] 🇨🇳` and `> [!en] 🇺🇸` alternate, forming aligned pairs
- Entity names wrapped in `[[wikilinks]]`: `[可口可乐](companies/可口可乐.md)`, `[查理·芒格](people/查理·芒格.md)`, `[内在价值](concepts/内在价值.md)`
- Styled via `bilingual-reading.css`: Chinese = blue tint 15px, English = gray tint 14px

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
