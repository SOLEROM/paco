#!/usr/bin/env python3
"""
PACO Test Suite
Run this to verify all core functionality works
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paco_lib


class TestPACO:
    """Test suite for PACO functionality"""
    
    def __init__(self):
        self.test_dir = None
        self.original_paco_dir = None
        self.tests_passed = 0
        self.tests_failed = 0
    
    def setup(self):
        """Set up test environment"""
        print("🔧 Setting up test environment...")
        
        # Create temporary test directory
        self.test_dir = Path(tempfile.mkdtemp(prefix="paco_test_"))
        
        # Override PACO directories for testing
        self.original_paco_dir = paco_lib.PACO_DIR
        paco_lib.PACO_DIR = self.test_dir
        paco_lib.PROJECTS_DIR = self.test_dir / "projects"
        paco_lib.DAILY_DIR = self.test_dir / "daily"
        paco_lib.DAILY_SUMMARIES_DIR = self.test_dir / "daily" / "summaries"
        
        print(f"  Test directory: {self.test_dir}")
        print()
    
    def teardown(self):
        """Clean up test environment"""
        print("\n🧹 Cleaning up...")
        
        # Restore original
        paco_lib.PACO_DIR = self.original_paco_dir
        
        # Remove test directory
        if self.test_dir and self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            print(f"  Removed: {self.test_dir}")
    
    def assert_true(self, condition, test_name):
        """Assert a condition is true"""
        if condition:
            print(f"  ✅ {test_name}")
            self.tests_passed += 1
        else:
            print(f"  ❌ {test_name}")
            self.tests_failed += 1
    
    def test_initialization(self):
        """Test directory initialization"""
        print("📁 Testing initialization...")
        
        paco_lib.init_paco_dirs()
        
        self.assert_true(
            paco_lib.PACO_DIR.exists(),
            "PACO directory created"
        )
        self.assert_true(
            paco_lib.PROJECTS_DIR.exists(),
            "Projects directory created"
        )
        self.assert_true(
            paco_lib.DAILY_DIR.exists(),
            "Daily directory created"
        )
        self.assert_true(
            paco_lib.DAILY_SUMMARIES_DIR.exists(),
            "Daily summaries directory created"
        )
        print()
    
    def test_project_creation(self):
        """Test project initialization"""
        print("🆕 Testing project creation...")
        
        project_name = "test-project"
        paco_lib.init_project(project_name)
        
        project_dir = paco_lib.get_project_dir(project_name)
        
        self.assert_true(
            project_dir.exists(),
            "Project directory created"
        )
        self.assert_true(
            (project_dir / "tasks.ndjson").exists(),
            "tasks.ndjson created"
        )
        self.assert_true(
            (project_dir / "log.md").exists(),
            "log.md created"
        )
        self.assert_true(
            (project_dir / "summary.md").exists(),
            "summary.md created"
        )
        self.assert_true(
            (project_dir / "index.json").exists(),
            "index.json created"
        )
        self.assert_true(
            (project_dir / "archive").exists(),
            "archive directory created"
        )
        print()
    
    def test_task_operations(self):
        """Test task creation, loading, and updates"""
        print("✅ Testing task operations...")
        
        project = "test-project"
        paco_lib.init_project(project)
        
        # Add tasks
        task1 = paco_lib.add_task(project, "Task 1", priority="high", tags=["urgent"])
        task2 = paco_lib.add_task(project, "Task 2", priority="medium")
        task3 = paco_lib.add_task(project, "Task 3", priority="low")
        
        self.assert_true(
            task1["id"] == 1,
            "Task 1 has ID 1"
        )
        self.assert_true(
            task2["id"] == 2,
            "Task 2 has ID 2"
        )
        self.assert_true(
            task1["priority"] == "high",
            "Task 1 has high priority"
        )
        self.assert_true(
            "urgent" in task1["tags"],
            "Task 1 has urgent tag"
        )
        
        # Load tasks
        active_tasks = paco_lib.load_tasks(project, status_filter="active")
        self.assert_true(
            len(active_tasks) == 3,
            "All 3 tasks are active"
        )
        
        # Update task status
        paco_lib.update_task_status(project, 1, "completed")
        active_tasks = paco_lib.load_tasks(project, status_filter="active")
        completed_tasks = paco_lib.load_tasks(project, status_filter="completed")
        
        self.assert_true(
            len(active_tasks) == 2,
            "2 tasks remain active after completion"
        )
        self.assert_true(
            len(completed_tasks) == 1,
            "1 task is completed"
        )
        print()
    
    def test_logging(self):
        """Test log operations"""
        print("📝 Testing logging...")
        
        project = "test-project"
        paco_lib.init_project(project)
        
        # Append log entries
        paco_lib.append_to_log(project, "First log entry")
        paco_lib.append_to_log(project, "Second log entry")
        paco_lib.append_to_log(project, "Third log entry")
        
        # Read log
        log_file = paco_lib.get_project_dir(project) / "log.md"
        log_content = log_file.read_text()
        
        self.assert_true(
            "First log entry" in log_content,
            "First log entry present"
        )
        self.assert_true(
            "Second log entry" in log_content,
            "Second log entry present"
        )
        self.assert_true(
            log_content.count("**[") >= 3,
            "Timestamps present for all entries"
        )
        
        # Test log tail
        tail = paco_lib.get_log_tail(project, max_lines=5)
        self.assert_true(
            "Third log entry" in tail,
            "Log tail contains recent entry"
        )
        print()
    
    def test_daily_notes(self):
        """Test daily note operations"""
        print("📅 Testing daily notes...")
        
        paco_lib.init_paco_dirs()
        
        # Write daily notes
        paco_lib.write_daily_note("Morning thoughts")
        paco_lib.write_daily_note("Afternoon update")
        
        # Read today's note
        today = datetime.now().strftime("%Y-%m-%d")
        daily_content = paco_lib.get_daily_note(today)
        
        self.assert_true(
            "Morning thoughts" in daily_content,
            "Morning note present"
        )
        self.assert_true(
            "Afternoon update" in daily_content,
            "Afternoon note present"
        )
        
        # Check file exists
        daily_file = paco_lib.DAILY_DIR / f"{today}.md"
        self.assert_true(
            daily_file.exists(),
            "Daily file created"
        )
        print()
    
    def test_context_building(self):
        """Test bounded context building"""
        print("🎯 Testing context building...")
        
        project = "test-project"
        paco_lib.init_project(project)
        
        # Add some data
        for i in range(30):
            paco_lib.add_task(project, f"Task {i+1}", priority="medium")
        
        for i in range(100):
            paco_lib.append_to_log(project, f"Log entry {i+1}")
        
        # Build context
        context = paco_lib.build_context_for_llm(project)
        
        # Check size
        within_limit, size_kb = paco_lib.check_prompt_size(context)
        
        self.assert_true(
            within_limit,
            f"Context within limit ({size_kb:.1f}KB < {paco_lib.MAX_PROMPT_SIZE_KB}KB)"
        )
        self.assert_true(
            "## Project Summary" in context,
            "Context includes project summary"
        )
        self.assert_true(
            "## Active Tasks" in context,
            "Context includes active tasks"
        )
        self.assert_true(
            "## Recent Log" in context,
            "Context includes recent log"
        )
        
        # Verify bounded: should not include all 30 tasks
        task_count = context.count("Task ")
        self.assert_true(
            task_count <= paco_lib.MAX_TASKS_IN_CONTEXT,
            f"Only {task_count} tasks in context (≤{paco_lib.MAX_TASKS_IN_CONTEXT})"
        )
        
        # Verify bounded: should not include all 100 log entries
        log_count = context.count("Log entry")
        self.assert_true(
            log_count <= paco_lib.MAX_LOG_LINES_IN_CONTEXT,
            f"Only {log_count} log entries in context (≤{paco_lib.MAX_LOG_LINES_IN_CONTEXT})"
        )
        print()
    
    def test_list_projects(self):
        """Test project listing"""
        print("📋 Testing project listing...")
        
        paco_lib.init_paco_dirs()
        
        # Create projects
        paco_lib.init_project("project-a")
        paco_lib.init_project("project-b")
        paco_lib.init_project("project-c")
        
        projects = paco_lib.list_projects()
        
        self.assert_true(
            len(projects) >= 3,
            f"At least 3 projects listed (found {len(projects)})"
        )
        self.assert_true(
            "project-a" in projects,
            "project-a in list"
        )
        self.assert_true(
            "project-b" in projects,
            "project-b in list"
        )
        print()
    
    def test_summary_file_operations(self):
        """Test summary reading"""
        print("📄 Testing summary operations...")
        
        project = "test-project"
        paco_lib.init_project(project)
        
        # Write custom summary
        summary_file = paco_lib.get_project_dir(project) / "summary.md"
        summary_file.write_text("# Custom Summary\n\nThis is a test summary.")
        
        # Read summary
        summary = paco_lib.get_project_summary(project)
        
        self.assert_true(
            "Custom Summary" in summary,
            "Custom summary retrieved"
        )
        self.assert_true(
            "test summary" in summary,
            "Summary content correct"
        )
        print()
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("PACO Test Suite")
        print("=" * 60)
        print()
        
        self.setup()
        
        try:
            self.test_initialization()
            self.test_project_creation()
            self.test_task_operations()
            self.test_logging()
            self.test_daily_notes()
            self.test_context_building()
            self.test_list_projects()
            self.test_summary_file_operations()
        finally:
            self.teardown()
        
        print()
        print("=" * 60)
        print(f"Results: {self.tests_passed} passed, {self.tests_failed} failed")
        print("=" * 60)
        
        if self.tests_failed == 0:
            print("✨ All tests passed!")
            return 0
        else:
            print(f"❌ {self.tests_failed} test(s) failed")
            return 1


def main():
    """Run the test suite"""
    tester = TestPACO()
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
