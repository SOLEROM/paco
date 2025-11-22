# PACO v2.0 - Daily Notes Refactoring

## What Changed

Daily notes are now **project-specific features** instead of global notes. This dramatically improves AI context and makes PACO more intelligent.

## Why This Is Better

### Before (v1.0)
- Daily notes were global (`~/paco/daily/`)
- Not tied to any project
- AI couldn't use them for project-specific recommendations
- Disconnected from project workflow

### After (v2.0)
- Daily notes live in each project (`~/paco/projects/myproject/daily/`)
- Directly tied to the project
- AI uses them for context when giving recommendations
- Integrated into project workflow

## Key Benefits

### 1. **Smarter AI Recommendations**
When you run `paco next myproject`, the AI now sees:
- Project summary
- **Recent daily notes (last 3 days)** ← NEW!
- Active tasks
- Recent log

This means AI knows:
- Your recent decisions and why
- Insights you've had
- Problems you're thinking about
- Strategic direction

### 2. **Better Context for Summarization**
When you run `paco summarize myproject`, the AI analyzes:
- Project logs
- Tasks
- **Daily notes** ← NEW!

Result: Much richer, more insightful summaries.

### 3. **Clearer Separation of Concerns**
- **Log**: Technical updates, what you did
- **Daily**: Insights, decisions, why you did it

Both feed into AI recommendations, but serve different purposes.

## New Data Structure

```
~/paco/
├── config.json
└── projects/
    └── myproject/
        ├── tasks.ndjson
        ├── log.md              # Technical updates
        ├── summary.md          # AI summary
        ├── daily/              # ← NEW! Project-specific daily notes
        │   ├── 2025-01-15.md
        │   ├── 2025-01-16.md
        │   └── 2025-01-17.md
        ├── index.json
        └── archive/
```

## Updated Commands

### Daily Notes (Changed)
**Before:**
```bash
paco daily "Had a breakthrough"
```

**After:**
```bash
paco daily myproject "Had a breakthrough"
```

Now you specify which project the note belongs to!

### Summarization (Simplified)
**Before:**
```bash
paco summarize project myproject
paco summarize day
```

**After:**
```bash
paco summarize myproject
```

Single command now includes daily notes automatically!

## Usage Examples

### Typical Workflow

```bash
# Morning - get recommendation (AI sees your recent daily notes!)
paco next blog

# Work - log technical progress
paco log blog "Implemented authentication"
paco log blog "Fixed database query bug"

# Work - capture insights and decisions
paco daily blog "Decided to use JWT instead of sessions - simpler"
paco daily blog "Need to refactor auth module - getting too complex"
paco daily blog "Client wants feature X - should we prioritize?"

# AI now has full context when you ask
paco ask blog "Should I refactor now or add features first?"

# Weekly - summarize (includes logs AND daily insights)
paco summarize blog --archive
```

### Log vs Daily: When to Use Each

**Use `paco log` for:**
- Technical updates
- What you did
- Milestones reached
- Deployments
- Bug fixes

**Use `paco daily` for:**
- Insights and learnings
- Decisions and rationale
- Strategic thinking
- Blockers and concerns
- Direction changes

**Both feed into AI**, but daily notes give the "why" while logs give the "what".

## AI Context Building

The AI now builds context like this:

```
## Project Summary (from summary.md)
Project goal, accomplishments, blockers...

## Recent Daily Notes (last 3 days)
## 2025-01-17
[09:30] Decided to use PostgreSQL over MongoDB
[14:00] Realized we need caching layer

## 2025-01-16
[10:00] Client wants real-time feature
[15:00] Need to refactor authentication

## 2025-01-15
...

## Active Tasks (top 20)
- [ID:1] [high] Implement auth
- [ID:2] [medium] Add caching
...

## Recent Log (last 40 lines)
**[2025-01-17 15:30]** Deployed to staging
**[2025-01-17 14:00]** Fixed critical bug
...
```

This gives AI **much richer context** for recommendations!

## Backward Compatibility

⚠️ **Breaking Change**: Old global daily notes won't be automatically migrated.

