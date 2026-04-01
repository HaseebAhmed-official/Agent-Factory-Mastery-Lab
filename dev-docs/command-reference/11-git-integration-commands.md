# Git Integration Commands Reference

## Quick Reference Table

| Command | Purpose | When it runs |
|---------|---------|-------------|
| `python3 scripts/git-auto-push.py checkpoint 3.1 L1` | Commit checkpoint files | Auto after Checkpoint Stage 7 |
| `python3 scripts/git-auto-push.py finish 3.1` | Commit all artifacts + tag | Auto after Finish Stage 9 |
| `python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L1` | Test without committing | Manual testing |
| `python3 scripts/git-auto-push.py --skip-quality finish 3.1` | Commit bypassing quality checks | Not recommended |
| `.git/hooks/pre-commit` | Quality gate (auto-runs on commit) | Every `git commit` |
| `./scripts/validate-notes.sh 3.1` | Check quality score manually | Manual |
| `./scripts/validate-notes.sh all` | Check all lessons manually | Manual |

---

## Overview

The git integration system automatically commits and tags checkpoint files to version control. It runs automatically as part of the Checkpoint and Finish workflows but can also be invoked manually.

---

## Setup (One-Time)

```bash
# Step 1: Initialize git repo (if not already)
git init
git branch -M main

# Step 2: Add remote
git remote add origin https://github.com/yourusername/agent-factory-notes.git

# Step 3: Verify setup
python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L1
```

---

## git-auto-push.py

### Checkpoint auto-push

Stages and commits checkpoint part files, bridge updates, and metadata after a Checkpoint command.

```bash
python3 scripts/git-auto-push.py checkpoint 3.1 L1
```

### Finish auto-push (with tagging)

Stages all lesson artifacts, commits, creates a git tag, and pushes to remote after a Finish command.

```bash
python3 scripts/git-auto-push.py finish 3.1
```

### Dry run

Tests the full workflow without making any changes to git history or the remote.

```bash
python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L2
```

### Skip quality checks

Bypasses the pre-commit quality gate. Not recommended — use only when you need to commit partial or in-progress content.

```bash
python3 scripts/git-auto-push.py --skip-quality finish 3.1
```

---

## How It Fits Into the Checkpoint Workflow

After Stage 7 of Checkpoint (context reloaded):

1. Stages checkpoint part files, bridge updates, and metadata
2. Creates a semantic commit message
3. Runs `git commit` — pre-commit hook fires (quality validation)
4. If quality score ≥ 70/100: commit succeeds, pushes to remote
5. If quality score < 70/100: commit is blocked, user is notified

---

## How It Fits Into the Finish Workflow

After Stage 9 of Finish:

1. Stages all lesson artifacts (10–20 files)
2. Creates a semantic commit message
3. Runs `git commit` — pre-commit hook fires
4. Creates git tag: `lesson-{X.Y}`
5. Pushes commit and tags: `git push origin main --tags`
6. If GitHub Pages is configured: deployment workflow triggers

---

## Commit Message Formats

### On Checkpoint

```
docs(checkpoint): lesson 3.1 layer L1

Checkpoint saved at 2026-03-31 14:32
Layer: L1
Lesson: 3.1

Concepts covered:
- Hook system architecture
- Lifecycle events
- Registration patterns

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### On Finish

```
docs(lesson): complete lesson 3.1

6-tier synthesis completed at 2026-03-31 15:45
- Master lesson documentation
- Cumulative context bridge
- Interactive HTML presentations
- Quick reference cheatsheet
- Flashcards
- Discovery updates

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Commit Type Prefixes (Conventional Commits)

| Action | Prefix | Example |
|--------|--------|---------|
| Checkpoint | `docs(checkpoint):` | `docs(checkpoint): lesson 3.1 layer L1` |
| Finish | `docs(lesson):` | `docs(lesson): complete lesson 3.1` |
| Rewind | `refactor(checkpoint):` | `refactor(checkpoint): rewind to L1` |

---

## Pre-Commit Quality Hook

