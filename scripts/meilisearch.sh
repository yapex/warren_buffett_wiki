#!/usr/bin/env bash
#
# Meilisearch 管理脚本 — Buffett Wiki
#
# 用法:
#   ./meili.sh start    — 启动服务
#   ./meili.sh stop     — 停止服务
#   ./meili.sh restart  — 重启服务
#   ./meili.sh status   — 查看状态
#   ./meili.sh logs     — 查看日志
#   ./meili.sh reindex  — 重新索引
#   ./meili.sh dump     — 导出备份
#   ./meili.sh test     — 运行测试

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MEILI_BIN="/opt/homebrew/bin/meilisearch"
MEILI_KEY="meilisearch-buffett-wiki-key"
MEILI_ADDR="127.0.0.1:7700"
STDOUT_LOG="/tmp/meilisearch-buffett-wiki.stdout.log"
STDERR_LOG="/tmp/meilisearch-buffett-wiki.stderr.log"

case "${1:-help}" in
    start)
        echo "🚀 启动 Meilisearch..."
        if curl -sf "$MEILI_ADDR/health" > /dev/null 2>&1; then
            echo "   ✅ 已在运行中"
            exit 0
        fi
        nohup "$MEILI_BIN" \
            --http-addr "$MEILI_ADDR" \
            --master-key "$MEILI_KEY" \
            --db-path "$PROJECT_DIR/data.ms" \
            --dump-dir "$PROJECT_DIR/dumps" \
            > "$STDOUT_LOG" 2> "$STDERR_LOG" &
        # 等待就绪
        for i in $(seq 1 10); do
            if curl -sf "$MEILI_ADDR/health" > /dev/null 2>&1; then
                echo "   ✅ 启动成功 (PID: $!)"
                exit 0
            fi
            sleep 1
        done
        echo "   ❌ 启动超时，查看日志: $STDERR_LOG"
        exit 1
        ;;

    stop)
        echo "🛑 停止 Meilisearch..."
        pkill -f "meilisearch.*--master-key.*$MEILI_KEY" 2>/dev/null || true
        echo "   ✅ 已停止"
        ;;

    restart)
        "$0" stop
        sleep 2
        "$0" start
        ;;

    status)
        echo "📊 Meilisearch 状态:"
        echo ""
        if pgrep -f "meilisearch.*--master-key.*$MEILI_KEY" > /dev/null 2>&1; then
            PID=$(pgrep -f "meilisearch.*--master-key.*$MEILI_KEY" | head -1)
            echo "   进程: ✅ 运行中 (PID: $PID)"
        else
            echo "   进程: ❌ 未运行"
        fi
        HEALTH=$(curl -sf "$MEILI_ADDR/health" 2>/dev/null || echo '{"status":"unreachable"}')
        echo "   健康: $HEALTH"
        STATS=$(curl -sf -H "Authorization: Bearer $MEILI_KEY" \
            "$MEILI_ADDR/indexes/buffett-wiki/stats" 2>/dev/null || echo 'null')
        if [ "$STATS" != "null" ]; then
            DOCS=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('numberOfDocuments', 'N/A'))" 2>/dev/null || echo "N/A")
            echo "   文档数: $DOCS"
        fi
        ;;

    logs)
        echo "📋 最近日志:"
        tail -30 "$STDOUT_LOG" 2>/dev/null || echo "(无日志)"
        ;;

    reindex)
        echo "🔄 重新索引..."
        cd "$PROJECT_DIR"
        uv run python scripts/step3_migrate_data.py
        ;;

    dump)
        echo "💾 导出备份..."
        curl -sf -X POST -H "Authorization: Bearer $MEILI_KEY" \
            "$MEILI_ADDR/dumps" | python3 -m json.tool
        echo "   备份目录: $PROJECT_DIR/dumps/"
        ;;

    test)
        cd "$PROJECT_DIR"
        uv run python scripts/step5_test.py
        ;;

    help|*)
        echo "📚 Meilisearch 管理脚本 — Buffett Wiki"
        echo ""
        echo "用法: ./meili.sh <命令>"
        echo ""
        echo "命令:"
        echo "  start    启动服务"
        echo "  stop     停止服务"
        echo "  restart  重启服务"
        echo "  status   查看状态"
        echo "  logs     查看日志"
        echo "  reindex  重新索引"
        echo "  dump     导出备份"
        echo "  test     运行测试"
        ;;
esac
