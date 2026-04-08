# Buffett Wiki

基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，构建巴菲特知识库。

## 核心理念

- **LLM 是 IDE**：LLM 直接读取原始数据，维护 Wiki 页面
- **持久累积**：Wiki 是 LLM 构建的知识库，跨链接已建立
- **源可追溯**：每个 Wiki 页面可追溯到原始信件

## 目录结构

```
raw/                    # 原始材料（不可修改）
├── berkshire/zh/       # 伯克希尔中文信 (60封, 1965-2024)
├── berkshire/en/       # 伯克希尔英文信 (30封, 缺2007+)
└── partnership/zh/     # 合伙人中文信 (35封)

wiki/                   # LLM 维护的 Wiki
├── index.md           # 总索引
├── log.md             # 变更日志
├── letters/           # 信件笔记
├── concepts/          # 概念笔记
├── companies/        # 公司笔记
└── people/           # 人物笔记
```

## LLM 工作流

### 读取原始信件

```
你: 读取 1965 年的信件，提取关键概念

LLM → 读取 raw/berkshire/zh/1965-letter-zh.md
     → 分析内容，提取概念/公司/人物
     → 更新 wiki/letters/1965-letter.md
```

### 维护 Wiki

LLM 直接更新以下页面：
- `wiki/letters/` - 每封信的笔记
- `wiki/concepts/` - 概念定义和演变
- `wiki/companies/` - 公司投资逻辑
- `wiki/people/` - 人物关系
- `wiki/index.md` - 总索引
- `wiki/log.md` - 变更记录

## 概念索引

| 概念 | 英文名 | 首次阐述 |
|------|--------|----------|
| [内在价值](./wiki/concepts/内在价值.md) | Intrinsic Value | 1960s |
| [护城河](./wiki/concepts/护城河.md) | Economic Moat | 1990s |
| [浮存金](./wiki/concepts/浮存金.md) | Float | 1967 |
| [安全边际](./wiki/concepts/安全边际.md) | Margin of Safety | 1960s |

## 数据来源

- **中文源**: [buffett-letters-eir](https://buffett-letters-eir.pages.dev)
- **英文源**: Berkshire Hathaway 官网

## 维护指南

详见 [SCHEMA.md](./SCHEMA.md)

---
*本项目由 LLM 维护，人类负责数据 curation*
