# PACO Architecture & Design Decisions

## Core Philosophy

PACO is built on three fundamental principles:

1. **Privacy First**: All data stays local, no cloud dependencies
2. **Bounded Complexity**: Context size stays constant regardless of data growth
3. **Human-Readable**: All data is plain text (Markdown/JSON)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                             │
│  paco-add-task │ paco-log │ paco-next │ paco-ask │ etc.    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Core Library (paco_lib.py)               │
│  • Data operations  • Context building  • LLM interface     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌──────────────┐  ┌──────────┐  ┌─────────────┐
│ File System  │  │  Ollama  │  │  Summaries  │
│   (NoSQL)    │  │  (LLM)   │  │  (Bounded)  │
└──────────────┘  └──────────┘  └─────────────┘
```

## Why NoSQL File-Based Storage?

### Decision: Plain Text Files Instead of Database

**Alternatives Considered:**
- SQLite database
- PostgreSQL/MySQL
- Redis/Key-value store
- JSON document store

**Why Files Won:**

1. **Human-Readable**: `cat ~/paco/projects/myproject/log.md` just works
2. **Git-Friendly**: Automatic version control and diffing
3. **Zero Setup**: No database installation or configuration
4. **Portable**: Copy `~/paco` folder = full backup
5. **Simple**: Append operations are fast and atomic
6. **Inspectable**: Debug by reading the file
7. **No Schema**: Structure can evolve freely

**Trade-offs Accepted:**
- ❌ No ACID transactions (acceptable for personal notes)
- ❌ No complex queries (we don't need them)
- ❌ No concurrent writes (single user, CLI context)

## The Bounded Context Strategy

### The Problem
LLMs have token limits. Reading gigabytes of logs would:
- Be slow (5-10 seconds per query)
- Hit token limits quickly
- Degrade over time as logs grow
- Waste tokens on irrelevant old data

### The Solution: Bounded Context

**What LLM Sees (Always Small):**
```
┌─────────────────────────────────────────┐
│  Project Summary      (~300 words)      │  ←  Compressed knowledge
│  Daily Summary        (~100 words)      │  ←  Recent context
│  Active Tasks         (≤20 tasks)       │  ←  Current priorities
│  Recent Log           (≤40 lines)       │  ←  Latest activity
├─────────────────────────────────────────┤
│  Total: ~8-15KB                         │  ←  Always constant
└─────────────────────────────────────────┘
```

**What LLM Never Sees:**
- Full logs (could be 1000s of lines)
- Archive files
- Completed tasks (unless recently updated)
- Old daily notes

### How It Works

1. **Append-Only Logs**: Fast writes, simple code
2. **Periodic Summarization**: Compress old data with LLM
3. **Archiving**: Move old logs to `archive/` folder
4. **Smart Slicing**: Only load recent/relevant data

### Benefits

- ⚡ **Constant Performance**: Query time never increases
- 💾 **Predictable Memory**: Always ~8-15KB prompts
- 📈 **Infinite Scale**: Can log for years without slowdown
- 🎯 **Better Results**: LLM focuses on relevant info

## Data Flow

### Write Path (Logging)
```
User Command
    ↓
CLI Tool
    ↓
paco_lib.append_to_log()
    ↓
Append to log.md (atomic operation)
    ↓
Done (< 1ms)
```

### Read Path (AI Query)
```
User Command (paco-next/paco-ask)
    ↓
paco_lib.build_context_for_llm()
    ↓
├─ Read summary.md (latest summary)
├─ Read daily summary (today)
├─ Load 20 active tasks (sorted by priority)
└─ Read last 40 log lines
    ↓
Build prompt (enforce <15KB limit)
    ↓
Call Ollama (local LLM)
    ↓
Return formatted response
```

### Summarization Path
```
User: paco-summarize-project myproject --archive
    ↓
Read full log.md + all tasks
    ↓
Send to LLM: "Summarize this project"
    ↓
