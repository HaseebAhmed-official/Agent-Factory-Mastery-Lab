#!/usr/bin/env python3
"""
health-check.py — Agent Factory System Health Validator
Run: python3 scripts/health-check.py
"""
import json
import os
import sys
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_DIR = os.path.join(BASE_DIR, "context-bridge")
STATUS_FILE = os.path.join(BRIDGE_DIR, "status.json")
BRIDGE_FILE = os.path.join(BRIDGE_DIR, "master-cumulative.md")

REQUIRED_SECTIONS = [
    "## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.",
    "## 7.", "## 8.", "## 9.", "## 10.", "## 11.", "## 12.",
    "## 13.", "## 14.", "## 15.", "## 16.", "## 17.", "## 18."
]

issues = []
checks = []

# Check 1: status.json
if not os.path.exists(STATUS_FILE):
    issues.append("MISSING: context-bridge/status.json")
else:
    try:
        with open(STATUS_FILE) as f:
            data = json.load(f)
        required_keys = ["lesson", "layer", "concept", "last_checkpoint", "status"]
        missing = [k for k in required_keys if k not in data]
        if missing:
            issues.append(f"status.json missing keys: {missing}")
        else:
            checks.append("✅ status.json — valid")
    except json.JSONDecodeError as e:
        issues.append(f"status.json INVALID JSON: {e}")

# Check 2: master-cumulative.md
if not os.path.exists(BRIDGE_FILE):
    issues.append("MISSING: context-bridge/master-cumulative.md")
else:
    with open(BRIDGE_FILE) as f:
        content = f.read()
    missing_sections = [s for s in REQUIRED_SECTIONS if s not in content]
    if missing_sections:
        issues.append(f"Bridge missing sections: {missing_sections}")
    else:
        checks.append("✅ master-cumulative.md — all 18 sections present")

# Check 3: orphaned .tmp files
tmp_files = glob.glob(os.path.join(BRIDGE_DIR, "**/*.tmp"), recursive=True)
tmp_files += glob.glob(os.path.join(BRIDGE_DIR, "*.tmp"))
if tmp_files:
    issues.append(f"ORPHANED .tmp files found: {tmp_files}")
else:
    checks.append("✅ No orphaned .tmp files")

# Report
print("\n=== AGENT FACTORY HEALTH CHECK ===\n")
for c in checks:
    print(c)
if issues:
    print(f"\n❌ UNHEALTHY — {len(issues)} issue(s) found:")
    for i in issues:
        print(f"   ⚠️  {i}")
    print("\nRun 'Repair' command in your session to attempt automatic fixes.")
    sys.exit(1)
else:
    print(f"\n✅ HEALTHY — All {len(checks)} checks passed.")
    sys.exit(0)
