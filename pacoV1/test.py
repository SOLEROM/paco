#!/usr/bin/env python3
"""
PACO Test Script - Verify all functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paco_lib as lib


def test_basic_operations():
    """Test basic PACO operations"""
    print("🧪 Testing PACO...")
    test_dir = Path(tempfile.mkdtemp(prefix="paco_test_"))
    
    # Override directories for testing
    original_paco_dir = lib.PACO_DIR
    lib.PACO_DIR = test_dir
    lib.PROJECTS_DIR = test_dir / "projects"
    lib.CONFIG_FILE = test_dir / "config.json"
    
    try:
        print("\n📁 Test 1: Initialization")
        lib.init_paco_dirs()
        assert lib.PACO_DIR.exists(), "PACO dir not created"
        assert lib.CONFIG_FILE.exists(), "Config file not created"
        print("  ✅ Passed")
        
        print("\n📋 Test 2: Configuration")
        config = lib.load_config()
        assert config["model"] == "llama3.2", "Default model wrong"
        lib.set_config_value("model", "test-model")
        assert lib.get_config_value("model") == "test-model", "Config set failed"
        print("  ✅ Passed")
        
        print("\n🆕 Test 3: Project Creation")
        lib.init_project("test-project")
        project_dir = lib.get_project_dir("test-project")
        assert project_dir.exists(), "Project dir not created"
        assert (project_dir / "tasks.ndjson").exists(), "tasks.ndjson not created"
        print("  ✅ Passed")
        
        print("\n✅ Test 4: Task Operations")
        task1 = lib.add_task("test-project", "Task 1", priority="high")
        task2 = lib.add_task("test-project", "Task 2", priority="medium", tags=["urgent"])
        assert task1["id"] == 1, "Task ID wrong"
        assert task2["id"] == 2, "Task ID wrong"
        
        tasks = lib.load_tasks("test-project")
        assert len(tasks) == 2, "Tasks not loaded"
        
        lib.update_task_status("test-project", 1, "completed")
        active = lib.load_tasks("test-project", status_filter="active")
        assert len(active) == 1, "Task completion failed"
        print("  ✅ Passed")
        
        print("\n📝 Test 5: Logging")
        lib.append_to_log("test-project", "Test log entry")
        log = lib.get_log_tail("test-project")
        assert "Test log entry" in log, "Log entry not found"
        print("  ✅ Passed")
        
        print("\n📅 Test 6: Daily Notes")
        lib.write_daily_note("test-project", "Test daily note")
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        daily = lib.get_daily_note("test-project", today)
        assert "Test daily note" in daily, "Daily note not found"
        
        # Test recent daily notes
        lib.write_daily_note("test-project", "Another note")
        recent = lib.get_recent_daily_notes("test-project", days=7)
        assert "Test daily note" in recent, "Recent notes not retrieved"
        print("  ✅ Passed")
        
        print("\n🎯 Test 7: Context Building")
        for i in range(30):
            lib.add_task("test-project", f"Task {i+3}", priority="medium")
        
        context = lib.build_context_for_llm("test-project")
        within_limit, size_kb = lib.check_prompt_size(context)
        assert within_limit, f"Context too large: {size_kb}KB"
        assert "## Project Summary" in context, "Missing summary"
        assert "## Active Tasks" in context, "Missing tasks"
        print(f"  ✅ Passed (context: {size_kb:.1f}KB)")
        
        print("\n📋 Test 8: Project Listing")
        lib.init_project("project-a")
        lib.init_project("project-b")
        projects = lib.list_projects()
        assert "test-project" in projects, "Project not listed"
        assert len(projects) >= 3, f"Not enough projects: {len(projects)}"
        print("  ✅ Passed")
        
        print("\n" + "="*60)
        print("✨ All tests passed!")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        lib.PACO_DIR = original_paco_dir
        if test_dir.exists():
            shutil.rmtree(test_dir)
        print(f"\n🧹 Cleaned up test directory")


if __name__ == "__main__":
    sys.exit(test_basic_operations())
