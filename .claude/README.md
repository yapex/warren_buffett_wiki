# .claude Directory

此目录包含项目特定的 Claude skill 和配置。

## 目录结构

```
.claude/
├── skills/           # 项目特定 skills
│   ├── wiki-lint/   # Wiki 质量检查工具
│   └── wiki-query/  # Wiki RAG 查询工具
└── README.md        # 本文件
```

## Skills

### wiki-lint

Wiki 知识库质量检查工具。

**使用方法**：
```bash
# 完整检查
pi "lint wiki"

# 检查特定目录
pi "lint wiki/research/cases/"

# 自动修复
pi "lint wiki --fix"
```

详见 [wiki-lint/SKILL.md](skills/wiki-lint/SKILL.md)

### wiki-query

Wiki RAG 查询工具。

**使用方法**：
```bash
# 基础搜索
pi "查询 '安全边际'"

# 概念时间线
pi "查询 '护城河' --timeline"

# 文档内搜索
pi "在 1985-letter.md 中搜索 '纺织'"

# 年份范围
pi "搜索 '收购' --year=1970-1980"
```

详见 [wiki-query/SKILL.md](skills/wiki-query/SKILL.md)

## 与 pi 集成

pi 不会自动加载 `.claude/skills/` 中的技能，需要手动配置。

### 方法 1：全局配置（推荐）

在 `~/.pi/agent/settings.json` 中添加：

```json
{
  "skills": ["~/.agents/skills"]
}
```

然后创建软链接：

```bash
ln -s /Users/yapex/workspace/warren_buffett_wiki/.claude/skills/wiki-lint ~/.agents/skills/
ln -s /Users/yapex/workspace/warren_buffett_wiki/.claude/skills/wiki-query ~/.agents/skills/
```

### 方法 2：项目配置

在项目根目录创建 `.pi/settings.json`：

```json
{
  "skills": ["../.claude/skills"]
}
```

**注意**：由于 macOS 文件系统限制，软链接可能无法正常工作。推荐使用方法 1 的全局配置。

### 验证配置

```bash
# 测试 wiki-lint
pi "lint wiki"

# 测试 wiki-query
pi "查询 '安全边际'"
```

## 添加新 Skill

1. 在 `skills/` 目录下创建新目录
2. 添加 `SKILL.md` 定义触发条件和功能
3. 添加实现代码（Python/Shell 等）
4. 更新本 README

## 相关资源

- [Skills CLI](https://github.com/anthropics/skills)
- [Write a Skill](https://github.com/anthropics/write-a-skill)

---

*Last Updated: 2026-04-09*
