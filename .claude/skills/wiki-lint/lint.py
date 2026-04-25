#!/usr/bin/env python3
"""
Buffett Wiki Lint — 入口脚本。

编排 scripts/ 下的模块完成检查或修复。
用法：
    python lint.py                    # 全量检查
    python lint.py --dir companies    # 只检查某目录
    python lint.py --fix              # 自动修复
    python lint.py --fix --add-fm     # 自动修复 + 补 frontmatter
    python lint.py --check links      # 只检查链接
    python lint.py -v                 # 详细报告
"""

import argparse
import fnmatch
import sys
from pathlib import Path

# 将 scripts/ 加入 import path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from scripts.config import resolve_project_root, WIKI_DIR_NAME, IGNORE_PATTERNS
from scripts.report import LintResult, Issue, Level, C
from scripts.links import check_links
from scripts.naming import check_naming
from scripts.frontmatter import check_frontmatter
from scripts.quality import check_quality
from scripts.fix import apply_fixes, fix_missing_frontmatter


def should_ignore(rel_path: str) -> bool:
    """检查文件是否匹配忽略模式。"""
    for pattern in IGNORE_PATTERNS:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def collect_files(wiki_dir: Path, subdir: str = ".") -> list:
    """收集需要检查的 .md 文件。"""
    target = wiki_dir / subdir if subdir != "." else wiki_dir
    if not target.exists():
        print(f"{C.RED}错误：目录不存在：{target}{C.RESET}")
        sys.exit(1)

    files = sorted(target.rglob("*.md"))
    return [f for f in files if not should_ignore(str(f.relative_to(wiki_dir)))]


def lint(result: LintResult, wiki_dir: Path, subdir: str, checks: set):
    """执行检查。"""
    files = collect_files(wiki_dir, subdir)
    result.files_scanned = len(files)

    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            result.issues.append(Issue(
                level=Level.ERROR,
                file=str(f.relative_to(wiki_dir)),
                line=0,
                message=f"无法读取：{e}",
            ))
            continue

        result.files_checked += 1

        if "links" in checks:
            result.issues.extend(check_links(content, f, wiki_dir))
        if "naming" in checks:
            result.issues.extend(check_naming(f, wiki_dir))
        if "frontmatter" in checks:
            result.issues.extend(check_frontmatter(content, f, wiki_dir))
        if "quality" in checks:
            result.issues.extend(check_quality(content, f, wiki_dir))


def fix(result: LintResult, wiki_dir: Path, subdir: str, add_frontmatter: bool = False):
    """执行自动修复。"""
    from scripts.fix import FIX_STRATEGIES

    files = collect_files(wiki_dir, subdir)
    total_actions = 0

    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue

        strategies = list(FIX_STRATEGIES)
        if add_frontmatter:
            strategies.append(fix_missing_frontmatter)

        new_content, actions = apply_fixes(content, f, wiki_dir, strategies)

        if actions:
            f.write_text(new_content, encoding="utf-8")
            total_actions += len(actions)
            rel = str(f.relative_to(wiki_dir))
            for a in actions:
                print(f"  {C.GREEN}✓{C.RESET} {rel}:{a.line} — {a.description}")

    print(f"\n{C.GREEN}共修复 {total_actions} 处问题{C.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Buffett Wiki Lint Tool")
    parser.add_argument("subdir", nargs="?", default=".",
                        help="只检查 wiki/ 下的某个子目录")
    parser.add_argument("--root", default=None,
                        help="显式指定项目根目录")
    parser.add_argument("--fix", action="store_true",
                        help="自动修复可修复的问题")
    parser.add_argument("--add-fm", action="store_true",
                        help="配合 --fix，同时补全缺失的 frontmatter")
    parser.add_argument("--check", choices=["links", "frontmatter", "naming", "quality", "all"],
                        default="all", help="只检查特定类别")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="详细报告")
    args = parser.parse_args()

    # 确定项目根目录
    root = resolve_project_root(args.root)
    wiki_dir = root / WIKI_DIR_NAME

    if not wiki_dir.is_dir():
        print(f"{C.RED}错误：未找到 wiki 目录：{wiki_dir}{C.RESET}")
        sys.exit(1)

    print(f"{C.BOLD}🔍 开始检查 Buffett Wiki...{C.RESET}\n")

    result = LintResult(root=root)

    if args.check == "all":
        checks = {"links", "naming", "frontmatter", "quality"}
    else:
        checks = {args.check}

    if args.fix:
        fix(result, wiki_dir, args.subdir, add_frontmatter=args.add_fm)
    else:
        lint(result, wiki_dir, args.subdir, checks)
        result.print_report(verbose=args.verbose)

    # 返回码
    if result.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
