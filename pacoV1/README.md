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

# Add daily note to project
paco daily <project> "<message>"

# Examples
paco log blog "Finished the introduction section"
paco daily blog "Had a breakthrough on the architecture"
paco daily blog "Decided to use PostgreSQL instead of MongoDB"
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
# Summarize project (includes daily notes, compresses old logs)
paco summarize <project> [--archive] [--keep N]

# Examples
paco summarize blog --archive
paco summarize myproject --keep 30
```

The summarize command now:
- Analyzes project logs, tasks, AND daily notes
- Generates intelligent summary with context from daily notes
- Optionally archives old logs

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
└── projects/
    └── myproject/
        ├── tasks.ndjson     # Tasks (one JSON per line)
        ├── log.md           # Activity log
        ├── summary.md       # AI-generated summary
        ├── index.json       # Project metadata
        ├── daily/           # Daily notes for this project
        │   ├── 2025-01-15.md
        │   └── 2025-01-16.md
        └── archive/         # Old archived logs
```

All files are plain text - inspect them anytime!

## How It Works: Bounded Context

PACO uses a **bounded context** approach to stay fast forever:

**What the AI sees (always small):**
- Project summary (~300 words)
- Recent daily notes (last 3 days)
- Top 20 active tasks
- Last 40 lines of log

**What the AI never sees:**
- Full logs (could be thousands of lines)
- Archive files
- Old daily notes (only last 3 days)
- Completed tasks

**Result:** Constant-time queries, infinite scalability.

**Key Innovation:** Daily notes are now **project-specific**, so the AI gets rich context about each project's recent activities and insights when making recommendations.

## Typical Workflows

### Morning Routine
```bash
paco next myproject          # What should I work on?
```

### During Work
```bash
paco log myproject "Fixed authentication bug"
paco daily myproject "Key insight: use JWT tokens instead of sessions"
paco task add myproject "Add rate limiting" --priority high
```

### End of Day
```bash
paco task done myproject 5   # Mark tasks complete
paco daily myproject "Summary: Completed auth module, next is API endpoints"
```

### Weekly Maintenance
```bash
# Summarize project (AI will analyze logs AND daily notes)
paco summarize myproject --archive
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

# Work on it - use log for technical updates
paco log blog "Found 5 good sources"
paco log blog "Outlined the structure"

# Use daily for insights and decisions
paco daily blog "Decided to focus on practical examples rather than theory"
paco daily blog "Realized the introduction needs to hook readers better"

# Ask for help
paco ask blog "How should I approach the introduction?"

# Get recommendation (AI sees your daily insights!)
paco next blog

# Complete task
paco task done blog 1

# Weekly: Summarize everything (includes daily notes context)
paco summarize blog --archive
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
| `paco log` | Add log entry (for technical updates) |
| `paco daily` | Add daily note (for insights & decisions) |
| `paco next` | Get AI recommendation |
| `paco ask` | Ask AI a question |
| `paco summarize` | Analyze logs + daily notes, compress |

## Tips

### 1. Use Log vs Daily Appropriately
**Log** for technical updates:
```bash
paco log myproject "Fixed CSS bug"
paco log myproject "Deployed to staging"
```

**Daily** for insights, decisions, and reflection:
```bash
paco daily myproject "Need to refactor auth module - too complex"
paco daily myproject "Client wants feature X - should we prioritize it?"
paco daily myproject "Learned that async approach won't work here"
```

### 2. Daily Notes Power the AI
Your daily notes give the AI crucial context:
- Past decisions and why they were made
- Learnings and insights
- Blockers and how you think about them
- Direction and strategy

### 3. Use Daily Notes Liberally
Don't wait for big events:
```bash
paco daily myproject "Quick thought: might need caching here"
paco daily myproject "Stuck on database query - need different approach"
```

### 4. Prioritize Ruthlessly
- **high**: Urgent, blocking
- **medium**: Normal work
- **low**: Nice-to-have

### 5. Review Weekly
```bash
paco projects
paco summarize projectA --archive
```

The summary will synthesize logs AND daily notes into actionable insights.

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
