#!/usr/bin/env python3
"""
Buffett Wiki Lint Tool

检查 Wiki 知识库的质量问题：
- 死链检测
- 命名规范
- Frontmatter 验证
- 链接格式检查
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml

# 颜色定义
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# 错误级别
class Level:
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'

# 问题记录
class Issue:
    def __init__(self, level: str, file: str, line: int, message: str, suggestion: str = ''):
        self.level = level
        self.file = file
        self.line = line
        self.message = message
        self.suggestion = suggestion
    
    def __str__(self):
        if self.level == Level.ERROR:
            color = Colors.RED
            icon = '🔴'
        elif self.level == Level.WARNING:
            color = Colors.YELLOW
            icon = '🟡'
        else:
            color = Colors.CYAN
            icon = 'ℹ️'
        
        line_info = f'Line {self.line}: ' if self.line > 0 else ''
        suggestion = f'\n  {Colors.BLUE}建议：{self.suggestion}{Colors.RESET}' if self.suggestion else ''
        
        return f'{color}[{self.level}] {self.file}{Colors.RESET}\n  {line_info}{self.message}{suggestion}'

# Wiki Lint 检查器
class WikiLint:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.wiki_dir = self.root_dir / 'wiki'
        self.issues: List[Issue] = []
        self.files_checked = 0
        self.files_passed = 0
        
        # 建立文件索引
        self.existing_files: Dict[str, Path] = {}
        self._scan_existing_files()
    
    def _scan_existing_files(self):
        """扫描所有存在的 Markdown 文件"""
        if not self.wiki_dir.exists():
            return
        
        for md_file in self.wiki_dir.rglob('*.md'):
            rel_path = md_file.relative_to(self.wiki_dir)
            self.existing_files[str(rel_path)] = md_file
    
    def _get_relative_path(self, file_path: Path) -> str:
        """获取相对于 wiki 目录的路径"""
        try:
            return str(file_path.relative_to(self.wiki_dir))
        except ValueError:
            return str(file_path)
    
    def _resolve_link(self, link_path: str, current_file: Path) -> Optional[Path]:
        """解析链接路径，返回实际文件路径"""
        if link_path.startswith('http://') or link_path.startswith('https://'):
            return None  # 外部链接，不检查
        
        if link_path.startswith('/'):
            link_path = link_path[1:]
        
        # 解析相对路径
        current_dir = current_file.parent
        resolved = (current_dir / link_path).resolve()
        
        try:
            resolved = resolved.relative_to(self.wiki_dir)
            return self.wiki_dir / resolved
        except ValueError:
            return None
    
    def _check_links(self, content: str, file_path: Path):
        """检查 Markdown 链接"""
        # 匹配 [text](path) 格式
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        for match in re.finditer(link_pattern, content):
            link_text = match.group(1)
            link_path = match.group(2)
            line_num = content[:match.start()].count('\n') + 1
            
            # 跳过外部链接
            if link_path.startswith('http://') or link_path.startswith('https://'):
                continue
            
            # 跳过锚点链接
            if link_path.startswith('#'):
                continue
            
            # 解析链接路径
            target_file = self._resolve_link(link_path, file_path)
            
            if target_file and not target_file.exists():
                self.issues.append(Issue(
                    Level.ERROR,
                    self._get_relative_path(file_path),
                    line_num,
                    f'死链 → {link_text}({link_path})',
                    f'检查文件是否存在或路径是否正确'
                ))
        
        # 检查 [[Wiki Link]] 格式（应该转换为标准 Markdown）
        wiki_link_pattern = r'\[\[([^\]]+)\]\]'
        for match in re.finditer(wiki_link_pattern, content):
            link_text = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            self.issues.append(Issue(
                Level.WARNING,
                self._get_relative_path(file_path),
                line_num,
                f'过时链接格式 [[{link_text}]]',
                f'应改为 [{link_text}](../../concepts/{link_text}.md) 或相应路径'
            ))
    
    def _check_frontmatter(self, content: str, file_path: Path):
        """检查 YAML frontmatter"""
        if not content.startswith('---'):
            self.issues.append(Issue(
                Level.WARNING,
                self._get_relative_path(file_path),
                1,
                '缺少 frontmatter',
                '添加 YAML frontmatter，包含 type 等字段'
            ))
            return
        
        # 解析 frontmatter
        try:
            end_index = content.find('---', 3)
            if end_index == -1:
                return
            
            frontmatter = yaml.safe_load(content[3:end_index])
            
            if not frontmatter:
                return
            
            # 检查 type 字段
            if 'type' not in frontmatter:
                self.issues.append(Issue(
                    Level.WARNING,
                    self._get_relative_path(file_path),
                    1,
                    '缺少 type 字段',
                    '添加 type: letter/company/concept/person/case_study'
                ))
            else:
                valid_types = ['letter', 'company', 'concept', 'person', 'case_study', 'interview', 'research', 'special', 'index']
                if frontmatter['type'] not in valid_types:
                    self.issues.append(Issue(
                        Level.WARNING,
                        self._get_relative_path(file_path),
                        1,
                        f'无效的 type 值：{frontmatter["type"]}',
                        f'使用以下值之一：{", ".join(valid_types)}'
                    ))
        
        except yaml.YAMLError as e:
            self.issues.append(Issue(
                Level.ERROR,
                self._get_relative_path(file_path),
                1,
                f'frontmatter YAML 解析错误：{str(e)}',
                '检查 YAML 格式是否正确'
            ))
    
    def _check_naming(self, file_path: Path):
        """检查文件命名规范"""
        filename = file_path.name
        rel_path = self._get_relative_path(file_path)
        
        # 检查特殊字符
        invalid_chars = ['?', '*', ':', '|', '<', '>']
        for char in invalid_chars:
            if char in filename:
                self.issues.append(Issue(
                    Level.WARNING,
                    rel_path,
                    0,
                    f'文件名包含特殊字符：{char}',
                    '移除特殊字符'
                ))
        
        # 检查信件文件命名
        if 'letters' in rel_path:
            if not re.match(r'^\d{4}-letter\.md$', filename):
                self.issues.append(Issue(
                    Level.WARNING,
                    rel_path,
                    0,
                    f'信件文件命名不规范：{filename}',
                    '应使用 YYYY-letter.md 格式，如 1965-letter.md'
                ))
    
    def _check_empty_file(self, content: str, file_path: Path):
        """检查空文件"""
        if len(content.strip()) < 50:
            self.issues.append(Issue(
                Level.WARNING,
                self._get_relative_path(file_path),
                0,
                '文件内容过短（< 50 字符）',
                '添加内容或删除空文件'
            ))
    
    def check_file(self, file_path: Path):
        """检查单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.issues.append(Issue(
                Level.ERROR,
                self._get_relative_path(file_path),
                0,
                f'无法读取文件：{str(e)}',
                ''
            ))
            return
        
        self.files_checked += 1
        
        # 执行检查
        self._check_links(content, file_path)
        self._check_frontmatter(content, file_path)
        self._check_naming(file_path)
        self._check_empty_file(content, file_path)
    
    def check_directory(self, directory: str):
        """检查目录"""
        dir_path = self.wiki_dir / directory if directory != '.' else self.wiki_dir
        
        if not dir_path.exists():
            print(f'{Colors.RED}错误：目录不存在：{dir_path}{Colors.RESET}')
            return
        
        for md_file in dir_path.rglob('*.md'):
            self.check_file(md_file)
    
    def fix_wiki_links(self, file_path: Path):
        """自动修复 Wiki 链接格式"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return False
        
        original = content
        fixed = False
        
        # 修复 [[概念]] 格式
        def replace_wiki_link(match):
            nonlocal fixed
            fixed = True
            link_text = match.group(1)
            
            # 尝试判断是概念还是人物
            concepts_dir = self.wiki_dir / 'concepts'
            people_dir = self.wiki_dir / 'people'
            companies_dir = self.wiki_dir / 'companies'
            
            if (concepts_dir / f'{link_text}.md').exists():
                return f'[{link_text}](../../concepts/{link_text}.md)'
            elif (people_dir / f'{link_text}.md').exists():
                return f'[{link_text}](../../people/{link_text}.md)'
            elif (companies_dir / f'{link_text}.md').exists():
                return f'[{link_text}](../../companies/{link_text}.md)'
            else:
                return link_text  # 找不到目标，只保留文本
        
        content = re.sub(r'\[\[([^\]]+)\]\]', replace_wiki_link, content)
        
        # 修复信件链接
        letter_mapping = {
            r'(\d{4})-致合伙人信\.md': r'\1-letter.md',
            r'(\d{4})-致股东信\.md': r'\1-letter.md',
        }
        
        for pattern, replacement in letter_mapping.items():
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                fixed = True
        
        if fixed and content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def fix_directory(self, directory: str):
        """自动修复目录中的问题"""
        dir_path = self.wiki_dir / directory if directory != '.' else self.wiki_dir
        
        if not dir_path.exists():
            print(f'{Colors.RED}错误：目录不存在：{dir_path}{Colors.RESET}')
            return
        
        fixed_count = 0
        for md_file in dir_path.rglob('*.md'):
            if self.fix_wiki_links(md_file):
                fixed_count += 1
                print(f'{Colors.GREEN}✓ 修复：{self._get_relative_path(md_file)}{Colors.RESET}')
        
        print(f'\n{Colors.GREEN}共修复 {fixed_count} 个文件{Colors.RESET}')
    
    def check_root_files(self):
        """检查根目录的重要文件（如 index.md）"""
        root_files = ['index.md', 'README.md']
        for filename in root_files:
            file_path = self.root_dir / filename
            if file_path.exists():
                self.check_file(file_path)
                print(f'{Colors.BLUE}✓ 检查根目录文件：{filename}{Colors.RESET}')
    
    def print_report(self):
        """打印检查报告"""
        print(f'\n{Colors.BOLD}🔍 Buffett Wiki Lint 报告{Colors.RESET}\n')
        print(f'{Colors.CYAN}📁 检查范围：{self.wiki_dir}{Colors.RESET}')
        print(f'{Colors.CYAN}📄 文件总数：{self.files_checked}{Colors.RESET}')
        print(f'{Colors.CYAN}📄 根目录文件：index.md, README.md{Colors.RESET}\n')
        
        # 按级别分组问题
        errors = [i for i in self.issues if i.level == Level.ERROR]
        warnings = [i for i in self.issues if i.level == Level.WARNING]
        infos = [i for i in self.issues if i.level == Level.INFO]
        
        # 打印错误
        if errors:
            print(f'{Colors.RED}{Colors.BOLD}🔴 ERRORS ({len(errors)}){Colors.RESET}')
            print(f'{Colors.RED}{"━" * 60}{Colors.RESET}')
            for issue in errors:
                print(f'{issue}\n')
        
        # 打印警告
        if warnings:
            print(f'{Colors.YELLOW}{Colors.BOLD}🟡 WARNINGS ({len(warnings)}){Colors.RESET}')
            print(f'{Colors.YELLOW}{"━" * 60}{Colors.RESET}')
            for issue in warnings:
                print(f'{issue}\n')
        
        # 打印信息
        if infos:
            print(f'{Colors.CYAN}{Colors.BOLD}ℹ️ INFO ({len(infos)}){Colors.RESET}')
            print(f'{Colors.CYAN}{"━" * 60}{Colors.RESET}')
            for issue in infos:
                print(f'{issue}\n')
        
        # 打印摘要
        files_with_issues = len(set(f'{i.file}:{i.line}' for i in self.issues))
        files_passed = self.files_checked - files_with_issues
        
        print(f'{Colors.BOLD}ℹ️ SUMMARY{Colors.RESET}')
        print(f'{Colors.CYAN}{"━" * 60}{Colors.RESET}')
        print(f'{Colors.GREEN}✅ 通过检查：{files_passed} 个文件{Colors.RESET}')
        
        if errors:
            print(f'{Colors.RED}🔴 错误：{len(errors)} 个{Colors.RESET}')
        if warnings:
            print(f'{Colors.YELLOW}🟡 警告：{len(warnings)} 个{Colors.RESET}')
        
        if errors:
            print(f'\n{Colors.RED}❌ 检查失败，请修复错误后再继续{Colors.RESET}')
            sys.exit(1)
        elif warnings:
            print(f'\n{Colors.YELLOW}⚠️ 检查通过，但有警告需要关注{Colors.RESET}')
        else:
            print(f'\n{Colors.GREEN}✅ 检查通过，所有文件都符合规范！{Colors.RESET}')

def main():
    parser = argparse.ArgumentParser(description='Buffett Wiki Lint Tool')
    parser.add_argument('directory', nargs='?', default='.', help='要检查的目录（相对于 wiki/）')
    parser.add_argument('--fix', action='store_true', help='自动修复可修复的问题')
    parser.add_argument('--check', choices=['links', 'frontmatter', 'naming', 'all'], 
                       default='all', help='只检查特定类型的问题')
    parser.add_argument('--verbose', '-v', action='store_true', help='输出详细报告')
    
    args = parser.parse_args()
    
    # 确定项目根目录
    root_dir = Path(__file__).parent.parent.parent.parent
    lint = WikiLint(str(root_dir))
    
    print(f'{Colors.BOLD}🔍 开始检查 Buffett Wiki...{Colors.RESET}\n')
    
    if args.fix:
        lint.fix_directory(args.directory)
    else:
        lint.check_directory(args.directory)
        lint.check_root_files()  # 检查根目录文件
        lint.print_report()

if __name__ == '__main__':
    main()
