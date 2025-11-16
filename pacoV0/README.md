# PACO - Personal AI Assistant, Contextual and Offline

A **local, offline, Linux CLI-driven** personal assistant that helps you manage tasks, projects, and ideas while staying completely private on your machine.

## Features

✨ **Stage 1 MVP** (Fully Implemented):
- ✅ File-based NoSQL data store (human-readable)
- ✅ Task management with priorities and tags
- ✅ Project logging with timestamps
- ✅ Daily notes and journaling
- ✅ LLM-powered task recommendations (`paco-next`)
- ✅ LLM-powered project Q&A (`paco-ask`)
- ✅ **Bounded context** - LLM never reads full files
- ✅ Privacy-first - all data stays local

🚀 **Stage 2** (Fully Implemented):
- ✅ Project summarization with archiving
- ✅ Daily note summarization
- ✅ Automatic log rotation

## Prerequisites

1. **Python 3.8+** (usually pre-installed on Linux)
2. **Ollama** - Local LLM runner

### Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the default model (llama3.2)
ollama pull llama3.2
```

## Installation

```bash
# 1. Copy all PACO files to a directory (e.g., ~/paco-bin)
mkdir -p ~/paco-bin
cp paco-* ~/paco-bin/
cp paco_lib.py ~/paco-bin/

# 2. Make scripts executable (if not already)
chmod +x ~/paco-bin/paco-*

# 3. Add to PATH (add this to your ~/.bashrc or ~/.zshrc)
export PATH="$HOME/paco-bin:$PATH"
export PYTHONPATH="$HOME/paco-bin:$PYTHONPATH"

# 4. Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

## Quick Start

```bash
# Add your first task
paco-add-task myproject "Set up development environment" --priority high

# Add more tasks
paco-add-task myproject "Write README" --priority medium
paco-add-task myproject "Create tests" --priority low --tags testing,python

# List your projects
paco-list projects

# List tasks in a project
paco-list tasks myproject

# Add a log entry
paco-log myproject "Started working on setup, installed dependencies"

# Write a daily note
paco-daily "Had a productive morning, figured out the architecture"

# Ask the AI what to work on next
paco-next myproject

# Ask the AI a question about your project
paco-ask myproject "What should I focus on to unblock progress?"

# Mark a task as complete
paco-complete myproject 1

# Generate a project summary
paco-summarize-project myproject --archive

# Summarize your day
paco-summarize-day
```

## CLI Commands Reference

### Core Commands (Stage 1)

#### `paco-add-task`
Add a new task to a project.

```bash
paco-add-task <project> "<title>" [--priority high|medium|low] [--tags tag1,tag2]
```

**Examples:**
```bash
paco-add-task blog "Write post about AI" --priority high
paco-add-task website "Fix mobile layout" --priority medium --tags css,responsive
```

#### `paco-log`
Add a timestamped log entry to a project.

```bash
paco-log <project> "<message>"
```

**Examples:**
```bash
paco-log blog "Finished research phase, found 5 good sources"
paco-log website "Discovered flexbox bug in Safari"
```

#### `paco-daily`
Write a note to today's daily log.

```bash
paco-daily "<message>"
```

**Examples:**
```bash
paco-daily "Morning: focused deep work on the blog. Afternoon: meetings."
paco-daily "Key insight: should use composition over inheritance here"
```

#### `paco-list`
List projects or tasks.

```bash
paco-list projects
paco-list tasks <project> [--all]
```

**Examples:**
```bash
paco-list projects
paco-list tasks blog
paco-list tasks blog --all  # Include completed tasks
```

#### `paco-complete`
Mark a task as completed.

```bash
paco-complete <project> <task_id>
```

**Examples:**
```bash
paco-complete blog 1
paco-complete website 5
```

#### `paco-next`
Get AI recommendation for what to work on next.

```bash
paco-next <project> [--model llama3.2]
```

**Examples:**
```bash
paco-next blog
paco-next website --model llama3.2
```

**Output includes:**
- Recommended task(s)
- Reasoning why
- Three concrete steps to start

#### `paco-ask`
Ask the AI a question about your project.

```bash
paco-ask <project> "<question>" [--model llama3.2]
```

**Examples:**
```bash
paco-ask blog "How should I structure the introduction?"
paco-ask website "What's blocking me from deploying?"
paco-ask myproject "Should I refactor now or add features first?"
```

### Summarization Commands (Stage 2)

#### `paco-summarize-project`
Generate or update project summary using AI.

```bash
paco-summarize-project <project> [--archive] [--keep-lines N] [--model llama3.2]
```

**Examples:**
```bash
# Just update summary
paco-summarize-project blog

# Update summary and archive old logs (keeping last 40 lines)
paco-summarize-project blog --archive

# Keep only last 20 lines in main log
paco-summarize-project blog --archive --keep-lines 20
```

**What it does:**
- Reads project log and tasks
- Generates 150-400 word summary with AI
- Optionally archives old log entries
- Keeps project summary small and focused

#### `paco-summarize-day`
Generate summary of daily notes.

```bash
paco-summarize-day [date] [--model llama3.2]
```

**Examples:**
```bash
# Summarize today
paco-summarize-day

# Summarize a specific date
paco-summarize-day 2025-01-15
```

**What it does:**
- Reads daily note
- Generates 5-15 sentence summary
- Captures key insights and decisions
- Stores for future context

## Data Structure

All your data lives in `~/paco/`:

