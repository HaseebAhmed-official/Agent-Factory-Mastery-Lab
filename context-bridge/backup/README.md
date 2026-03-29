# Context Bridge — Backup Directory

> **Purpose**: Rolling backup of `master-cumulative.md`
> **Created by**: Stage 3 of Checkpoint workflow (automatically before each bridge update)
> **Managed by**: Professor Agent — no manual editing needed

---

## How Backups Work

Before every checkpoint updates the master bridge, the current state is copied here as a dated backup. This protects against:
- Partial write failures during bridge update
- Accidental corruption of the master file
- Recovery after unexpected session termination

## File Naming

```
master-cumulative-{YYYY-MM-DD}.md
```

**Examples**:
- `master-cumulative-2026-03-06.md`
- `master-cumulative-2026-03-15.md`

## Retention Policy

Only the **3 most recent backups** are kept. When a 4th backup is created, the oldest is automatically deleted.

## Recovery

If `master-cumulative.md` becomes corrupted or unreadable:
1. Open the most recent backup from this directory
2. Copy it to `../master-cumulative.md`
3. The Resume Protocol will detect and load it on next session start

## Important

- Backups are created **before** each write (not after)
- If two checkpoints happen on the same date, the second overwrites the first backup for that date
- These files are read-only references — do not edit them
