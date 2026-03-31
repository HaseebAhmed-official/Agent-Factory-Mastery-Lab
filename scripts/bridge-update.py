#!/usr/bin/env python3
"""
bridge-update.py — Idempotent Bridge Section Updater
Appends content to a specific section of master-cumulative.md
with checksum verification to prevent duplicate writes.

Usage:
  python3 scripts/bridge-update.py --section 7 --content "| NewTerm | L3.1 | L1 | 2026-03-29 | 2026-03-30 | 0 | - |"
  python3 scripts/bridge-update.py --section 14 --content "| L1 | 2026-03-29 | Hook Arch | 3.1-L1-hook-architecture.md | ✓ Archived |"
  python3 scripts/bridge-update.py --section 17 --content "| 1 | 2026-03-29 | 3.1 | 1 | Fresh start |"
"""
import argparse
import hashlib
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_FILE = os.path.join(BASE_DIR, "context-bridge", "master-cumulative.md")
CHECKSUM_FILE = os.path.join(BASE_DIR, "context-bridge", ".update-checksums.json")

def content_checksum(section: int, content: str) -> str:
    raw = f"section:{section}::content:{content.strip()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def load_checksums() -> dict:
    if os.path.exists(CHECKSUM_FILE):
        try:
            import json
            with open(CHECKSUM_FILE) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_checksums(checksums: dict):
    import json
    tmp = CHECKSUM_FILE + ".tmp"
    with open(tmp, 'w') as f:
        json.dump(checksums, f, indent=2)
    os.replace(tmp, CHECKSUM_FILE)

def find_section_end(lines: list, section_num: int) -> int:
    """Find the last line of a section (just before the next ## header or EOF)."""
    in_section = False
    section_header = f"## {section_num}."
    for i, line in enumerate(lines):
        if line.strip().startswith(section_header):
            in_section = True
            continue
        if in_section:
            # Next section starts
            if re.match(r'^## \d+\.', line.strip()):
                return i - 1
    return len(lines) - 1 if in_section else -1

def append_to_section(section: int, content: str, idempotent: bool = True) -> bool:
    if not os.path.exists(BRIDGE_FILE):
        print(f"ERROR: Bridge file not found: {BRIDGE_FILE}")
        return False

    # Idempotency check
    if idempotent:
        checksums = load_checksums()
        chk = content_checksum(section, content)
        if chk in checksums.values():
            print(f"⚠️  Skipped (duplicate write detected): section {section}")
            return True

    with open(BRIDGE_FILE) as f:
        lines = f.readlines()

    insert_pos = find_section_end(lines, section)
    if insert_pos == -1:
        print(f"ERROR: Section {section} not found in bridge")
        return False

    # Insert after last non-empty line in section
    while insert_pos > 0 and lines[insert_pos].strip() == '':
        insert_pos -= 1

    new_line = content.strip() + "\n"
    lines.insert(insert_pos + 1, new_line)

    # Atomic write
    tmp = BRIDGE_FILE + ".tmp"
    try:
        with open(tmp, 'w') as f:
            f.writelines(lines)
        with open(tmp) as f:
            written = f.read()
        os.replace(tmp, BRIDGE_FILE)

        # Record checksum
        if idempotent:
            checksums = load_checksums()
            chk = content_checksum(section, content)
            checksums[f"sec{section}_{len(checksums)}"] = chk
            save_checksums(checksums)

        print(f"✅ Appended to Section {section}: {content[:60]}...")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        if os.path.exists(tmp):
            os.remove(tmp)
        return False

def main():
    parser = argparse.ArgumentParser(description="Idempotent bridge section updater")
    parser.add_argument("--section", type=int, required=True, help="Section number (1-18)")
    parser.add_argument("--content", type=str, required=True, help="Content to append")
    parser.add_argument("--no-idempotent", action="store_true", help="Skip duplicate check")
    args = parser.parse_args()

    if not 1 <= args.section <= 18:
        print("ERROR: Section must be 1-18")
        sys.exit(1)

    success = append_to_section(args.section, args.content, idempotent=not args.no_idempotent)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
