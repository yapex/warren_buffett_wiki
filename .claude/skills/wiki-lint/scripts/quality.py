"""内容质量检查：空文件、过短页面。

阈值可配置，不写死。
"""

from pathlib import Path
from typing import List

from .report import Issue, Level
from .frontmatter import strip_frontmatter

# 默认阈值
MIN_CONTENT_LINES = 3   # 去掉 frontmatter + 空行后少于此行数视为过短
MIN_CONTENT_CHARS = 50  # 内容字符数少于此值视为空文件


def check_quality(content: str, file_path: Path, wiki_dir: Path,
                  min_lines: int = MIN_CONTENT_LINES,
                  min_chars: int = MIN_CONTENT_CHARS) -> List[Issue]:
    """检查内容质量，返回 Issue 列表。"""
    issues = []
    rel_path = str(file_path.relative_to(wiki_dir))
    filename = file_path.name

    if filename == "index.md":
        return issues

    body = strip_frontmatter(content)

    # 空文件
    if len(body.strip()) < min_chars:
        issues.append(Issue(
            level=Level.WARNING,
            file=rel_path,
            line=0,
            message=f"文件内容过少（{len(body.strip())} 字符 < {min_chars}）",
            suggestion="添加内容或删除空文件",
        ))
        return issues  # 空文件不再报过短

    # 过短页面（非空行数）
    non_empty_lines = [l for l in body.split("\n") if l.strip()]
    if len(non_empty_lines) < min_lines:
        issues.append(Issue(
            level=Level.WARNING,
            file=rel_path,
            line=0,
            message=f"内容过短（{len(non_empty_lines)} 行 < {min_lines} 行）",
            suggestion="补充内容",
        ))

    return issues