**Location**: `.git/hooks/pre-commit`

Runs automatically on every `git commit`. Validates checkpoint files before allowing the commit to proceed.

### Four Quality Dimensions (25 points each, 100 total)

| Dimension | Points | Checks |
|-----------|--------|--------|
| **Completeness** | 25 | Terminology table, What Goes Wrong, comprehension questions, connections, real-world applications |
| **Clarity** | 25 | ≥3 examples, ≥1 analogy, ≥1 diagram/table, code snippets with explanations, step-by-step procedures |
| **Professionalism** | 25 | No typos, consistent heading levels, proper markdown, no "Let me..." artifacts, professional voice |
| **Actionability** | 25 | ≥3 executable examples, exercises with expected outcomes, commands with explanations, troubleshooting guidance, next steps |

### Threshold Grading

| Score | Grade | Commit allowed? |
|-------|-------|----------------|
| 90–100 | Excellent | Yes |
| 80–89 | Good | Yes |
| 70–79 | Pass | Yes |
| 60–69 | Needs Improvement | No — blocked |
| 0–59 | Fail | No — blocked |

### Quality Gate Output: Passing

```
┌─────────────────────────────────────────────────────────┐
│   PRE-COMMIT QUALITY GATE                               │
└─────────────────────────────────────────────────────────┘
ℹ Found checkpoint files to validate:
  - revision-notes/3.1-L1-hook-architecture.md

✓ Lesson 3.1 passed (score: 87/100)

Validation Summary:
  ✓ Lesson 3.1: 87/100 (PASS)

✓ QUALITY GATE PASSED
```

### Quality Gate Output: Failing

```
✗ Quality checks failed! Commit blocked.

  Lesson 3.1: 52/100 (FAIL)
  - Completeness: 18/25 (missing: exercises, next steps)
  - Clarity: 12/25 (missing: examples, analogies)
  - Professionalism: 15/25
  - Actionability: 7/25 (no runnable examples!)

  To fix:
    1. Review the validation output above
    2. Improve the checkpoint content to meet quality standards
    3. Run: ./scripts/validate-notes.sh 3.1 to re-check
    4. Try committing again after fixes

  Emergency bypass (NOT recommended):
    git commit --no-verify
```

### Changing the Minimum Score

Edit `.git/hooks/pre-commit`, line 26:

```bash
readonly MIN_SCORE=70  # Change to 80 for strict, 60 for lenient
```

---

## Tagging Convention

| Event | Tag format | Example |
|-------|-----------|---------|
| Lesson complete | `lesson-{X.Y}` | `lesson-3.1` |
| Chapter complete | `chapter-{N}-complete` | `chapter-3-complete` |
| Milestone | `milestone-{name}` | `milestone-part1-complete` |

### Manage Tags

```bash
git tag -l                                     # List all tags
git tag -d lesson-3.1                          # Delete tag locally
git push origin :refs/tags/lesson-3.1          # Delete tag remotely
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Commit blocked by quality check | Score < 70/100 | Run `./scripts/validate-notes.sh 3.1`, review output, improve content |
| Push failed | Remote conflict | `git pull origin main` then retry |
| No remote configured | No origin set | `git remote add origin {url}` |
| Tag already exists | Re-running Finish | `git tag -d lesson-3.1` then retry |
| Pre-commit hook not executing | Hook not executable | `chmod +x .git/hooks/pre-commit` |

---

## Disabling and Re-Enabling Auto-Push

```bash
# Disable (rename script)
mv scripts/git-auto-push.py scripts/git-auto-push.py.disabled

# Re-enable
mv scripts/git-auto-push.py.disabled scripts/git-auto-push.py
```

---

## Advanced Usage

### Batch commit multiple lessons

```bash
for lesson in 3.1 3.15 3.17; do
    python3 scripts/git-auto-push.py finish $lesson
done
```

### Manually run quality validation

```bash
./scripts/validate-notes.sh 3.1    # Validate a specific lesson
./scripts/validate-notes.sh all    # Validate all lessons
```
