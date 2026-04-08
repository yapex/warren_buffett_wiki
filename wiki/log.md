# Buffett Wiki 变更日志

按时间倒序记录 Wiki 的重要变更。

---

## [2026-04-08] 初始化 Wiki 结构

**类型**: setup | 初始化

### 完成的工作
- 创建 `wiki/index.md` - 总索引
- 创建 `wiki/log.md` - 变更日志
- 创建 `concepts/index.md` - 概念索引（含 10+ 核心概念）
- 创建 `companies/index.md` - 公司索引（含 10+ 核心公司）
- 创建 `people/index.md` - 人物索引（含 20+ 核心人物）

### 创建的详情页面
- 公司：伯克希尔·哈撒韦、盖可保险、可口可乐、美国运通、喜诗糖果
- 人物：沃伦·巴菲特、查理·芒格、本杰明·格雷厄姆、阿吉特·杰恩
- 概念：内在价值、护城河、浮存金、安全边际

### 使用的工具
- ClawTeam 多智能体协调
- pi coding agent (extractor + builder)

---

## [2026-04-07] 初始编译

**类型**: ingest | 初始数据导入

### 完成的工作
- 下载 60 封伯克希尔中文信
- 下载 35 封合伙人中文信
- 编译 60 封信件到 `wiki/letters/`
- 构建 RAG 索引

### 来源
- 中文源: buffett-letters-eir
- 英文源: Berkshire Hathaway 官网

---

*格式说明：每条日志以 `## [YYYY-MM-DD]` 开头，后跟类型标签*
*类型：setup | ingest | update | lint | query*
