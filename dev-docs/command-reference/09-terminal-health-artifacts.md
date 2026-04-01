# 09 — Terminal: Health & Artifacts Reference

Run all commands from the repo root:

```bash
cd /root/code/Agent-Factory-Mastery-Lab/.claude/worktrees/updating-stuff
```

---

## Quick Reference Table

| Command | Purpose | Expected output |
|---------|---------|----------------|
| `python3 scripts/health-check.py` | System health check | `✅ HEALTHY — All 3 checks passed` |
| `python3 scripts/session-start.py` | Session state as JSON | JSON with banner, session count, health |
| `python3 scripts/generate-html.py --demo` | Test HTML pipeline | `✅ HTML generated: visual-presentations/demo-...` |
| `python3 scripts/generate-html.py --lesson 3.1` | Generate HTML for lesson | `✅ HTML generated: visual-presentations/session-01-...` |
| `python3 scripts/generate-index.py` | Rebuild INDEX.html | `✅ INDEX.html generated` |

---

## health-check.py

### Command

```bash
python3 scripts/health-check.py
```

### Purpose

Verifies the system is healthy before/after a session. Run this first when anything seems wrong.

### What it checks

1. **Bridge file exists and is valid** — `context-bridge/master-cumulative.md` present and properly structured (all 18 sections)
2. **No orphaned .tmp files** — no `*.tmp` files in `context-bridge/` (indicates a failed write)
3. **status.json is valid** — `context-bridge/status.json` exists, valid JSON, no `repair_needed: true` flag

### Expected output (healthy)

```
✅ HEALTHY — All 3 checks passed
  ✓ Bridge file valid (18 sections)
  ✓ No orphaned .tmp files
  ✓ status.json valid, repair_needed: false
```

### Output when unhealthy

```
❌ UNHEALTHY — 1 of 3 checks failed
  ✓ Bridge file valid
  ✗ Orphaned .tmp files found: context-bridge/master-cumulative.md.tmp
  ✓ status.json valid

Action: Type "Repair" in Claude Code chat to fix.
```

### When to run

- At the START of every session (before opening Claude Code)
- After a `Checkpoint` to confirm it wrote successfully
- When the system seems to be behaving oddly
- After any unexpected crash or interruption

### If health check shows UNHEALTHY

1. Note which check failed
2. Open Claude Code
3. Type `Repair`
4. Re-run health check to confirm fixed

---

## session-start.py

### Command

```bash
python3 scripts/session-start.py
```

### Purpose

Shows session recovery information as JSON. Used to programmatically inspect what a new Claude Code session would see on startup.

### What it outputs

JSON containing:
- Recovery banner content (the message Claude shows at cold start)
- Session count (how many sessions have been run)
- Health status (same as health-check.py but in JSON format)
- Last lesson/layer/concept from status.json
- Bridge load status

### Expected output

```json
{
  "banner": "Context restored: Lesson 3.1 | Layer L2 | Last checkpoint: 2026-03-31 14:30",
  "session_count": 7,
  "health": "healthy",
  "lesson": "3.1",
  "layer": "L2",
  "concept": "Custom Hook Patterns",
  "repair_needed": false,
  "bridge_loaded": true
}
```

### When to use

- Debugging — to see exactly what Claude will be told on startup
- Scripting — if you want to programmatically read session state
- Verifying that status.json has the right data after a `Checkpoint`

---

## generate-html.py

### Commands

```bash
# Demo mode — test the pipeline
python3 scripts/generate-html.py --demo

# Generate HTML for a specific lesson
python3 scripts/generate-html.py --lesson 3.1
```

### Purpose

Generates an HTML presentation file for a lesson. The `--demo` flag creates a sample presentation to verify the HTML generation pipeline works.

### Prerequisites

```bash
pip install jinja2
```

### Expected output

Demo mode:

```
✅ HTML generated: visual-presentations/demo-2026-03-31-143022.html
```

Lesson mode:

```
✅ HTML generated: visual-presentations/session-01-lesson-3.1-hook-architecture.html
```

### When to use

- When `Finish` completed in chat but no HTML appeared in `visual-presentations/`
- To test the HTML pipeline is working (use `--demo`)
- When you want to manually regenerate an HTML without running `Finish` again

### What it generates

A polished keynote-style HTML presentation:
- Fullscreen slides with arrow-key/click/swipe navigation
- Dot indicators for slide position
- Animated transitions
- CSS-drawn diagrams (not ASCII)
- Flip cards for vocabulary
- Light professional theme (off-white, indigo/cyan accents)

### Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: jinja2` | Run `pip install jinja2` |
| Script runs but no file appears | Check `visual-presentations/` directory exists |
| HTML opens blank | Check browser console (F12) for errors |
| Script errors on lesson | Try `--demo` first to verify pipeline |

---

## generate-index.py

### Command

```bash
python3 scripts/generate-index.py
```

### Purpose

Rebuilds `visual-presentations/INDEX.html` — the master navigation page that lists all lesson presentations as clickable tiles.

### Expected output

```
✅ INDEX.html generated
   Lessons indexed: 5
   Output: visual-presentations/INDEX.html
```

### What INDEX.html contains

- A clickable tile/card for each completed lesson
- Each tile links to that lesson's master HTML presentation
- Tiles show: lesson number, title, checkpoint count, date completed
- Arrow-key/click navigation between tiles

### When to use

- After running `Finish` — to make the new lesson appear in the index
- If INDEX.html is missing or outdated
- After manually moving/renaming HTML files
- Part of Test Sequence C (Step 4)

### Verify it worked

```bash
ls visual-presentations/
# Should see INDEX.html
# Open in browser — lesson cards should appear
```

---

## Checking generated files

```bash
ls visual-presentations/          # HTML presentations + INDEX.html
ls flashcards/                    # JSON flashcard decks
ls quick-reference/               # Markdown cheatsheets
ls context-bridge/backup/         # Dated backup files
ls context-bridge/snapshots/      # Frozen checkpoint snapshots
```

---

## Setup — install dependencies

```bash
pip install jinja2    # Required for HTML generation
```
