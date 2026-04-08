# Buffett Wiki 规范

## 角色分工

| 角色 | 职责 |
|------|------|
| **人类** | 数据 curation，不修改 raw 以外的内容 |
| **LLM** | 读取 raw，直接维护 wiki 页面 |

## 工作流

```
原始信件 (raw/) 
    ↓ LLM 读取
Wiki 页面 (wiki/)
    ↓ LLM 更新
索引/日志 (wiki/index.md, wiki/log.md)
```

## 页面类型

### 信件笔记 (wiki/letters/)

```markdown
# YYYY 巴菲特致股东信

## 核心观点
- ...

## 关键概念
- [内在价值](../concepts/内在价值.md)
- [浮存金](../concepts/浮存金.md)

## 相关公司
- [伯克希尔](../companies/伯克希尔.md)

## 相关人物
- [巴菲特](../people/巴菲特.md)

## 投资决策
...

## 我的理解
...

---
source: ../../raw/berkshire/zh/YYYY-letter-zh.md
```

### 概念笔记 (wiki/concepts/概念名.md)

```markdown
# 内在价值 (Intrinsic Value)

## 定义
对未来现金流的折现。

## 巴菲特观点
"模糊的正确胜过精确的错误"

## 演变历程
- **1960s**: 从格雷厄姆处学习
- **1980s**: 强调业务质量
- **2000s**: 强调确定性

## 相关概念
- [安全边际](安全边际.md)
- [市场先生](市场先生.md)

## 相关信件
- [1965-letter](../letters/1965-letter.md)
```

### 公司笔记 (wiki/companies/公司名.md)

```markdown
# 伯克希尔·哈撒韦

## 投资时间
1965 年

## 投资逻辑
纺织业务的隐蔽资产

## 转型
从纺织厂转型为保险集团

## 关键数据
- 1965 年收购价: ~$14.86/股
- 当前状态: 仍在伯克希尔旗下

## 相关信件
- [1965-letter](../letters/1965-letter.md)
```

### 人物笔记 (wiki/people/人物名.md)

```markdown
# 巴菲特

## 角色
伯克希尔董事长兼 CEO

## 相关概念
- [内在价值](../concepts/内在价值.md)
- [护城河](../concepts/护城河.md)

## 相关公司
- [伯克希尔](../companies/伯克希尔.md)
```

## 链接规范

使用标准 Markdown 链接：

| 类型 | 语法 |
|------|------|
| 同级目录 | `[名称](./name.md)` |
| 上级目录 | `[名称](../path/name.md)` |
| 原文链接 | `[原文](../../raw/berkshire/zh/YYYY-letter-zh.md)` |

## LLM 维护指南

### 首次读取信件

1. 读取 `raw/berkshire/zh/YYYY-letter-zh.md`
2. 创建 `wiki/letters/YYYY-letter.md`
3. 提取核心观点、关键概念、相关实体
4. 更新 `wiki/concepts/` 中相关概念笔记
5. 更新 `wiki/companies/` 和 `wiki/people/`
6. 记录到 `wiki/log.md`

### 扩展已有笔记

1. 读取新的信件内容
2. 更新概念的"演变历程"
3. 添加新的相关公司/人物
4. 补充投资决策细节
5. 记录到 `wiki/log.md`

### 维护索引

- 概念索引: `wiki/concepts/index.md`
- 公司索引: `wiki/companies/index.md`
- 人物索引: `wiki/people/index.md`

## 日志格式

```markdown
# Buffett Wiki 变更日志

## 2026-04-08

**操作**: 添加 1965 年信件笔记

### 完成的工作
- 创建 wiki/letters/1965-letter.md
- 创建 wiki/concepts/内在价值.md
- 更新 wiki/index.md

### 来源
raw/berkshire/zh/1965-letter-zh.md
```
