#!/bin/bash
# 巴菲特 Wiki - 初始化安装脚本
# 首次 clone 仓库后运行此脚本完成所有配置

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_step() {
    printf "\n${BLUE}═══════════════════════════════════════════════${NC}\n"
    printf "${BLUE}%s${NC}\n" "$1"
    printf "${BLUE}═══════════════════════════════════════════════${NC}\n\n"
}

echo_success() {
    printf "${GREEN}✅ %s${NC}\n" "$1"
}

echo_warn() {
    printf "${YELLOW}⚠️  %s${NC}\n" "$1"
}

echo_error() {
    printf "${RED}❌ %s${NC}\n" "$1"
}

# 开始
echo ""
printf "${GREEN}🐸 巴菲特 Wiki 初始化安装脚本${NC}\n"
printf "   仓库路径：%s\n\n" "$REPO_ROOT"

# ═══════════════════════════════════════════════
# Step 1: 安装 Git Hooks
# ═══════════════════════════════════════════════
echo_step "Step 1: 安装 Git Hooks"

if [ -d "$SCRIPT_DIR/hooks" ]; then
    git config core.hooksPath scripts/hooks
    chmod +x "$SCRIPT_DIR/hooks/"* 2>/dev/null || true
    echo_success "Git Hooks 已安装 (scripts/hooks)"
else
    echo_warn "scripts/hooks 目录不存在，跳过 Git Hooks 安装"
fi

# ═══════════════════════════════════════════════
# Step 2: 安装 Python 依赖
# ═══════════════════════════════════════════════
echo_step "Step 2: 安装 Python 依赖"

if command -v uv &> /dev/null; then
    echo "使用 uv 安装依赖..."
    uv sync
    echo_success "Python 依赖已安装"
    
    # 创建别名（可选，方便使用）
    ALIAS_CMD="alias buffett-wiki='cd $REPO_ROOT && uv run buffett-wiki'"
    echo ""
    echo "💡 提示：添加以下别名到 ~/.zshrc 或 ~/.bashrc 可简化使用："
    echo "   $ALIAS_CMD"
    echo ""
    echo "   或直接用 uv run："
    echo "   cd $REPO_ROOT && uv run buffett-wiki search 安全边际"
else
    echo_warn "uv 未安装，请先安装：curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "或使用 pip 安装依赖："
    printf "  ${YELLOW}pip install -e .${NC}\n"
fi

# ═══════════════════════════════════════════════
# Step 3: 创建 .env.meilisearch 配置文件
# ═══════════════════════════════════════════════
echo_step "Step 3: 配置 Meilisearch"

if [ -f "$REPO_ROOT/.env.meilisearch" ]; then
    echo_success ".env.meilisearch 已存在"
else
    cat > "$REPO_ROOT/.env.meilisearch" << 'EOF'
# Meilisearch Configuration for Buffett Wiki
# Created by install.sh

# Server Configuration
MEILI_URL=http://127.0.0.1:7700
MEILI_MASTER_KEY=meilisearch-buffett-wiki-key

# Index Configuration
MEILI_INDEX_UID=buffett-wiki

# Note: This file is gitignored, keep it secure!
EOF
    echo_success ".env.meilisearch 已创建"
fi

# ═══════════════════════════════════════════════
# Step 4: 检查 Meilisearch 服务
# ═══════════════════════════════════════════════
echo_step "Step 4: 检查 Meilisearch 服务状态"

if command -v curl &> /dev/null; then
    if curl -s "http://127.0.0.1:7700/health" > /dev/null 2>&1; then
        echo_success "Meilisearch 服务正在运行 (http://127.0.0.1:7700)"
        
        # 检查索引是否存在
        INDEX_EXISTS=$(curl -s -H "Authorization: Bearer meilisearch-buffett-wiki-key" \
            "http://127.0.0.1:7700/indexes/buffett-wiki/stats" 2>/dev/null | \
            python3 -c "import sys,json; print('yes' if json.load(sys.stdin).get('numberOfDocuments', 0) > 0 else 'no')" 2>/dev/null || echo "no")
        
        if [ "$INDEX_EXISTS" = "yes" ]; then
            echo_success "buffett-wiki 索引已存在且有数据"
        else
            echo_warn "buffett-wiki 索引不存在或为空"
            echo ""
            echo "   需要初始化索引吗？运行以下命令："
            printf "   ${YELLOW}uv run python scripts/rebuild_index.py${NC}\n"
        fi
    else
        echo_warn "Meilisearch 服务未运行"
        echo ""
        echo "   启动 Meilisearch 服务："
        printf "   ${YELLOW}meilisearch --master-key meilisearch-buffett-wiki-key${NC}\n"
        echo ""
        echo "   或使用 Homebrew (macOS):"
        printf "   ${YELLOW}brew services start meilisearch${NC}\n"
    fi
else
    echo_warn "curl 未安装，跳过服务检查"
fi

# ═══════════════════════════════════════════════
# Step 5: 检查 wiki 目录
# ═══════════════════════════════════════════════
echo_step "Step 5: 检查 Wiki 内容"

if [ -d "$REPO_ROOT/wiki" ]; then
    MD_COUNT=$(find "$REPO_ROOT/wiki" -name "*.md" | wc -l | tr -d ' ')
    echo_success "Wiki 目录存在：$MD_COUNT 篇笔记"
else
    echo_error "wiki 目录不存在！"
    echo "   请确认仓库结构是否正确"
fi

# ═══════════════════════════════════════════════
# 完成
# ═══════════════════════════════════════════════
echo_step "安装完成"

printf "${GREEN}🎉 初始化完成！${NC}\n"
echo ""
echo "📚 常用命令："
echo ""
printf "   ${YELLOW}# 搜索测试${NC}\n"
echo "   uv run python scripts/test_search.py"
echo ""
printf "   ${YELLOW}# 更新索引（全量重建）${NC}\n"
echo "   uv run python scripts/rebuild_index.py"
echo ""
printf "   ${YELLOW}# 更新索引（增量，最近 1 小时）${NC}\n"
echo "   uv run python scripts/update_index.py --recent 60"
echo ""
printf "   ${YELLOW}# 启动 Meilisearch 服务 (如未运行)${NC}\n"
echo "   meilisearch --master-key meilisearch-buffett-wiki-key"
echo ""
echo "📖 详细文档：docs/plans/PLAN-meilisearch-migration.md"
echo ""
printf "${BLUE}═══════════════════════════════════════════════${NC}\n"
echo ""
