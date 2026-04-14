# Buffett Wiki 项目概览

**最后更新**: 2026-04-14  
**项目状态**: ✅ 生产就绪

---

## 📊 内容统计

| 类型 | 数量 | 说明 |
|------|------|------|
| **信件笔记** | 60 | 1965-2024 年伯克希尔股东信 |
| **合伙人信** | 36 | 1956-1970 年合伙人信件 |
| **访谈演讲** | 25 | 1985-2025 年访谈与演讲 |
| **概念笔记** | 121 | 投资概念与哲学 |
| **公司笔记** | 80 | 投资案例分析 |
| **人物笔记** | 63 | 相关人物传记 |
| **研究笔记** | 6 | 深度主题研究 |
| **特殊笔记** | 4 | 其他类型 |
| **总计** | **438** | 篇笔记 |

---

## 🏗️ 项目结构

```
warren_buffett_wiki/
├── wiki/                      # 知识库内容
│   ├── letters/              # 股东信笔记 (60 篇)
│   ├── partnership/          # 合伙人信笔记 (36 篇)
│   ├── interviews/           # 访谈演讲 (25 篇)
│   ├── concepts/             # 概念笔记 (121 篇)
│   ├── companies/            # 公司笔记 (80 篇)
│   ├── people/               # 人物笔记 (63 篇)
│   ├── research/             # 研究笔记 (6 篇)
│   └── special/              # 特殊笔记 (4 篇)
│
├── rag/                       # 搜索模块（Meilisearch）
│   ├── __init__.py           # 包入口
│   ├── __main__.py           # python -m rag 兼容
│   ├── query.py              # 统一 CLI 入口
│   └── meilisearch_search.py # Meilisearch 封装
│
├── scripts/                   # 工具脚本
│   ├── install.sh            # 一键安装脚本
│   ├── update_index.py       # 增量更新索引
│   ├── rebuild_index.py      # 全量重建索引
│   ├── test_search.py        # 搜索测试
│   ├── meilisearch.sh        # 服务管理
│   └── hooks/
│       └── post-commit       # Git Hook 自动化
│
├── docs/                      # 项目文档
│   └── plans/                # 计划文档（已完成即删除）
│
├── pyproject.toml             # Python 项目配置
├── README.md                  # 快速开始指南
└── SCHEMA.md                  # 数据结构说明
```

---

## 🔍 搜索功能（Meilisearch）

### 性能指标
- **平均查询时间**: < 10ms
- **索引文档数**: 438 篇
- **索引大小**: ~50MB

### 使用方式
```bash
cd warren_buffett_wiki

# 搜索段落
uv run buffett-wiki search 安全边际

# 概念时间线
uv run buffett-wiki timeline 护城河

# 文档内搜索
uv run buffett-wiki doc 安全边际 wiki/concepts/安全边际.md

# 带过滤搜索
uv run buffett-wiki filter 投资 --type letters --from 1980

# 分面统计
uv run buffett-wiki facets doc_type

# 重建索引
uv run buffett-wiki rebuild

# 性能测试
uv run buffett-wiki benchmark
```

### 可选别名
```bash
# 添加到 ~/.zshrc
alias buffett-wiki='cd ~/workspace/warren_buffett_wiki && uv run buffett-wiki'
```

---

## 🔄 自动化工作流

### Git Hook 自动更新
```bash
# 配置（install.sh 自动完成）
git config core.hooksPath scripts/hooks

# 提交后自动触发
git add wiki/concepts/新洞察.md
git commit -m "feat: 添加新洞察"
# → 自动更新 Meilisearch 索引
```

### 手动更新
```bash
# 增量更新（最近 1 小时）
uv run python scripts/update_index.py --recent 60

# 全量重建
uv run python scripts/rebuild_index.py
```

---

## 📦 依赖管理

### Python 依赖
```toml
[project]
name = "buffett-wiki"
version = "0.2.0"
dependencies = [
    "matplotlib>=3.10.8",
    "meilisearch>=0.40.0",
]

[project.scripts]
buffett-wiki = "rag.query:main"
```

