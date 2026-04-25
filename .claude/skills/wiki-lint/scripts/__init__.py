"""wiki-lint 核心模块
"""

from .config import resolve_project_root, WIKI_DIR_NAME
from .report import Issue, Level, LintResult, C
from .links import check_links
from .naming import check_naming
from .frontmatter import check_frontmatter
from .quality import check_quality
from .fix import apply_fixes, FIX_STRATEGIES

__all__ = [
    "resolve_project_root", "WIKI_DIR_NAME",
    "Issue", "Level", "LintResult", "C",
    "check_links", "check_naming", "check_frontmatter", "check_quality",
    "apply_fixes", "FIX_STRATEGIES",
]
