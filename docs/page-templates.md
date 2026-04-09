# 页面模板

> 各类 Wiki 页面的完整模板。创建新页面时参考。

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

> 📊 数据来源: 其他信件中的历史对比表

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
tags: [标签1, 标签2]
---

# 概念名 (英文名)

## 定义
...

## 巴菲特观点

### 核心论述
> 原文引用

### 演变历程
- **YYYY年**: ...
- **YYYY年**: ...

## 相关概念
- [概念1](概念1.md)

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
sources: [1969-合伙人信, 1992-信, 1999-信, ...]
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

## 链接规范

使用标准 Markdown 链接（不用 `[[]]`）：

| 类型 | 语法 |
|------|------|
| 同级 | `[名称](./name.md)` |
| 上级 | `[名称](../path/name.md)` |
| 原文 | `[原文](../../raw/berkshire/zh/YYYY-letter-zh.md)` |
