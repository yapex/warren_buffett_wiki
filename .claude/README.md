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

## pi 集成配置

### 已完成配置

技能已软链接到 `~/.agents/skills/`，pi 已配置加载：

```bash
# 验证软链接
ls -la ~/.agents/skills/ | grep wiki

# 测试技能
pi "lint wiki"
pi "查询 '安全边际'"
```

### 在其他项目中配置

如果要在其他项目中使用这些技能，添加软链接：

```bash
ln -s /Users/yapex/workspace/warren_buffett_wiki/.claude/skills/wiki-lint ~/.agents/skills/
ln -s /Users/yapex/workspace/warren_buffett_wiki/.claude/skills/wiki-query ~/.agents/skills/
```

或在项目 `.pi/settings.json` 中添加：

```json
{
  "skills": ["../warren_buffett_wiki/.claude/skills"]
}
```

## 与全局 Skills 的区别

- **全局 Skills** (`~/.pi/agent/skills/` 或 `~/.agents/skills/`): 跨项目通用的技能
- **项目 Skills** (`.claude/skills/`): 本项目特定的技能

本项目技能通过软链接注册到 `~/.agents/skills/`，可在所有项目中使用。

## 添加新 Skill

1. 在 `skills/` 目录下创建新目录
2. 添加 `SKILL.md` 定义触发条件和功能
3. 添加实现代码（Python/Shell 等）
4. 创建软链接到 `~/.agents/skills/`
5. 更新本 README

## 相关资源

- [Skills CLI](https://github.com/anthropics/skills)
- [Write a Skill](https://github.com/anthropics/write-a-skill)

---

*Last Updated: 2026-04-09*
