# wiki-lint

Buffett Wiki 知识库质量检查工具。

## 触发条件

当用户提到以下关键词时触发此 skill：
- "lint wiki"
- "检查 wiki"
- "验证链接"
- "检查链接"
- "质量检查"
- "wiki lint"
- "检查 Markdown"
- "修复链接"
- "validate wiki"
- "check links"

## 功能

### 1. 链接检查

检查所有 Markdown 文件中的链接：
- 内部链接是否指向存在的文件
- 链接格式是否统一（相对路径）
- 检测死链和悬空链接

### 2. 命名规范检查

验证文件命名是否符合规范：
- 信件：`YYYY-letter.md`（如 `1965-letter.md`）
- 概念：`概念名.md`（如 `安全边际.md`）
- 公司：`公司名.md`（如 `美国运通.md`）
- 人物：`人名.md`（如 `沃伦·巴菲特.md`）
- 案例：`公司名 - 年份 - 主题.md`（如 `美国运通 -1964-色拉油危机.md`）

### 3. Frontmatter 检查

验证 YAML frontmatter：
- 必需字段是否存在（type, title 等）
- 字段值是否符合规范
- 检测重复的 type

### 4. 内容质量检查

- 检测空文件
- 检测过短的页面
- 检测重复内容
- 检测过时的链接格式（如 `[[概念]]`）

## 使用方法

### 基础检查

```
lint wiki
```

### 检查特定目录

```
lint wiki/research/cases/
```

### 检查特定类型

```
lint wiki --type=letters
lint wiki --type=companies
lint wiki --type=concepts
```

### 自动修复

```
lint wiki --fix
```

## 输出格式

### 错误级别

- 🔴 **ERROR**: 必须修复的问题（死链、缺失文件）
- 🟡 **WARNING**: 建议修复的问题（命名不规范、缺少 frontmatter）
- ℹ️ **INFO**: 信息提示（统计信息）

### 示例输出

```
🔍 开始检查 Buffett Wiki...

📁 检查范围：wiki/
📄 文件总数：156

🔴 ERRORS (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ERROR] wiki/research/cases/案例 1.md
  Line 45: 死链 → [概念](../../concepts/不存在的概念.md)
  Line 78: 死链 → [公司](../../companies/不存在的公司.md)

[ERROR] wiki/companies/公司名.md
  Line 1: 缺少 frontmatter

🟡 WARNINGS (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[WARNING] wiki/letters/1965-letter.md
  Line 23: 过时链接格式 [[安全边际]] → 应改为 [安全边际](../../concepts/安全边际.md)

[WARNING] wiki/concepts/新概念.md
  缺少 type 字段

ℹ️ SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 通过检查：148 个文件
🔴 错误：3 个文件
🟡 警告：5 个文件

运行 'lint wiki --fix' 自动修复可修复的问题
```

## 检查规则

### 链接规则

1. **内部链接必须使用相对路径**
   - ✅ `[概念](../../concepts/安全边际.md)`
   - ❌ `[概念](/wiki/concepts/安全边际.md)`
   - ❌ `[概念](wiki/concepts/安全边际.md)`

2. **信件链接格式**
   - ✅ `[1965-letter.md](../../letters/1965-letter.md)`
   - ❌ `[1965 年致股东信](../../letters/1965-致股东信.md)`

3. **禁止 Obsidian 链接格式**
   - ✅ `[安全边际](../../concepts/安全边际.md)`
   - ❌ `[[安全边际]]`

### 命名规则

1. **信件文件**
   - 格式：`YYYY-letter.md`
   - 示例：`1965-letter.md`, `2024-letter.md`

2. **案例研究**
   - 格式：`公司名 - 年份 - 主题.md`
   - 示例：`美国运通 -1964-色拉油危机.md`

3. **避免特殊字符**
   - 文件名不应包含：`? * : | < >`

### Frontmatter 规则

1. **必需字段**
   - `type`: 页面类型（letter/company/concept/person/case_study）
   - `title`: 页面标题（可选，如与文件名相同可省略）

2. **type 有效值**
   - `letter`: 信件
   - `company`: 公司
   - `concept`: 概念
   - `person`: 人物
   - `case_study`: 案例研究

## 自动修复功能

使用 `--fix` 标志时自动修复以下问题：

1. **链接格式转换**
   - `[[概念]]` → `[概念](../../concepts/概念.md)`
   - `[[人物]]` → `[人物](../../people/人物.md)`

2. **信件链接标准化**
   - `XXX-致合伙人信.md` → `XXX-letter.md`
   - `XXX-致股东信.md` → `XXX-letter.md`

3. **路径规范化**
   - 统一使用 `../../` 前缀

## 配置文件

可在项目根目录创建 `.wiki-lint.json` 自定义规则：

```json
{
  "ignore": [
    "wiki/ebooks/**",
    "wiki/temp/**"
  ],
  "rules": {
    "check-links": true,
    "check-frontmatter": true,
    "check-naming": true,
    "check-empty-files": true
  },
  "fix": {
    "convert-wiki-links": true,
    "normalize-letter-links": true
  }
}
```

## 集成建议

### Git Hook

在提交前自动运行 lint：

```bash
# .git/hooks/pre-commit
#!/bin/bash
pi "lint wiki"
if [ $? -ne 0 ]; then
  echo "❌ Lint 检查失败，请修复问题后再提交"
  exit 1
fi
```

### CI/CD

在 GitHub Actions 中添加检查：

```yaml
- name: Lint Wiki
  run: pi "lint wiki"
```

## 相关文件

- 项目根目录：`/Users/yapex/workspace/warren_buffett_wiki/`
- Wiki 目录：`wiki/`
- 信件目录：`wiki/letters/`
- 概念目录：`wiki/concepts/`
- 公司目录：`wiki/companies/`
- 人物目录：`wiki/people/`
- 案例目录：`wiki/research/cases/`

## 示例命令

```bash
# 完整检查
pi "lint wiki"

# 只检查案例研究
pi "lint wiki/research/cases/"

# 检查并自动修复
pi "lint wiki --fix"

# 只检查链接
pi "lint wiki --check=links"

# 只检查 frontmatter
pi "lint wiki --check=frontmatter"

# 输出详细报告
pi "lint wiki --verbose"
```

## 维护说明

当添加新的检查规则时：
1. 在 SKILL.md 中更新"检查规则"部分
2. 更新输出格式示例
3. 测试新规则的有效性

---

*Last Updated: 2026-04-09*
