#!/usr/bin/env python3
"""
PACO - Personal AI Assistant, Contextual and Offline
Core library with data structures and helper functions
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Constants
PACO_DIR = Path.home() / "paco"
PROJECTS_DIR = PACO_DIR / "projects"
CONFIG_FILE = PACO_DIR / "config.json"

# Context limits (guardrails)
MAX_TASKS_IN_CONTEXT = 20
MAX_LOG_LINES_IN_CONTEXT = 40
MAX_PROMPT_SIZE_KB = 15

# Default settings
DEFAULT_CONFIG = {
    "model": "llama3.2",
    "max_tasks": MAX_TASKS_IN_CONTEXT,
    "max_log_lines": MAX_LOG_LINES_IN_CONTEXT,
    "max_prompt_kb": MAX_PROMPT_SIZE_KB
}


def init_paco_dirs():
    """Initialize PACO directory structure"""
    PACO_DIR.mkdir(exist_ok=True)
    PROJECTS_DIR.mkdir(exist_ok=True)
    
    # Create default config if it doesn't exist
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)


def load_config() -> Dict:
    """Load configuration from config file"""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    try:
        return json.loads(CONFIG_FILE.read_text())
    except:
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict):
    """Save configuration to config file"""
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def get_config_value(key: str, default=None):
    """Get a single config value"""
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value):
    """Set a single config value"""
    config = load_config()
    config[key] = value
    save_config(config)


def get_project_dir(project_name: str) -> Path:
    """Get project directory path"""
    return PROJECTS_DIR / project_name


def init_project(project_name: str):
    """Initialize a new project directory structure"""
    project_dir = get_project_dir(project_name)
    project_dir.mkdir(exist_ok=True)
    (project_dir / "archive").mkdir(exist_ok=True)
    (project_dir / "daily").mkdir(exist_ok=True)
    
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
    return sorted([d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()])


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


def get_log_tail(project_name: str, max_lines: Optional[int] = None) -> str:
    """Get last N lines from project log"""
    if max_lines is None:
        max_lines = get_config_value("max_log_lines", MAX_LOG_LINES_IN_CONTEXT)
    
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


def write_daily_note(project_name: str, note: str):
    """Write to project's daily note for today"""
    init_project(project_name)
    today = datetime.now().strftime("%Y-%m-%d")
    daily_dir = get_project_dir(project_name) / "daily"
    daily_dir.mkdir(exist_ok=True)
    daily_file = daily_dir / f"{today}.md"
    
    timestamp = datetime.now().strftime("%H:%M")
    entry = f"**[{timestamp}]** {note}\n\n"
    
    with daily_file.open("a") as f:
        f.write(entry)


def get_daily_note(project_name: str, date: Optional[str] = None) -> str:
    """Get daily note for a project and specific date (default: today)"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    daily_file = get_project_dir(project_name) / "daily" / f"{date}.md"
    if not daily_file.exists():
        return ""
    return daily_file.read_text()


def get_recent_daily_notes(project_name: str, days: int = 7) -> str:
    """Get recent daily notes for a project (last N days)"""
    daily_dir = get_project_dir(project_name) / "daily"
    if not daily_dir.exists():
        return ""
    
    # Get all daily note files, sorted by date
    daily_files = sorted(daily_dir.glob("*.md"), reverse=True)
    
    recent_notes = []
    for daily_file in daily_files[:days]:
        date = daily_file.stem
        content = daily_file.read_text().strip()
        if content:
            recent_notes.append(f"## {date}\n{content}\n")
    
    return "\n".join(recent_notes)


def build_context_for_llm(project_name: str) -> str:
    """
    Build bounded context for LLM following guardrails:
    - Project summary
    - Recent daily notes (last 3 days)
    - Top active tasks (max MAX_TASKS_IN_CONTEXT)
    - Recent log tail (max MAX_LOG_LINES_IN_CONTEXT lines)
    """
    config = load_config()
    max_tasks = config.get("max_tasks", MAX_TASKS_IN_CONTEXT)
    
    context_parts = []
    
    # Project summary
    context_parts.append("## Project Summary\n")
    context_parts.append(get_project_summary(project_name))
    context_parts.append("\n")
    
    # Recent daily notes (last 3 days)
    recent_daily = get_recent_daily_notes(project_name, days=3)
    if recent_daily:
        context_parts.append("## Recent Daily Notes\n")
        context_parts.append(recent_daily)
        context_parts.append("\n")
    
    # Active tasks (limited)
    tasks = load_tasks(project_name, status_filter="active")
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 1), 
                              t.get("updated", "")), 
               reverse=True)
    tasks = tasks[:max_tasks]
    
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


def call_ollama(prompt: str, model: Optional[str] = None, system_prompt: Optional[str] = None) -> str:
    """Call local Ollama LLM"""
    if model is None:
        model = get_config_value("model", "llama3.2")
    
    try:
        cmd = ["ollama", "run", model]
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
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
    max_size = get_config_value("max_prompt_kb", MAX_PROMPT_SIZE_KB)
    size_kb = estimate_prompt_size_kb(prompt)
    return size_kb <= max_size, size_kb
