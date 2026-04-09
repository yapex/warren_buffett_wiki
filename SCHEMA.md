# Buffett Wiki 规范

> 基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)：LLM 持久化地增量构建结构化 Wiki，好的分析写回 Wiki 而非消失在对话中。

## 核心理念

- **LLM 维护 Wiki**：人类管 raw 数据，LLM 管一切 wiki 内容
- **知识持久累积**：好的分析写回 `wiki/research/`，不留在对话历史

## 三种操作

| 操作 | 说明 | 产出 |
|------|------|------|
| **Ingest** | 新信件放入 raw/ → LLM 读取生成笔记 | `wiki/letters/`、`wiki/concepts/` 等 |
| **Query** | 用户提问 → 检索相关内容 → 综合分析 → **好的答案写回 Wiki** | `wiki/research/` |
| **Lint** | 检查孤立页面、断链、缺失交叉引用、过时结论 | 修复现有页面 |

### Query 的关键

> Karpathy: "Good answers can be filed back into the wiki as new pages. This way your explorations compound."

写回 Wiki 的判断标准：
- ✅ 跨信件的对比分析、主题演变、汇总研究
- ✅ 用户明确要求保存的分析
- ❌ 简单事实查询、临时探索性对话

## 目录结构

```
raw/                        # 原始数据（不可变，LLM 只读）
├── berkshire/zh/           # 伯克希尔股东信中文
├── partnership/zh/         # 合伙人信件中文
└── other/                  # 其他资料

wiki/                       # LLM 维护的 Wiki
├── letters/                # 信件笔记（每封信一页）
├── concepts/               # 概念笔记（安全边际、能力圈...）
├── companies/              # 公司笔记
├── people/                 # 人物笔记
├── research/               # 📌 研究笔记（跨信件的深度分析）
├── partnership/            # 合伙人信件笔记
└── log.md                  # 变更日志
```

## 页面类型

页面模板详见 → [docs/page-templates.md](docs/page-templates.md)

| 类型 | 目录 | 说明 |
|------|------|------|
| 信件笔记 | `wiki/letters/YYYY-letter.md` | 每封信的分析 + 原文 + 关联 |
| 概念笔记 | `wiki/concepts/概念名.md` | 定义 + 巴菲特观点 + 演变历程 |
| 公司笔记 | `wiki/companies/公司名.md` | 简介 + 关键数据 + 投资逻辑 |
| 人物笔记 | `wiki/people/人物名.md` | 简介 + 思想贡献 + 关联 |
| **研究笔记** | `wiki/research/主题名.md` | 跨信件的深度分析，Query 产出 |

## 处理原则

| 原则 | 说明 |
|------|------|
| 原文不可变 | raw/ 目录永远不修改 |
| 分析持久化 | 好的分析写回 Wiki，不留在对话历史 |
| 日志可追溯 | 每次操作记录 `wiki/log.md` |

## RAG 系统（可选增强）

项目内置 RAG 系统（`.rag/`），能对 raw 信件和 wiki 页面做段落级语义搜索，大幅提升跨信件查询效率。

**以下操作后必须重建索引：**

- 首次使用
- `wiki/` 目录文件变更（新增研究笔记、补充原文、修改概念页面等）
- 从 `raw/` 编译生成新 wiki 页面后

```bash
uv run python .rag/query.py rebuild
```

> ⚠️ 不重建索引，RAG 将查不到新增/修改的内容。每次 Ingest 或 Query 写回 wiki 后都应执行。

RAG 只索引 `wiki/` 目录，不直接索引 `raw/`。`raw/` 中的原始信件需先编译为 wiki 页面，再通过重建索引纳入检索。

索引文件（`.rag/*.json`）是可重建的缓存，已从 git 排除。代码（`.rag/config.py`、`.rag/query.py` 等）在 git 中。

**有 RAG 时**：查询用 RAG 多轮迭代，不用 grep/sed。详见 skill → `buffett-rag`

**无 RAG 时**：直接 read raw 文件，功能完整，只是效率更低。

## 日志格式

```
## YYYY-MM-DD
**操作**: ingest | query | lint | update | rebuild
### 完成的工作: ...
### 来源: raw 文件或用户提问
### RAG 查询（如有）: "查询内容"
```

## 详细参考

| 文档 | 内容 |
|------|------|
| `.pi/skills/buffett-rag/` | RAG 查询 skill（自动加载） |
| [docs/page-templates.md](docs/page-templates.md) | 各类页面的完整模板 |

## 当前进度

| 年份范围 | 状态 |
|----------|------|
| 1965-2024 伯克希尔信件 | ✅ |
| 1956-1969 合伙人信件 | ⏳ |
