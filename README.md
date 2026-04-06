# Buffett Shareholder Letters Wiki

A bilingual (中文/English) knowledge base built from Warren Buffett's shareholder letters, following the [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

An Obsidian vault that doubles as an LLM-readable wiki — every claim links back to its source, entities are cross-referenced via `[[wikilinks]]`, and knowledge compounds over time.

## Quick Start (for LLM agents)

1. **Read [`SCHEMA.md`](SCHEMA.md) first.** It defines all conventions, templates, and operations. This is your single source of truth.
2. **Read [`index.md`](index.md)** to understand what's already ingested (letters, concepts, companies, people).
3. **To ingest a new letter** — follow the Ingest workflow in SCHEMA.md: fetch raw sources → align ZH/EN → create letter page → extract entities → update/create wiki pages → verify links → update index & log.
4. **To query** — read index.md, navigate to relevant pages, synthesize answers with `[[source-links]]`.
5. **To lint** — run the Lint workflow in SCHEMA.md to catch broken links and missing cross-references.

## Project Structure

```
warren_buffett_wiki/
├── SCHEMA.md          # ⚙️  START HERE — conventions, templates, workflows
├── index.md           # Master index with stats
├── log.md             # Append-only changelog
├── raw/               # Immutable source material (not wiki)
├── letters/           # Bilingual paragraph-aligned letters + summaries
├── concepts/          # Investment concepts (内在价值, 烟蒂投资法, ...)
├── companies/         # Companies mentioned (可口可乐, 盖可保险, ...)
├── people/            # Key people (查理·芒格, B夫人, ...)
├── analysis/          # Deep-dive analyses
└── assets/            # Images, charts
```

## Key Principles

- **Source-backed**: every fact links to its origin letter
- **Bilingual**: Chinese and English co-located, paragraph-aligned via Obsidian callouts
- **Cross-linked**: `[[wikilinks]]` connect letters ↔ concepts ↔ companies ↔ people
- **Compounding**: wiki pages are updated as new letters are ingested, building an evolving knowledge graph
- **No dangling links**: all `[[wikilinks]]` must resolve to existing `.md` files

## Current Progress

- Letters ingested: **3** (1977, 1978, 1989) out of ~99
- Concepts: **14** · Companies: **19** · People: **16**

## For Humans

Open this directory in [Obsidian](https://obsidian.md/). Enable the `bilingual-reading` CSS snippet for styled paragraph-aligned reading. Use Graph View, Backlinks, and Full-text Search to navigate.
