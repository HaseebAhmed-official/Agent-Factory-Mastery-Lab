# Finish / End Command Reference

## Quick Reference

| Item | Detail |
|------|--------|
| **Primary trigger** | `Finish` |
| **Alias** | `End` (backward compatible, identical behavior) |
| **Requires confirmation** | Yes — type `YES` after the confirmation dialog |
| **Ends lesson?** | Yes — lesson is marked complete in the context bridge |
| **Output tiers** | 6 (notes, bridge, HTML, cheatsheet, assessments, flashcards) |
| **Git integration** | Auto-commit + tag + push (if configured) |
| **Analogy** | Level complete screen (vs. Checkpoint = save game mid-level) |

---

## Overview

The `Finish` command (or its alias `End`) executes the full six-tier knowledge synthesis for the current lesson. It aggregates all checkpoint parts, generates interactive HTML presentations, produces a quick-reference cheatsheet, creates Anki-compatible flashcards, updates discovery indexes, and marks the lesson complete in the cumulative context bridge.

---

## Confirmation Dialog

After typing `Finish`, a confirmation message lists everything that will be created. Type `YES` to proceed, or anything else to cancel.

Example confirmation prompt:

```
Professor Agent:
This will complete Lesson 3.1 and generate:
📚 Final notes (L3 part file)
🎨 HTML presentations (master + L1/L2/L3 individual)
📋 Quick reference cheatsheet
🃏 Flashcards (Anki-compatible)
🔍 Discovery index update

Type YES to proceed or anything else to cancel.
```

---

## Full 10-Step Workflow

| Step | Action |
|------|--------|
| 1 | Fetches `Knowledge_Vault/Protocols/finish-synthesis.md` and executes six-tier synthesis |
| 2 | Creates final part file `{X.Y}-L{N}-{concept}.md` — only if new content exists since the last checkpoint |
| 3 | Reads ALL `{X.Y}-L*-*.md` files from the lesson directory |
| 4 | Generates **master navigation HTML**: overview + checkpoint cards linking to individual HTMLs |
| 5 | Generates **individual checkpoint HTMLs**: one focused presentation per layer (L1, L2, L3...) |
| 6 | Generates **quick reference cheatsheet**: `quick-reference/lesson-{X.Y}-cheatsheet.md` (2–3 pages) |
| 7 | Generates **flashcards**: `flashcards/lesson-{X.Y}-deck.json` (Anki-compatible) |
| 8 | Updates **discovery systems**: `visual-presentations/INDEX.html` and concept map data |
| 9 | Final update to `context-bridge/master-cumulative.md` — lesson marked complete |
| 10 | Confirms with paths to all created files, then offers: "Continue to next lesson or end session?" |

### Confirmation message format

```
Lesson {X.Y} complete. 6-tier synthesis finished. HTML presentations created at {paths}.
```

---

## Files Created

| File | Description |
|------|-------------|
| `revision-notes/{lesson}/{X.Y}-L{N}-{concept}.md` | Final part file (only if new content since last checkpoint) |
| `context-bridge/master-cumulative.md` | Updated — lesson marked complete |
| `context-bridge/status.json` | Updated |
| `context-bridge/backup/master-cumulative-{DATE}.md` | Backup created before write |
| `visual-presentations/session-{NN}-lesson-{X.Y}-{lesson-kebab-title}.html` | Master navigation HTML |
| `visual-presentations/session-{NN}-lesson-{X.Y}-L{N}-presentation.html` | One file per checkpoint layer |
| `visual-presentations/INDEX.html` | Updated lesson index |
| `quick-reference/lesson-{X.Y}-cheatsheet.md` | 2–3 page condensed summary |
| `flashcards/lesson-{X.Y}-deck.json` | Anki-compatible flashcard deck |

---

## The 6-Tier Knowledge System

| Tier | Location | Purpose |
|------|----------|---------|
| T1: Context Bridge | `context-bridge/master-cumulative.md` | Session continuity across conversations |
| T2: Master Notes | `revision-notes/.../X.Y-LN-concept.md` | Deep revision guide per checkpoint layer |
| T3: Visual Presentation | `visual-presentations/session-NN-*.html` | Interactive slide deck for review |
| T4: Quick Reference | `quick-reference/lesson-X.Y-cheatsheet.md` | 2–3 page summary for fast recall |
| T5: Assessments | `assessments/lesson-X.Y-quiz.md` | Quiz questions for self-testing |
| T6: Flashcards | `flashcards/lesson-X.Y-deck.json` | Spaced repetition cards (Anki) |

---

## HTML Presentation Details

### Master Navigation HTML

**File**: `session-{NN}-lesson-{X.Y}-{lesson-kebab-title}.html`

- Overview of the entire lesson
- Checkpoint cards — click any card to open its individual checkpoint HTML
- Aggregates all layers (L1 + L2 + L3 and beyond)

### Individual Checkpoint HTMLs

**File**: `session-{NN}-lesson-{X.Y}-L{N}-presentation.html`

- Focused review of a single checkpoint layer
- "Back to Master" navigation button
- Only that checkpoint's concepts — no overlap with other layers

### Design Specification (polished keynote-style)

