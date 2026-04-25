"""链接检查核心：提取、解析、模糊匹配。

设计原则：
- 所有方法都是「纯函数式」的，不依赖全局状态
- 模糊匹配策略可扩展（FUZZY_STRATEGIES 列表）
- 不写死任何具体文件名
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple, Callable

from .report import Issue, Level


# ── 链接提取 ──────────────────────────────────────────────

# Markdown 链接: [text](url)
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# Obsidian wikilink: [[text]]
_WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def extract_md_links(content: str) -> List[Tuple[int, str, str]]:
    """提取所有 Markdown 链接，返回 [(行号, 链接文字, 链接路径)]。"""
    results = []
    for m in _MD_LINK_RE.finditer(content):
        line = content[: m.start()].count("\n") + 1
        results.append((line, m.group(1), m.group(2)))
    return results


def extract_wikilinks(content: str) -> List[Tuple[int, str]]:
    """提取所有 [[wikilink]]，返回 [(行号, 链接文字)]。"""
    results = []
    for m in _WIKI_LINK_RE.finditer(content):
        line = content[: m.start()].count("\n") + 1
        results.append((line, m.group(1)))
    return results


# ── 链接分类 ──────────────────────────────────────────────

def classify_link(link_path: str) -> str:
    """分类链接：external / anchor / internal_md / internal_other"""
    if link_path.startswith(("http://", "https://", "mailto:")):
        return "external"
    if link_path.startswith("#"):
        return "anchor"
    # 去掉 anchor fragment 后判断
    pure = link_path.split("#")[0]
    if pure.endswith(".md"):
        return "internal_md"
    # 图片等资源
    if re.search(r"\.(png|jpg|jpeg|gif|svg|webp|pdf)$", pure, re.IGNORECASE):
        return "internal_asset"
    return "other"


# ── 链接解析 ──────────────────────────────────────────────

def resolve_link(link_path: str, source_file: Path, wiki_dir: Path) -> Optional[Path]:
    """将链接解析为 wiki 目录下的绝对路径。
    
    返回 None 表示是外部链接/锚点。
    返回 Path 但文件可能不存在。
    """
    lt = classify_link(link_path)
    if lt in ("external", "anchor"):
        return None

    pure = link_path.split("#")[0]
    if not pure:
        return None

    src_dir = source_file.parent
    resolved = (src_dir / pure).resolve()

    # 尝试确认在 wiki 目录内
    try:
        resolved.relative_to(wiki_dir)
    except ValueError:
        pass  # 超出 wiki 目录的链接（如 ./assets/xxx.png 在项目根），也检查

    return resolved


# ── 模糊匹配 ──────────────────────────────────────────────
# 每个策略是一个函数：(broken_path, wiki_dir) → Optional[Path]
# 按优先级排列，首次命中即返回

def _normalize_spaces_dashes(broken_path: Path, wiki_dir: Path) -> Optional[Path]:
    """策略 1：去掉「空格-空格」→ 纯连字符。
    
    例: 「可口可乐 - 消费巨头.md」→「可口可乐-消费巨头.md」
    """
    parts = broken_path.parts
    filename = broken_path.name
    # 替换文件名中的「 - 」为「-」
    normalized = re.sub(r"\s*-\s*", "-", filename)
    if normalized == filename:
        return None
    candidate = broken_path.parent / normalized
    return candidate if candidate.exists() else None


def _strip_spaces(broken_path: Path, wiki_dir: Path) -> Optional[Path]:
    """策略 2：去掉文件名中的空格。
    
    例: 「吉列 - 宝洁.md」→「吉列-宝洁.md」
    """
    filename = broken_path.name
    normalized = filename.replace(" ", "")
    if normalized == filename:
        return None
    candidate = broken_path.parent / normalized
    return candidate if candidate.exists() else None


def _find_similar_in_dir(broken_path: Path, wiki_dir: Path) -> Optional[Path]:
    """策略 3：在同名目录下按前缀/关键片段模糊查找。
    
    例: 「吉列.md」在 companies/ 下找不到，但存在「吉列-宝洁.md」
    """
    parent = broken_path.parent
    stem = broken_path.stem  # 不含 .md

    if not parent.is_dir():
        return None

    # 精确前缀匹配：文件名以 stem 开头
    for f in parent.glob("*.md"):
        if f.stem.startswith(stem) and f.stem != stem:
            return f

    # 子串包含匹配
    for f in parent.glob("*.md"):
        if stem in f.stem and f.stem != stem:
            return f

    return None


FUZZY_STRATEGIES: List[Callable[[Path, Path], Optional[Path]]] = [
    _normalize_spaces_dashes,
    _strip_spaces,
    _find_similar_in_dir,
]


def fuzzy_match(broken_path: Path, wiki_dir: Path) -> Optional[Path]:
    """依次尝试所有模糊匹配策略，返回第一个命中结果。"""
    for strategy in FUZZY_STRATEGIES:
        result = strategy(broken_path, wiki_dir)
        if result is not None:
            return result
    return None


# ── 链接检查主函数 ────────────────────────────────────────

def check_links(content: str, source_file: Path, wiki_dir: Path) -> List[Issue]:
    """检查单个文件的链接，返回 Issue 列表。"""
    issues = []
    rel_path = str(source_file.relative_to(wiki_dir))

    # 1. 检查 Markdown 链接
    for line_num, text, raw_link in extract_md_links(content):
        lt = classify_link(raw_link)
        if lt != "internal_md":
            continue

        resolved = resolve_link(raw_link, source_file, wiki_dir)
        if resolved is None:
            continue

        if resolved.exists():
            continue

        # 死链！尝试模糊匹配给出建议
        suggestion = ""
        matched = fuzzy_match(resolved, wiki_dir)
        if matched:
            # 计算新的相对路径
            import os
            src_dir = str(source_file.resolve().parent)
            matched_abs = str(Path(matched).resolve())
            new_rel = os.path.relpath(matched_abs, src_dir)
            suggestion = f"文件名可能为「{matched.name}」，修复链接为 {new_rel}"

        issues.append(Issue(
            level=Level.ERROR,
            file=rel_path,
            line=line_num,
            message=f"死链 → [{text}]({raw_link})",
            suggestion=suggestion,
        ))

    # 2. 检查 [[wikilink]] 格式
    for line_num, link_text in extract_wikilinks(content):
        issues.append(Issue(
            level=Level.WARNING,
            file=rel_path,
            line=line_num,
            message=f"过时链接格式 [[{link_text}]]",
            suggestion="应改为标准 Markdown 链接 [text](path)",
        ))

    return issues
