# PACO - Personal AI Assistant, Contextual and Offline

A **local, offline, CLI-driven** personal assistant that helps you manage tasks, projects, and ideas while staying completely private.

## Quick Start

```bash
# 1. Install Ollama (one-time setup)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# 2. Install PACO
./install.sh

# 3. Start using it
paco init
paco task add myproject "First task" --priority high
paco next myproject
```

## Features

- ✅ **100% Local & Private** - No cloud, no tracking
- ✅ **Bounded Context** - Always fast, never slows down
- ✅ **AI-Powered** - Smart recommendations and advice
- ✅ **Human-Readable** - All data in plain text
- ✅ **Single Command** - One CLI tool, multiple operations

## Installation

```bash
# Copy files to ~/paco-bin
mkdir -p ~/paco-bin
cp paco paco_lib.py ~/paco-bin/
chmod +x ~/paco-bin/paco

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/paco-bin:$PATH"
export PYTHONPATH="$HOME/paco-bin:$PYTHONPATH"

# Reload shell
source ~/.bashrc
```

Or use the provided installer:
```bash
./install.sh
```

## Commands

### Setup & Configuration

```bash
# Initialize PACO
paco init

# View configuration
paco config --list

# Change default model
paco config --set model=llama3.2

# Get a setting
paco config --get model
```

### Projects

```bash
# List all projects
paco projects
```

### Tasks

```bash
# Add a task
paco task add <project> "<title>" [--priority high|medium|low] [--tags tag1,tag2]

# List tasks in a project
paco task list <project>
paco task list <project> --all    # Include completed

# Mark task complete
paco task done <project> <task_id>

# Examples
paco task add blog "Write about AI" --priority high
paco task add website "Fix bug" --priority medium --tags css,urgent
paco task done blog 1
```

### Logging

```bash
# Add project log
paco log <project> "<message>"

# Add daily note
paco daily "<message>"

# Examples
paco log blog "Finished the introduction section"
paco daily "Had a breakthrough on the architecture"
```

### AI Features

```bash
# Get task recommendations
paco next <project> [--model MODEL]

# Ask questions
paco ask <project> "<question>" [--model MODEL]

# Examples
paco next blog
paco ask blog "How should I structure the conclusion?"
paco next myproject --model llama3.2
```

### Maintenance

```bash
# Summarize project (compress old logs)
paco summarize project <project> [--archive] [--keep N]

# Summarize daily notes
paco summarize day [--date YYYY-MM-DD]

# Examples
paco summarize project blog --archive
paco summarize day
paco summarize day --date 2025-01-15
```

## Configuration

Configuration is stored in `~/paco/config.json`. Default settings:

```json
{
  "model": "llama3.2",
  "max_tasks": 20,
  "max_log_lines": 40,
  "max_prompt_kb": 15
}
```

Change settings with:
```bash
paco config --set model=llama3.2
paco config --set max_tasks=30
```

## Data Structure

All data lives in `~/paco/`:

```
~/paco/
├── config.json              # Your settings
├── projects/
│   └── myproject/
│       ├── tasks.ndjson     # Tasks (one JSON per line)
│       ├── log.md           # Activity log
│       ├── summary.md       # AI-generated summary
│       ├── index.json       # Project metadata
│       └── archive/         # Old archived logs
└── daily/
    ├── 2025-01-15.md        # Daily notes
    └── summaries/
        └── 2025-01-15.summary.md  # AI summaries
```

All files are plain text - inspect them anytime!

## How It Works: Bounded Context

PACO uses a **bounded context** approach to stay fast forever:

**What the AI sees (always small):**
- Project summary (~300 words)
- Today's daily summary
- Top 20 active tasks
- Last 40 lines of log

**What the AI never sees:**
- Full logs (could be thousands of lines)
- Archive files
- Completed tasks
- Old daily notes

**Result:** Constant-time queries, infinite scalability.

## Typical Workflows

### Morning Routine
```bash
paco next myproject          # What should I work on?
```

### During Work
```bash
paco log myproject "Fixed authentication bug"
paco daily "Key insight: use JWT tokens"
paco task add myproject "Add rate limiting" --priority high
```

### End of Day
```bash
paco task done myproject 5   # Mark tasks complete
paco summarize day           # Summarize your day
```

