# 页面模板

> 各类 Wiki 页面的完整模板。创建新页面时参考。
> 
> **最后更新**: 2026-04-09

## 信件笔记 (wiki/letters/YYYY-letter.md)

```markdown
# YYYY 年巴菲特致股东信

> **原文**: [raw/berkshire/zh/YYYY-letter-zh.md](../../raw/berkshire/zh/YYYY-letter-zh.md)
> **执笔**: 沃伦·巴菲特

---

## 分析

### 背景
- ...

### 关键数据
| 指标 | 数值 |
|------|------|
| ... | ... |

### 历史业绩 (YYYY-YYYY+2)
| 年份 | 伯克希尔 | 标普 500 |
|------|----------|----------|

> 📊 数据来源：其他信件中的历史对比表

---

## 原文

[原文内容，只做段落分隔]

---

## 相关

- [伯克希尔](../companies/伯克希尔.md) | [巴菲特](../people/巴菲特.md)
- [YYYY+1 年信件](./YYYY+1-letter.md)
```

## 概念笔记 (wiki/concepts/概念名.md)

```markdown
---
type: concept
first_appeared: YYYY
tags: [标签 1, 标签 2]
---

# 概念名 (英文名)

## 定义
...

## 巴菲特观点

### 核心论述
> 原文引用

### 演变历程
- **YYYY 年**: ...
- **YYYY 年**: ...

## 相关概念
- [概念 1](概念 1.md)

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

## 公司笔记 (wiki/companies/公司名.md)

```markdown
# 公司名

## 简介
...

## 关键数据
| 项目 | 详情 |
|------|------|
| 投资时间 | YYYY |
| 持仓规模 | ... |

## 投资逻辑
...

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

## 人物笔记 (wiki/people/人物名.md)

```markdown
---
type: person
first_appeared: YYYY
---

# 人物名

## 人物简介
...

## 思想贡献 / 对巴菲特的影响
...

## 相关概念
- [概念](../concepts/概念.md)

## 相关公司
- [公司](../companies/公司.md)

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

## 研究笔记 (wiki/research/主题名.md)

> 跨信件的深度分析。Query 操作中好的答案写回为此类型。

```markdown
---
type: research
created: YYYY-MM-DD
updated: YYYY-MM-DD  # 可选，最后更新日期
sources: [1969-合伙人信，1992-信，1999-信，...]
status: draft | complete
---

# 研究标题

## 研究问题
简述要回答的问题。

## 结论摘要
一两句话概括核心发现。

---

## 详细分析

### 主题一
...

## 证据清单

| 来源 | 引用 | 要点 |
|------|------|------|
| [YYYY-letter](../letters/YYYY-letter.md) | "..." | ... |

## 相关概念
- [概念](../concepts/概念.md)

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

## 案例研究笔记 (wiki/research/cases/公司名 - 年份 - 主题.md)

> 单个投资案例的深度研究，通常基于《巴菲特的第一桶金》等资料。

```markdown
---
type: case_study
company: 公司名
year: 年份
source: 来源（如：巴菲特的第一桶金）
created: YYYY-MM-DD
theme: 投资主题（可选）
---

# 公司名：年份 - 主题

> **参考来源**：《巴菲特的第一桶金》案例 X（格伦·阿诺德著）

---

## 案例概述
- 一句话总结
- 关键数据表格

## 投资背景
- 市场环境
- 公司状况
- 危机/机会

## 巴菲特的调研/分析
- 调研方法
- 关键发现
- 核心结论

## 投资决策与执行
- 关键时点
- 仓位管理
- 买卖决策

## 投资逻辑分析
- 为什么符合/不符合格雷厄姆标准
- 关键洞察
- 竞争优势分析

## 投资哲学意义
- 在投资哲学演变中的位置
- 与前后案例的关联
- 影响因素（费雪、芒格等）

## 学习要点
- 3-5 个核心教训
- 每个要点有具体说明

## 相关链接
### 公司页面
- [公司名](../../companies/公司名.md)

### 信件
- [YYYY-letter](../../letters/YYYY-letter.md)

### 概念
- [概念 1](../../concepts/概念 1.md)

### 其他案例
- [相关案例](./相关案例.md)

## 原文摘录
- 2-3 段关键原文引用

---

> **研究笔记**：本案例研究基于格伦·阿诺德《巴菲特的第一桶金》案例 X。
```

