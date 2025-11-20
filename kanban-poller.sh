#!/bin/bash
# Kanban Work Poller Control Script
# Usage: ./kanban-poller.sh [start|stop|status|restart]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$SCRIPT_DIR"
VENV_PYTHON="$WORKSPACE_DIR/venv/bin/python"
POLLER_SCRIPT="$WORKSPACE_DIR/santiago_core/services/kanban_work_poller.py"
PID_FILE="$WORKSPACE_DIR/kanban-work-poller.pid"
LOG_DIR="$WORKSPACE_DIR/logs"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Default arguments for the poller
POLL_INTERVAL=60
MAX_CONCURRENT=2

start() {
    echo "🚀 Starting Kanban Work Poller..."

    if [ -f "$PID_FILE" ]; then
        if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "❌ Poller is already running (PID: $(cat "$PID_FILE"))"
            return 1
        else
            echo "🧹 Removing stale PID file"
            rm "$PID_FILE"
        fi
    fi

    cd "$WORKSPACE_DIR"

    # Start the poller in background
    PYTHONPATH="$WORKSPACE_DIR" nohup "$VENV_PYTHON" "$POLLER_SCRIPT" \
        --poll-interval "$POLL_INTERVAL" \
        --max-concurrent "$MAX_CONCURRENT" \
        > "$LOG_DIR/kanban-work-poller.out" \
        2> "$LOG_DIR/kanban-work-poller.err" \
        &

    POLLER_PID=$!
    echo $POLLER_PID > "$PID_FILE"

    echo "✅ Kanban Work Poller started (PID: $POLLER_PID)"
    echo "📋 Logs: $LOG_DIR/kanban-work-poller.out"
    echo "❌ Errors: $LOG_DIR/kanban-work-poller.err"
}

stop() {
    echo "🛑 Stopping Kanban Work Poller..."

    if [ ! -f "$PID_FILE" ]; then
        echo "❌ PID file not found. Is the poller running?"
        return 1
    fi

    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        echo "📡 Sending SIGTERM to process $PID..."
        kill "$PID"

        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done

        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            echo "⚠️  Process didn't stop gracefully, sending SIGKILL..."
            kill -9 "$PID"
        fi
    else
        echo "⚠️  Process $PID was not running"
    fi

    rm -f "$PID_FILE"
    echo "✅ Kanban Work Poller stopped"
}

status() {
    echo "📊 Kanban Work Poller Status:"

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ Running (PID: $PID)"
            echo "📋 Uptime: $(ps -p "$PID" -o etime= | tr -d ' ')"
        else
            echo "❌ PID file exists but process is not running"
        fi
    else
        echo "❌ Not running"
    fi

    echo "📁 Log directory: $LOG_DIR"
    echo "📄 PID file: $PID_FILE"

    # Show recent log entries
    if [ -f "$LOG_DIR/kanban-work-poller.out" ]; then
        echo ""
        echo "📋 Recent log entries:"
        tail -5 "$LOG_DIR/kanban-work-poller.out" | sed 's/^/  /'
    fi
}

restart() {
    echo "🔄 Restarting Kanban Work Poller..."
    stop
    sleep 2
    start
}

case "${1:-status}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 [start|stop|status|restart]"
        echo ""
        echo "Commands:"
        echo "  start   - Start the Kanban Work Poller"
        echo "  stop    - Stop the Kanban Work Poller"
        echo "  status  - Show poller status and recent logs"
        echo "  restart - Restart the Kanban Work Poller"
        exit 1
        ;;
esac