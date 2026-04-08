# Buffett Wiki

基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，构建巴菲特知识库。

## 核心理念

- **LLM 是 IDE**: 直接读取 raw 数据，维护 Wiki 页面
- **RAG 增强**: 提供全局上下文，跨信件关联
- **持久累积**: Wiki 是 LLM 构建的知识库

## 目录结构

```
raw/                    # 原始材料（不可修改）
├── berkshire/zh/       # 伯克希尔中文信 (60封, 1965-2024)
├── berkshire/en/       # 伯克希尔英文信 (30封)
└── partnership/zh/     # 合伙人中文信 (35封)

wiki/                   # LLM 维护的 Wiki
├── letters/           # 信件笔记 [示例](./wiki/letters/1965-letter.md)
├── concepts/          # 概念笔记
├── companies/        # 公司笔记
├── people/           # 人物笔记
├── index.md         # 总索引
└── log.md           # 变更日志

.rag/                  # RAG 索引和查询
└── query.py          # uv run python .rag/query.py "查询"
```

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

## 当前进度

| 类型 | 数量 | 状态 |
|------|------|------|
| 伯克希尔中文信 | 60 | 1965 ✅ |
| 合伙人中文信 | 35 | ⏳ |
| 信件笔记 | 60 | 1/60 |
| 概念笔记 | - | ⏳ |
| 公司笔记 | - | ⏳ |
| 人物笔记 | - | ⏳ |

## 数据来源

- **中文源**: [buffett-letters-eir](https://buffett-letters-eir.pages.dev)
- **英文源**: Berkshire Hathaway 官网
