#!/usr/bin/env python3
"""
PACO - Personal AI Assistant, Contextual and Offline
Core library with data structures and helper functions
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import subprocess

# Constants
PACO_DIR = Path.home() / "paco"
PROJECTS_DIR = PACO_DIR / "projects"
DAILY_DIR = PACO_DIR / "daily"
DAILY_SUMMARIES_DIR = DAILY_DIR / "summaries"

# Context limits (guardrails)
MAX_TASKS_IN_CONTEXT = 20
MAX_LOG_LINES_IN_CONTEXT = 40
MAX_PROMPT_SIZE_KB = 15

# LLM settings
DEFAULT_MODEL = "llama3.2"


def init_paco_dirs():
    """Initialize PACO directory structure"""
    PACO_DIR.mkdir(exist_ok=True)
    PROJECTS_DIR.mkdir(exist_ok=True)
    DAILY_DIR.mkdir(exist_ok=True)
    DAILY_SUMMARIES_DIR.mkdir(exist_ok=True)


def get_project_dir(project_name: str) -> Path:
    """Get project directory path"""
    return PROJECTS_DIR / project_name


def init_project(project_name: str):
    """Initialize a new project directory structure"""
    project_dir = get_project_dir(project_name)
    project_dir.mkdir(exist_ok=True)
    (project_dir / "archive").mkdir(exist_ok=True)
    
    # Create empty files if they don't exist
    tasks_file = project_dir / "tasks.ndjson"
    if not tasks_file.exists():
        tasks_file.touch()
    
    log_file = project_dir / "log.md"
    if not log_file.exists():
        log_file.write_text(f"# {project_name} - Log\n\n")
    
    summary_file = project_dir / "summary.md"
    if not summary_file.exists():
        summary_file.write_text(f"# {project_name} - Summary\n\nProject initialized.\n")
    
    index_file = project_dir / "index.json"
    if not index_file.exists():
        index_data = {
            "project_name": project_name,
            "created": datetime.now().isoformat(),
            "next_task_id": 1,
            "tags": []
        }
        index_file.write_text(json.dumps(index_data, indent=2))


def list_projects() -> List[str]:
    """List all existing projects"""
    if not PROJECTS_DIR.exists():
        return []
    return [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]


def get_next_task_id(project_name: str) -> int:
    """Get next task ID for a project"""
    index_file = get_project_dir(project_name) / "index.json"
    if index_file.exists():
        data = json.loads(index_file.read_text())
        task_id = data.get("next_task_id", 1)
        data["next_task_id"] = task_id + 1
        index_file.write_text(json.dumps(data, indent=2))
        return task_id
    return 1


def add_task(project_name: str, title: str, priority: str = "medium", 
             tags: Optional[List[str]] = None) -> Dict:
    """Add a task to project's tasks.ndjson"""
    init_project(project_name)
    
    task = {
        "id": get_next_task_id(project_name),
        "title": title,
        "status": "active",
        "priority": priority,
        "tags": tags or [],
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    
    tasks_file = get_project_dir(project_name) / "tasks.ndjson"
    with tasks_file.open("a") as f:
        f.write(json.dumps(task) + "\n")
    
    return task


def load_tasks(project_name: str, status_filter: Optional[str] = "active") -> List[Dict]:
    """Load tasks from tasks.ndjson, optionally filtered by status"""
    tasks_file = get_project_dir(project_name) / "tasks.ndjson"
    if not tasks_file.exists():
        return []
    
    tasks = []
    for line in tasks_file.read_text().strip().split("\n"):
        if line:
            task = json.loads(line)
            if status_filter is None or task.get("status") == status_filter:
                tasks.append(task)
    
    return tasks


def update_task_status(project_name: str, task_id: int, new_status: str):
    """Update task status by rewriting tasks.ndjson"""
    tasks_file = get_project_dir(project_name) / "tasks.ndjson"
    if not tasks_file.exists():
        return
    
    tasks = []
    for line in tasks_file.read_text().strip().split("\n"):
        if line:
            task = json.loads(line)
            if task["id"] == task_id:
                task["status"] = new_status
                task["updated"] = datetime.now().isoformat()
            tasks.append(task)
    
    with tasks_file.open("w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")


def append_to_log(project_name: str, message: str):
    """Append timestamped entry to project log"""
    init_project(project_name)
    log_file = get_project_dir(project_name) / "log.md"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"**[{timestamp}]** {message}\n\n"
    
    with log_file.open("a") as f:
        f.write(entry)


def get_log_tail(project_name: str, max_lines: int = MAX_LOG_LINES_IN_CONTEXT) -> str:
    """Get last N lines from project log"""
    log_file = get_project_dir(project_name) / "log.md"
    if not log_file.exists():
        return ""
    
    lines = log_file.read_text().strip().split("\n")
    return "\n".join(lines[-max_lines:])


def get_project_summary(project_name: str) -> str:
    """Get project summary"""
    summary_file = get_project_dir(project_name) / "summary.md"
    if not summary_file.exists():
        return f"No summary yet for {project_name}"
    return summary_file.read_text()


def write_daily_note(note: str):
    """Write to today's daily note"""
    init_paco_dirs()
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = DAILY_DIR / f"{today}.md"
    
    timestamp = datetime.now().strftime("%H:%M")
    entry = f"**[{timestamp}]** {note}\n\n"
    
    with daily_file.open("a") as f:
        f.write(entry)


def get_daily_note(date: Optional[str] = None) -> str:
    """Get daily note for a specific date (default: today)"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    daily_file = DAILY_DIR / f"{date}.md"
    if not daily_file.exists():
        return ""
    return daily_file.read_text()


def get_daily_summary(date: Optional[str] = None) -> str:
    """Get daily summary for a specific date (default: today)"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    summary_file = DAILY_SUMMARIES_DIR / f"{date}.summary.md"
    if not summary_file.exists():
        return ""
    return summary_file.read_text()


def build_context_for_llm(project_name: str) -> str:
    """
    Build bounded context for LLM following guardrails:
    - Project summary
    - Today's daily summary
    - Top active tasks (max MAX_TASKS_IN_CONTEXT)
    - Recent log tail (max MAX_LOG_LINES_IN_CONTEXT lines)
    """
    context_parts = []
    
    # Project summary
    context_parts.append("## Project Summary\n")
    context_parts.append(get_project_summary(project_name))
    context_parts.append("\n")
    
    # Daily summary
    daily_summary = get_daily_summary()
    if daily_summary:
        context_parts.append("## Today's Summary\n")
        context_parts.append(daily_summary)
        context_parts.append("\n")
    
    # Active tasks (limited)
    tasks = load_tasks(project_name, status_filter="active")
    # Sort by priority then by updated time
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 1), 
                              t.get("updated", "")), 
               reverse=True)
    tasks = tasks[:MAX_TASKS_IN_CONTEXT]
    
    if tasks:
        context_parts.append("## Active Tasks\n")
        for task in tasks:
            context_parts.append(f"- [ID:{task['id']}] [{task.get('priority', 'medium')}] {task['title']}\n")
        context_parts.append("\n")
    
    # Recent log tail
    log_tail = get_log_tail(project_name)
    if log_tail:
        context_parts.append("## Recent Log\n")
        context_parts.append(log_tail)
        context_parts.append("\n")
    
    return "".join(context_parts)


def call_ollama(prompt: str, model: str = DEFAULT_MODEL, system_prompt: Optional[str] = None) -> str:
    """
    Call local Ollama LLM
    Returns the response text
    """
    try:
        # Build the ollama command
        cmd = ["ollama", "run", model]
        
        # Construct full prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Run ollama
        result = subprocess.run(
            cmd,
            input=full_prompt,
            text=True,
            capture_output=True,
            timeout=120
        )
        
        if result.returncode != 0:
            return f"Error calling Ollama: {result.stderr}"
        
        return result.stdout.strip()
    
    except FileNotFoundError:
        return "Error: Ollama not found. Please install ollama first."
    except subprocess.TimeoutExpired:
        return "Error: LLM request timed out."
    except Exception as e:
        return f"Error: {str(e)}"


def estimate_prompt_size_kb(text: str) -> float:
    """Estimate prompt size in KB"""
    return len(text.encode('utf-8')) / 1024


def check_prompt_size(prompt: str) -> Tuple[bool, float]:
    """Check if prompt is within size limits"""
    size_kb = estimate_prompt_size_kb(prompt)
    return size_kb <= MAX_PROMPT_SIZE_KB, size_kb
