# Analytics & Migration Commands Reference

## Quick Reference Table

| Command | Purpose | Output |
|---------|---------|--------|
| `python3 scripts/analytics-dashboard.py` | Overall progress dashboard | Terminal output |
| `python3 scripts/analytics-dashboard.py --lesson 3.1` | Lesson-specific analytics | Terminal output |
| `python3 scripts/analytics-dashboard.py --export-html` | HTML progress report | `analytics/dashboard.html` |
| `python3 scripts/analytics-dashboard.py --export-html --output reports/progress.html` | HTML report at custom path | Custom path |
| `python3 scripts/migrate-schema.py --version v2 --preview` | Preview v2 migration | Terminal diff |
| `python3 scripts/migrate-schema.py --version v2 --execute` | Run v2 migration | Updated checkpoint files |
| `python3 scripts/migrate-schema.py --rollback` | Undo last migration | Restored from backup |
| `python3 scripts/migrate-schema.py --rollback --backup-path .migration-backups/backup-20260303-143000` | Rollback to specific backup | Restored from named backup |

---

## Overview

These are Phase 5 optional extension scripts. They are not required for normal learning — they add progress tracking and schema upgrade capabilities on top of the core checkpoint system.

- **`analytics-dashboard.py`** — tracks how much you have studied, your pace, consistency, and where you are in the curriculum.
- **`migrate-schema.py`** — safely upgrades checkpoint file schemas from v1 to v2, adding spaced repetition and mastery tracking fields without data loss.

---

## analytics-dashboard.py

### View overall dashboard

```bash
python3 scripts/analytics-dashboard.py
```

### View lesson-specific dashboard

```bash
python3 scripts/analytics-dashboard.py --lesson 3.1
```

### Export HTML dashboard

```bash
python3 scripts/analytics-dashboard.py --export-html

# Custom output path:
python3 scripts/analytics-dashboard.py --export-html --output reports/progress.html
```

---

### Expected output — overall dashboard

```
═══════════════════════════════════════════════════════
           Analytics Dashboard
═══════════════════════════════════════════════════════

📊 Overall Progress
  Total Lessons: 5
  Completed: 2
  In Progress: 3
  Completion Rate: 40.0%

📚 Learning Stats
  Total Checkpoints: 18
  Concepts Learned: 87
  Total Study Time: 6h 45m
  Avg Time/Lesson: 1h 21m

🔥 Study Streaks
  Current Streak: 7 days
  Longest Streak: 12 days
  Lessons/Week: 2.3

📈 Lesson Progress
  Lesson 3.1       ███████████████████████████████░░░░░░░░░  75.0% (3 checkpoints)
  Lesson 3.15      ████████████████████████████████████████ 100.0% (4 checkpoints)
  Lesson 3.17      ██████████████████████░░░░░░░░░░░░░░░░░░  50.0% (2 checkpoints)

⏱  Recent Activity
  2h ago     Lesson 3.1 L2 (5 concepts)
  1d ago     Lesson 3.17 L2 (8 concepts)
```

---

### Expected output — lesson-specific (`--lesson 3.1`)

```
═══════════════════════════════════════════════════════
    Lesson 3.1 - Detailed Analytics
═══════════════════════════════════════════════════════

📊 Overview
  Checkpoints: 3
  Layers: L1, L2, L3
  Completion: 100.0%

📚 Learning Stats
  Concepts: 15
  Study Duration: 2h 15m
  Avg Checkpoint Interval: 45m

📅 Timeline
  First Checkpoint: 2026-02-28 14:30
  Last Checkpoint: 2026-03-03 16:45

📝 Checkpoint History
  2026-02-28 14:30 | L1 | 4 concepts
  2026-03-01 10:15 | L2 | 5 concepts
  2026-03-03 16:45 | L3 | 6 concepts
```

---

### Metrics explained

| Metric | How calculated |
|--------|---------------|
| **Completion %** | L1 only = 33%, L1+L2 = 67%, L1+L2+L3 = 100% |
| **Study Duration** | Time between first and last checkpoint for a lesson |
| **Checkpoint Interval** | Average time between consecutive checkpoints |
| **Current Streak** | Consecutive days with at least 1 checkpoint activity back from today |
| **Longest Streak** | Maximum consecutive days ever |
| **Lessons/Week** | Total lessons divided by total weeks since first checkpoint |

---

### Data sources

- Checkpoint file YAML frontmatter (`lesson`, `layer`, `depth`, `concepts`, `date`)
- File creation/modification timestamps
- `context-bridge/master-cumulative.md` (session history, vocab bank)

