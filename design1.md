

# **Offline Personal AI Assistant – Master Design Plan**

## 1. Purpose

a **local**, **offline**, **Linux CLI-driven** personal assistant that:

* Knows your tasks, projects, ideas, and progress.
* Helps choose the **next best task**.
* Gives **practical advice** on how to start, debug, or plan.
* Learns context over time without ever reading massive raw logs into the model.
* Runs on your machine, uses your files, and stays private.

---

# **2. High-Level Architecture**

### Components

1. **File-based data store**

   * Human-readable
   * Append-only logs
   * Small summaries for LLM input
   * Zero SQL

2. **Python CLI tools** (your interaction layer):

   * `paco-add-task`
   * `paco-log`
   * `paco-next`
   * `paco-ask`
   * `paco-summarize-project`
   * `paco-summarize-day`

3. **Local LLM backend**

   * `ollama` (preferred)
   * Model: `llama3.2` or similar
   * LLM is stateless; your files hold the memory.

4. **Optional daemon**

   * Only needed later for background summarization or new features.
   * Not required for core functionality.

---

# **3. Filesystem Data Layout (NoSQL memory)**

```
~/paco/
  projects/
    <project-name>/
      tasks.ndjson
      log.md
      summary.md
      index.json
      archive/
        log-YYYY-MM-DD.md
    daily/
      YYYY-MM-DD.md
    Summaries/
        YYYY-MM-DD.summary.md
```

### Purpose of each file

**`tasks.ndjson`**

* One JSON object per task
* Easy to append, easy to parse
* Contains: title, id, status, priority, tags, timestamps

**`log.md`**

* Free-form notes
* Append-only
* Eventually rotated to `archive/`

**`summary.md`**

* LLM-friendly compressed representation of the whole project
* Updated manually or automatically via LLM summarizer
* Always small: ~150–400 words

**`index.json`**

* Optional small metadata reference
* Tracks next task ID, project tags, etc.

**Daily files**

* `daily/YYYY-MM-DD.md`: raw daily brain dump
* `daily/summaries/YYYY-MM-DD.summary.md`: ~5–15 sentence summary

**Archive directory**

* Old logs moved here to keep working folder lightweight

---

# **4. Memory Strategy**

LLM sees **only bounded data**, NOT full files.

### LLM context includes:

* Project’s `summary.md`
* Today’s daily summary
* Top active tasks (extracted from `tasks.ndjson`)
* Only last N lines of `log.md` (e.g., last 20–40 lines)

### NEVER included:

* Full logs
* Full task history
* Full days of notes
* Archive files
* Entire FS dump

This ensures:

* Constant-time prompts
* Constant small context
* Predictable performance
* Files can grow infinitely without LLM slowdown

---

# **5. CLI Commands Overview**

## 5.1 `paco-add-task`

Adds a new task to a project by appending to `tasks.ndjson`.

## 5.2 `paco-log`

Appends a timestamped entry to `log.md` for a project.

## 5.3 `paco-daily`

Writes a free-form note into `daily/YYYY-MM-DD.md`.

## 5.4 `paco-summarize-project`

* Reads old log portion
* Sends to LLM to create/update `summary.md`
* Moves older log parts to `archive/`
* Keeps recent N lines in main `log.md`

## 5.5 `paco-summarize-day`

Creates brief daily summary for LLM based on full daily raw note.

## 5.6 `paco-next`

LLM-consulted “what should I work on now?”:

Uses:

* `summary.md`
* Daily summary
* Recent log tail
* Active tasks slice
  Output:
* 1–3 recommended next tasks
* “why this?”,
* and “three steps to start”.

## 5.7 `paco-ask "question"`

General advice:

Uses:

* Active tasks
* Project summary
* Daily summary
* Recent log tail

LLM answers with guidance.

---

# **6. Context Extraction Rules (Critical)**

To keep the assistant fast:

### Tasks

* Load at most **10–20** active tasks.
* Sort by:

  * priority ↓
  * recently updated ↓

### Logs

* Only include:

  * Last **20–40** lines
  * Never entire file

### Summaries

* Project summary always included.
* Daily summary included if exists.

### Max prompt size

Should stay **under 8–15 KB**.

This ensures stable fast inference once and forever.

---

# **7. Summarization Mechanics**

## 7.1 Project summarization

Triggered by:

* Manual `paco-summarize-project projectX`
* OR automatically when log.md grows > N lines

Summaries contain:

* Project goal
* Recent accomplishments
* Current blockers
* Small list of next steps

## 7.2 Daily summarization

Triggered by:

* `paco-summarize-day`
* Could be a cron job

Summaries contain:

* What you did today
* Key insights
* What should be remembered tomorrow
* Any decisions made

---



# **9. Implementation Roadmap**

## Stage 1: MVP (recommended)

* Implement file layout
* Implement core CLI:

  * add-task
  * log
  * daily
  * next
  * ask
* No daemon
* No rotation
* No automatic summaries
* Basic manual summarization

## Stage 2: Summarization layer

* Add:

  * summarize-project
  * summarize-day
* Add log rotation and archive

## Stage 3: Smartness / indexing

* Project metadata (index.json)
* Task retrieval using tags or keyword matching
* Optional embeddings (offline, small model)

## Stage 4: Daemon

* Automate project+daily summarization
* Trigger summarization on size thresholds
* Provide local API for integrations

---

# **10. Core Principles (Guardrails)**

These rules ensure this system stays fast and sane:

### 10.1 LLM is **never** an archive reader

It only reads:

* Summaries
* Recent logs
* Active tasks

### 10.2 File store can grow unlimited

Archive prevents folders from bloating.

### 10.3 Prompts always small

Final prompt budget must be enforced programmatically.

### 10.4 Human-readable structure

All project data stays in plain Markdown/NDJSON.

### 10.5 CLI always simple

The assistant is a tool, not a world simulation.

---

