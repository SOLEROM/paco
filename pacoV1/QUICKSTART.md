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

# Logging
paco log <project> "<message>"
paco daily "<note>"

# AI
paco next <project>
paco ask <project> "<question>"

# Maintenance
paco summarize project <project> --archive
paco summarize day

# Config
paco config --list
paco config --set model=llama3.2
```

## File Structure

```
~/paco/
├── config.json          # Settings
├── projects/
│   └── myproject/
│       ├── tasks.ndjson
│       ├── log.md
│       └── summary.md
└── daily/
    └── 2025-01-15.md
```

## Daily Workflow

**Morning:**
```bash
paco next myproject
```

**During work:**
```bash
paco log myproject "Progress update"
paco daily "Key insight"
```

**End of day:**
```bash
paco task done myproject 5
paco summarize day
```

## Tips

1. **Log often** - Small updates count
2. **Use priorities** - high/medium/low
3. **Ask when stuck** - `paco ask`
4. **Review weekly** - Summarize and archive

## Help

- Full docs: `cat README.md`
- Test: `python3 test.py`
- Demo: `./demo.sh`
- Config: `paco config --list`

That's it! Simple, fast, private.