LLM generates 150-400 word summary
    ↓
Write to summary.md
    ↓
Split log.md: archive old → keep recent 40 lines
    ↓
Move old lines to archive/log-YYYY-MM-DD.md
```

## File Format Decisions

### Why NDJSON for Tasks?
**Format**: Newline-Delimited JSON (one JSON object per line)

```json
{"id":1,"title":"Task 1","status":"active","priority":"high",...}
{"id":2,"title":"Task 2","status":"active","priority":"medium",...}
{"id":3,"title":"Task 3","status":"completed","priority":"low",...}
```

**Advantages:**
- ✅ Append-only: Add new task = append one line
- ✅ Easy to parse: Read line by line
- ✅ Efficient updates: Rewrite entire file is fine (small)
- ✅ Human-readable: Can inspect with `cat` or any editor
- ✅ Structured: Unlike free-form text, but simpler than SQL

**Why Not SQLite?**
- We don't need complex queries
- Files are more portable
- Easier to inspect and debug

### Why Markdown for Logs?
**Advantages:**
- ✅ Human-readable
- ✅ Supports formatting (bold, lists, code blocks)
- ✅ Works in any text editor
- ✅ Git shows nice diffs
- ✅ Can be rendered as HTML if needed

**Timestamp Format:**
```markdown
**[2025-01-15 14:30]** Fixed the authentication bug

**[2025-01-15 16:45]** Deployed to staging environment
```

## LLM Integration Design

### Why Ollama?
**Alternatives Considered:**
- OpenAI API (requires internet + API key)
- llama.cpp directly (more complex setup)
- LocalAI (similar to Ollama)
- Hugging Face Transformers (heavier dependencies)

**Why Ollama Won:**
1. **Easy Setup**: `curl | sh` + `ollama pull model`
2. **Local**: No internet required after model download
3. **Fast**: Optimized inference
4. **Simple API**: Just pipe text via stdin
5. **Model Management**: Easy to switch models
6. **Active Development**: Well maintained

### Stateless LLM Design

**Key Decision**: LLM has no memory between calls

```python
# Each call is independent
def call_ollama(prompt, model):
    result = subprocess.run(["ollama", "run", model], 
                          input=prompt, 
                          capture_output=True)
    return result.stdout
```

**Why Stateless?**
- ✅ Simple: No session management
- ✅ Predictable: Same context = same results
- ✅ Testable: Easy to reproduce issues
- ✅ Reliable: No memory leaks or state corruption

**How Context is Maintained:**
- All context comes from files
- Files are the source of truth
- Summaries provide compressed history

## Guardrails Implementation

### Hard Limits (Enforced in Code)

```python
# paco_lib.py
MAX_TASKS_IN_CONTEXT = 20
MAX_LOG_LINES_IN_CONTEXT = 40
MAX_PROMPT_SIZE_KB = 15
```

### Why These Numbers?

**20 Tasks:**
- Average: 50-100 bytes per task
- Total: ~2KB maximum
- Rationale: Enough to see priorities, not overwhelming

**40 Log Lines:**
- Average: 80 bytes per line
- Total: ~3KB maximum
- Rationale: Captures last day or two of activity

**15KB Total:**
- Fits comfortably in smallest LLMs
- Leaves room for system prompts
- Fast inference (<2s on modest hardware)

### Enforcement

```python
def check_prompt_size(prompt: str) -> Tuple[bool, float]:
    """Check if prompt is within limits"""
    size_kb = len(prompt.encode('utf-8')) / 1024
    return size_kb <= MAX_PROMPT_SIZE_KB, size_kb
```

Warning printed if exceeded, but not blocked (user can judge).

## Summarization Algorithm

### Project Summarization

**Input:**
- Full log history
- All tasks (active + completed)
- Previous summary (if exists)

**LLM Prompt:**
```
Generate a concise project summary (150-400 words) that includes:
1. Project goal/purpose
2. Recent accomplishments
3. Current blockers
4. Key next steps

