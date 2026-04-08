# Buffett Wiki

基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，构建巴菲特知识库。

## 核心理念

- **LLM 是 IDE**: 直接读取 raw 数据，维护 Wiki 页面
- **RAG 增强**: 提供全局上下文，跨信件关联
- **持久累积**: Wiki 是 LLM 构建的知识库

## LLM 工作流

```
For each letter (1965-2024):
    
    1. RAG 查询 → 获取全局上下文
    2. 读取原文 → raw/berkshire/zh/YYYY-letter-zh.md
    3. 生成笔记 → wiki/letters/YYYY-letter.md
    4. 关联更新 → concepts/companies/people 笔记
    5. 记录日志 → wiki/log.md
```

详见 [SCHEMA.md](./SCHEMA.md)

## 快速开始

```bash
# RAG 查询
uv run python .rag/query.py "巴菲特如何看待保险"

# 交互模式
uv run python .rag/query.py
```

## 总索引

👉 **[查看 index.md](./index.md)** - 包含 60 封信件、25 个核心概念、32 家公司、25 位人物的完整索引

## 当前进度

| 类型 | 数量 | 状态 |
|------|------|------|
| 伯克希尔中文信 | 60 | 1965-2024 ✅ |
| 合伙人中文信 | 35 | ⏳ 待处理 |
| 信件笔记 | 60 | ✅ |
| 概念笔记 | 25+ | ✅ |
| 公司笔记 | 32+ | ✅ |
| 人物笔记 | 25+ | ✅ |

## 致谢

本 Wiki 的原始数据来源于：

- **[巴菲特致股东信](https://buffett-letters-eir.pages.dev/)** - 提供完整的中文翻译
- **Berkshire Hathaway 官网** - 提供官方英文原版