## 访谈笔记 (wiki/interviews/YYYY-标题.md)

> 借鉴 Tina 巴菲特知识库的访谈格式：核心要点 → 详细摘要 → 交叉引用 → 金句 → 原文。

```markdown
---
type: interview
year: YYYY
subtype: speech | interview | shareholder_meeting | dialogue
venue: 场所/机构
date: YYYY-MM-DD（精确日期，未知用年份）
tags: [标签 1, 标签 2]
---

# YYYY 年标题

> **类型**: 演讲 / 专访 / 股东大会问答 / 对谈
> **场合**: 场所或机构
> **日期**: YYYY-MM-DD

---

## 核心要点

1. **要点一**：一句话概括（加粗关键词）
2. **要点二**：一句话概括
3. ...

---

## 详细摘要

### 主题一

2-3 段详细阐述，包含原文引用和背景说明。

### 主题二

...

---

## 提到的概念

- [概念名](../concepts/概念名.md) — 一句话说明在本次访谈中的含义
- ...

## 提到的公司

- [公司名](../companies/公司名.md) — 一句话说明
- ...

## 提到的人物

- [人物名](../people/人物名.md) — 一句话说明
- ...

---

## 原文金句

> "金句一"

> "金句二"

---

## 原文

[完整原文或可展开的原文链接]

---

## 相关

- [相关信件](../letters/YYYY-letter.md)
- [相关概念](../concepts/概念.md)
- [下一年访谈](./YYYY+1-标题.md)
```

## 链接规范

使用标准 Markdown 链接（不用 `[[]]`）：

| 类型 | 语法 | 示例 |
|------|------|------|
| 同级 | `[名称](./name.md)` | `[1966 年信件](./1966-letter.md)` |
| 上级 | `[名称](../path/name.md)` | `[伯克希尔](../companies/伯克希尔.md)` |
| 原文 | `[原文](../../raw/berkshire/zh/YYYY-letter-zh.md)` | `[原文](../../raw/berkshire/zh/1965-letter-zh.md)` |
| 跨目录 | `[名称](../../dir/name.md)` | `[案例](../../research/cases/案例.md)` |

---

## Frontmatter 字段说明

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | ✅ | 页面类型 | `letter`, `concept`, `company`, `person`, `research`, `case_study`, `interview` |
| `created` | date | ✅ | 创建日期 | `2026-04-09` |
| `updated` | date | ❌ | 最后更新日期 | `2026-04-09` |
| `sources` | array | ✅ (research) | 数据来源列表 | `[1969-合伙人信，1992-信]` |
| `status` | string | ✅ (research) | 完成状态 | `draft`, `complete` |
| `first_appeared` | number | ❌ | 首次出现年份 | `1965` |
| `tags` | array | ❌ | 标签列表 | `["估值", "投资哲学"]` |
| `company` | string | ❌ (case_study) | 所属公司 | `美国运通` |
| `year` | number | ❌ (case_study) | 案例年份 | `1964` |
| `theme` | string | ❌ (case_study) | 案例主题 | `色拉油危机` |
| `subtype` | string | ❌ (interview) | 访谈子类型 | `speech`, `interview`, `shareholder_meeting`, `dialogue` |
| `venue` | string | ❌ (interview) | 访谈场合 | `佛罗里达大学` |
| `date` | string | ❌ (interview) | 精确日期 | `1998-10-15` |