### Weekly Maintenance
```bash
paco summarize project myproject --archive
```

## Examples

### Complete Workflow
```bash
# Start a project
paco task add blog "Research topic" --priority high
paco task add blog "Write draft" --priority medium
paco task add blog "Edit & publish" --priority low

# Check tasks
paco task list blog

# Work on it
paco log blog "Found 5 good sources"
paco log blog "Outlined the structure"

# Ask for help
paco ask blog "How should I approach the introduction?"

# Get recommendation
paco next blog

# Complete task
paco task done blog 1

# Track your day
paco daily "Productive morning on the blog"

# End of day
paco summarize day
```

## Command Reference

| Command | Description |
|---------|-------------|
| `paco init` | Initialize PACO directories |
| `paco config --list` | Show all settings |
| `paco config --set KEY=VALUE` | Change a setting |
| `paco projects` | List all projects |
| `paco task add` | Add a task |
| `paco task list` | List tasks |
| `paco task done` | Complete a task |
| `paco log` | Add log entry |
| `paco daily` | Add daily note |
| `paco next` | Get AI recommendation |
| `paco ask` | Ask AI a question |
| `paco summarize project` | Compress project logs |
| `paco summarize day` | Summarize daily notes |

## Tips

### 1. Log Often
Don't wait for big events. Small progress counts:
```bash
paco log myproject "Fixed CSS bug"
paco log myproject "Stuck on database query"
```

### 2. Use Daily Notes
Your thinking space:
```bash
paco daily "Need to refactor auth module"
paco daily "Client approved mockups"
```

### 3. Ask the AI When Stuck
```bash
paco ask myproject "How to approach this refactoring?"
paco ask myproject "What's blocking me?"
```

### 4. Prioritize Ruthlessly
- **high**: Urgent, blocking
- **medium**: Normal work
- **low**: Nice-to-have

### 5. Review Weekly
```bash
paco projects
paco summarize project projectA --archive
```

## Troubleshooting

### "Ollama not found"
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

### "Command not found: paco"
```bash
# Check PATH
echo $PATH | grep paco-bin

# If not found, add to ~/.bashrc:
export PATH="$HOME/paco-bin:$PATH"
export PYTHONPATH="$HOME/paco-bin:$PYTHONPATH"
source ~/.bashrc
```

### AI responses are slow
```bash
# Use a smaller/faster model
ollama pull llama3.2:1b
paco config --set model=llama3.2:1b
```

### Context too large warning
```bash
# Time to archive!
paco summarize project myproject --archive --keep 20
```

## Backup Your Data

```bash
# Simple backup
cp -r ~/paco ~/backups/paco-$(date +%Y%m%d)

# Or use git
cd ~/paco
git init
git add .
git commit -m "Backup"
```

## System Requirements

- **OS**: Linux (Ubuntu, Debian, Arch, etc.)
- **Python**: 3.8+
- **Ollama**: For AI features
- **Disk**: ~500MB for models
- **RAM**: 4GB minimum (8GB recommended)

## Performance

- Add task: <1ms
- Log entry: <1ms
- List tasks: <10ms
- AI query: 1-5 seconds
- **Never slows down** as data grows

## Privacy & Security

- ✅ No internet required (after setup)
- ✅ No cloud services
- ✅ No API keys
- ✅ No data collection
- ✅ All data in `~/paco/`
- ✅ Easy to backup and encrypt

## Architecture

PACO uses:
- **File-based NoSQL** - Plain text files as database
- **NDJSON** for tasks - One JSON object per line
- **Markdown** for logs and notes
- **Bounded context** - AI sees only recent/relevant data
- **Stateless LLM** - No memory between calls

This ensures:
- ⚡ Constant performance
- 🔒 Complete privacy
- 📈 Infinite scalability
- 👁️ Human-readable data

## Why PACO?

### vs. Cloud Assistants (Notion, Asana)
- ✅ Complete privacy
- ✅ Works offline
- ✅ No subscription
- ✅ Your data, your rules

### vs. Other Local Tools
- ✅ AI-powered
- ✅ Infinite scale
- ✅ Human-readable
- ✅ Simple CLI

## License

Use it however you want. It's yours.

---

**Built for humans who want AI help without giving up privacy or control.**

Start with: `paco init`
