# Command Reference — Master Index

> **One place for every command in the Agent Factory system.**
> Chat commands, terminal scripts, git integration, analytics, testing sequences.

---

## Quick Navigation

| # | File | What's Inside |
|---|------|---------------|
| 01 | [Teaching Commands](01-teaching-commands.md) | `start`, `lesson X.Y`, `continue`, `Next`, `Go slower`, `go deeper`, `explain`, `connect`, `anti-patterns` |
| 02 | [Checkpoint Command](02-checkpoint-command.md) | `Checkpoint` / `Save progress` — mid-lesson save, how it works, files created |
| 03 | [Finish / End Command](03-finish-end-command.md) | `Finish` / `End` — lesson completion, 6-tier synthesis, all artifacts |
| 04 | [Rewind Command](04-rewind-command.md) | `Rewind` — rollback to past checkpoint, branching, merge strategies |
| 05 | [Resume & Repair Commands](05-resume-repair-commands.md) | `Resume`, `Repair` — cold-start recovery, bridge repair |
| 06 | [Navigation & Status Commands](06-navigation-status-commands.md) | `Status`, `Verify`, `where am I?`, `what should I know so far?` |
| 07 | [Review & Quiz Commands](07-review-quiz-commands.md) | `quiz me`, `Review X.Y`, `review chapter X`, `exam prep` |
| 08 | [Export, Sync & Compare Commands](08-export-sync-compare-commands.md) | `Export X.Y`, `Sync`, `Compare` |
| 09 | [Terminal: Health & Artifacts](09-terminal-health-artifacts.md) | `health-check.py`, `session-start.py`, `generate-html.py`, `generate-index.py` |
| 10 | [Terminal: Backup & Bridge](10-terminal-backup-bridge.md) | `checkpoint-write.py`, `bridge-update.py`, hard reset script |
| 11 | [Git Integration Commands](11-git-integration-commands.md) | `git-auto-push.py`, pre-commit hook, quality gates, tagging |
| 12 | [Analytics & Migration Commands](12-analytics-migration-commands.md) | `analytics-dashboard.py`, `migrate-schema.py` |
| 13 | [Test Sequences A–F](13-test-sequences.md) | Six full end-to-end test scenarios with pass/fail criteria |
| 14 | [Troubleshooting Guide](14-troubleshooting.md) | Signs something is wrong + fixes for every known failure mode |
| 15 | [GitHub Pages Deployment](15-github-pages-deployment.md) | Publishing Finish outputs to the web via GitHub Actions |

---

## Command Decision Tree

```
What do you want to do?
│
├── LEARN something new ──────────────────────────── → 01 Teaching Commands
│
├── SAVE progress mid-lesson ─────────────────────── → 02 Checkpoint
│
├── COMPLETE a lesson (HTML + flashcards + ref) ───── → 03 Finish
│
├── GO BACK to an earlier state ───────────────────── → 04 Rewind
│
├── RESUME after closing Claude Code ─────────────── → 05 Resume
├── FIX a broken bridge or corrupted state ─────────── → 05 Repair
│
├── CHECK where you are / how much is done ─────────── → 06 Status / Verify
│
├── QUIZ yourself on past material ────────────────── → 07 Review / Quiz
│
├── EXPORT a bundle / SYNC new curriculum ──────────── → 08 Export / Sync / Compare
│
├── RUN terminal scripts ───────────────────────────── → 09 Health & Artifacts
│                                                         10 Backup & Bridge
│
├── USE git version control ────────────────────────── → 11 Git Integration
│
├── TRACK progress / UPGRADE schema ───────────────── → 12 Analytics & Migration
│
├── TEST the whole system ──────────────────────────── → 13 Test Sequences
│
├── SOMETHING IS BROKEN ────────────────────────────── → 14 Troubleshooting
│
└── PUBLISH to the web ─────────────────────────────── → 15 GitHub Pages
```

---

## Chat Commands — One-Line Summary

