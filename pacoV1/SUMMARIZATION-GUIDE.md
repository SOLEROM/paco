# PACO v1.0 - Configurable Summarization

## 📋 Summary of What `paco summarize` Uses

When you run:
```bash
paco summarize myproject
```

The command analyzes these sources **based on your config settings**:

### Data Sources (All Configurable!)

| Source | Config Parameter | Default | What It Means |
|--------|-----------------|---------|---------------|
| **Log entries** | `summarize_log_lines` | `-1` | All log entries |
| **Daily notes** | `summarize_daily_days` | `7` | Last 7 days |
| **Active tasks** | `summarize_active_tasks` | `10` | Up to 10 tasks |
| **Completed tasks** | `summarize_completed_tasks` | `5` | Last 5 tasks |

**Special value `-1` = "no limit" - use all available data**

---

## ⚙️ Configuration

Edit these in `~/paco/config.json` or via CLI:

```bash
# View current settings
paco config --list

# Set specific values
paco config --set summarize_log_lines=200    # Last 200 lines
paco config --set summarize_daily_days=14    # Last 2 weeks
paco config --set summarize_log_lines=-1     # ALL entries

# No limits - comprehensive analysis
paco config --set summarize_log_lines=-1
paco config --set summarize_daily_days=-1
paco config --set summarize_active_tasks=-1
paco config --set summarize_completed_tasks=-1
```

---

## 💡 When You Summarize

The command shows exactly what it's analyzing:

```bash
$ paco summarize myproject

📝 Summarizing 'myproject'...
  📊 Analyzing:
     • Full log file                    ← summarize_log_lines: -1
     • Last 7 days of daily notes       ← summarize_daily_days: 7
     • 10 active tasks                  ← summarize_active_tasks: 10
     • 5 completed tasks                ← summarize_completed_tasks: 5
💭 Generating summary...
✓ Summary updated: ~/paco/projects/myproject/summary.md
```

**You always know what data the AI is using!**

---

## 🎯 Use Cases

### Comprehensive Monthly Review
```bash
# Analyze EVERYTHING
paco config --set summarize_log_lines=-1
paco config --set summarize_daily_days=-1
paco config --set summarize_active_tasks=-1
paco config --set summarize_completed_tasks=-1

paco summarize myproject --archive
```

### Quick Weekly Summary
```bash
# Focus on recent data
paco config --set summarize_log_lines=300
paco config --set summarize_daily_days=7
paco config --set summarize_active_tasks=10
paco config --set summarize_completed_tasks=5

paco summarize myproject
```

### Fast Summary (Large Projects)
```bash
# Minimum data for speed
paco config --set summarize_log_lines=100
paco config --set summarize_daily_days=3
paco config --set summarize_active_tasks=5
paco config --set summarize_completed_tasks=3

paco summarize myproject
```

---

## 🔄 How It Works

### 1. Config-Based Data Retrieval

The summarization reads from config:
```python
# From config.json
summarize_log_lines = -1        # Use all logs
summarize_daily_days = 7        # Last week
```

### 2. Data Collection

Based on config, PACO collects:
- Log: Entire file OR last N lines
- Daily: All notes OR last N days
- Tasks: Limited by config OR unlimited (-1)

### 3. AI Analysis

All collected data goes to the AI for analysis.

### 4. Summary Generation

AI creates 150-400 word summary including:
- Project goals
- Recent accomplishments
- Current blockers
- Key insights from daily notes
- Next steps

---

## 📊 Default Configuration

```json
{
  "model": "llama3.2",
  "max_tasks": 20,              // For paco next/ask (bounded context)
  "max_log_lines": 40,          // For paco next/ask (bounded context)
  "max_prompt_kb": 15,          // For paco next/ask (bounded context)
  "summarize_log_lines": -1,    // For paco summarize (comprehensive)
  "summarize_daily_days": 7,    // For paco summarize
  "summarize_active_tasks": 10, // For paco summarize
  "summarize_completed_tasks": 5 // For paco summarize
}
```

**Note the difference:**
- `max_*` settings = Bounded context for **daily queries** (fast!)
- `summarize_*` settings = What to analyze for **summaries** (comprehensive!)

---

## 🎓 Understanding the Two Contexts

### Daily AI Queries (`paco next`, `paco ask`)
**Goal:** Fast, focused recommendations
**Uses:** Bounded context (summary + recent data)
**Config:** `max_tasks`, `max_log_lines`, `max_prompt_kb`

### Summarization (`paco summarize`)
**Goal:** Comprehensive understanding to create summary
**Uses:** Configurable comprehensive data
**Config:** `summarize_*` parameters

**The cycle:**
```
Full Data → [Summarize with config] → Compact Summary
                                            ↓
                                    Used in daily queries
                                    (bounded, fast)
```

---

## 🔧 Advanced Examples

### Progressive Detail Levels

**Level 1: Quick overview**
```bash
paco config --set summarize_log_lines=50
paco config --set summarize_daily_days=3
paco summarize myproject
```

**Level 2: Standard weekly**
```bash
paco config --set summarize_log_lines=200
paco config --set summarize_daily_days=7
paco summarize myproject
```

**Level 3: Deep monthly**
```bash
paco config --set summarize_log_lines=-1
paco config --set summarize_daily_days=30
paco summarize myproject --archive
```

**Level 4: Complete analysis**
```bash
paco config --set summarize_log_lines=-1
paco config --set summarize_daily_days=-1
paco config --set summarize_active_tasks=-1
paco config --set summarize_completed_tasks=-1
paco summarize myproject --archive
```

### Project-Specific Strategies

**Small project (< 100 log entries):**
```bash
# Analyze everything - it's not much data
paco config --set summarize_log_lines=-1
```

**Large project (1000+ log entries):**
```bash
# Focus on recent - or wait longer for full analysis
paco config --set summarize_log_lines=500
```

**Active project (daily updates):**
```bash
# Recent data is most relevant
paco config --set summarize_daily_days=7
```

**Mature project (infrequent updates):**
```bash
# Include more history for context
paco config --set summarize_daily_days=30
```

---

## ✅ Verification

Test your config:
```bash
# Check current settings
paco config --list

# Change a setting
paco config --set summarize_daily_days=14

# Verify it changed
paco config --get summarize_daily_days

# Run summarize and see what it analyzes
paco summarize myproject
# Look for: "📊 Analyzing: • Last 14 days of daily notes"
```

---

## 📝 Summary

**Key Points:**
1. ✅ All summarization data sources are **configurable**
2. ✅ Use `-1` for "no limit" on any parameter
3. ✅ The command **shows what it's analyzing** before starting
4. ✅ Separate configs for daily queries vs summarization
5. ✅ Balance speed vs comprehensiveness as needed

**You're now in full control of what PACO analyzes when creating summaries!**
