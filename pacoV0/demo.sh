#!/bin/bash
# PACO Demo Script - Shows off the key features

set -e

echo "🎯 PACO Demo - Personal AI Assistant"
echo "===================================="
echo ""

# Setup PATH for this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH="${SCRIPT_DIR}:${PATH}"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

PROJECT="demo"

echo "📝 Step 1: Adding tasks to the '$PROJECT' project"
echo ""

python3 "${SCRIPT_DIR}/paco-add-task" $PROJECT "Set up development environment" --priority high
python3 "${SCRIPT_DIR}/paco-add-task" $PROJECT "Write documentation" --priority medium --tags docs
python3 "${SCRIPT_DIR}/paco-add-task" $PROJECT "Create unit tests" --priority low --tags testing
python3 "${SCRIPT_DIR}/paco-add-task" $PROJECT "Review code quality" --priority medium --tags review

echo ""
echo "✅ Tasks added!"
echo ""

echo "📋 Step 2: Listing tasks"
echo ""
python3 "${SCRIPT_DIR}/paco-list" tasks $PROJECT

echo ""
echo "📝 Step 3: Adding log entries"
echo ""

python3 "${SCRIPT_DIR}/paco-log" $PROJECT "Started working on the dev environment setup"
python3 "${SCRIPT_DIR}/paco-log" $PROJECT "Installed all dependencies, running tests"
python3 "${SCRIPT_DIR}/paco-log" $PROJECT "Found a bug in the authentication module, investigating"

echo "✅ Log entries added!"
echo ""

echo "📅 Step 4: Adding daily notes"
echo ""

python3 "${SCRIPT_DIR}/paco-daily" "Morning: Deep work on the demo project"
python3 "${SCRIPT_DIR}/paco-daily" "Had a breakthrough on the architecture design"
python3 "${SCRIPT_DIR}/paco-daily" "Afternoon: Documentation and testing"

echo "✅ Daily notes added!"
echo ""

echo "✓ Step 5: Completing a task"
echo ""

python3 "${SCRIPT_DIR}/paco-complete" $PROJECT 1

echo ""

echo "📋 Step 6: Viewing updated tasks"
echo ""
python3 "${SCRIPT_DIR}/paco-list" tasks $PROJECT

echo ""
echo "📁 Step 7: Checking the file structure"
echo ""

if [ -d "${HOME}/paco/projects/${PROJECT}" ]; then
    echo "Project directory contents:"
    ls -lh "${HOME}/paco/projects/${PROJECT}/"
    echo ""
    
    echo "Tasks file (tasks.ndjson):"
    cat "${HOME}/paco/projects/${PROJECT}/tasks.ndjson"
    echo ""
    
    echo "Recent log entries (log.md):"
    tail -n 15 "${HOME}/paco/projects/${PROJECT}/log.md"
    echo ""
fi

if [ -d "${HOME}/paco/daily" ]; then
    TODAY=$(date +%Y-%m-%d)
    if [ -f "${HOME}/paco/daily/${TODAY}.md" ]; then
        echo "Today's daily note:"
        cat "${HOME}/paco/daily/${TODAY}.md"
        echo ""
    fi
fi

echo "===================================="
echo "✨ Demo complete!"
echo ""
echo "Your demo project is now set up at: ~/paco/projects/${PROJECT}"
echo ""
echo "Try these commands:"
echo "  paco-next ${PROJECT}                           # Get AI recommendation"
echo "  paco-ask ${PROJECT} 'What should I focus on?'  # Ask the AI"
echo "  paco-summarize-project ${PROJECT}              # Generate summary"
echo "  paco-summarize-day                             # Summarize today"
echo ""
echo "Note: AI commands require Ollama with llama3.2 model installed"
echo "Install: curl -fsSL https://ollama.com/install.sh | sh"
echo "Then: ollama pull llama3.2"
