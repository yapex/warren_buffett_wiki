"""自动修复策略。

每个修复函数都是通用的，不写死具体内容。
新增修复策略只需加一个函数 + 注册到 FIX_STRATEGIES。
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass

from .links import (
    extract_md_links,
    resolve_link,
    fuzzy_match,
    classify_link,
    extract_wikilinks,
)


@dataclass
class FixAction:
    """单次修复操作。"""
    file: Path
    line: int
    original: str
    replacement: str
    description: str


def fix_spaces_in_links(content: str, source_file: Path, wiki_dir: Path) -> Tuple[str, List[FixAction]]:
    """修复策略 1：链接路径中的空格问题（模糊匹配修正）。
    
    对每个内部 .md 链接：
    1. 解析路径
    2. 如果文件不存在，尝试模糊匹配
    3. 如果匹配成功，替换链接中的路径
    """
    actions = []
    lines = content.split("\n")

    for line_idx, line in enumerate(lines):
        new_line = line
        # 找到所有 [text](path) 中 .md 结尾的链接
        for m in re.finditer(r"\[([^\]]*)\]\(([^)]+\.md[^)]*)\)", line):
            full_match = m.group(0)
            text = m.group(1)
            raw_link = m.group(2)

            resolved = resolve_link(raw_link, source_file, wiki_dir)
            if resolved is None or resolved.exists():
                continue

            matched = fuzzy_match(resolved, wiki_dir)
            if matched is None:
                continue

            # 计算新的相对路径（使用 os.path.relpath 处理 sibling 路径）
            import os
            src_dir = str(source_file.resolve().parent)
            matched_abs = str(Path(matched).resolve())
            new_rel = os.path.relpath(matched_abs, src_dir)
            if not new_rel:
                continue

            new_link_str = f"[{text}]({new_rel})"
            new_line = new_line.replace(full_match, new_link_str, 1)

            actions.append(FixAction(
                file=source_file,
                line=line_idx + 1,
                original=full_match,
                replacement=new_link_str,
                description=f"修复链接：{raw_link} → {new_rel}",
            ))

        lines[line_idx] = new_line

    return "\n".join(lines), actions


def fix_wikilinks(content: str, source_file: Path, wiki_dir: Path) -> Tuple[str, List[FixAction]]:
    """修复策略 2：将 [[wikilink]] 转为标准 Markdown 链接。
    
    自动推断目标目录：
    - wiki/concepts/ 下存在同名文件 → concepts
    - wiki/people/ 下存在 → people
    - wiki/companies/ 下存在 → companies
    - 都不存在 → 只保留文本
    """
    actions = []

    def _replace(m: re.Match) -> str:
        link_text = m.group(1)
        stem = link_text.split("|")[0].strip()  # 支持 [[text|alias]] 格式

        # 在各子目录中查找
        search_dirs = ["concepts", "people", "companies", "research"]
        for subdir in search_dirs:
            candidate = wiki_dir / subdir / f"{stem}.md"
            if candidate.exists():
                import os
                src_dir = str(source_file.resolve().parent)
                cand_abs = str(candidate.resolve())
                rel = os.path.relpath(cand_abs, src_dir)
                actions.append(FixAction(
                    file=source_file,
                    line=0,
                    original=m.group(0),
                    replacement=f"[{link_text}]({rel})",
                    description=f"转换 [[{link_text}]] → [{link_text}]({rel})",
                ))
                return f"[{link_text}]({rel})"

        # 找不到，保留文本
        actions.append(FixAction(
            file=source_file,
            line=0,
            original=m.group(0),
            replacement=link_text,
            description=f"无法匹配 [[{link_text}]]，转为纯文本",
        ))
        return link_text

    new_content = re.sub(r"\[\[([^\]]+)\]\]", _replace, content)
    return new_content, actions


def fix_missing_frontmatter(content: str, source_file: Path, wiki_dir: Path) -> Tuple[str, List[FixAction]]:
    """修复策略 3：为缺少 frontmatter 的文件添加最简 frontmatter。
    
    type 值根据文件所在目录自动推断。
    """
    from .frontmatter import parse_frontmatter
    from .config import NAMING_RULES

    if parse_frontmatter(content) is not None:
        return content, []

    # 根据目录推断 type
    rel = source_file.relative_to(wiki_dir)
    parts = rel.parts

    type_inference = {
        "letters": "letter",
        "partnership": "partnership",
        "shareholders_meeting": "shareholders_meeting",
        "concepts": "concept",
        "companies": "company",
        "people": "person",
        "interviews": "interview",
        "research": "research",
        "special": "special",
    }

    inferred_type = "unknown"
    if len(parts) >= 2:
        inferred_type = type_inference.get(parts[0], "unknown")

    # 如果是 research/cases 下的文件
    if len(parts) >= 3 and parts[0] == "research" and parts[1] == "cases":
        inferred_type = "case_study"

    frontmatter = f"---\ntype: {inferred_type}\n---\n"
    new_content = frontmatter + content
    actions = [FixAction(
        file=source_file,
        line=0,
        original="（无 frontmatter）",
        replacement=frontmatter.strip(),
        description=f"添加 frontmatter: type={inferred_type}",
    )]
    return new_content, actions


# ── 修复注册表 ──────────────────────────────────────────────
# 按顺序执行，每个策略对 content 做增量修改

FIX_STRATEGIES: List[Callable] = [
    fix_spaces_in_links,
    fix_wikilinks,
    # fix_missing_frontmatter,  # 默认不自动加 frontmatter，需显式启用
]


def apply_fixes(content: str, source_file: Path, wiki_dir: Path,
                strategies: Optional[List[Callable]] = None) -> Tuple[str, List[FixAction]]:
    """依次应用修复策略，返回 (修复后内容, 所有操作记录)。"""
    if strategies is None:
        strategies = FIX_STRATEGIES

    all_actions = []
    for strategy in strategies:
        content, actions = strategy(content, source_file, wiki_dir)
        all_actions.extend(actions)

    return content, all_actions
