"""Issue 数据类 + 报告格式化。

所有检查器产出 Issue 列表，由 report 统一输出。
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


# ── 颜色 ──────────────────────────────────────────────────
class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


# ── 错误级别 ──────────────────────────────────────────────
class Level:
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Issue:
    level: str
    file: str          # 相对于 wiki/ 的路径
    line: int          # 0 表示不针对特定行
    message: str
    suggestion: str = ""

    @property
    def icon(self) -> str:
        return {"ERROR": "🔴", "WARNING": "🟡", "INFO": "ℹ️"}.get(self.level, "·")

    @property
    def color(self) -> str:
        return {Level.ERROR: C.RED, Level.WARNING: C.YELLOW, Level.INFO: C.CYAN}.get(
            self.level, ""
        )


@dataclass
class LintResult:
    """一次 lint 运行的完整结果。"""
    root: Path
    issues: List[Issue] = field(default_factory=list)
    files_checked: int = 0
    files_scanned: int = 0   # 总扫描文件数（含跳过的）

    # ── 统计 ──────────────────────────────────────────────
    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.level == Level.ERROR]

    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.level == Level.WARNING]

    @property
    def error_files(self) -> int:
        return len({i.file for i in self.errors})

    @property
    def warning_files(self) -> int:
        return len({i.file for i in self.warnings})

    @property
    def passed_files(self) -> int:
        issue_files = {i.file for i in self.issues}
        return self.files_checked - len(issue_files)

    # ── 输出 ──────────────────────────────────────────────
    def print_report(self, verbose: bool = False):
        print(f"\n{C.BOLD}🔍 Buffett Wiki Lint 报告{C.RESET}\n")
        print(f"📁 检查范围：{self.root / 'wiki'}")
        print(f"📄 文件总数：{self.files_scanned}")
        print(f"📄 实际检查：{self.files_checked}\n")

        # 按级别输出
        self._print_group(self.errors, "ERRORS", C.RED)
        self._print_group(self.warnings, "WARNINGS", C.YELLOW)

        # 按 file 分组汇总
        if self.errors and verbose:
            self._print_root_cause_analysis()

        # 摘要
        bar = "━" * 60
        print(f"{C.BOLD}{bar}{C.RESET}")
        print(f"{C.BOLD}📊 SUMMARY{C.RESET}")
        print(f"{bar}")
        print(f"  ✅ 通过：{C.GREEN}{self.passed_files}{C.RESET} 个文件")

        if self.errors:
            print(f"  🔴 错误：{C.RED}{len(self.errors)}{C.RESET} 条 ({self.error_files} 个文件)")
        if self.warnings:
            print(f"  🟡 警告：{C.YELLOW}{len(self.warnings)}{C.RESET} 条 ({self.warning_files} 个文件)")

        print()
        if self.errors:
            print(f"{C.RED}❌ 检查未通过，请修复 {len(self.errors)} 个错误{C.RESET}")
        elif self.warnings:
            print(f"{C.YELLOW}⚠️ 检查通过，但有 {len(self.warnings)} 个警告{C.RESET}")
        else:
            print(f"{C.GREEN}✅ 全部通过！{C.RESET}")
        print()

    def _print_group(self, issues: List[Issue], title: str, color: str):
        if not issues:
            return
        bar = "━" * 60
        print(f"{color}{C.BOLD}{issues[0].icon} {title} ({len(issues)}){C.RESET}")
        print(f"{color}{bar}{C.RESET}")
        for i in issues:
            line = f"Line {i.line}: " if i.line else ""
            sugg = f"\n   {C.BLUE}建议：{i.suggestion}{C.RESET}" if i.suggestion else ""
            print(f"  {i.icon} {color}{i.file}{C.RESET}")
            print(f"   {line}{i.message}{sugg}")
        print()

    def _print_root_cause_analysis(self):
        """按文件分组统计错误，便于定位根因。"""
        from collections import Counter

        bar = "━" * 60
        print(f"{C.BOLD}📌 错误按文件分布{C.RESET}")
        print(f"{bar}")

        file_counts = Counter(i.file for i in self.errors)
        for f, cnt in file_counts.most_common():
            print(f"  {C.RED}{cnt:3d}{C.RESET} 条  {f}")
        print()