If you have old daily notes in `~/paco/daily/`, you can:
1. Leave them there (they won't interfere)
2. Manually copy to specific projects if needed
3. Start fresh (recommended for simplicity)

## Migration Guide

If you're upgrading from v1.0:

### Option 1: Start Fresh (Recommended)
Just start using the new syntax:
```bash
paco daily myproject "New note"
```

Old global notes will remain in `~/paco/daily/` but won't be used.

### Option 2: Manual Migration
If you have important daily notes:

```bash
# Copy relevant notes to a project
cp ~/paco/daily/2025-01-15.md ~/paco/projects/myproject/daily/
```

## Summary of Changes

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| Daily notes location | `~/paco/daily/` | `~/paco/projects/X/daily/` |
| Command | `paco daily "note"` | `paco daily project "note"` |
| AI context | No daily notes | Last 3 days of daily notes |
| Summarize command | `paco summarize project X` | `paco summarize X` |
| Summarize includes | Logs + tasks | Logs + tasks + **daily notes** |
| Summarize config | Hard-coded | **Configurable in config.json** |

## New: Configurable Summarization (v1.0+)

You can now control exactly what data the `paco summarize` command analyzes!

### Configuration Parameters

In `~/paco/config.json`:

```json
{
  "summarize_log_lines": -1,        // -1 = all, or specific number
  "summarize_daily_days": 7,        // Last N days, or -1 for all
  "summarize_active_tasks": 10,     // Max active tasks to analyze
  "summarize_completed_tasks": 5    // Max completed tasks to analyze
}
```

### Examples

```bash
# Use ALL data for comprehensive summary
paco config --set summarize_log_lines=-1
paco config --set summarize_daily_days=-1

# Use only recent data for focused summary
paco config --set summarize_log_lines=100
paco config --set summarize_daily_days=3

# Analyze more tasks
paco config --set summarize_active_tasks=20
paco config --set summarize_completed_tasks=10
```

### What `-1` Means

Use `-1` for "no limit" on any parameter:
- `summarize_log_lines: -1` → Analyze entire log file (default)
- `summarize_daily_days: -1` → Analyze all daily notes ever written
- `summarize_active_tasks: -1` → Include all active tasks
- `summarize_completed_tasks: -1` → Include all completed tasks

### When to Use What

**Comprehensive summaries** (recommended for weekly/monthly reviews):
```bash
paco config --set summarize_log_lines=-1
paco config --set summarize_daily_days=-1
paco summarize myproject --archive
```

**Quick summaries** (for faster processing):
```bash
paco config --set summarize_log_lines=200
paco config --set summarize_daily_days=7
paco summarize myproject
```

### See What's Being Analyzed

When you run `paco summarize myproject`, it shows:
```
📝 Summarizing 'myproject'...
  📊 Analyzing:
     • Full log file
     • Last 7 days of daily notes
     • 10 active tasks
     • 5 completed tasks
💭 Generating summary...
```

This transparency helps you know exactly what context the AI is using!

## Why 3 Days of Daily Notes?

The AI sees the last **3 days** of daily notes to balance:
- **Enough context**: Recent decisions and insights
- **Stay bounded**: Keep prompt size small and fast
- **Relevant information**: Recent enough to be actionable

You can change this in the code if needed (`days=3` in `build_context_for_llm`).

## File Size Impact

Daily notes are:
- Small text files (~1-5KB each)
- Only last 3 days loaded into AI context
- Won't affect performance

Even after years of use, performance stays constant!

## Benefits Recap

1. ✅ **Smarter AI** - Sees your insights and decisions
2. ✅ **Better recommendations** - Context-aware suggestions
3. ✅ **Richer summaries** - Includes daily insights
4. ✅ **Clearer workflow** - Log vs daily distinction
5. ✅ **Project-scoped** - Everything about a project in one place
6. ✅ **Still bounded** - Performance stays constant

## Testing

All tests pass! ✅

```bash
python3 test.py
```

8 tests covering:
- Initialization
- Configuration
- Project creation
- Task operations
- Logging
- Daily notes (new project-based structure)
- Context building (includes daily notes)
- Project listing

## Getting Started with v2.0

```bash
# Install
./install.sh
source ~/.bashrc

# Initialize
paco init

# Start using project-based daily notes
paco task add blog "Write post" --priority high
paco log blog "Started research"
paco daily blog "Decided to focus on practical examples"
paco next blog  # AI now sees your daily note!
```

---

**This refactoring makes PACO significantly more intelligent by giving the AI the context it needs to truly understand your projects.**
