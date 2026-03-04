# Phase 5 Optional Extensions Guide

> **Agent Factory Part 1 - Checkpoint System**
> **Version**: 1.0.0
> **Last Updated**: 2026-03-03

---

## Table of Contents

1. [Overview](#overview)
2. [Schema Migration System](#schema-migration-system)
3. [Analytics Dashboard](#analytics-dashboard)
4. [Quick Start](#quick-start)
5. [Use Cases](#use-cases)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Overview

The **Phase 5 Optional Extensions** add advanced features to the checkpoint system:

### 1. Schema Migration System

**Purpose**: Future-proof the system by enabling safe schema upgrades without data loss

**Features**:
- Staging migration strategy (.migration-staging/)
- Zero data loss validation
- User approval workflow
- Automatic rollback on failure
- Diff preview before migration
- Backup creation

### 2. Analytics Dashboard

**Purpose**: Track learning progress and performance trends

**Features**:
- Checkpoint frequency analysis
- Study time tracking per lesson
- Comprehension performance trends
- Progress visualizations
- HTML dashboard export
- Streak tracking

---

## Schema Migration System

### What It Does

The schema migration system allows you to upgrade checkpoint file formats (e.g., from v1 to v2) safely and automatically.

**Example scenario**: You want to add new fields to track `mastery_level`, `learning_objectives`, and `review_count` to all existing checkpoint files.

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  MIGRATION WORKFLOW                          │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌─────────────────────────────────────┐
        │  1. DISCOVER FILES                  │
        │  Scan revision-notes/ for *.md      │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │  2. CREATE PLAN                     │
        │  Identify files needing migration   │
        │  Estimate changes                   │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │  3. PREVIEW                         │
        │  Show what will change              │
        │  Sample file diff                   │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │  4. USER APPROVAL                   │
        │  "Proceed? (yes/no)"                │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │  5. MIGRATE TO STAGING              │
        │  .migration-staging/v2/             │
        │  Apply schema transformations       │
        └────────────────┬────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │  6. VALIDATE                        │
        │  Check for data loss                │
        │  Verify schema compliance           │
        └────────────────┬────────────────────┘
                         │
               ┌─────────┴─────────┐
               │                   │
               ▼                   ▼
        ✓ VALIDATION        ✗ VALIDATION
          PASSED               FAILED
               │                   │
               ▼                   ▼
        ┌──────────┐         ┌──────────┐
        │ FINALIZE │         │ ROLLBACK │
        │ Backup   │         │ Restore  │
        │ Move to  │         │ from     │
        │ prod     │         │ backup   │
        └──────────┘         └──────────┘
```

### Usage

#### Preview Migration

```bash
# See what will change without making modifications
python3 scripts/migrate-schema.py --version v2 --preview
```

**Expected output**:
```
═══════════════════════════════════════════════════════
           Migration Preview
═══════════════════════════════════════════════════════

Source Version: v1
Target Version: v2
Files to Migrate: 12
Estimated Changes: 72

ℹ Preview of changes (first file):

Sample file: 3.1-L1-hook-architecture.md

Changes:
  1. Added field: version = 'v2'
  2. Added field: learning_objectives (inferred from concepts)
  3. Added field: mastery_level = 'learning'
  4. Added field: review_count = 0
  5. Added field: last_reviewed = null
  6. Added field: comprehension_score = null
```

#### Execute Migration

```bash
# Execute the migration (creates backup first)
python3 scripts/migrate-schema.py --version v2 --execute
```

**Workflow**:
1. Shows preview
2. Asks for confirmation: "Proceed with migration? (yes/no)"
3. Creates backup in `.migration-backups/`
4. Migrates files to `.migration-staging/v2/`
5. Validates (checks for data loss)
6. If validation passes: moves to production
7. If validation fails: keeps in staging, shows issues

#### Rollback Migration

```bash
# Rollback to most recent backup
python3 scripts/migrate-schema.py --rollback

# Rollback to specific backup
python3 scripts/migrate-schema.py --rollback --backup-path .migration-backups/backup-20260303-143000
```

### Schema Versions

#### v1 (Current/Original)

**Fields**:
```yaml
lesson: "3.1"
layer: "L1"
depth: 1
semantic_name: "hook-architecture"
title: "Hook System Architecture"
concepts: ["Hooks", "Lifecycle", "Callbacks"]
tags: ["architecture", "system-design"]
keywords: ["hook", "lifecycle", "event"]
prerequisites: []
difficulty: "intermediate"
estimated_time: "45min"
date: "2026-03-03"
status: "complete"
parent_checkpoint: null
```

#### v2 (Enhanced)

**New fields** (added to v1):
```yaml
version: "v2"
learning_objectives:
  - "Understand hook system architecture"
  - "Master lifecycle event handling"
  - "Apply hook patterns to real scenarios"
mastery_level: "learning"  # learning | reviewing | mastered
review_count: 0
last_reviewed: null
comprehension_score: null  # 0-100
```

**Benefits**:
- Track learning progress (mastery_level)
- Support spaced repetition (review_count, last_reviewed)
- Measure comprehension (comprehension_score)
- Clear learning objectives per checkpoint

### Validation

The validation script (`validate-migration.py`) checks:

1. **Zero Data Loss**:
   - No files missing
   - Content not truncated
   - Concepts preserved
   - Body content intact

2. **Schema Compliance**:
   - All required fields present
   - Field types correct
   - Lesson format valid (X.Y)
   - Layer format valid (L1/L2/L3)

3. **Content Integrity**:
   - YAML frontmatter valid
   - Markdown body preserved
   - No corruption

**Example output**:
```
═══════════════════════════════════════════════════════
           Validation Report
═══════════════════════════════════════════════════════

Files Checked: 12
Files Passed: 12
Files Failed: 0

Critical Issues: 0
Errors: 0
Warnings: 1

WARNINGS:
  ℹ 3.1-L1-hook-architecture.md
    short_content: Content is very short (250 chars)

✓ VALIDATION PASSED: No issues found
```

### Safety Features

1. **Automatic Backups**: Every migration creates timestamped backup
2. **Staging Directory**: Changes go to `.migration-staging/` first
3. **Validation Before Finalize**: No production changes until validation passes
4. **Rollback Capability**: Easy restoration from any backup
5. **Dry-run Mode**: Test without making changes

### Creating Custom Migrations

To add a new schema version (e.g., v3):

1. **Define schema** in `SCHEMA_VERSIONS`:
   ```python
   "v3": {
       "description": "Schema with quiz integration",
       "yaml_fields": [...v2_fields, "quiz_score", "quiz_attempts"]
   }
   ```

2. **Create migration strategy**:
   ```python
   class V2toV3Migration(MigrationStrategy):
       def migrate_frontmatter(self, frontmatter: Dict) -> Tuple[Dict, List[str]]:
           changes = []
           migrated = frontmatter.copy()

           # Add new fields
           migrated['quiz_score'] = None
           migrated['quiz_attempts'] = 0
           changes.append("Added quiz tracking fields")

           return migrated, changes
   ```

3. **Register strategy**:
   ```python
   MIGRATION_STRATEGIES = {
       ('v1', 'v2'): V1toV2Migration,
       ('v2', 'v3'): V2toV3Migration  # NEW
   }
   ```

---

## Analytics Dashboard

### What It Does

The analytics dashboard tracks your learning progress and provides insights:

- **How much have you studied?** (total time, checkpoints, concepts)
- **What's your pace?** (lessons per week, checkpoint frequency)
- **Are you consistent?** (study streaks, activity patterns)
- **Where are you?** (completion %, lessons in progress)

### Usage

#### View Overall Dashboard

```bash
python3 scripts/analytics-dashboard.py
```

**Example output**:
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

  Lesson 3.1       ███████████████████████████████░░░░░░░░░  75.0% (3)
  Lesson 3.15      ████████████████████████████████████████ 100.0% (4)
  Lesson 3.17      ██████████████████████░░░░░░░░░░░░░░░░░░  50.0% (2)
  Lesson 3.22      ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  33.3% (1)
  Lesson 3.23      ████████████████████████████████████████ 100.0% (4)

⏱  Recent Activity

  2h ago     Lesson 3.1 L2 (5 concepts)
  1d ago     Lesson 3.17 L2 (8 concepts)
  1d ago     Lesson 3.17 L1 (6 concepts)
  3d ago     Lesson 3.1 L1 (4 concepts)
  5d ago     Lesson 3.15 L3 (7 concepts)
```

#### View Lesson-Specific Dashboard

```bash
python3 scripts/analytics-dashboard.py --lesson 3.1
```

**Example output**:
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

#### Export HTML Dashboard

```bash
# Generate interactive HTML dashboard
python3 scripts/analytics-dashboard.py --export-html

# Custom output path
python3 scripts/analytics-dashboard.py --export-html --output reports/progress.html
```

Opens beautiful interactive dashboard in browser with:
- Stat cards (lessons, checkpoints, concepts, streaks)
- Progress bars for each lesson
- Recent activity timeline
- Responsive design
- Print-friendly styles

### Metrics Explained

#### Completion Percentage

Calculated based on checkpoint depth:
- L1 only: 33%
- L1 + L2: 67%
- L1 + L2 + L3: 100%

#### Study Duration

Time between first and last checkpoint for a lesson (not actual active time).

#### Checkpoint Interval

Average time between consecutive checkpoints (indicates pacing).

#### Streaks

Consecutive days with at least one checkpoint activity.
- **Current Streak**: Days from today back to last gap
- **Longest Streak**: Maximum consecutive days ever

#### Lessons per Week

Total lessons divided by total weeks since first checkpoint.

### Data Sources

Analytics are extracted from:

1. **Checkpoint Files**: YAML frontmatter
   - `lesson`, `layer`, `depth`
   - `concepts`, `date`
   - `learning_objectives` (v2)
   - `comprehension_score` (v2)

2. **File Metadata**: Timestamps
   - Creation time
   - Modification time
   - Last access time

3. **Context Bridges**: Session data
   - Checkpoint history
   - Vocabulary bank
   - Anti-patterns covered

### Customization

Add custom metrics by modifying `AnalyticsEngine`:

```python
def calculate_comprehension_trend(self):
    """Calculate comprehension score trend over time"""
    scores = []
    for event in self.checkpoint_events:
        frontmatter = self._get_frontmatter(event.file_path)
        score = frontmatter.get('comprehension_score')
        if score:
            scores.append((event.timestamp, score))

    # Calculate trend...
    return trend_data
```

---

## Quick Start

### 1. Schema Migration

```bash
# Preview what v2 migration would do
python3 scripts/migrate-schema.py --version v2 --preview

# Execute migration (creates backup first)
python3 scripts/migrate-schema.py --version v2 --execute

# If something goes wrong, rollback
python3 scripts/migrate-schema.py --rollback
```

### 2. Analytics Dashboard

```bash
# View overall progress
python3 scripts/analytics-dashboard.py

# View specific lesson
python3 scripts/analytics-dashboard.py --lesson 3.1

# Generate HTML report
python3 scripts/analytics-dashboard.py --export-html
# Open: analytics/dashboard.html in browser
```

---

## Use Cases

### Use Case 1: Adding Spaced Repetition Tracking

**Scenario**: You want to track when you last reviewed each checkpoint for spaced repetition.

**Solution**:
1. Migrate to v2 (adds `review_count`, `last_reviewed`)
2. Use analytics to see which lessons need review
3. After reviewing, update frontmatter:
   ```yaml
   review_count: 3
   last_reviewed: "2026-03-03"
   ```

### Use Case 2: Measuring Learning Effectiveness

**Scenario**: You want to track how well you're understanding material.

**Solution**:
1. Migrate to v2 (adds `comprehension_score`)
2. After Review command, update score:
   ```yaml
   comprehension_score: 85  # Based on quiz performance
   ```
3. View analytics to see comprehension trends

### Use Case 3: Progress Reports for Accountability

**Scenario**: You want weekly progress reports to share with a mentor.

**Solution**:
1. Export HTML dashboard weekly:
   ```bash
   python3 scripts/analytics-dashboard.py --export-html \
       --output reports/week-$(date +%U)-progress.html
   ```
2. Share HTML file with mentor
3. Track week-over-week improvement

### Use Case 4: Identifying Study Patterns

**Scenario**: You want to optimize your study schedule.

**Solution**:
1. Use analytics to see checkpoint frequency
2. Identify optimal checkpoint intervals
3. Notice if streaks correlate with performance
4. Adjust study schedule based on data

### Use Case 5: Preparing for Exam

**Scenario**: Exam in 2 weeks, need to prioritize review.

**Solution**:
1. Check analytics for lessons < 100% complete
2. View last_reviewed dates (v2)
3. Prioritize lessons not reviewed in >7 days
4. Use spaced repetition schedule

---

## Troubleshooting

### Problem 1: Migration Validation Failed

**Symptoms**:
```
✗ VALIDATION FAILED: Critical issues found (data loss detected!)
```

**Solutions**:

1. **Check validation output**:
   ```bash
   python3 scripts/validate-migration.py .migration-staging/v2
   ```

2. **Inspect staged files**:
   ```bash
   cd .migration-staging/v2
   git diff revision-notes/  # Compare with original
   ```

3. **Fix issues manually** (if safe):
   - Edit staged files in `.migration-staging/v2/`
   - Re-run validation
   - If passes, manually copy to production

4. **Rollback** (if uncertain):
   ```bash
   python3 scripts/migrate-schema.py --rollback
   ```

### Problem 2: Analytics Shows Zero Lessons

**Symptoms**:
```
Total Lessons: 0
Completed: 0
```

**Solutions**:

1. **Check file structure**:
   ```bash
   ls -R revision-notes/
   # Ensure files match pattern: *-L*-*.md
   ```

2. **Verify YAML frontmatter**:
   ```bash
   head -20 revision-notes/3.1-L1-*.md
   # Should start with: ---
   ```

3. **Check file paths**:
   ```python
   # Analytics looks for:
   REVISION_NOTES_DIR / "**/*-L*-*.md"
   ```

### Problem 3: HTML Dashboard Not Loading

**Symptoms**: Opens blank page or shows errors

**Solutions**:

1. **Check file was created**:
   ```bash
   ls -lh analytics/dashboard.html
   ```

2. **Verify file permissions**:
   ```bash
   chmod 644 analytics/dashboard.html
   ```

3. **Open in different browser**:
   - Try Chrome, Firefox, Safari
   - Check browser console for errors (F12)

### Problem 4: Incorrect Study Duration

**Symptoms**: Duration shows 0h or unrealistic values

**Solutions**:

1. **Check timestamp data**:
   - Analytics uses `date` field from frontmatter
   - Falls back to file modification time
   - Ensure dates are in ISO format: `YYYY-MM-DD`

2. **Update date fields**:
   ```yaml
   date: "2026-03-03"  # Not: "March 3, 2026"
   ```

---

## Best Practices

### Schema Migration

1. **Always preview first**:
   ```bash
   python3 scripts/migrate-schema.py --version v2 --preview
   ```

2. **Test on subset**: Copy a few files to test directory, migrate those first

3. **Commit before migrating**:
   ```bash
   git add .
   git commit -m "Pre-migration checkpoint"
   python3 scripts/migrate-schema.py --version v2 --execute
   ```

4. **Verify after migration**:
   ```bash
   ./scripts/validate-notes.sh all
   git diff  # Review changes
   ```

5. **Keep backups**: Don't delete `.migration-backups/` for at least a week

### Analytics Dashboard

1. **Regular exports**: Generate HTML weekly for progress tracking

2. **Update review dates**: After reviewing, update v2 fields:
   ```yaml
   review_count: 2
   last_reviewed: "2026-03-03"
   ```

3. **Set goals**: Use metrics to set concrete goals:
   - "Maintain 7-day streak"
   - "Complete 2 lessons/week"
   - "Achieve 80%+ comprehension scores"

4. **Compare trends**: Export HTML over time, compare progress

5. **Share dashboards**: Use for accountability with mentors/study groups

---

## Future Enhancements

### Planned Features

1. **Schema Migration**:
   - Automatic migration on `Finish` command
   - Migration history tracking
   - Schema version detection
   - Multi-step migrations (v1 → v2 → v3)

2. **Analytics Dashboard**:
   - Study time heatmap (GitHub-style)
   - Concept coverage visualization
   - Comprehension score trends
   - Spaced repetition schedule
   - Export to PDF/JSON
   - API for external integrations

3. **Integration**:
   - Auto-update analytics on `Checkpoint`/`Finish`
   - Analytics command in Professor Agent
   - Weekly email reports
   - Mobile dashboard (PWA)

---

## Summary

The **Phase 5 Optional Extensions** provide:

✅ **Schema Migration**:
- Safe schema upgrades without data loss
- Staging + validation workflow
- Automatic backups and rollback
- Support for future schema versions

✅ **Analytics Dashboard**:
- Track learning progress and trends
- Visualize completion rates
- Monitor study patterns and streaks
- Export beautiful HTML dashboards

**When to use**:
- **Migration**: When adding new tracking fields or upgrading schema
- **Analytics**: Weekly to monitor progress, identify gaps, stay accountable

**Next steps**:
1. Decide if you want enhanced tracking (v2 schema)
2. If yes, run migration preview then execute
3. Start using analytics to monitor progress
4. Export HTML dashboards for accountability

---

**Questions or issues?** Check the [Troubleshooting](#troubleshooting) section or consult the main checkpoint system documentation.
