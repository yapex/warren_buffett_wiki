"""文件命名规范检查。

规则来自 config.NAMING_RULES，不写死具体文件名。
"""

import re
from pathlib import Path
from typing import List

from .report import Issue, Level
from .config import NAMING_RULES

# 文件名不应包含的特殊字符（跨目录通用）
INVALID_CHARS_RE = re.compile(r"[?*:|<>]")


def check_naming(file_path: Path, wiki_dir: Path) -> List[Issue]:
    """检查单个文件的命名是否符合规范，返回 Issue 列表。"""
    issues = []
    rel_path = str(file_path.relative_to(wiki_dir))
    filename = file_path.name

    # index.md 豁免
    if filename == "index.md":
        return issues

    # 通用：禁止特殊字符
    bad_chars = INVALID_CHARS_RE.findall(filename)
    if bad_chars:
        issues.append(Issue(
            level=Level.WARNING,
            file=rel_path,
            line=0,
            message=f"文件名包含特殊字符：{', '.join(bad_chars)}",
            suggestion="移除特殊字符 ? * : | < >",
        ))

    # 按目录匹配规则
    for rule in NAMING_RULES:
        rule_dir = rule["dir"]
        # 检查文件是否在该目录下
        try:
            file_path.relative_to(wiki_dir / rule_dir)
        except ValueError:
            continue

        pattern = rule["pattern"]
        if not pattern.match(filename):
            issues.append(Issue(
                level=Level.WARNING,
                file=rel_path,
                line=0,
                message=f"命名不符合规范：{filename}",
                suggestion=f"应为 {rule['description']}，例：{rule['example']}",
            ))
        break  # 只匹配第一条命中规则

    return issues
