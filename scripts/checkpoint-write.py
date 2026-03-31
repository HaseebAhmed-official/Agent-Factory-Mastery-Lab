#!/usr/bin/env python3
"""
checkpoint-write.py — Atomic Bridge Update Tool
Usage: python3 scripts/checkpoint-write.py --action backup
       python3 scripts/checkpoint-write.py --action update-status --lesson 3.1 --layer L1 --concept "Hook Architecture"
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_DIR = os.path.join(BASE_DIR, "context-bridge")
BRIDGE_FILE = os.path.join(BRIDGE_DIR, "master-cumulative.md")
STATUS_FILE = os.path.join(BRIDGE_DIR, "status.json")
BACKUP_DIR = os.path.join(BRIDGE_DIR, "backup")

def atomic_write(filepath, content):
    tmp_path = filepath + ".tmp"
    try:
        with open(tmp_path, 'w') as f:
            f.write(content)
        with open(tmp_path) as f:
            written = f.read()
        if written != content:
            os.remove(tmp_path)
            return False
        os.replace(tmp_path, filepath)
        return True
    except Exception as e:
        print(f"ERROR in atomic_write: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        # Log failure to status.json for repair detection
        try:
            import json as _json
            if os.path.exists(STATUS_FILE):
                with open(STATUS_FILE) as _f:
                    _status = _json.load(_f)
            else:
                _status = {}
            _status["repair_needed"] = True
            _status["last_error"] = str(e)
            _status["failed_file"] = filepath
            with open(STATUS_FILE, 'w') as _f:
                _json.dump(_status, _f, indent=2)
        except Exception:
            pass  # Don't fail while logging a failure
        return False

def backup_bridge():
    if not os.path.exists(BRIDGE_FILE):
        print("No bridge file to backup.")
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d-%H%M")
    backup_path = os.path.join(BACKUP_DIR, f"master-cumulative-{date_str}.md")
    shutil.copy2(BRIDGE_FILE, backup_path)
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("master-cumulative-") and f.endswith(".md")])
    while len(backups) > 3:
        os.remove(os.path.join(BACKUP_DIR, backups.pop(0)))
    print(f"✅ Bridge backed up to: {backup_path}")
    return backup_path

def update_status(updates):
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE) as f:
            data = json.load(f)
    else:
        data = {}
    data.update(updates)
    data["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if atomic_write(STATUS_FILE, json.dumps(data, indent=2)):
        print(f"✅ status.json updated: {updates}")
    else:
        print("❌ Failed to update status.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["backup", "update-status"], required=True)
    parser.add_argument("--lesson", default=None)
    parser.add_argument("--layer", default=None)
    parser.add_argument("--concept", default=None)
    parser.add_argument("--status", default=None)
    parser.add_argument("--message-count", type=int, default=None)
    args = parser.parse_args()

    if args.action == "backup":
        backup_bridge()
    elif args.action == "update-status":
        updates = {}
        if args.lesson: updates["lesson"] = args.lesson
        if args.layer: updates["layer"] = args.layer
        if args.concept: updates["concept"] = args.concept
        if args.status: updates["status"] = args.status
        if args.message_count is not None: updates["message_count_since_checkpoint"] = args.message_count
        update_status(updates)

if __name__ == "__main__":
    main()