### 安装方式
```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

---

## 🛠️ 工具脚本

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `install.sh` | 一键安装 | 新用户首次设置 |
| `update_index.py` | 增量更新 | Git Hook / 手动更新 |
| `rebuild_index.py` | 全量重建 | 定期维护 / 修复索引 |
| `test_search.py` | 搜索测试 | 功能验证 |
| `meilisearch.sh` | 服务管理 | 启动/停止 Meilisearch |

---

## 📚 核心技能（Skills）

### 已安装技能
- `meilisearch-migration` — Meilisearch 迁移与运维指南
- `buffett-wiki-research` — 深度研究全流程
- `obsidian` — Obsidian 笔记管理
- `getnote` — Get 笔记管理
- `acorn-*` — 价值投资分析工具集

### 技能更新
所有技能已统一使用 `uv run buffett-wiki` 命令。

---

## 🎯 快速开始

### 新用户
```bash
# 1. 克隆仓库
git clone git@github.com:yapex/warren_buffett_wiki.git
cd warren_buffett_wiki

# 2. 一键安装
./scripts/install.sh

# 3. 开始使用
uv run buffett-wiki search 安全边际
```

### 日常编辑
```bash
# 1. 编辑笔记
vim wiki/concepts/新洞察.md

# 2. 提交（自动更新索引）
git add wiki/concepts/新洞察.md
git commit -m "feat: 添加新洞察"

# 3. 验证搜索
uv run buffett-wiki search 新洞察
```

---

## 📊 Git 提交历史（最近）

```
2db14d2 fix: 更新 rag/__init__.py 使用 meilisearch_search
9524932 chore: 删除旧 RAG 文件（config.py, batch_timeline.py, update_concepts.py, .rag/）
9cce4a6 docs: 更新 README 使用 uv run buffett-wiki（添加别名提示）
f9e2fea docs: 更新 skills 和 README，统一使用 buffett-wiki CLI
12bdd05 feat: 统一 CLI 入口 (buffett-wiki)，基于 Meilisearch
8e2837b chore: 删除已完成的计划文档
06ad1dc refactor: 重命名脚本文件 (step3→rebuild_index, incremental→update_index, etc)
18b8f8a docs: 添加运维指南和自动化更新说明
33b8db3 docs: 更新 README 添加 Meilisearch 和安装脚本说明
a47b05b feat: 添加初始化安装脚本 (scripts/install.sh)
```

---

## 🗑️ 清理完成

### 已删除
- `.rag/` — 旧倒排索引（63MB）
- `rag/config.py` — 旧 RAG 配置
- `rag/batch_timeline.py` — 旧时间线生成
- `rag/update_concepts.py` — 旧概念更新
- `docs/plans/*.md` — 已完成的计划文档

### 保留
- `rag/meilisearch_search.py` — Meilisearch 封装
- `rag/query.py` — 统一 CLI
- `scripts/` — 工具脚本（精简后 6 个）

---

## 📈 项目里程碑

| 日期 | 事件 |
|------|------|
| 2026-01-01 | 项目启动 |
| 2026-04-11 | 完成 438 篇笔记 |
| 2026-04-14 | Meilisearch 迁移完成 |
| 2026-04-14 | 统一 CLI 完成 |
| 2026-04-14 | 旧 RAG 清理完成 |

---

## 🎓 参考资源

- [README.md](./README.md) — 快速开始指南
- [SCHEMA.md](./SCHEMA.md) — 数据结构说明
- [index.md](./index.md) — 总索引
- [skills/meilisearch-migration](~/.hermes/skills/meilisearch-migration/) — 运维指南
- [skills/buffett-wiki-research](~/.hermes/skills/buffett-wiki-research/) — 研究流程

---

**维护说明**: 本项目由 Hermes AI 维护，基于 Meilisearch 搜索引擎提供快速查询。
