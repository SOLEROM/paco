# Getting Started with PACO

Welcome! Let's get you up and running with PACO in 5 minutes.

## Step 1: Prerequisites (2 minutes)

### Install Ollama
```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the AI model (this might take a few minutes)
ollama pull llama3.2
```

### Verify Python
```bash
# Check Python version (need 3.8+)
python3 --version
```

## Step 2: Install PACO (1 minute)

```bash
# Run the installation script
./install.sh

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc if you use zsh
```

That's it! PACO is now installed.

## Step 3: Your First Project (2 minutes)

Let's create a sample project and see PACO in action:

```bash
# Create your first task
paco-add-task learning "Learn how PACO works" --priority high

# Add a few more tasks
paco-add-task learning "Try the AI features" --priority high
paco-add-task learning "Read the documentation" --priority medium
paco-add-task learning "Customize for my needs" --priority low

# See your tasks
paco-list tasks learning
```

Output will look like:
```
📋 learning - Active Tasks (4):

  HIGH:
    ○ [ID:1] Learn how PACO works
    ○ [ID:2] Try the AI features

  MEDIUM:
    ○ [ID:3] Read the documentation

  LOW:
    ○ [ID:4] Customize for my needs
```

## Step 4: Try the AI (1 minute)

```bash
# Ask the AI what to work on next
paco-next learning
```

The AI will analyze your tasks and recommend what to work on, with reasoning and concrete steps!

## Step 5: Log Your Progress (30 seconds)

```bash
# Add a log entry
paco-log learning "Just finished setting up PACO. Seems intuitive!"

# Write a daily note
paco-daily "Explored a new productivity tool today. Looking promising."

# Mark a task complete
paco-complete learning 1
```

## 🎉 You're Ready!

You now know the basics. Here's what to do next:

### Daily Workflow

**Morning:**
```bash
paco-next myproject  # See what to work on
```

**During work:**
```bash
paco-log myproject "Making progress on feature X"
paco-daily "Had a breakthrough on the architecture"
```

**End of day:**
```bash
paco-complete myproject 5  # Mark tasks done
paco-summarize-day         # Summarize your day
```

### Weekly Maintenance

```bash
# Keep your project summaries fresh
paco-summarize-project myproject --archive
```

## Common Commands

```bash
# Task Management
paco-add-task <project> "<task>" --priority high
paco-list tasks <project>
paco-complete <project> <task-id>

# Logging
paco-log <project> "<note>"
paco-daily "<note>"

# AI Features
paco-next <project>                    # What should I work on?
paco-ask <project> "<question>"        # Ask for advice

# Maintenance
paco-summarize-project <project>       # Compress old logs
paco-summarize-day                     # Summarize today
```

## Tips for Success

### 1. Log Often
Don't wait for "significant" events. Log small wins, blockers, and insights:
```bash
paco-log myproject "Fixed that annoying CSS bug"
paco-log myproject "Stuck on the database query optimization"
```

### 2. Use Daily Notes
Your daily note is your thinking space:
```bash
paco-daily "Realized we need to refactor the auth module"
paco-daily "Client meeting went well, they approved the mockups"
```

### 3. Ask the AI
When stuck, ask for help:
```bash
paco-ask myproject "How should I approach the refactoring?"
paco-ask myproject "What's blocking me from shipping?"
```

### 4. Prioritize Ruthlessly
Use priorities to focus:
- **high**: Urgent, blocking, important
- **medium**: Normal work
- **low**: Nice-to-have, someday

### 5. Review Weekly
Once a week, summarize and clean up:
```bash
paco-list projects
paco-summarize-project projectA --archive
paco-summarize-project projectB --archive
```

## Where's My Data?

Everything lives in `~/paco/`:
```
~/paco/
├── projects/
│   └── learning/
│       ├── tasks.ndjson     # Your tasks
│       ├── log.md           # Your log
│       ├── summary.md       # AI summary
│       └── archive/         # Old logs
└── daily/
    ├── 2025-01-15.md        # Daily notes
    └── summaries/           # Daily summaries
```

All files are plain text - you can read them with any text editor!

## Backup Your Data

```bash
# Simple backup
cp -r ~/paco ~/backups/paco-$(date +%Y%m%d)

# Or use git
cd ~/paco
git init
git add .
git commit -m "Daily backup"
```

## Troubleshooting

### "Ollama not found"
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

### "Command not found: paco-add-task"
```bash
# Make sure PATH is set
echo $PATH | grep paco-bin

# If not, add to ~/.bashrc:
export PATH="$HOME/paco-bin:$PATH"
export PYTHONPATH="$HOME/paco-bin:$PYTHONPATH"

# Then reload
source ~/.bashrc
```

### "No module named 'paco_lib'"
```bash
# Set PYTHONPATH
export PYTHONPATH="$HOME/paco-bin:$PYTHONPATH"

# Add to ~/.bashrc to make permanent
```

### AI responses are slow
This is normal! LLM inference takes a few seconds. For faster responses:
```bash
# Use a smaller model
ollama pull llama3.2:1b
paco-next myproject --model llama3.2:1b
```

## Next Steps

1. **Read the full README**: `cat ~/paco-bin/README.md`
2. **Understand the architecture**: `cat ~/paco-bin/ARCHITECTURE.md`
3. **Try the demo**: `~/paco-bin/demo.sh`
4. **Create your first real project**: Start tracking something you're actually working on!

## Get Help

- Check `README.md` for detailed documentation
- Check `QUICK_REFERENCE.md` for command cheatsheet  
- Check `ARCHITECTURE.md` to understand how it works
- All your data is plain text - just open the files to inspect

## Philosophy

Remember:
- 📝 **Log everything** - small progress counts
- 🤖 **Use the AI** - it's there to help
- 🔒 **Your data is yours** - completely private
- 📅 **Review regularly** - weekly summaries keep you on track
- 🎯 **Focus matters** - priorities help you choose

---

**You're all set! Start with your first real project:**
```bash
paco-add-task myproject "The first real task" --priority high
paco-next myproject
```

Happy productivity! 🚀
