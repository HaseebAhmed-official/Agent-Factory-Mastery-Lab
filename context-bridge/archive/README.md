# Context Bridge — Archive Directory

> **Purpose**: Long-term storage of old bridge content when master file exceeds 300 lines
> **Created by**: Stage 3 of Checkpoint workflow (automatically when threshold reached)
> **Threshold**: When `master-cumulative.md` exceeds 300 lines

---

## How Archival Works

When `master-cumulative.md` grows beyond 300 lines, older content is moved here to keep the active file lean and within context window limits:

**What gets archived**:
- Section 5 (Session Flow) — older session entries beyond last 3
- Section 14 (Checkpoint History) — rows older than 5 most recent checkpoints

**What stays in master**:
- All structural sections (1-4, 6-13, 15-18)
- Last 5 rows of checkpoint history
- Current state and next steps

## File Naming

```
master-cumulative-archived-{YYYY-MM-DD}.md
```

**Example**: `master-cumulative-archived-2026-04-01.md`

## Access

To review full learning history including archived content:
1. Check this directory for archived files
2. Open the relevant dated archive
3. Cross-reference with current `master-cumulative.md` for complete picture

## Note

A link is always added to `master-cumulative.md` when content is archived:
```
> See archive/master-cumulative-archived-{date}.md for earlier session content.
```
