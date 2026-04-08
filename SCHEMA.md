# Buffett Wiki 规范

## 项目定位

基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，从巴菲特致股东信构建中文知识库。

### 核心理念

Wiki 是持久累积的知识库：
- **持久性**：知识被编译并保持最新，不必每次查询时重新推导
- **跨链接**：引用已建立，可追溯到原始信
- **增量更新**：新增信件时，更新相关概念/公司/人物页面
- **LLM 维护**：LLM 负责编译和维护，人类负责源 curation

## 目录结构

```
raw/                    # 原始材料（不可修改）
├── berkshire/zh/       # 伯克希尔中文信 (1965-2024)
├── berkshire/en/       # 伯克希尔英文信 (1977-2024)
└── partnership/zh/     # 合伙人中文信 (1956-1970)

wiki/                   # 编译后的中文 Wiki
├── index.md           # 总索引（内容导向）
├── log.md             # 变更日志（时间导向）
├── letters/           # 信件页面
├── concepts/           # 概念页面 + 索引
├── companies/         # 公司页面 + 索引
└── people/            # 人物页面 + 索引
```

## Wiki 页面模板

### 信件页 (letters/YYYY-letter.md)

```markdown
---
source: ../../raw/berkshire/zh/YYYY-letter-zh.md
year: YYYY
compiled: YYYY-MM-DD
---

# YYYY 巴菲特致股东信

> [!原文]
> [EN](../../raw/berkshire/en/YYYY-letter-en.md)

## 概要

本信回顾了伯克希尔 YYYY 年的经营成果和投资理念。

## 关键主题

- 主题1
- 主题2
- ...

## 涉及实体

- **公司**: [公司名](../companies/公司名.md), [公司名](../companies/公司名.md)
- **人物**: [人物名](../people/人物名.md), [人物名](../people/人物名.md)

---

## 全文

[格式化正文，每段适当宽度]

---

*本页面由 LLM 编译，原始中文文本见 [YYYY-letter-zh.md](../../raw/berkshire/zh/YYYY-letter-zh.md)*
```

### 概念页 (concepts/概念名.md)

```markdown
---
type: concept
first_appeared: YYYY
---

# 概念名

## 定义

## 巴菲特观点

## 相关概念

- [相关概念1](../concepts/相关概念1.md)
- [相关概念2](../concepts/相关概念2.md)

## 相关公司

- [相关公司](../companies/相关公司.md)

## 相关人物

- [相关人物](../people/相关人物.md)

## 相关信件

- [YYYY-letter](../letters/YYYY-letter.md)
```

### 公司页 (companies/公司名.md)

```markdown
---
type: company
first_appeared: YYYY
---

# 公司名

## 公司简介

## 巴菲特投资逻辑

## 关键数据

- **投资时间**: YYYY
- **持股比例**: XX%
- **投资金额**: XX亿美元

## 相关概念

- [概念1](../concepts/概念1.md)
- [概念2](../concepts/概念2.md)

## 相关信件

- [YYYY-letter](../letters/YYYY-letter.md)
```

### 人物页 (people/人物名.md)

```markdown
---
type: person
first_appeared: YYYY
---

# 人物名

## 人物简介

## 角色

## 相关概念

- [概念1](../concepts/概念1.md)

## 相关公司

- [公司](../companies/公司.md)

## 相关信件

- [YYYY-letter](../letters/YYYY-letter.md)
```

### 总索引页 (index.md)

```markdown
---
type: index
title: Buffett Wiki 总索引
---

# Buffett Wiki

## 概述

## 核心概念

| 概念 | 说明 |
|------|------|
| [内在价值](./concepts/内在价值.md) | ... |
| [护城河](./concepts/护城河.md) | ... |

## 核心公司

## 核心人物

## 与 Karpathy LLM Wiki 的对应

| 层次 | 本项目实现 |
|------|-----------|
| 原始材料 | raw/ |
| Wiki | wiki/ |
| Schema | SCHEMA.md |
```

### 变更日志 (log.md)

```markdown
# Buffett Wiki 变更日志

## [YYYY-MM-DD] 变更描述

**类型**: setup | ingest | update | lint | query

### 完成的工作
- ...

### 使用的工具
- ...
```

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 信件 | `YYYY-letter.md` | `2023-letter.md` |
| 公司 | 中文全称 | `伯克希尔·哈撒韦.md` |
| 人物 | 中文名 | `沃伦·巴菲特.md` |
| 概念 | 中文核心术语 | `内在价值.md` |

## 链接规范

| 类型 | 语法 | 指向 |
|------|------|------|
| Markdown 链接 | `[名称](./path/name.md)` | wiki 内部页面 |
| 原文链接 | `[EN](path)` | 英文原文 |
| 索引链接 | `[index](./path/index.md)` | 索引页面 |

> 💡 使用标准 Markdown 链接格式，兼容所有阅读器

## 维护流程

### 新增信件

1. 将原始信件放入 `raw/berkshire/zh/`
2. 运行 `scripts/compile_wiki.py`
3. LLM 更新：
   - 相关概念页面（提及的概念）
   - 相关公司页面（提及的公司）
   - 相关人物页面（提及的人物）
   - `log.md` 记录变更

### 查询

1. 搜索相关 Wiki 页面
2. 阅读摘要和关键主题
3. 点击 wikilink 查看详情
4. 可追溯到原始信件

### 定期检查

定期运行 LLM lint：
- 检查页面间矛盾
- 检查过时内容
- 检查孤立页面
- 检查缺失链接

## 编译脚本

```bash
# 编译所有信件
uv run python scripts/compile_wiki.py
```

脚本功能：
1. 提取关键主题
2. 提取涉及实体
3. 生成 wikilink
4. 格式化正文
