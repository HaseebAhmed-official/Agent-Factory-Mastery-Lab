# 10 — Terminal: Backup & Bridge Reference

Run all commands from the repo root:

```bash
cd /root/code/Agent-Factory-Mastery-Lab/.claude/worktrees/updating-stuff
```

---

## Quick Reference Table

| Command | Purpose | Expected Output |
|---------|---------|----------------|
| `python3 scripts/checkpoint-write.py --action backup` | Backup bridge file before changes | `✅ Bridge backed up to: context-bridge/backup/...` |
| `python3 scripts/checkpoint-write.py --action update-status --lesson 3.1 --layer L1 --concept "Hook Architecture"` | Manually update status.json | `✅ status.json updated` |
| `python3 scripts/bridge-update.py --section 17 --content "pipe-separated row"` | Append row to bridge section 17 | `✅ Appended to Section 17` |
| Hard reset (inline `python3 -c`) | Wipe session progress, fresh start | `✅ Reset to fresh start` |

---

## checkpoint-write.py

Core script for saving, backing up, and updating session state. Runs automatically during the Checkpoint workflow and can be called manually when needed.

---

### Action 1: backup

```bash
python3 scripts/checkpoint-write.py --action backup
```

**Purpose**: Creates a dated backup of the master context bridge before modifying it.

**What it does**:
- Copies `context-bridge/master-cumulative.md` to `context-bridge/backup/master-cumulative-{DATE}.md`
- DATE format: `YYYY-MM-DD` (e.g., `master-cumulative-2026-03-31.md`)
- Reports success or failure

**Expected output**:
```
✅ Bridge backed up to: context-bridge/backup/master-cumulative-2026-03-31.md
```

**When to use**:
- Before any manual edits to the bridge
- Before running a risky operation
- As a safety step before `--action update-status`

**Failure case (read-only file)**:
```
❌ Backup failed: Permission denied
   context-bridge/master-cumulative.md is read-only
```

When backup fails, the script sets `repair_needed: true` in `status.json`. The Resume Protocol will surface this flag as a repair prompt on the next session start.

---

### Action 2: update-status

```bash
python3 scripts/checkpoint-write.py --action update-status --lesson 3.1 --layer L1 --concept "Hook Architecture"
```

**Purpose**: Manually updates `context-bridge/status.json` to a specific lesson/layer/concept. Use when the bridge and chat are out of sync.

**Required flags**:

| Flag | Description | Example |
|------|-------------|---------|
| `--lesson` | Lesson number | `3.1`, `3.17` |
| `--layer` | Checkpoint layer | `L1`, `L2`, `L3` |
| `--concept` | Concept name (quote if it contains spaces) | `"Hook Architecture"` |

**Expected output**:
```
✅ status.json updated
   lesson: 3.1
   layer: L1
   concept: Hook Architecture
   last_updated: 2026-03-31
```

**What gets written to status.json**:
```json
{
  "lesson": "3.1",
  "layer": "L1",
  "concept": "Hook Architecture",
  "last_checkpoint": "2026-03-31T14:30:00",
  "message_count_since_checkpoint": 0,
  "session_count": 7,
  "status": "active",
  "next_review_due_count": 2,
  "last_updated": "2026-03-31",
  "repair_needed": false
}
```

**When to use**:
- Recovery after a failed checkpoint where `status.json` shows the wrong lesson
- Manually setting state after direct bridge edits
- Testing — to simulate being at a specific lesson/layer

---

## bridge-update.py

### Command

```bash
python3 scripts/bridge-update.py --section 17 --content "pipe-separated row"
```

**Purpose**: Appends a row to a specific section of `context-bridge/master-cumulative.md`. Section 17 is the Session History table.

**Required flags**:

| Flag | Description | Example |
|------|-------------|---------|
| `--section` | Section number (1–18) | `17` |
| `--content` | Pipe-separated row matching the section's table columns | `"S07 | 2026-03-31 | 3.1 | 2 | Normal session"` |

**Expected output**:
```
✅ Appended to Section 17
```

**Section 17 structure (Session History)**:
```markdown
## 17. Session History
| Session | Date | Lessons Covered | Checkpoints | Notes |
|---------|------|-----------------|-------------|-------|
| S07 | 2026-03-31 | 3.1 | 2 | Normal session |
```

**Content format for Section 17**:
```
"S{NN} | {DATE} | {LESSONS} | {CHECKPOINT_COUNT} | {NOTES}"
```

**Full example**:
```bash
python3 scripts/bridge-update.py --section 17 --content "S07 | 2026-03-31 | 3.1 | 2 | Covered L1 and L2 of Hook Architecture"
```

**When to use**:
- Manually logging a session that was not auto-logged
- Recovering a missing session history row after a crash
- Testing bridge append behavior

**Other sections**:
Any section (1–18) can be appended to with this script. Use caution — `master-cumulative.md` is the single source of truth. Run `--action backup` first when appending to sensitive sections.

---

## Hard Reset Script

### When to use

When you want to wipe all session progress and start over with a completely fresh state.

### Command

```bash
python3 -c "
import json
data = {
  'lesson':'none','layer':'none','concept':'none',
  'last_checkpoint':'never','message_count_since_checkpoint':0,
  'session_count':0,'status':'fresh_start',
  'next_review_due_count':0,'last_updated':'2026-03-29'
}
open('context-bridge/status.json','w').write(json.dumps(data,indent=2))
print('✅ Reset to fresh start')
"
```

### What it does

- Overwrites `context-bridge/status.json` with a clean `fresh_start` state
- Does NOT delete revision notes, backups, snapshots, or HTML files
- Does NOT modify `master-cumulative.md`
- Next Claude Code session will see no recovery banner — fresh start greeting instead

### Warning

This resets the STATUS, not the files. Your checkpoint notes and bridge content are preserved. To also clear the bridge content, you would need to manually reset `master-cumulative.md` — that is destructive and rarely needed.

### Verify the reset

```bash
cat context-bridge/status.json
# Should show: lesson: "none", status: "fresh_start"
```

---

## Checking Backup and Snapshot Files

```bash
ls context-bridge/backup/
# Expected: dated backup files
# Example:  master-cumulative-2026-03-31.md

ls context-bridge/snapshots/
# Expected: frozen checkpoint snapshots
# Example:  lesson-3.1-L1-hook-architecture-snapshot.md
```