```
~/paco/
├── projects/
│   └── myproject/
│       ├── tasks.ndjson          # All tasks (one JSON per line)
│       ├── log.md                # Recent log entries
│       ├── summary.md            # AI-generated summary
│       ├── index.json            # Metadata
│       └── archive/              # Old archived logs
│           └── log-2025-01-15.md
├── daily/
│   ├── 2025-01-15.md             # Daily notes
│   ├── 2025-01-16.md
│   └── summaries/
│       ├── 2025-01-15.summary.md # AI summaries
│       └── 2025-01-16.summary.md
```

### Why This Structure?

1. **Human-readable**: Everything is Markdown or JSON
2. **Git-friendly**: Text files are easy to version control
3. **Append-only**: Fast writes, no database overhead
4. **Bounded**: Summaries and archives keep context small
5. **Private**: All files stay on your machine

## How It Works: The Memory Strategy

PACO uses a smart **bounded context** approach:

### What the LLM Sees (Small, Fast):
- ✅ Project summary (~150-400 words)
- ✅ Today's daily summary
- ✅ Top 20 active tasks
- ✅ Last 40 lines of project log

### What the LLM Never Sees (Unbounded):
- ❌ Full log files
- ❌ Full task history
- ❌ Complete daily notes
- ❌ Archive files

This ensures:
- ⚡ **Constant-time prompts** - never slow down
- 💾 **Predictable memory** - ~8-15KB per request
- 📈 **Infinite scalability** - files can grow forever
- 🎯 **Relevant context** - only what matters

## Example Workflow

### Morning Routine
```bash
# Check what to work on
paco-next myproject

# Start working, log progress
paco-log myproject "Starting on the database schema design"

# Add insights to daily note
paco-daily "Realized we need an index on user_id for performance"
```

### During Work
```bash
# Get unstuck
paco-ask myproject "How should I handle the authentication flow?"

# Add new tasks as they come up
paco-add-task myproject "Add rate limiting" --priority high

# Log progress
paco-log myproject "Finished auth module, all tests passing"
```

### End of Day
```bash
# Mark completed tasks
paco-complete myproject 3
paco-complete myproject 7

# Summarize the day
paco-summarize-day

# Check tomorrow's priorities
paco-next myproject
```

### Weekly Maintenance
```bash
# Summarize project and archive old logs
paco-summarize-project myproject --archive

# Review all projects
paco-list projects
paco-list tasks project1
paco-list tasks project2
```

## Advanced Tips

### 1. Use Tags for Organization
```bash
paco-add-task myproject "Fix login bug" --tags bug,urgent,frontend
paco-add-task myproject "Add tests" --tags testing,backend
```

### 2. Different Priority Levels
```bash
# High priority - blockers, urgent items
paco-add-task myproject "Production is down!" --priority high

# Medium priority - normal work
paco-add-task myproject "Implement feature X" --priority medium

# Low priority - nice-to-haves
paco-add-task myproject "Refactor old code" --priority low
```

### 3. Regular Summarization
Set up a cron job to summarize daily:
```bash
# Add to crontab (crontab -e)
0 21 * * * /path/to/paco-summarize-day
```

### 4. Backup Your Data
```bash
# All your data is in ~/paco - just back it up!
cp -r ~/paco ~/backups/paco-$(date +%Y%m%d)

# Or use git
cd ~/paco
git init
git add .
git commit -m "Daily backup"
```

### 5. Multiple Models
```bash
# Try different models for different tasks
paco-next myproject --model llama3.2          # Fast, everyday use
paco-ask myproject "Complex question" --model llama3.2  # For harder questions
```

## Troubleshooting

### "Ollama not found"
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Make sure it's running
ollama serve
```

### "No module named 'paco_lib'"
```bash
# Make sure PYTHONPATH is set
export PYTHONPATH="$HOME/paco-bin:$PYTHONPATH"

# Or run from the directory containing paco_lib.py
cd ~/paco-bin
./paco-next myproject
```

### LLM responses are slow
```bash
# Use a smaller model
ollama pull llama3.2:1b  # Smaller, faster

# Then use it
paco-next myproject --model llama3.2:1b
```

### Context too large warning
```bash
# Time to summarize and archive!
paco-summarize-project myproject --archive --keep-lines 20
```

## Privacy & Security

- ✅ **100% Local**: No data ever leaves your machine
- ✅ **No Cloud**: No API calls to external services
- ✅ **No Tracking**: No analytics, no telemetry
- ✅ **Human-Readable**: Inspect your data anytime
- ✅ **Git-Compatible**: Version control your life

## Roadmap

### Stage 3 (Not Yet Implemented)
- [ ] Advanced task search with keywords
- [ ] Tag-based task filtering
- [ ] Optional embeddings for semantic search
- [ ] Better task prioritization algorithms

### Stage 4 (Not Yet Implemented)
- [ ] Background daemon for auto-summarization
- [ ] Local HTTP API for integrations
- [ ] Web UI (optional)
- [ ] Mobile companion app (optional)

## Philosophy

PACO follows these principles:

1. **Privacy First**: Your data is yours, period.
2. **Simplicity**: Plain text files, simple commands.
3. **Bounded Complexity**: Context stays small, performance stays fast.
4. **Incremental Capture**: Log as you go, summarize later.
5. **LLM as Tool**: AI assists, you decide.

## Contributing

This is your personal assistant! Feel free to:
- Modify the prompts in the code
- Adjust context limits in `paco_lib.py`
- Add new commands
- Share improvements

## License

Use it however you want. It's yours.

---

**Built for humans who want AI help without giving up privacy or control.**

Start with: `paco-add-task myproject "Get things done"`
