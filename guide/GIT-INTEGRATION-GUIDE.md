# Git Integration Guide

> **Agent Factory Part 1 - Checkpoint System**
> **Version**: 1.0.0
> **Last Updated**: 2026-03-03

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Components](#components)
5. [Workflows](#workflows)
6. [Configuration](#configuration)
7. [Quality Gates](#quality-gates)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)
10. [Best Practices](#best-practices)

---

## Overview

The Git Integration system automatically commits and tags checkpoint files to version control, ensuring:

- **Automatic version history** for all lesson content
- **Quality validation** before commits (via pre-commit hooks)
- **Semantic commit messages** following Conventional Commits
- **Milestone tagging** at lesson completion
- **GitHub Pages integration** (auto-deploy on push)

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     USER TRIGGERS COMMAND                     │
│                  Checkpoint  /  Finish                        │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              CHECKPOINT/FINISH PROTOCOL                       │
│  (1) Create files  (2) Update bridge  (3) Generate HTML      │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   GIT AUTO-PUSH SCRIPT                        │
│            scripts/git-auto-push.py                           │
│  • Auto-detect remote                                         │
│  • Stage relevant files                                       │
│  • Create semantic commit message                             │
│  • Tag (on Finish only)                                       │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   PRE-COMMIT HOOK                             │
│            .git/hooks/pre-commit                              │
│  • Validate quality scores                                    │
│  • Check completeness                                         │
│  • Block low-quality commits                                  │
└─────────────────────────┬────────────────────────────────────┘
                          │
               ┌──────────┴──────────┐
               │                     │
               ▼                     ▼
        ✓ PASS                   ✗ FAIL
               │                     │
               ▼                     ▼
       Git commit created    Commit blocked
       Push to remote        User notified
       Tag created (Finish)
```

---

## Quick Start

### 1. Enable Git Integration (3 Steps)

```bash
# Step 1: Initialize git repo (if not already done)
cd "/root/code/Agent-Factory-Part 1-test-prep"
git init
git branch -M main

# Step 2: Add remote (GitHub, GitLab, etc.)
git remote add origin https://github.com/yourusername/agent-factory-notes.git

# Step 3: Verify setup
python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L1
```

### 2. Test the Integration

```bash
# Dry run (shows what would happen without making changes)
python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L1

# Expected output:
# ═══════════════════════════════════════════════════════
#    Checkpoint Auto-Push: Lesson 3.1 Layer L1
# ═══════════════════════════════════════════════════════
# ℹ [DRY RUN] Would stage: revision-notes/**/module*/3.1-*/3.1-L1-*.md
# ℹ [DRY RUN] Would commit with message:
#   docs(checkpoint): lesson 3.1 layer L1
#   ...
```

### 3. Use During Learning

The integration runs **automatically** when you use checkpoint commands:

1. **During lesson** → Type `Checkpoint`
2. System saves files
3. System auto-commits to git (if enabled)
4. **At lesson end** → Type `Finish`
5. System creates all artifacts (HTML, flashcards, etc.)
6. System auto-commits and creates tag `lesson-3.1`

---

## Features

### 1. Auto-Commit on Checkpoint

**What it does**:
- Stages checkpoint part files, bridge updates, metadata
- Creates semantic commit message
- Validates quality via pre-commit hook
- Pushes to remote if configured

**Commit message format**:
```
docs(checkpoint): lesson 3.1 layer L1

Checkpoint saved at 2026-03-03 14:32
Layer: L1
Lesson: 3.1

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 2. Auto-Tag on Finish

**What it does**:
- Stages ALL lesson artifacts (notes, HTML, flashcards, indexes)
- Creates semantic commit message
- Creates git tag: `lesson-{X.Y}`
- Pushes commit and tags to remote

**Tag format**:
```
Tag: lesson-3.1
Message: Lesson 3.1 complete (6-tier synthesis)
```

**Commit message format**:
```
docs(lesson): complete lesson 3.1

6-tier synthesis completed at 2026-03-03 15:45
- Master lesson documentation
- Cumulative context bridge
- Interactive HTML presentations
- Quick reference cheatsheet
- Flashcards
- Discovery updates

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 3. Quality Validation (Pre-Commit Hook)

**What it does**:
- Automatically runs before every commit
- Validates checkpoint files using `scripts/validate-notes.sh`
- Blocks commits with quality scores below 70/100
- Provides detailed feedback on what needs improvement

**Quality dimensions checked**:
1. **Completeness** (25 points) - All required sections present
2. **Clarity** (25 points) - Examples, analogies, diagrams included
3. **Professionalism** (25 points) - No typos, consistent formatting
4. **Actionability** (25 points) - Exercises, hands-on practice included

### 4. Semantic Commit Messages

Follows [Conventional Commits](https://www.conventionalcommits.org/) specification:

| Action | Prefix | Example |
|--------|--------|---------|
| Checkpoint | `docs(checkpoint):` | `docs(checkpoint): lesson 3.1 layer L1` |
| Finish | `docs(lesson):` | `docs(lesson): complete lesson 3.1` |
| Rewind | `refactor(checkpoint):` | `refactor(checkpoint): rewind to L1` |

---

## Components

### 1. Pre-Commit Hook

**Location**: `.git/hooks/pre-commit`

**Purpose**: Quality gate that validates notes before allowing commits

**Features**:
- Automatic execution on every `git commit`
- Detects staged checkpoint files
- Runs quality validation
- Blocks commits with scores < 70/100
- Colorized output with detailed feedback
- Bypass option: `git commit --no-verify` (emergency only)

**Example output**:
```bash
┌─────────────────────────────────────────────────────────┐
│   PRE-COMMIT QUALITY GATE                               │
└─────────────────────────────────────────────────────────┘

ℹ Found checkpoint files to validate:
  - revision-notes/3.1-L1-hook-architecture.md

ℹ Validating lesson 3.1...
✓ Lesson 3.1 passed (score: 87/100)

Validation Summary:
  ✓ Lesson 3.1: 87/100 (PASS)

✓ All quality checks passed! Commit allowed.

✓ QUALITY GATE PASSED
```

### 2. Auto-Push Script

**Location**: `scripts/git-auto-push.py`

**Purpose**: Intelligent auto-commit and push for checkpoints and finishes

**Features**:
- Auto-detects git remote (origin, upstream, etc.)
- Smart file staging (pattern-based)
- Semantic commit message generation
- Auto-tagging on Finish
- Conflict detection
- Dry-run mode for testing
- Skip quality checks option (use with caution)

**Usage**:
```bash
# Checkpoint auto-push
python3 scripts/git-auto-push.py checkpoint 3.1 L1

# Finish auto-push (with tagging)
python3 scripts/git-auto-push.py finish 3.1

# Dry run (test without making changes)
python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L2

# Skip quality checks (not recommended)
python3 scripts/git-auto-push.py --skip-quality finish 3.1
```

---

## Workflows

### Workflow 1: Normal Checkpoint

```
User types "Checkpoint"
    │
    ▼
Checkpoint protocol executes (Stages 1-5)
    │
    ├─ Create part file: 3.1-L1-concept.md
    ├─ Update bridge: session-01-cumulative.md
    └─ Update metadata: .checkpoint-meta.json
    │
    ▼
Git Auto-Push (Stage 6) - AUTOMATIC
    │
    ├─ Stage files matching patterns
    ├─ Create semantic commit message
    ├─ Run: git commit -m "..."
    │      │
    │      └─> Pre-commit hook runs
    │          ├─ Validate quality (validate-notes.sh)
    │          ├─ Score: 87/100 ✓ PASS
    │          └─ Allow commit
    │
    ├─ Detect remote: origin
    └─ Push to origin/main
    │
    ▼
User sees confirmation:
  📦 Git auto-commit:
  - Files staged: 3
  - Commit: "docs(checkpoint): lesson 3.1 layer L1"
  - Quality hook: ✓ Passed
  - Pushed to: origin/main
```

### Workflow 2: Finish with Tagging

```
User types "Finish"
    │
    ▼
Finish protocol executes (Stages 1-8)
    │
    ├─ Create final part file (if needed)
    ├─ Update bridge (mark complete)
    ├─ Generate HTMLs (master + individual)
    ├─ Generate quick reference
    ├─ Generate flashcards
    ├─ Update INDEX.md
    └─ Update concept map data
    │
    ▼
Git Auto-Push (Stage 9) - AUTOMATIC
    │
    ├─ Stage ALL lesson artifacts (~10-20 files)
    ├─ Create semantic commit message
    ├─ Run: git commit -m "..."
    │      │
    │      └─> Pre-commit hook runs (validates all)
    │
    ├─ Create tag: lesson-3.1
    ├─ Detect remote: origin
    └─ Push with tags: git push origin main --tags
    │
    ▼
GitHub Pages workflow triggers (if configured)
    │
    └─> Deploys HTMLs to https://yourusername.github.io/agent-factory-notes/
    │
    ▼
User sees confirmation:
  📦 Git auto-commit & tagging:
  - Files staged: 15
  - Commit: "docs(lesson): complete lesson 3.1"
  - Tag created: lesson-3.1
  - Quality hook: ✓ Passed
  - Pushed to: origin/main (with tags)
```

### Workflow 3: Quality Gate Failure

```
User types "Checkpoint"
    │
    ▼
Checkpoint protocol executes (Stages 1-5)
    │
    └─ Creates: 3.1-L1-concept.md (incomplete, missing examples)
    │
    ▼
Git Auto-Push attempts commit
    │
    └─> Pre-commit hook runs
        │
        ├─ Validate: 3.1-L1-concept.md
        ├─ Score: 52/100 ✗ FAIL
        │   - Completeness: 18/25
        │   - Clarity: 12/25
        │   - Professionalism: 15/25
        │   - Actionability: 7/25 (no examples!)
        │
        └─ BLOCK COMMIT
    │
    ▼
User sees error:
  ✗ Quality checks failed! Commit blocked.

  To fix:
    1. Review the validation output above
    2. Improve the checkpoint content to meet quality standards
    3. Run: ./scripts/validate-notes.sh 3.1 to re-check
    4. Try committing again after fixes

  To bypass (NOT recommended):
    git commit --no-verify
    │
    ▼
User improves content, retries Checkpoint
    │
    └─> Quality check passes (85/100) → Commit succeeds
```

---

## Configuration

### 1. Minimum Quality Score

**File**: `.git/hooks/pre-commit`

**Default**: 70/100

**To change**:
```bash
# Edit line 26
readonly MIN_SCORE=70  # Change to desired threshold (e.g., 80, 90)
```

**Recommended values**:
- **70** - Balanced (default)
- **80** - Strict (high quality required)
- **60** - Lenient (learning mode)

### 2. Strict Mode

**File**: `.git/hooks/pre-commit`

**Default**: Disabled

**To enable**:
```bash
# Edit line 27
readonly STRICT_MODE=true  # Blocks commits with ANY warnings
```

### 3. Auto-Push Enabled/Disabled

**To disable auto-push**:
```bash
# Option 1: Remove the script
rm scripts/git-auto-push.py

# Option 2: Rename it
mv scripts/git-auto-push.py scripts/git-auto-push.py.disabled

# Option 3: Make non-executable
chmod -x scripts/git-auto-push.py
```

**To re-enable**:
```bash
chmod +x scripts/git-auto-push.py
```

### 4. Remote Detection

The script auto-detects remotes in this order:
1. `origin` (preferred)
2. First available remote

**To force a specific remote**:
```bash
# Edit scripts/git-auto-push.py, line 48
DEFAULT_REMOTE = "upstream"  # Change from "origin"
```

---

## Quality Gates

### Validation Dimensions

The pre-commit hook validates four dimensions:

#### 1. Completeness (25 points)

Checks for required sections:
- [x] Terminology table
- [x] What Goes Wrong framework
- [x] Comprehension questions
- [x] Knowledge connections
- [x] Real-world applications

**Scoring**:
- 5 points per required section
- Full points if all present
- Partial credit if incomplete

#### 2. Clarity (25 points)

Checks for pedagogical aids:
- [x] At least 3 examples
- [x] At least 1 analogy
- [x] At least 1 diagram/table/ASCII art
- [x] Code snippets with explanations
- [x] Step-by-step procedures

**Scoring**:
- 5 points per clarity element
- Full points if all present

#### 3. Professionalism (25 points)

Checks for quality markers:
- [x] No obvious typos
- [x] Consistent heading levels
- [x] Proper markdown formatting
- [x] No conversational artifacts ("Let me...", "Great!")
- [x] Professional voice (imperative/third-person)

**Scoring**:
- 5 points per professionalism check
- Deductions for violations

#### 4. Actionability (25 points)

Checks for hands-on practice:
- [x] At least 3 executable examples
- [x] Exercises with expected outcomes
- [x] Commands with explanations
- [x] Troubleshooting guidance
- [x] Next steps clearly defined

**Scoring**:
- 5 points per actionability element
- Full points if all present

### Threshold Grading

| Score | Grade | Action |
|-------|-------|--------|
| 90-100 | **Excellent** | ✓ Commit allowed |
| 80-89 | **Good** | ✓ Commit allowed |
| 70-79 | **Pass** | ✓ Commit allowed |
| 60-69 | **Needs Improvement** | ✗ Commit blocked |
| 0-59 | **Fail** | ✗ Commit blocked |

---

## Troubleshooting

### Problem 1: Commit Blocked by Quality Check

**Symptoms**:
```
✗ Quality checks failed! Commit blocked.
```

**Solutions**:

1. **Check validation output**:
   ```bash
   ./scripts/validate-notes.sh 3.1
   ```

2. **Identify low-scoring dimension**:
   - Completeness → Add missing sections
   - Clarity → Add examples, analogies, diagrams
   - Professionalism → Fix typos, formatting
   - Actionability → Add exercises, runnable examples

3. **Improve content and retry**:
   ```
   # In teaching session, continue adding content
   # Then type "Checkpoint" again
   ```

4. **Emergency bypass** (NOT recommended):
   ```bash
   git commit --no-verify -m "emergency save"
   ```

### Problem 2: Push Failed

**Symptoms**:
```
⚠ Push failed. You may need to pull first.
```

**Solutions**:

1. **Pull changes first**:
   ```bash
   git pull origin main
   ```

2. **Resolve conflicts** (if any):
   ```bash
   git status
   git mergetool  # Or manually edit conflicted files
   git add .
   git commit
   ```

3. **Retry push**:
   ```bash
   git push origin main
   ```

### Problem 3: No Remote Configured

**Symptoms**:
```
⚠ No git remote configured. Skipping push.
```

**Solutions**:

1. **Add remote**:
   ```bash
   git remote add origin https://github.com/yourusername/repo.git
   ```

2. **Verify**:
   ```bash
   git remote -v
   ```

### Problem 4: Tag Already Exists

**Symptoms**:
```
⚠ Tag 'lesson-3.1' already exists, skipping
```

**Solutions**:

1. **List existing tags**:
   ```bash
   git tag -l
   ```

2. **Delete tag locally** (if re-running Finish):
   ```bash
   git tag -d lesson-3.1
   ```

3. **Delete tag remotely** (if already pushed):
   ```bash
   git push origin :refs/tags/lesson-3.1
   ```

4. **Retry Finish command**

### Problem 5: Pre-Commit Hook Not Executing

**Symptoms**:
- Commits succeed even with low-quality content
- No validation output shown

**Solutions**:

1. **Check hook exists**:
   ```bash
   ls -la .git/hooks/pre-commit
   ```

2. **Make executable**:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

3. **Test manually**:
   ```bash
   .git/hooks/pre-commit
   ```

---

## Advanced Usage

### 1. Manual Commit (Without Auto-Push)

```bash
# Disable auto-push temporarily
mv scripts/git-auto-push.py scripts/git-auto-push.py.disabled

# Run checkpoint/finish (no auto-commit)
# ... teaching session ...

# Manually commit
git add revision-notes/3.1-*
git commit -m "docs(checkpoint): lesson 3.1 layer L1"

# Re-enable auto-push
mv scripts/git-auto-push.py.disabled scripts/git-auto-push.py
```

### 2. Batch Commit Multiple Lessons

```bash
# If you've completed multiple lessons without git
for lesson in 3.1 3.15 3.17; do
    python3 scripts/git-auto-push.py finish $lesson
done
```

### 3. Rebase and Clean History

```bash
# Interactive rebase to clean up commits
git rebase -i HEAD~10

# Squash checkpoint commits into lesson commit
# In editor:
#   pick abc1234 docs(lesson): complete lesson 3.1
#   squash def5678 docs(checkpoint): lesson 3.1 layer L1
#   squash ghi9012 docs(checkpoint): lesson 3.1 layer L2
```

### 4. Create Release Branches

```bash
# Create chapter release branch
git checkout -b chapter-3-complete

# Include all chapter 3 lessons
git cherry-pick lesson-3.1..lesson-3.23

# Push branch
git push origin chapter-3-complete
```

### 5. GitHub Actions Integration

Create `.github/workflows/validate-on-pr.yml`:

```yaml
name: Validate Notes on PR

on:
  pull_request:
    paths:
      - 'revision-notes/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate quality
        run: |
          chmod +x scripts/validate-notes.sh
          ./scripts/validate-notes.sh all
```

---

## Best Practices

### 1. Commit Frequency

**Recommended**:
- **Checkpoint**: Every 30-45 minutes of teaching (natural concept boundaries)
- **Finish**: At lesson completion (every 2-4 hours)

**Why**:
- Smaller, focused commits
- Easier to review and revert
- Better change history

### 2. Commit Messages

**Good**:
```
docs(checkpoint): lesson 3.1 layer L1

Checkpoint saved at 2026-03-03 14:32
Layer: L1
Lesson: 3.1

Concepts covered:
- Hook system architecture
- Lifecycle events
- Registration patterns
```

**Bad**:
```
update files
checkpoint
wip
```

### 3. Quality Thresholds

**For learning** (initial study):
- Minimum score: 70/100
- Focus on completeness

**For review** (exam prep):
- Minimum score: 85/100
- Require all dimensions

**For publishing** (share with others):
- Minimum score: 90/100
- Strict mode enabled

### 4. Branching Strategy

**Main branch**: Completed, high-quality lessons only

**Feature branches**: Work in progress
```bash
git checkout -b lesson-3.1-wip
# ... work on lesson ...
git checkout main
git merge lesson-3.1-wip
```

**Backup branches**: Before major revisions
```bash
git branch backup-lesson-3.1
# ... make risky changes ...
# If needed: git checkout backup-lesson-3.1
```

### 5. Tag Naming

**Lesson completion**:
- Format: `lesson-{X.Y}`
- Example: `lesson-3.1`, `lesson-3.15`

**Chapter completion**:
- Format: `chapter-{N}-complete`
- Example: `chapter-3-complete`

**Milestones**:
- Format: `milestone-{name}`
- Example: `milestone-part1-complete`

---

## Integration with Other Tools

### GitHub Pages

Tags trigger auto-deployment:
```yaml
# .github/workflows/publish-pages.yml
on:
  push:
    tags:
      - 'lesson-*'
      - 'chapter-*-complete'
```

### Anki Sync

Export flashcards on tag:
```bash
# After finish creates tag
git tag -l | grep lesson-3.1
python3 scripts/export-flashcards-to-anki.py flashcards/lesson-3.1-deck.json
```

### Obsidian Git Plugin

Auto-sync with Obsidian:
1. Install "Obsidian Git" community plugin
2. Configure auto-commit interval
3. Integrates with pre-commit hook

---

## Summary

The Git Integration system provides:

✅ **Automatic version control** for all lesson content
✅ **Quality validation** before every commit
✅ **Semantic commit history** for easy navigation
✅ **Milestone tagging** at lesson completion
✅ **GitHub integration** for web deployment
✅ **Rollback capability** to any checkpoint
✅ **Collaboration support** via standard git workflows

**Next steps**:
1. Initialize git and add remote
2. Test with dry-run
3. Start learning with automatic commits
4. Deploy to GitHub Pages (see GITHUB-PAGES-SETUP.md)
5. Import to Obsidian (see OBSIDIAN-GUIDE.md in guide directory)

---

**Questions or issues?** Check the [Troubleshooting](#troubleshooting) section or consult the checkpoint system documentation.
