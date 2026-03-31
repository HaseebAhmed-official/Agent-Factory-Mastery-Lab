#!/usr/bin/env python3
"""
session-start.py — Cold-Start Orchestrator
Runs at every session start. Reads status.json, runs health check,
outputs a formatted recovery banner for Professor Agent to display.

Usage: python3 scripts/session-start.py
Output: JSON to stdout with banner text + health status
"""
import json
import os
import sys
import subprocess
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_DIR = os.path.join(BASE_DIR, "context-bridge")
STATUS_FILE = os.path.join(BRIDGE_DIR, "status.json")
HEALTH_SCRIPT = os.path.join(os.path.dirname(__file__), "health-check.py")

def read_status():
    if not os.path.exists(STATUS_FILE):
        return {
            "lesson": "none", "layer": "none", "concept": "none",
            "last_checkpoint": "never", "status": "fresh_start",
            "message_count_since_checkpoint": 0, "session_count": 0,
            "next_review_due_count": 0
        }
    try:
        with open(STATUS_FILE) as f:
            return json.load(f)
    except Exception:
        return {"status": "corrupted", "lesson": "unknown"}

def run_health_check():
    try:
        result = subprocess.run(
            [sys.executable, HEALTH_SCRIPT],
            capture_output=True, text=True, timeout=10
        )
        healthy = result.returncode == 0
        output = result.stdout.strip()
        return healthy, output
    except Exception as e:
        return False, f"Health check failed to run: {e}"

def increment_session_count(status):
    count = status.get("session_count", 0) + 1
    status["session_count"] = count
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f, indent=2)
    except Exception:
        pass
    return count

def format_banner(status, healthy, health_output, session_count):
    is_fresh = status.get("status") == "fresh_start"
    lesson = status.get("lesson", "none")
    layer = status.get("layer", "none")
    concept = status.get("concept", "none")
    last_cp = status.get("last_checkpoint", "never")
    msgs = status.get("message_count_since_checkpoint", 0)
    reviews_due = status.get("next_review_due_count", 0)

    health_icon = "✅" if healthy else "⚠️"
    is_3rd_session = session_count % 3 == 0 and session_count > 0

    if is_fresh:
        banner = (
            "╔══════════════════════════════════════════╗\n"
            "║   🎓 AGENT FACTORY — FRESH START         ║\n"
            "╚══════════════════════════════════════════╝\n"
            f"System health: {health_icon}\n"
            "No prior session found. Starting from scratch.\n"
        )
    else:
        interleaved_note = "\n🔀 INTERLEAVED REVIEW SESSION — First 10 min: cross-chapter retrieval" if is_3rd_session else ""
        review_note = f"\n📚 {reviews_due} concept(s) due for spaced review" if reviews_due > 0 else ""
        banner = (
            "╔══════════════════════════════════════════╗\n"
            f"║   🎓 SESSION #{session_count} RESTORED               ║\n"
            "╚══════════════════════════════════════════╝\n"
            f"📍 Lesson:     {lesson}\n"
            f"🏷️  Layer:      {layer}\n"
            f"💡 Concept:    {concept}\n"
            f"⏱️  Checkpoint: {last_cp}\n"
            f"💬 Messages since last checkpoint: {msgs}\n"
            f"System health: {health_icon}{review_note}{interleaved_note}\n"
        )

    if not healthy:
        banner += f"\n{health_output}\n"
        banner += "\nType 'Repair' to attempt automatic fixes before continuing.\n"

    return banner

def main():
    status = read_status()
    healthy, health_output = run_health_check()
    session_count = increment_session_count(status)
    banner = format_banner(status, healthy, health_output, session_count)

    output = {
        "banner": banner,
        "healthy": healthy,
        "status": status,
        "session_count": session_count,
        "is_3rd_session": session_count % 3 == 0 and session_count > 0,
        "reviews_due": status.get("next_review_due_count", 0)
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
