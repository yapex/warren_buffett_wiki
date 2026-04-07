# Buffett Wiki + LightRAG

基于 [Karpathy 的 LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，构建巴菲特知识库。

## 项目定位

1. **原始材料收集** → 下载所有中文/英文巴菲特信（raw 目录）
2. **Wiki 编译** → 纯中文，概念提取，wikilink 指向英文原文
3. **LightRAG 集成** → 支持复杂查询，可追溯到原始信

## 目录结构

```
├── raw/                    # 原始材料
│   ├── berkshire/zh/       # 伯克希尔中文 (60封, 1965-2024)
│   ├── berkshire/en/       # 伯克希尔英文 (30封, 缺2007+)
│   └── partnership/zh/     # 合伙人中文 (35封)
├── wiki/                   # 中文 Wiki (60封已编译)
│   └── letters/            # 信件
├── rag/                    # RAG 查询
│   ├── config.py           # 索引配置
│   └── query.py            # 查询脚本
└── scripts/                # 下载/编译脚本
    ├── download_berkshire_zh.py
    ├── download_berkshire_en.py
    ├── download_partnership_zh.py
    └── compile_wiki.py
```

## 快速开始

### 1. 下载信件

```bash
uv run python scripts/download_berkshire_zh.py   # 中文伯克希尔信
uv run python scripts/download_partnership_zh.py # 中文合伙人信
uv run python scripts/download_berkshire_en.py   # 英文信
```

### 2. 编译 Wiki

```bash
uv run python scripts/compile_wiki.py
```

### 3. RAG 查询

```bash
# 命令行
uv run python rag/query.py "巴菲特如何看待保险业务"

# 交互模式
uv run python rag/query.py
```

## 当前进度

| 类型 | 数量 | 状态 |
|------|------|------|
| 伯克希尔中文 | 60封 | ✅ 完成 |
| 合伙人中文 | 35封 | ✅ 完成 |
| 伯克希尔英文 | 30/48封 | ⚠️ 部分缺失 |
| Wiki 编译 | 60封 | ✅ 完成 |
| RAG 索引 | 60封 | ✅ 完成 |

## 数据来源

- **中文源**: [buffett-letters-eir](https://buffett-letters-eir.pages.dev)
- **英文源**: Berkshire Hathaway 官网

## 待完成

- [ ] 补全缺失的英文信件 (2007-2024)
- [ ] 概念提取 (concepts/)
- [ ] 公司/人物页面 (companies/, people/)
- [ ] 集成真正的 LLM 支持
