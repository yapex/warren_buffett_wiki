#!/bin/bash
# 启动 RAG 服务

cd "$(dirname "$0")/.."

echo "📚 Buffett Wiki RAG"
echo "=================="

# 检查是否有索引
if [ ! -d "rag/graph_store" ]; then
    echo "🔨 初始化索引..."
    uv run python -c "
from rag.config import initialize_rag, rag
print(f'📊 正在索引 {initialize_rag()} 个文档...')
print('✅ 索引完成!')
"
fi

echo ""
echo "🚀 启动查询服务..."
echo ""

uv run python rag/query.py
