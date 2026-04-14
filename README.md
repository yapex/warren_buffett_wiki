---
type: index
---

# Buffett Wiki

基于 [Karpathy LLM Wiki 精神](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，构建巴菲特知识库。

> ⚠️ **重要声明**：本知识库仅供个人学习、研究和教育目的使用，不得用于商业用途。内容不构成投资建议。

---

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

### 🚀 首次安装

克隆仓库后，运行一键安装脚本：

```bash
cd warren_buffett_wiki
./scripts/install.sh
```

安装脚本会自动完成：
- ✅ Git Hooks 配置（自动索引更新）
- ✅ Python 依赖安装（uv sync）
- ✅ Meilisearch 配置（.env.meilisearch）
- ✅ 服务状态检查

### 🔍 搜索功能（Meilisearch）

```bash
# 搜索段落
buffett-wiki search 安全边际
buffett-wiki s 护城河

# 概念时间线
buffett-wiki timeline 内在价值
buffett-wiki t 浮存金

# 文档内搜索
buffett-wiki doc 安全边际 wiki/concepts/安全边际.md

# 带过滤搜索
buffett-wiki filter 投资 --type letters --from 1980
buffett-wiki f 可口可乐 --type companies

# 分面统计
buffett-wiki facets doc_type
buffett-wiki facets year

# 增量更新索引（最近 1 小时修改的文件）
buffett-wiki rebuild

# 性能测试
buffett-wiki benchmark
```

### 📜 旧版 RAG 命令（保留兼容）

```bash
# 搜索段落
uv run buffett-rag search 安全边际
uv run buffett-rag s 护城河

# 概念时间线
uv run buffett-rag timeline 内在价值
uv run buffett-rag t 浮存金

# 重建索引
uv run buffett-rag rebuild
```

## 总索引

👉 **[查看 index.md](./index.md)** - 包含 60 封信件、24 篇访谈演讲、95 个概念、57 家公司、41 位人物的完整索引

## 当前进度

| 类型 | 数量 | 状态 |
|------|------|------|
| 伯克希尔股东信笔记 | 60 | 1965-2024 ✅ |
| 合伙人信笔记 | 15 | 1956-1970 ✅ |
| 访谈与演讲笔记 | 24 | 1985-2025 ✅ |
| 概念笔记 | 95 | ✅ |
| 公司笔记 | 57 | ✅ |
| 人物笔记 | 41 | ✅ |
| 研究笔记 | 3 | ✅ |
| 经典案例 | 24 | ✅ |

## 致谢

本 Wiki 的原始数据来源于：

- **[巴菲特致股东信](https://buffett-letters-eir.pages.dev/)** - 提供完整的中文翻译
- **Berkshire Hathaway 官网** - 提供官方英文原版

---

## 许可与声明

### 许可协议

本知识库采用 [CC BY-NC-SA 4.0](LICENSE) 许可协议：

- ✅ **署名** - 使用时须注明原始来源
- ✅ **非商业性使用** - 不得用于商业目的
- ✅ **相同方式共享** - 衍生作品须采用相同许可

### 重要声明

1. **仅供个人学习使用**：本知识库仅供个人学习、研究和教育目的使用，禁止任何形式的商业用途。

2. **不构成投资建议**：所有内容仅供参考和学习，不构成任何投资建议、推荐或建议。投资决策应基于您自己的研究或咨询专业财务顾问。

3. **内容准确性**：不保证信息的完整性、准确性或时效性。

4. **版权尊重**：巴菲特致股东信、合伙人信等原始内容的版权归原版权所有人所有。本知识库的整理和注释采用 CC BY-NC-SA 4.0 许可。

5. **电子书内容**：涉及《巴菲特的第一桶金》等电子书的案例研究仅供个人学习研究使用。原电子书版权归出版社和作者所有，请勿传播原始电子书内容。

详见 [LICENSE](LICENSE) 完整条款。
