#!/bin/bash

# WhatsApp Bot Launcher Script
# Usage: ./start_bot.sh [run|test|schedule|setup|stop]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/whatsapp_automation.py"
PID_FILE="$SCRIPT_DIR/whatsapp_bot.pid"
LOG_FILE="$SCRIPT_DIR/whatsapp_bot.log"
VENV_DIR="$SCRIPT_DIR/venv"

# Function to get the correct Python executable
get_python_exe() {
    if [ -d "$VENV_DIR" ]; then
        echo "$VENV_DIR/bin/python"
    else
        echo "python3"
    fi
}

case "$1" in
    "setup")
        echo "Setting up WhatsApp Bot..."
        python3 "$SCRIPT_DIR/setup.py"
        ;;
    
    "run")
        echo "Starting WhatsApp Bot..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "Bot is already running (PID: $PID)"
                exit 1
            else
                rm -f "$PID_FILE"
            fi
        fi
        
        PYTHON_EXE=$(get_python_exe)
        nohup "$PYTHON_EXE" "$PYTHON_SCRIPT" run > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "WhatsApp Bot started in background (PID: $!)"
        echo "Python: $PYTHON_EXE"
        echo "Logs: $LOG_FILE"
        ;;
    
    "stop")
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                kill $PID
                rm -f "$PID_FILE"
                echo "WhatsApp Bot stopped (PID: $PID)"
            else
                echo "Bot is not running"
                rm -f "$PID_FILE"
            fi
        else
            echo "No PID file found. Bot may not be running."
        fi
        ;;
    
    "status")
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "WhatsApp Bot is running (PID: $PID)"
            else
                echo "Bot is not running (stale PID file)"
                rm -f "$PID_FILE"
            fi
        else
            echo "WhatsApp Bot is not running"
        fi
        ;;
    
    "test")
        if [ -z "$2" ]; then
            echo "Usage: $0 test <phone_number> [message]"
            echo "Example: $0 test +1234567890 'Hello World'"
            exit 1
        fi
        
        PHONE="$2"
        MESSAGE="${3:-Test message from WhatsApp Bot}"
        echo "Sending test message to $PHONE..."
        PYTHON_EXE=$(get_python_exe)
        "$PYTHON_EXE" "$PYTHON_SCRIPT" test "$PHONE" "$MESSAGE"
        ;;
    
    "schedule")
        echo "Listing scheduled jobs..."
        PYTHON_EXE=$(get_python_exe)
        "$PYTHON_EXE" "$PYTHON_SCRIPT" schedule
        ;;
    
    "logs")
        if [ -f "$LOG_FILE" ]; then
            tail -f "$LOG_FILE"
        else
            echo "No log file found at $LOG_FILE"
        fi
        ;;
    
    *)
        echo "WhatsApp Automation Bot Launcher"
        echo "Usage: $0 {setup|run|stop|status|test|schedule|logs}"
        echo ""
        echo "Commands:"
        echo "  setup     - Install dependencies and setup the bot"
        echo "  run       - Start the bot in background"
        echo "  stop      - Stop the running bot"
        echo "  status    - Check if bot is running"
        echo "  test      - Send a test message"
        echo "  schedule  - List scheduled jobs"
        echo "  logs      - Show live logs"
        echo ""
        echo "Examples:"
        echo "  $0 setup"
        echo "  $0 run"
        echo "  $0 test +1234567890 'Hello World'"
        echo "  $0 stop"
        exit 1
        ;;
esac