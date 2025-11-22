#!/bin/bash
# PACO Demo - Shows the unified CLI in action

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH="${SCRIPT_DIR}:${PATH}"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

PROJECT="demo"

echo "🎯 PACO Demo - Unified CLI"
echo "===================================="
echo ""

echo "📝 Step 1: Initialize PACO"
python3 "${SCRIPT_DIR}/paco" init
echo ""

echo "📋 Step 2: Add tasks"
python3 "${SCRIPT_DIR}/paco" task add $PROJECT "Set up development environment" --priority high
python3 "${SCRIPT_DIR}/paco" task add $PROJECT "Write documentation" --priority medium --tags docs
python3 "${SCRIPT_DIR}/paco" task add $PROJECT "Create tests" --priority low --tags testing
echo ""

echo "📋 Step 3: List tasks"
python3 "${SCRIPT_DIR}/paco" task list $PROJECT
echo ""

echo "📝 Step 4: Add log entries"
python3 "${SCRIPT_DIR}/paco" log $PROJECT "Started working on the setup"
python3 "${SCRIPT_DIR}/paco" log $PROJECT "Installed dependencies"
python3 "${SCRIPT_DIR}/paco" log $PROJECT "Fixed a bug in authentication"
echo ""

echo "📅 Step 5: Add daily notes"
python3 "${SCRIPT_DIR}/paco" daily "Morning: Working on demo project"
python3 "${SCRIPT_DIR}/paco" daily "Had a breakthrough on architecture"
echo ""

echo "✓ Step 6: Complete a task"
python3 "${SCRIPT_DIR}/paco" task done $PROJECT 1
echo ""

echo "📋 Step 7: List updated tasks"
python3 "${SCRIPT_DIR}/paco" task list $PROJECT
echo ""

echo "📁 Step 8: List all projects"
python3 "${SCRIPT_DIR}/paco" projects
echo ""

echo "⚙️  Step 9: Show configuration"
python3 "${SCRIPT_DIR}/paco" config --list
echo ""

echo "📂 Step 10: Check the files created"
if [ -d "${HOME}/paco/projects/${PROJECT}" ]; then
    echo "Project directory:"
    ls -lh "${HOME}/paco/projects/${PROJECT}/"
    echo ""
    
    echo "Tasks (tasks.ndjson):"
    cat "${HOME}/paco/projects/${PROJECT}/tasks.ndjson"
    echo ""
    
    echo "Recent logs:"
    tail -n 10 "${HOME}/paco/projects/${PROJECT}/log.md"
fi

echo ""
echo "===================================="
echo "✨ Demo complete!"
echo ""
echo "Your demo project is at: ~/paco/projects/${PROJECT}"
echo ""
echo "Try these commands:"
echo "  paco next ${PROJECT}                    # Get AI recommendation"
echo "  paco ask ${PROJECT} 'What to focus on?' # Ask the AI"
echo "  paco summarize project ${PROJECT}       # Generate summary"
echo ""
echo "Note: AI commands require Ollama installed"
echo "  curl -fsSL https://ollama.com/install.sh | sh"
echo "  ollama pull llama3.2"