---

### HTML export

`--export-html` generates `analytics/dashboard.html` — an interactive browser dashboard with:

- Stat cards (lessons, checkpoints, concepts, streaks)
- Progress bars per lesson
- Recent activity timeline
- Responsive design
- Print-friendly styles

Use `--output` to write to a custom path instead of the default `analytics/dashboard.html`.

---

## migrate-schema.py

### Preview migration (safe — no changes made)

```bash
python3 scripts/migrate-schema.py --version v2 --preview
```

### Execute migration

```bash
python3 scripts/migrate-schema.py --version v2 --execute
```

### Rollback to most recent backup

```bash
python3 scripts/migrate-schema.py --rollback
```

### Rollback to specific backup

```bash
python3 scripts/migrate-schema.py --rollback --backup-path .migration-backups/backup-20260303-143000
```

---

### Purpose

Safely upgrades checkpoint file YAML frontmatter from v1 to v2. The v2 schema adds learning objectives, mastery level, review tracking, and comprehension score fields — enabling spaced repetition workflows. All existing data is preserved.

---

### v1 vs v2 schema

**v1 fields (current)**:

```yaml
lesson: "3.1"
layer: "L1"
depth: 1
semantic_name: "hook-architecture"
title: "Hook System Architecture"
concepts: ["Hooks", "Lifecycle", "Callbacks"]
tags: ["architecture", "system-design"]
difficulty: "intermediate"
estimated_time: "45min"
date: "2026-03-03"
status: "complete"
```

**v2 adds these fields**:

```yaml
version: "v2"
learning_objectives:
  - "Understand hook system architecture"
  - "Master lifecycle event handling"
mastery_level: "learning"   # learning | reviewing | mastered
review_count: 0
last_reviewed: null
comprehension_score: null   # 0-100
```

---

### Migration workflow (`--execute`)

1. Shows preview of what will change
2. Asks for confirmation: `Proceed with migration? (yes/no)`
3. Creates backup in `.migration-backups/`
4. Migrates files to `.migration-staging/v2/`
5. Validates (zero data loss check)
6. If validation passes: moves files to production
7. If validation fails: keeps files in staging, shows issues — rollback available

---

### Validation checks

- **Zero data loss** — no files missing, content not truncated, concepts preserved
- **Schema compliance** — all required fields present, correct types
- **Content integrity** — YAML frontmatter valid, markdown body preserved

---

### Preview output

```
Migration Preview
═══════════════════════════════════════════
Source Version: v1
Target Version: v2
Files to Migrate: 12
Estimated Changes: 72

Preview (first file): 3.1-L1-hook-architecture.md
Changes:
  1. Added field: version = 'v2'
  2. Added field: learning_objectives (inferred from concepts)
  3. Added field: mastery_level = 'learning'
  4. Added field: review_count = 0
  5. Added field: last_reviewed = null
  6. Added field: comprehension_score = null
```

---

### Best practice order

Always preview before executing. Commit your current state first so you have a clean rollback point outside of the migration tool itself.

```bash
# 1. Always preview first
python3 scripts/migrate-schema.py --version v2 --preview

# 2. Commit current state before migrating
git add .
git commit -m "Pre-migration checkpoint"

# 3. Execute
python3 scripts/migrate-schema.py --version v2 --execute

# 4. Verify after
./scripts/validate-notes.sh all
```

---

### Troubleshooting

| Problem | Fix |
|---------|-----|
| `Validation FAILED: Critical issues found` | Check `.migration-staging/v2/`, fix issues manually, or rollback |
| `Analytics shows Total Lessons: 0` | Verify files match `*-L*-*.md` pattern; check YAML frontmatter starts with `---` |
| HTML dashboard not loading | `chmod 644 analytics/dashboard.html`; try a different browser |
| Incorrect study duration | Ensure `date` field is ISO format `YYYY-MM-DD` |

---

## When to use these

| Scenario | Command |
|----------|---------|
| Weekly progress check | `python3 scripts/analytics-dashboard.py` |
| Before mentor meeting | `python3 scripts/analytics-dashboard.py --export-html` |
| Check specific lesson progress | `python3 scripts/analytics-dashboard.py --lesson X.Y` |
| Add spaced repetition tracking | `python3 scripts/migrate-schema.py --version v2 --execute` |
| Something went wrong during migration | `python3 scripts/migrate-schema.py --rollback` |