- Fullscreen slides with arrow key / click / swipe navigation
- Dot indicators for slide position
- Animated transitions between slides
- CSS-drawn diagrams — no ASCII art
- Hover reveals and accordion sections
- Flip cards for vocabulary terms
- Light professional theme: off-white background, indigo/cyan accents, clean typography
- Must feel like a polished keynote presentation, not a text document

---

## Quick Reference Cheatsheet Details

**File**: `quick-reference/lesson-{X.Y}-cheatsheet.md`

Content included:

- Essential vocabulary (table format)
- Key frameworks (compact formulas)
- Decision trees (when to use X vs Y)
- Common pitfalls (top anti-patterns)
- Quick commands (code snippets)

Use cases:

- Coding / implementation reference while building
- Exam prep cram sheet
- Quick refresher before starting the next lesson

---

## Flashcard Details

**File**: `flashcards/lesson-{X.Y}-deck.json`

### Card types generated

| Card type | Front | Back |
|-----------|-------|------|
| Vocabulary | Term | Definition |
| Concept | Question | Explanation |
| Anti-pattern | What goes wrong? | Problem description + fix |
| Framework | Explain the framework | Formula + application example |

### Format

Anki-compatible JSON — importable directly into the Anki desktop or mobile app.

### Review workflow

1. Lesson completes → flashcards auto-generated in `flashcards/`
2. Import the `.json` deck into the Anki app
3. Review daily (5–15 minutes per session)
4. Anki automatically schedules cards based on your recall performance

---

## Example Full Interaction

```
You: Finish

Professor Agent:
This will complete Lesson 3.1 and generate:
📚 Final notes (L3 part file)
🎨 HTML presentations (master + L1/L2/L3 individual)
📋 Quick reference cheatsheet
🃏 Flashcards (Anki-compatible)
🔍 Discovery index update

Type YES to proceed or anything else to cancel.

You: YES

Professor Agent:
⏳ Running 6-tier synthesis for Lesson 3.1...

✅ Lesson 3.1 complete — 6-tier synthesis finished

Files created:

📚 Master Notes (3 checkpoint parts):
  - revision-notes/ch3/3.1-L1-hook-architecture.md
  - revision-notes/ch3/3.1-L2-custom-hooks.md
  - revision-notes/ch3/3.1-L3-advanced-patterns.md

🌉 Context Bridge (updated):
  - context-bridge/master-cumulative.md (lesson marked complete)

🎨 Visual Presentations:
  - visual-presentations/session-01-lesson-3.1-hook-architecture.html (master)
  - visual-presentations/session-01-lesson-3.1-L1-presentation.html
  - visual-presentations/session-01-lesson-3.1-L2-presentation.html
  - visual-presentations/session-01-lesson-3.1-L3-presentation.html
  - visual-presentations/INDEX.html (updated)

📋 Quick Reference:
  - quick-reference/lesson-3.1-cheatsheet.md

🃏 Flashcards:
  - flashcards/lesson-3.1-deck.json (28 cards)

Next Steps:
1. Review master HTML in browser
2. Study with flashcards (import to Anki)
3. Type "lesson 3.2" or "continue" to start next lesson
```

---

## Recommended Review Order After Finish

| Order | Resource | Why |
|-------|----------|-----|
| 1 | HTML presentation (`visual-presentations/`) | Visual and interactive — best for first pass review |
| 2 | Full notes (`revision-notes/`) | Deep study — all concepts in written form |
| 3 | Quick reference (`quick-reference/`) | Rapid recall test — can you remember without reading? |
| 4 | Flashcards (`flashcards/`) | Spaced repetition — review daily in Anki |

---

## After Finish — Continuing the Course

Once the lesson is marked complete, available actions:

- Type `lesson 3.2` (or any specific lesson number) to jump directly to that lesson
- Type `continue` to proceed to the next lesson in sequence
- Type `Status` to view overall curriculum progress and completion percentage
- Close the session — the context bridge is saved; the next session will display the recovery banner automatically

---

## Git Integration (Automatic)

After Step 9, if git is configured, the following runs automatically:

```bash
python3 scripts/git-auto-push.py finish {X.Y}
```

Actions performed:

- Stages ALL lesson artifacts (~10–20 files)
- Creates semantic commit: `docs(lesson): complete lesson {X.Y}`
- Creates git tag: `lesson-{X.Y}` (e.g., `lesson-3.1`)
- Pushes commit and tags to the remote
- If GitHub Pages is configured: triggers the auto-deploy workflow

See `11-git-integration-commands.md` for full git integration details.

---

## Finish vs. Checkpoint Comparison

| | Checkpoint | Finish |
|---|---|---|
| Ends lesson? | No — teaching continues immediately | Yes — lesson marked complete |
| Creates HTML? | No | Yes (master + one per layer) |
| Creates flashcards? | No | Yes |
| Creates cheatsheet? | No | Yes |
| Creates git tag? | No | Yes (`lesson-X.Y`) |
| Stages ~10–20 files? | No (checkpoint files only) | Yes |
| Analogy | Save game mid-level | Level complete screen |

---

## Verify the Output

Run these commands in the terminal to confirm all files were created:

```bash
ls visual-presentations/   # Check HTML files exist
ls flashcards/             # Check flashcard JSON exists
ls quick-reference/        # Check cheatsheet exists
python3 scripts/generate-index.py  # Rebuild INDEX.html if needed
```