[Full context here...]
```

**Output:**
- Markdown file (~300 words)
- Saved as `summary.md`

**Then:**
- Archive old log entries
- Keep only recent 40 lines in main log

### Daily Summarization

**Input:**
- Today's full daily note (could be 1000s of words)

**LLM Prompt:**
```
Create a brief daily summary (5-15 sentences):
1. What was done today
2. Key insights
3. What to remember tomorrow
4. Decisions made

[Today's notes...]
```

**Output:**
- Brief summary (~100 words)
- Saved as `daily/summaries/YYYY-MM-DD.summary.md`

## Scalability Analysis

### Linear Scaling Operations
- ✅ Add task: O(1) - append one line
- ✅ Log entry: O(1) - append to file
- ✅ Daily note: O(1) - append to file

### Constant Scaling (AI Queries)
- ✅ paco-next: O(1) - always reads same amount
- ✅ paco-ask: O(1) - bounded context

### Occasional Operations
- 📅 Summarize project: O(n) - but infrequent (weekly)
- 📅 Summarize day: O(n) - but n is one day (small)

### Long-Term Behavior

**After 1 Year:**
- Tasks: ~500 tasks (20KB NDJSON file)
- Log: Archived, main file stays 40 lines
- Daily notes: 365 files, ~1MB total
- Summaries: ~365 daily + ~52 project = ~1MB

**Performance Impact**: NONE
- AI queries still read ~15KB
- File operations stay fast (small working set)
- Archives don't slow anything down (not accessed)

## Security & Privacy

### Threat Model

**Protected Against:**
- ✅ Cloud data leaks (no cloud)
- ✅ API key theft (no APIs)
- ✅ Third-party tracking (no network)
- ✅ Data mining (local only)

**Not Protected Against:**
- ❌ Local malware (OS-level issue)
- ❌ Physical access (use disk encryption)
- ❌ Backup leaks (user responsibility)

### Best Practices

1. **Encrypt your disk**: Use LUKS/FileVault/BitLocker
2. **Backup securely**: Encrypted external drive
3. **Version control**: Use git with private repo
4. **File permissions**: Default `chmod 600` on sensitive files

## Future Architecture Considerations

### Stage 3: Semantic Search (Optional)

**If Implemented:**
```
Generate embeddings for each log entry
    ↓
Store in local vector DB (e.g., FAISS)
    ↓
Query: Find similar past experiences
    ↓
Enhance context with relevant past entries
```

**Impact on Bounded Context:**
- Still maintain 15KB limit
- But context is more relevant (not just recent)

### Stage 4: Daemon (Optional)

**If Implemented:**
```
Background daemon watches for:
- log.md growing >500 lines → auto-summarize
- Daily notes → auto-summarize at midnight
- New completed tasks → update summary
```

**Architecture:**
```
systemd service
    ↓
Watch filesystem (inotify)
    ↓
Trigger CLI tools when thresholds hit
```

**Why Not Yet:**
- MVP doesn't need it
- Adds complexity
- Manual summarization is fine

## Design Trade-offs Summary

| Decision | Chosen | Alternative | Why |
|----------|--------|-------------|-----|
| Storage | Files | Database | Human-readable, portable |
| Format | Markdown/NDJSON | Binary/SQL | Inspectable, git-friendly |
| LLM | Ollama | Cloud API | Privacy, offline |
| Context | Bounded | Full history | Speed, scalability |
| Interface | CLI | GUI/Web | Simple, scriptable |
| Memory | Stateless | Stateful | Reliable, predictable |

## Key Insights

1. **Files as Database**: With good structure, files are sufficient
2. **Summaries Scale**: Compress old data, keep recent data fresh
3. **Bounded Context**: The secret to infinite scalability
4. **Local LLMs**: Now good enough for personal assistant tasks
5. **Privacy ≠ Compromise**: Local can be as good as cloud

---

**The result**: A personal assistant that's private, fast, and scales forever.
