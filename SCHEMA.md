# Buffett Wiki 规范

## 核心理念

LLM 是 Wiki 的维护者，直接读取 raw 数据，按需更新 wiki 页面。RAG 提供全局上下文，增强 LLM 的跨信件分析能力。

## 角色分工

| 角色 | 职责 |
|------|------|
| **人类** | 数据 curation，不修改 raw 以外的内容 |
| **LLM** | 读取 raw，维护 wiki 页面 |
| **RAG** | 提供全局索引和跨信件上下文 |
| **Subagent** | 顺序处理每封信件 |

## 工具

### RAG 查询

```bash
uv run python .rag/query.py "查询内容"
```

LLM 可通过 RAG 查询：
- 某概念在所有信件中的分布
- 某公司/人物的跨信件关联
- 历史业绩对比数据
- 跨信件的关键信息

## 信件笔记模板

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
| ... | ... | ... |

> 📊 数据来源: 其他信件中的历史对比表

---

## 原文

[原文内容，只做段落分隔]

---

## 相关

- [伯克希尔](../companies/伯克希尔.md) | [巴菲特](../people/巴菲特.md)
- [YYYY+1 年信件](./YYYY+1-letter.md)
```

## 页面类型

### 信件笔记 (wiki/letters/YYYY-letter.md)

- **分析**: 背景、关键数据、历史业绩对比
- **原文**: 纯净原文，段落分隔
- **相关**: 关联的公司、人物、后续信件

### 概念笔记 (wiki/concepts/概念名.md)

```markdown
# 概念名 (英文名)

## 定义
...

## 巴菲特观点
...

## 演变历程
- **年份**: ...

## 相关概念
- [概念1](概念1.md)

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

### 公司笔记 (wiki/companies/公司名.md)

```markdown
# 公司名

## 简介
...

## 关键数据
| 项目 | 详情 |
|------|------|
| 投资时间 | YYYY |
| ... | ... |

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

### 人物笔记 (wiki/people/人物名.md)

```markdown
# 人物名

## 简介
...

## 相关概念
- [内在价值](../concepts/内在价值.md)

## 相关公司
- [伯克希尔](../companies/伯克希尔.md)

## 相关信件
- [YYYY-letter](../letters/YYYY-letter.md)
```

## 链接规范

使用标准 Markdown 链接：

| 类型 | 语法 |
|------|------|
| 同级目录 | `[名称](./name.md)` |
| 上级目录 | `[名称](../path/name.md)` |
| 原文链接 | `[原文](../../raw/berkshire/zh/YYYY-letter-zh.md)` |

## LLM 工作流

### Subagent 处理信件

LLM 按顺序处理每封信件：

```
For each letter (YYYY from 1965 to 2024):
    
    1. 查询 RAG
       ↓
       "查询 YYYY 年的关键信息"
       - 历史业绩对比
       - 相关概念/公司/人物
       - 在其他信中的提及
    
    2. 读取原文
       ↓
       raw/berkshire/zh/YYYY-letter-zh.md
    
    3. 分析并生成笔记
       ↓
       wiki/letters/YYYY-letter.md
       - 提取关键数据
       - 查询 RAG 获取历史对比
       - 关联已有概念/公司/人物
    
    4. 更新相关笔记
       ↓
       - 更新概念笔记的"演变历程"
       - 更新公司/人物笔记
       - 更新索引
    
    5. 记录日志
       ↓
       wiki/log.md
```

### 处理原则

| 原则 | 说明 |
|------|------|
| **原文优先** | 原文保持纯净，不做修改 |
| **分析前置** | 分析内容放在开头，便于快速了解 |
| **隔开段落** | 原文只做段落分隔，便于阅读 |
| **RAG 增强** | 利用 RAG 获取跨信件上下文 |
| **关联积累** | 每封信都关联已有的概念/公司/人物笔记 |

### 首次处理

1. **查询 RAG**: 获取该年份的历史背景
2. **读取原文**: 完整读取 `raw/berkshire/zh/YYYY-letter-zh.md`
3. **生成笔记**: 按模板生成 `wiki/letters/YYYY-letter.md`
4. **关联笔记**: 
   - 创建/更新 `wiki/concepts/` 相关概念
   - 创建/更新 `wiki/companies/` 相关公司
   - 创建/更新 `wiki/people/` 相关人物
5. **更新索引**: 更新 `wiki/concepts/index.md` 等
6. **记录日志**: 更新 `wiki/log.md`

### 扩展已有笔记

处理新信件时：

1. **查询 RAG**: 获取新信件与已有笔记的关联
2. **更新演变历程**: 在概念笔记中添加新年份
3. **添加相关信件**: 在公司/人物笔记中添加新信件链接
4. **记录日志**: 说明扩展的内容

## 日志格式

```markdown
## YYYY-MM-DD

**操作**: 添加 YYYY 年信件笔记

### 完成的工作
- 创建 wiki/letters/YYYY-letter.md
- 查询 RAG 获取历史业绩对比
- 更新 wiki/concepts/XXX.md 演变历程
- 更新 wiki/companies/XXX.md 相关信件

### 来源
raw/berkshire/zh/YYYY-letter-zh.md

### RAG 查询
"YYYY 年 伯克希尔 关键数据"
```

## 索引维护

- `wiki/concepts/index.md` - 概念索引
- `wiki/companies/index.md` - 公司索引
- `wiki/people/index.md` - 人物索引
- `wiki/log.md` - 变更日志

## 当前进度

| 年份范围 | 状态 |
|----------|------|
| 1965 | ✅ 完成 |
| 1966-2024 | ⏳ 待处理 |

---
*本规范由 LLM 维护*
