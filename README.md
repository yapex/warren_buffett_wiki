# Buffett Wiki + LightRAG

基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，构建巴菲特知识库。

## 项目定位

1. **原始材料收集** → 下载所有中文/英文巴菲特信（raw 目录）
2. **Wiki 编译** → 纯中文，概念提取，wikilink 指向英文原文
3. **LightRAG 集成** → 支持复杂查询，可追溯到原始信

### Karpathy LLM Wiki 精神对照

| 层次 | 要求 | 本项目实现 |
|------|------|-----------|
| **原始材料** | 不可修改的源文档 | `raw/` 目录 ✅ |
| **Wiki** | LLM 生成，跨链接，持久累积 | `wiki/` 目录 ✅ |
| **Schema** | 配置 LLM 如何维护 | `SCHEMA.md` ✅ |
| **Index** | 内容导向的总索引 | `wiki/index.md` ✅ |
| **Log** | 时间导向的变更记录 | `wiki/log.md` ✅ |

### 核心理念

- **持久累积**：Wiki 是持久累积的知识库，交叉引用已建立
- **增量更新**：新增信件时自动更新相关页面
- **源可追溯**：每个 Wiki 页面可追溯到原始信件
- **LLM 维护**：LLM 负责编译和维护，人类负责源 curation

## 目录结构

```
├── raw/                    # 原始材料（不可修改）
│   ├── berkshire/zh/       # 伯克希尔中文信 (60封, 1965-2024)
│   ├── berkshire/en/       # 伯克希尔英文信 (30封, 缺2007+)
│   └── partnership/zh/     # 合伙人中文信 (35封)
├── wiki/                   # 编译后的中文 Wiki
│   ├── index.md           # 总索引 ⭐
│   ├── log.md             # 变更日志 ⭐
│   ├── letters/           # 信件 (60封)
│   │   └── YYYY-letter.md # 每封信含概要、关键主题、涉及实体
│   ├── concepts/          # 概念 (4个核心概念 + 索引)
│   ├── companies/         # 公司 (5个核心公司 + 索引)
│   └── people/            # 人物 (4个核心人物 + 索引)
├── .rag/                   # LightRAG 索引和查询
├── scripts/               # 下载/编译脚本
└── SCHEMA.md              # Wiki 规范 ⭐
```

## Wiki 内容概览

### 概念 (concepts/)

| 概念 | 英文名 | 首次阐述 |
|------|--------|----------|
| [内在价值](./wiki/concepts/内在价值.md) | Intrinsic Value | 1960s |
| [护城河](./wiki/concepts/护城河.md) | Economic Moat | 1990s |
| [浮存金](./wiki/concepts/浮存金.md) | Float | 1967 |
| [安全边际](./wiki/concepts/安全边际.md) | Margin of Safety | 1960s |

### 公司 (companies/)

| 公司 | 英文名 | 首次提及 |
|------|--------|----------|
| [伯克希尔·哈撒韦](./wiki/companies/伯克希尔·哈撒韦.md) | Berkshire Hathaway | 1965 |
| [盖可保险](./wiki/companies/盖可保险.md) | GEICO | 1976 |
| [可口可乐](./wiki/companies/可口可乐.md) | Coca-Cola | 1988 |
| [美国运通](./wiki/companies/美国运通.md) | American Express | 1960s |
| [喜诗糖果](./wiki/companies/喜诗糖果.md) | See's Candies | 1972 |

### 人物 (people/)

| 人物 | 英文名 | 角色 |
|------|--------|------|
| [沃伦·巴菲特](./wiki/people/沃伦·巴菲特.md) | Warren Buffett | 董事长/CEO |
| [查理·芒格](./wiki/people/查理·芒格.md) | Charlie Munger | 副董事长 |
| [本杰明·格雷厄姆](./wiki/people/本杰明·格雷厄姆.md) | Benjamin Graham | 导师 |
| [阿吉特·杰恩](./wiki/people/阿吉特·杰恩.md) | Ajit Jain | 再保险负责人 |

## 快速开始

### 1. 下载信件

信件数据已预下载在 `raw/` 目录，无需手动下载。

### 2. 编译 Wiki

```bash
uv run python scripts/compile_wiki.py
```

这会生成包含以下内容的 Wiki 页面：
- **概要**：信件核心内容概述
- **关键主题**：识别的主要话题
- **涉及实体**：提及的公司和人物（带链接）
- **格式化正文**：易于阅读的排版

### 3. RAG 查询

```bash
# 命令行
uv run python .rag/query.py "巴菲特如何看待保险业务"

# 交互模式
uv run python .rag/query.py
```

## 当前进度

| 类型 | 数量 | 状态 |
|------|------|------|
| 伯克希尔中文 | 60封 | ✅ 完成 |
| 合伙人中文 | 35封 | ✅ 完成 |
| 伯克希尔英文 | 30/48封 | ⚠️ 部分缺失 |
| Wiki 信件 | 60封 | ✅ 完成（含概要/主题/实体） |
| Wiki 总索引 | index.md | ✅ 完成 |
| Wiki 变更日志 | log.md | ✅ 完成 |
| Wiki 概念 | 4个 + 索引 | ✅ 完成 |
| Wiki 公司 | 5个 + 索引 | ✅ 完成 |
| Wiki 人物 | 4个 + 索引 | ✅ 完成 |
| RAG 索引 | 60封 | ✅ 完成 |

## 数据来源

- **中文源**: [buffett-letters-eir](https://buffett-letters-eir.pages.dev)
- **英文源**: Berkshire Hathaway 官网

## 待完成

- [ ] 补全缺失的英文信件 (2007-2024)
- [ ] 扩展概念/公司/人物详情页（基于 [concepts/index](./wiki/concepts/index.md) 继续添加）
- [ ] 集成真正的 LLM 支持
- [ ] 添加 [companies/index](./wiki/companies/index.md) 更多公司详情页
- [ ] 添加 [people/index](./wiki/people/index.md) 更多人物详情页
- [ ] 定期 Lint 检查 Wiki 健康状态

## Wiki 维护指南

详见 [SCHEMA.md](./SCHEMA.md) 了解：
- Wiki 页面模板规范
- 命名和链接规范
- 新增信件的维护流程
- 定期检查清单