```
TEACHING                   SAVING                  NAVIGATION
─────────────────────────  ──────────────────────  ─────────────────────────
start / begin              Checkpoint              Resume
lesson X.Y                 Save progress           Rewind
continue                   Finish                  Status
Next                       End                     Verify
Go slower / simplify                               where am I?
go deeper                  REVIEW                  what should I know so far?
exercise                   quiz me
explain [term]             quiz me on chapter X    REPAIR
connect [A] to [B]         Review X.Y              Repair
show connections           review chapter X
anti-patterns              exam prep               EXPORT
                                                   Export X.Y
                                                   Sync
                                                   Compare
```

---

## Terminal Commands — One-Line Summary

```
HEALTH & STATUS                                ARTIFACTS
─────────────────────────────────────────────  ────────────────────────────────────
python3 scripts/health-check.py                python3 scripts/generate-html.py --demo
python3 scripts/session-start.py               python3 scripts/generate-index.py
cat context-bridge/status.json                 ls visual-presentations/
                                               ls flashcards/
                                               ls quick-reference/

BACKUP / UPDATE                                BRIDGE
─────────────────────────────────────────────  ────────────────────────────────────
python3 scripts/checkpoint-write.py            python3 scripts/bridge-update.py
  --action backup                                --section 17
  --action update-status                         --content "pipe-separated row"
  --lesson 3.1 --layer L1
  --concept "Hook Architecture"

ANALYTICS & MIGRATION
─────────────────────────────────────────────
python3 scripts/analytics-dashboard.py
python3 scripts/analytics-dashboard.py --lesson 3.1
python3 scripts/analytics-dashboard.py --export-html
python3 scripts/migrate-schema.py --version v2 --preview
python3 scripts/migrate-schema.py --version v2 --execute
python3 scripts/migrate-schema.py --rollback

GIT INTEGRATION
─────────────────────────────────────────────
python3 scripts/git-auto-push.py checkpoint 3.1 L1
python3 scripts/git-auto-push.py finish 3.1
python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L1
```

---

## What Each Command Creates

| Command | Files Created / Updated |
|---------|------------------------|
| **`Checkpoint`** | `revision-notes/{lesson}/X.Y-LN-concept.md`, `context-bridge/master-cumulative.md`, `context-bridge/status.json`, `context-bridge/backup/master-cumulative-DATE.md`, `context-bridge/snapshots/lesson-X.Y-LN-concept-snapshot.md` |
| **`Finish`** | All checkpoint files above + `visual-presentations/session-NN-lesson-X.Y.html`, `visual-presentations/session-NN-lesson-X.Y-LN-presentation.html`, `quick-reference/lesson-X.Y-cheatsheet.md`, `flashcards/lesson-X.Y-deck.json`, `visual-presentations/INDEX.html` |
| **`Rewind`** | Reads existing snapshots — no new files unless you choose "Continue from here" |
| **`Verify`** | Coverage report in chat only — no files written |
| **`Status`** | Dashboard in chat only — no files written |
| **`Export X.Y`** | `exports/lesson-X.Y-bundle.zip` |
| **`Sync`** | Updates `Knowledge_Vault/Curriculum/` with newly discovered lessons |

---

## 6-Tier Knowledge System

| Tier | Location | When Created |
|------|----------|--------------|
| **T1: Context Bridge** | `context-bridge/master-cumulative.md` | Every Checkpoint & Finish |
| **T2: Master Notes** | `revision-notes/.../X.Y-LN-concept.md` | Every Checkpoint & Finish |
| **T3: Visual Presentation** | `visual-presentations/session-NN-*.html` | Finish only |
| **T4: Quick Reference** | `quick-reference/lesson-X.Y-cheatsheet.md` | Finish only |
| **T5: Assessments** | `assessments/lesson-X.Y-quiz.md` | Manual / curriculum sync |
| **T6: Flashcards** | `flashcards/lesson-X.Y-deck.json` | Finish only |
