# Buffett Wiki 规范

## 项目定位

基于 Karpathy 的 LLM Wiki 精神，从巴菲特致股东信构建中文知识库。

## 目录结构

```
raw/                    # 原始材料（不可修改）
├── berkshire/zh/       # 伯克希尔中文信 (1965-2024)
├── berkshire/en/       # 伯克希尔英文信 (1977-2024)
└── partnership/zh/     # 合伙人中文信 (1956-1970)

wiki/                   # 编译后的中文 Wiki
├── letters/            # 信件
├── concepts/           # 概念
├── companies/          # 公司
└── people/             # 人物
```

## Wiki 页面模板

### 信件页 (letters/YYYY-letter.md)

```markdown
---
source: raw/berkshire/zh/YYYY-letter-zh.md
en: raw/berkshire/en/YYYY-letter-en.md
year: YYYY
---

# YYYY 巴菲特致股东信

> [!原文]
> [EN](../raw/berkshire/en/YYYY-letter-en.md)

## 概要

[LLM 提取的概要]

## 关键主题

- 主题1
- 主题2

## 涉及实体

- [[公司名]]
- [[人物名]]
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

## 相关信件

- [[YYYY-信件]]
```

## 命名规范

- 信件：`YYYY-letter.md`
- 公司：中文全称
- 人物：中文名（附英文）
- 概念：中文核心术语

## 链接规范

- Wikilink：`[[目标]]` 指向 wiki 内部
- 原文链接：`[EN](raw/berkshire/en/YYYY-letter-en.md)` 指向英文原文
