"""wiki-lint 配置：路径约定、命名规则、frontmatter 规范。

所有「规则」都以数据结构定义在这里，不散落在检查逻辑中。
新增目录/规则时只需修改本文件。
"""

from pathlib import Path
from typing import Dict, List, Optional, Pattern
import re

# ── 项目路径 ──────────────────────────────────────────────
# lint.py 入口通过 resolve_project_root() 计算，这里只做默认值
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[4]  # .pi/skills/wiki-lint/scripts → project root
WIKI_DIR_NAME = "wiki"


def resolve_project_root(explicit: Optional[str] = None) -> Path:
    """按优先级确定项目根目录：
    1. 显式传入的路径
    2. 向上查找包含 wiki/ 目录的祖先
    3. DEFAULT_PROJECT_ROOT
    """
    if explicit:
        p = Path(explicit).resolve()
        if (p / WIKI_DIR_NAME).is_dir():
            return p
        raise FileNotFoundError(f"指定路径下未找到 {WIKI_DIR_NAME}/ 目录：{p}")

    # 向上查找
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / WIKI_DIR_NAME).is_dir():
            return current
        current = current.parent

    return DEFAULT_PROJECT_ROOT


# ── 命名规则 ──────────────────────────────────────────────
# key = 相对于 wiki/ 的子目录前缀
# pattern = 该目录下 .md 文件应匹配的正则（index.md 例外）
# example = 规范示例，用于报错提示

NAMING_RULES: List[Dict] = [
    {
        "dir": "letters",
        "pattern": re.compile(r"^\d{4}-letter\.md$"),
        "example": "1965-letter.md",
        "description": "信件文件: YYYY-letter.md",
    },
    {
        "dir": "partnership",
        "pattern": re.compile(r"^\d{4}.*\.md$"),
        "example": "1957-巴菲特致合伙人信.md",
        "description": "合伙人信: YYYY-标题.md",
    },
    {
        "dir": "shareholders_meeting",
        "pattern": re.compile(r"^\d{4}-股东大会(_summary)?\.md$"),
        "example": "2024-股东大会.md / 2024-股东大会_summary.md",
        "description": "股东大会: YYYY-股东大会.md",
    },
    {
        "dir": "research/cases",
        "pattern": re.compile(r"^\d{4}-.+-.+\.md$"),
        "example": "1988-可口可乐-消费巨头.md",
        "description": "案例: YYYY-名称-主题.md（各段用 - 连接，无空格）",
    },
    {
        "dir": "concepts",
        "pattern": re.compile(r"^[^\s?*:|<>]+\.md$"),
        "example": "安全边际.md",
        "description": "概念: 名称.md（不含空格和特殊字符）",
    },
    {
        "dir": "companies",
        "pattern": re.compile(r"^[^\s?*:|<>]+\.md$"),
        "example": "可口可乐.md",
        "description": "公司: 名称.md（不含空格和特殊字符）",
    },
    {
        "dir": "people",
        "pattern": re.compile(r"^[^\s?*:|<>]+\.md$"),
        "example": "沃伦·巴菲特.md",
        "description": "人物: 名称.md（不含空格和特殊字符）",
    },
    {
        "dir": "interviews",
        "pattern": re.compile(r"^\d{4}-.+\.md$"),
        "example": "1998-佛罗里达大学演讲.md",
        "description": "访谈: YYYY-标题.md",
    },
]

# ── Frontmatter 规范 ─────────────────────────────────────

FRONTMATTER_REQUIRED_FIELDS = ["type"]
FRONTMATTER_VALID_TYPES = [
    "letter", "company", "concept", "person", "case_study",
    "interview", "research", "special", "index", "section",
    "shareholders_meeting", "partnership",
]

# ── 忽略规则 ─────────────────────────────────────────────
# glob 模式，相对于 wiki/
IGNORE_PATTERNS: List[str] = [
    "test/**",
    "temp/**",
    "*.tmp.md",
]
