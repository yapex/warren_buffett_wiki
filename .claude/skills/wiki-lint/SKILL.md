---
name: wiki-lint
description: Buffett Wiki 知识库质量检查工具。当用户提到 "lint wiki"、"检查 wiki"、"验证链接"、"质量检查"、"修复链接" 时触发。
---

# wiki-lint

Buffett Wiki 知识库质量检查与修复工具。

## 触发条件

- "lint wiki" / "wiki lint" / "检查 wiki" / "验证链接" / "检查链接"
- "质量检查" / "修复链接" / "validate wiki" / "check links"

## 架构

```
.pi/skills/wiki-lint/
├── SKILL.md              ← 本文件
├── lint.py               ← CLI 入口，编排各模块
└── scripts/              ← 可复用核心模块
    ├── config.py         ← 路径约定、命名规则、frontmatter 规范（数据驱动）
    ├── report.py         ← Issue 数据类 + 报告格式化
    ├── links.py          ← 链接提取 / 解析 / 模糊匹配（通用方法）
    ├── naming.py         ← 文件命名规范检查
    ├── frontmatter.py    ← frontmatter 解析与校验
    ├── quality.py        ← 内容质量（空文件、短文件）
    └── fix.py            ← 自动修复策略（可扩展）
```

## 使用方法

所有命令在项目根目录运行。

### 完整检查

```bash
python3 .pi/skills/wiki-lint/lint.py
```

### 只检查某一类

```bash
python3 .pi/skills/wiki-lint/lint.py --check links        # 只检查链接
python3 .pi/skills/wiki-lint/lint.py --check frontmatter  # 只检查 frontmatter
python3 .pi/skills/wiki-lint/lint.py --check naming       # 只检查命名
python3 .pi/skills/wiki-lint/lint.py --check quality      # 只检查内容质量
```

### 只检查某个子目录

```bash
python3 .pi/skills/wiki-lint/lint.py companies             # 只检查 wiki/companies/
python3 .pi/skills/wiki-lint/lint.py research/cases        # 只检查 wiki/research/cases/
```

### 自动修复

```bash
python3 .pi/skills/wiki-lint/lint.py --fix                 # 修复可自动修复的问题
python3 .pi/skills/wiki-lint/lint.py --fix --add-fm        # 同时补全缺失的 frontmatter
```

### 详细报告

```bash
python3 .pi/skills/wiki-lint/lint.py -v
```

## 检查规则

规则定义集中在 `scripts/config.py`，修改规则只需改数据，不影响检查逻辑。

### 链接规则

- 内部链接必须使用相对路径
- 死链检测：解析每个 `[text](path.md)` 并验证文件存在
- 过时格式检测：`[[wikilink]]` 标记为 WARNING
- **模糊匹配建议**：死链会自动尝试 3 种策略给出修复建议（见下方）

### 模糊匹配策略（`scripts/links.py`）

当链接目标不存在时，依次尝试：

| 优先级 | 策略 | 示例 |
|--------|------|------|
| 1 | 规范化空格连字符：「` - `」→「`-`」 | `可口可乐 - 消费巨头.md` → `可口可乐-消费巨头.md` |
| 2 | 去掉所有空格 | `吉列 - 宝洁.md` → `吉列-宝洁.md` |
| 3 | 前缀/子串匹配（在同级目录查找） | `吉列.md` → `吉列-宝洁.md` |

### 命名规则

在 `config.NAMING_RULES` 中以正则定义：

| 目录 | 格式 | 示例 |
|------|------|------|
| `letters/` | `YYYY-letter.md` | `1965-letter.md` |
| `partnership/` | `YYYY-标题.md` | `1957-巴菲特致合伙人信.md` |
| `shareholders_meeting/` | `YYYY-股东大会.md` | `2024-股东大会.md` |
| `research/cases/` | `YYYY-名-主题.md` | `1988-可口可乐-消费巨头.md` |
| `concepts/` | `名称.md`（无空格） | `安全边际.md` |
| `companies/` | `名称.md`（无空格） | `可口可乐.md` |
| `people/` | `名称.md`（无空格） | `沃伦·巴菲特.md` |
| `interviews/` | `YYYY-标题.md` | `1998-佛罗里达大学演讲.md` |

### Frontmatter 规则

- 必需字段：`type`（定义在 `config.FRONTMATTER_REQUIRED_FIELDS`）
- type 有效值定义在 `config.FRONTMATTER_VALID_TYPES`

## 自动修复策略（`scripts/fix.py`）

| 策略 | 说明 | 启用方式 |
|------|------|----------|
| `fix_spaces_in_links` | 用模糊匹配结果替换死链中的错误路径 | `--fix` 默认启用 |
| `fix_wikilinks` | `[[text]]` → `[text](相对路径.md)` | `--fix` 默认启用 |
| `fix_missing_frontmatter` | 自动推断 type 并添加 frontmatter | `--fix --add-fm` |

新增修复策略只需：写一个函数 → 加入 `FIX_STRATEGIES` 列表。

## 输出格式

```
🔴 ERROR   — 必须修复（死链、缺失文件）
🟡 WARNING — 建议修复（命名不规范、缺 frontmatter、内容过短）
ℹ️  INFO   — 信息提示
```

## 扩展指南

### 新增检查类型

1. 在 `scripts/` 下新建模块，导出 `check_xxx(content, file_path, wiki_dir) -> List[Issue]`
2. 在 `lint.py` 中 import 并调用
3. 在 `config.py` 中添加相关规则数据（如有）

### 新增模糊匹配策略

在 `scripts/links.py` 的 `FUZZY_STRATEGIES` 列表中追加函数，签名为：

```python
def my_strategy(broken_path: Path, wiki_dir: Path) -> Optional[Path]:
    """尝试匹配，返回存在的文件路径或 None。"""
    ...
```

### 新增自动修复策略

在 `scripts/fix.py` 的 `FIX_STRATEGIES` 列表中追加函数，签名为：

```python
def my_fix(content: str, source_file: Path, wiki_dir: Path) -> Tuple[str, List[FixAction]]:
    """返回 (修复后内容, 操作记录列表)。"""
    ...
```

---

*Last Updated: 2026-04-25*
