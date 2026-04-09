# RAG 查询指南

> 详细用法见项目 skill：`.pi/skills/buffett-rag/SKILL.md`
> 
> 本文档保留作为 SCHEMA.md 的参考链接目标。

## 核心规则

- **RAG 优先**：查询用 RAG 多轮迭代，不用 grep/sed
- **迭代查询**：宽泛 → 精确 → 补充 → 深入，最少 2-3 轮
- **重建索引**：新增/修改文件后执行 `uv run python .rag/query.py rebuild`
