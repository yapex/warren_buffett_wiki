# Research 文档创建 Checklist

> 每次创建新的 research 文档后，按此清单逐项完成

---

## 📋 必需操作（Must Do）

### 1. 更新 log.md
- [ ] 在 `wiki/log.md` 顶部添加本次操作记录
- [ ] 包含：日期、操作描述、创建的文件、关键数据摘要
- [ ] 添加相关文档链接

### 2. 检查 Frontmatter
- [ ] `type: research` 已设置
- [ ] `created: YYYY-MM-DD` 已填写
- [ ] `sources: [...]` 列出所有数据来源
- [ ] `status: complete` 或 `status: draft`

### 3. 验证内部链接
- [ ] 所有 `[[概念]]` 链接指向存在的文件
- [ ] 所有 `[信件](path)` 链接有效
- [ ] 所有 `[公司](path)`、`[人物](path)` 链接有效
- [ ] 无 404 链接

### 4. 数据可追溯
- [ ] 每个关键数据都标注了来源信件
- [ ] 表格数据可在原文中找到
- [ ] 引用有明确的页码或段落

---

## 🔗 推荐操作（Should Do）

### 5. 更新相关页面反向链接
- [ ] 在相关 `companies/xxx.md` 添加 "相关研究" 章节
- [ ] 在相关 `concepts/xxx.md` 添加 "相关研究" 章节
- [ ] 在相关 `people/xxx.md` 添加 "相关研究" 章节

### 6. 创建关联文档（如需要）
- [ ] 检查是否需要新的 `research/cases/xxx.md`
- [ ] 检查是否需要新的 `concepts/xxx.md`
- [ ] 检查是否需要新的 `companies/xxx.md`

### 7. 更新索引页（如存在）
- [ ] `wiki/research/index.md`（如有）
- [ ] `wiki/letters/index.md`（如相关）
- [ ] `wiki/companies/index.md`（如相关）

---

## 🔄 可选操作（Nice to Do）

### 8. RAG 索引更新
- [ ] 运行 `uv run python -m rag rebuild`（如使用 RAG）
- [ ] 验证新文档可被检索到

### 9. 质量检查
- [ ] 表格格式正确（Markdown 对齐）
- [ ] 无错别字
- [ ] 与现有 research 文档风格一致
- [ ] 数据计算正确（如年化收益率、累计收益）

### 10. Git 提交
- [ ] `git add wiki/research/xxx.md`
- [ ] `git add wiki/log.md`
- [ ] `git add` 其他相关文件
- [ ] `git commit -m "research: 创建 XXX 业绩表"`
- [ ] `git push`

---

## 📝 log.md 记录模板

```markdown
## YYYY-MM-DD

**操作**: 创建 XXX 研究

### 完成的工作
- 创建 wiki/research/XXX.md — 简短描述
- 更新 wiki/companies/XXX.md — 添加反向链接（如有）
- 更新 wiki/log.md — 本记录

### 关键数据
- 数据点 1
- 数据点 2

### 来源
- 来源文件 1
- 来源文件 2

### 相关文档
- [相关文档 1](./path/to/doc.md)
- [相关文档 2](./path/to/doc.md)
```

---

## 🚀 自动化脚本（进阶）

运行以下命令自动完成部分检查：

```bash
# 检查新 research 文件的链接有效性
uv run python scripts/check_research_links.py wiki/research/XXX.md

# 自动更新 log.md（需手动确认）
uv run python scripts/update_log.py --file wiki/research/XXX.md

# 完整工作流
uv run python scripts/research_workflow.py wiki/research/XXX.md
```

---

## ✅ 完成标准

一份 research 文档算"完成"，当且仅当：

- [x] log.md 已更新
- [x] Frontmatter 完整
- [x] 所有内部链接有效
- [x] 数据可追溯到原文
- [x] 至少 1 个相关页面添加了反向链接

---

*最后更新：2026-04-09*
