#!/usr/bin/env python3
"""
Meilisearch 索引增量更新

使用场景：
1. 新增/修改单个文档后，手动运行更新
2. Git hook 自动触发（post-commit）
3. 定时任务（如每天凌晨同步变更）

用法：
    # 更新单个文件
    uv run python scripts/update_index.py --file wiki/concepts/新概念.md
    
    # 更新多个文件
    uv run python scripts/update_index.py --files wiki/concepts/a.md wiki/concepts/b.md
    
    # 更新最近修改的文件（过去 1 小时）
    uv run python scripts/update_index.py --recent 60
    
    # 删除文档
    uv run python scripts/update_index.py --delete wiki/concepts/旧概念.md
    
    # 查看待更新的变更（dry-run）
    uv run python scripts/update_index.py --recent 60 --dry-run
"""
import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import meilisearch

# 配置
MEILI_URL = "http://127.0.0.1:7700"
MEILI_KEY = "meilisearch-buffett-wiki-key"
INDEX_UID = "buffett-wiki"
WIKI_DIR = Path(__file__).parent.parent / "wiki"


def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    fm = {}
    if not content.startswith("---"):
        return fm
    parts = content.split("---", 2)
    if len(parts) < 3:
        return fm
    yaml_text = parts[1].strip()
    for line in yaml_text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",") if v.strip()]
            fm[key] = value
        elif line.startswith("- ") and fm:
            last_key = list(fm.keys())[-1]
            val = line[2:].strip().strip('"').strip("'")
            if isinstance(fm[last_key], list):
                fm[last_key].append(val)
            else:
                fm[last_key] = [fm[last_key], val]
    return fm


def extract_title(content: str) -> str:
    """提取第一个 H1 标题"""
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_year(content: str, filepath: Path) -> str:
    """提取年份"""
    fm = parse_frontmatter(content)
    year = fm.get("year", "") or fm.get("first_appeared", "")
    if year:
        match = re.search(r'(\d{4})', str(year))
        return match.group(1) if match else str(year)
    match = re.search(r'(\d{4})', filepath.name)
    return match.group(1) if match else ""


def get_doc_type(filepath: Path) -> str:
    """确定文档类型"""
    rel = filepath.relative_to(WIKI_DIR)
    parts = rel.parts
    if len(parts) >= 2:
        top_dir = parts[0]
        if top_dir == "research" and len(parts) >= 3:
            return parts[1]
        return top_dir
    return "unknown"


def generate_doc_id(file_path: str) -> str:
    """生成合法的文档 ID（基于路径的 MD5）"""
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()[:16]


def build_document(file_path: Path) -> dict:
    """构建单个文档的索引数据"""
    content = file_path.read_text(encoding='utf-8')
    rel_path = str(file_path.relative_to(WIKI_DIR))
    doc_id = generate_doc_id(rel_path)
    
    fm = parse_frontmatter(content)
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    
    year = extract_year(content, file_path)
    year_sort = int(year) if year and year.isdigit() else None
    
    return {
        "id": doc_id,
        "title": extract_title(content),
        "content": content,
        "year": year,
        "year_sort": year_sort,
        "doc_type": get_doc_type(file_path),
        "tags": tags,
        "path": rel_path,
        "created_at": int(file_path.stat().st_mtime),
    }


def update_documents(file_paths: list[Path], dry_run: bool = False) -> dict:
    """增量更新文档"""
    client = meilisearch.Client(MEILI_URL, MEILI_KEY)
    index = client.get_index(INDEX_UID)
    
    documents = []
    for fp in file_paths:
        if not fp.exists():
            print(f"  ⚠️  文件不存在：{fp}")
            continue
        doc = build_document(fp)
        documents.append(doc)
        print(f"  📄 {fp.name} → ID: {doc['id']}")
    
    if not documents:
        return {"updated": 0}
    
    if dry_run:
        print(f"\n[dry-run] 将更新 {len(documents)} 个文档")
        return {"updated": len(documents)}
    
    # 使用 add_documents - 相同 ID 会自动更新
    task = index.add_documents(documents)
    client.wait_for_task(task.task_uid)
    
    print(f"\n✅ 已更新 {len(documents)} 个文档 (task_uid={task.task_uid})")
    return {"updated": len(documents)}


def delete_documents(file_paths: list[Path], dry_run: bool = False) -> dict:
    """删除文档"""
    client = meilisearch.Client(MEILI_URL, MEILI_KEY)
    index = client.get_index(INDEX_UID)
    
    doc_ids = []
    for fp in file_paths:
        rel_path = str(fp.relative_to(WIKI_DIR)) if fp.is_relative_to(WIKI_DIR) else str(fp)
        doc_id = generate_doc_id(rel_path)
        doc_ids.append(doc_id)
        print(f"  🗑️  {fp.name} → ID: {doc_id}")
    
    if not doc_ids:
        return {"deleted": 0}
    
    if dry_run:
        print(f"\n[dry-run] 将删除 {len(doc_ids)} 个文档")
        return {"deleted": len(doc_ids)}
    
    task = index.delete_documents(doc_ids)
    client.wait_for_task(task.task_uid)
    
    print(f"\n✅ 已删除 {len(doc_ids)} 个文档 (task_uid={task.task_uid})")
    return {"deleted": len(doc_ids)}


def find_recent_files(minutes: int) -> list[Path]:
    """查找最近修改的文件"""
    cutoff = datetime.now() - timedelta(minutes=minutes)
    recent = []
    
    for md_file in WIKI_DIR.rglob("*.md"):
        if md_file.name == "index.md":
            continue
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
        if mtime >= cutoff:
            recent.append(md_file)
    
    return sorted(recent, key=lambda f: f.stat().st_mtime, reverse=True)


def main():
    parser = argparse.ArgumentParser(description="增量更新 Meilisearch 索引")
    parser.add_argument("--file", type=Path, help="更新单个文件")
    parser.add_argument("--files", type=Path, nargs="+", help="更新多个文件")
    parser.add_argument("--recent", type=int, metavar="MIN", help="更新最近 N 分钟修改的文件")
    parser.add_argument("--delete", type=Path, nargs="+", help="删除文档")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Meilisearch 增量更新")
    print("=" * 60)
    
    if args.file:
        print(f"\n📝 更新单个文件：{args.file}")
        update_documents([args.file], args.dry_run)
    
    elif args.files:
        print(f"\n📝 更新 {len(args.files)} 个文件:")
        update_documents(args.files, args.dry_run)
    
    elif args.recent:
        print(f"\n📝 查找最近 {args.recent} 分钟修改的文件...")
        recent = find_recent_files(args.recent)
        if recent:
            print(f"找到 {len(recent)} 个文件:")
            for f in recent:
                print(f"  - {f.relative_to(WIKI_DIR)}")
            update_documents(recent, args.dry_run)
        else:
            print("没有找到最近修改的文件")
    
    elif args.delete:
        print(f"\n🗑️  删除 {len(args.delete)} 个文档:")
        delete_documents(args.delete, args.dry_run)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
