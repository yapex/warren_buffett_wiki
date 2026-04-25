"""Frontmatter 解析与校验。

规则来自 config，不写死具体字段值。
"""

from pathlib import Path
from typing import List, Optional, Tuple

from .report import Issue, Level
from .config import FRONTMATTER_REQUIRED_FIELDS, FRONTMATTER_VALID_TYPES


def parse_frontmatter(content: str) -> Optional[dict]:
    """解析 YAML frontmatter，返回 dict 或 None。
    
    不依赖 pyyaml，用简单的文本解析，避免外部依赖。
    """
    if not content.startswith("---"):
        return None

    # 找结束的 ---
    end = content.find("\n---", 3)
    if end == -1:
        return None

    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip("\"'")
    return result if result else None


def strip_frontmatter(content: str) -> str:
    """去除 frontmatter，返回纯内容。"""
    if not content.startswith("---"):
        return content
    end = content.find("\n---", 3)
    if end == -1:
        return content
    return content[end + 4:].lstrip("\n")


def check_frontmatter(content: str, file_path: Path, wiki_dir: Path) -> List[Issue]:
    """检查 frontmatter 完整性，返回 Issue 列表。"""
    issues = []
    rel_path = str(file_path.relative_to(wiki_dir))
    filename = file_path.name

    # index.md 不检查
    if filename == "index.md":
        return issues

    fm = parse_frontmatter(content)

    if fm is None:
        issues.append(Issue(
            level=Level.WARNING,
            file=rel_path,
            line=1,
            message="缺少 frontmatter",
            suggestion=f"在文件开头添加 ---\\ntype: xxx\\n---",
        ))
        return issues

    # 检查必需字段
    for field in FRONTMATTER_REQUIRED_FIELDS:
        if field not in fm:
            issues.append(Issue(
                level=Level.WARNING,
                file=rel_path,
                line=1,
                message=f"缺少必需字段：{field}",
                suggestion=f"添加 {field}: xxx",
            ))

    # 检查 type 有效值
    if "type" in fm and fm["type"] not in FRONTMATTER_VALID_TYPES:
        issues.append(Issue(
            level=Level.WARNING,
            file=rel_path,
            line=1,
            message=f"无效的 type 值：{fm['type']}",
            suggestion=f"有效值：{', '.join(FRONTMATTER_VALID_TYPES)}",
        ))

    return issues
