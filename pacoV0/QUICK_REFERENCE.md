# PACO Quick Reference

## Installation
```bash
./install.sh
source ~/.bashrc  # or ~/.zshrc
```

## Essential Commands

### Task Management
```bash
# Add task
paco-add-task <project> "<title>" [--priority high|medium|low] [--tags tag1,tag2]

# List projects
paco-list projects

# List tasks
paco-list tasks <project> [--all]

# Complete task
paco-complete <project> <task_id>
```

### Logging & Notes
```bash
# Add project log
paco-log <project> "<message>"

# Add daily note
paco-daily "<message>"
```

### AI Assistant
```bash
# Get task recommendation
paco-next <project>

# Ask question
paco-ask <project> "<question>"

# Summarize project
paco-summarize-project <project> [--archive]

# Summarize day
paco-summarize-day [date]
```

## Common Workflows

### Start Your Day
```bash
paco-next myproject
```

### Capture Progress
```bash
paco-log myproject "Completed feature X"
paco-daily "Key insight about problem Y"
```

### Get Unstuck
```bash
paco-ask myproject "How should I approach this?"
```

### End Your Day
```bash
paco-complete myproject 5
paco-summarize-day
```

### Weekly Cleanup
```bash
paco-summarize-project myproject --archive
```

## File Locations
- **All data**: `~/paco/`
- **Projects**: `~/paco/projects/<project>/`
- **Daily notes**: `~/paco/daily/YYYY-MM-DD.md`
- **Summaries**: `~/paco/daily/summaries/`

## Context Limits (Guardrails)
- **Max tasks in context**: 20
- **Max log lines**: 40
- **Max prompt size**: 15KB
- **Summary size**: 150-400 words

These limits ensure PACO stays fast forever.

## Tips
- Use `--priority high` for urgent/blocking tasks
- Add `--tags` to organize tasks
- Run `--archive` weekly to keep logs lean
- Daily summaries help the AI understand your flow
- All data is plain text - easy to backup/version

## Troubleshooting
```bash
# Check Ollama
ollama list

# Pull model if needed
ollama pull llama3.2

# Check installation
which paco-add-task
echo $PYTHONPATH
```

## Data Backup
```bash
# Everything is in ~/paco
cp -r ~/paco ~/backups/paco-$(date +%Y%m%d)

# Or use git
cd ~/paco && git init && git add . && git commit -m "Backup"
```
