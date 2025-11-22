# PACO - Quick Start

## Installation (30 seconds)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# 2. Install PACO
./install.sh
source ~/.bashrc
```

## First Steps (1 minute)

```bash
# Initialize
paco init

# Add your first task
paco task add myproject "Get started" --priority high

# List it
paco task list myproject

# Get AI recommendation
paco next myproject
```

## Essential Commands

```bash
# Tasks
paco task add <project> "<title>" --priority high
paco task list <project>
paco task done <project> <id>

# Logging (technical updates)
paco log <project> "<message>"

# Daily notes (insights & decisions)
paco daily <project> "<note>"

# AI
paco next <project>
paco ask <project> "<question>"

# Maintenance (includes daily notes)
paco summarize <project> --archive

# Config
paco config --list
paco config --set model=llama3.2
```

## File Structure

```
~/paco/
├── config.json          # Settings
└── projects/
    └── myproject/
        ├── tasks.ndjson
        ├── log.md       # Technical updates
        ├── summary.md   # AI-generated
        ├── daily/       # Daily insights
        │   ├── 2025-01-15.md
        │   └── 2025-01-16.md
        └── archive/
```

## Daily Workflow

**Morning:**
```bash
paco next myproject
```

**During work:**
```bash
paco log myproject "Progress update"
paco daily myproject "Key insight or decision"
```

**End of day:**
```bash
paco task done myproject 5
paco daily myproject "Summary of today's work"
```

## Tips

1. **Log vs Daily**: Use `log` for technical updates, `daily` for insights and decisions
2. **Use priorities**: high/medium/low
3. **Daily notes feed AI**: Your insights help AI give better recommendations
4. **Review weekly**: `paco summarize myproject --archive`

Daily notes are now **part of each project** - the AI uses them for context!

## Help

- Full docs: `cat README.md`
- Test: `python3 test.py`
- Demo: `./demo.sh`
- Config: `paco config --list`

That's it! Simple, fast, private.
