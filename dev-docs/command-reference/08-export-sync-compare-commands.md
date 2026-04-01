# Export, Sync & Compare Commands Reference

## Quick Reference Table

| Command | Purpose | Output | Files Written? |
|---------|---------|--------|---------------|
| `Export X.Y` | Bundle lesson for sharing/archiving | ZIP file in `exports/` | Yes — `.zip` |
| `Sync` | Discover new/updated curriculum lessons | Report in chat + updates `Knowledge_Vault/` | Yes — curriculum files |
| `Compare` | Diff between checkpoints, lessons, or curriculum | Diff report in chat | No |

---

## Export Command

### Trigger

```
Export X.Y
```

Example: `Export 3.1`

### What It Does

1. Fetches `Knowledge_Vault/Protocols/export-bundle.md`
2. Collects all files associated with lesson X.Y:
   - All revision notes (`{X.Y}-L*-*.md`)
   - HTML presentations (master navigation + all individual checkpoint HTMLs)
   - Quick reference cheatsheet (`quick-reference/lesson-X.Y-cheatsheet.md`)
   - Flashcards (`flashcards/lesson-X.Y-deck.json`)
   - Context bridge excerpt (lesson-specific section of `master-cumulative.md`)
3. Packages everything into a single ZIP file
4. Reports the output path and bundle contents

### Output File

```
exports/lesson-{X.Y}-bundle.zip
```

### Bundle Contents

| File | Description |
|------|-------------|
| `lesson-X.Y-notes-L1.md` | L1 checkpoint notes |
| `lesson-X.Y-notes-L2.md` | L2 checkpoint notes (if exists) |
| `lesson-X.Y-notes-L3.md` | L3 checkpoint notes (if exists) |
| `lesson-X.Y-presentation.html` | Master navigation HTML |
| `lesson-X.Y-L1-presentation.html` | Individual L1 checkpoint HTML |
| `lesson-X.Y-cheatsheet.md` | Quick reference cheatsheet |
| `lesson-X.Y-deck.json` | Anki-compatible flashcard deck |
| `lesson-X.Y-bridge-excerpt.md` | Context bridge excerpt for the lesson |

### Prerequisites

- Lesson X.Y must have at least one saved checkpoint (nothing to bundle otherwise)
- `Finish` should have been run first to ensure HTML presentations and flashcards exist

### Use Cases

- Share a completed lesson with a study partner or mentor
- Submit lesson notes for review
- Create an offline archive before major revisions
- Back up lesson content independently of the git repository

### Example Interaction

```
You: Export 3.1

Professor Agent:
Bundling Lesson 3.1...

✅ Bundle created: exports/lesson-3.1-bundle.zip

Contents (9 files):
  - lesson-3.1-notes-L1.md (Hook Architecture)
  - lesson-3.1-notes-L2.md (Custom Hooks)
  - lesson-3.1-notes-L3.md (Advanced Patterns)
  - lesson-3.1-presentation.html (master)
  - lesson-3.1-L1-presentation.html
  - lesson-3.1-L2-presentation.html
  - lesson-3.1-L3-presentation.html
  - lesson-3.1-cheatsheet.md
  - lesson-3.1-deck.json (28 cards)

Share: exports/lesson-3.1-bundle.zip
```

---

## Sync Command

### Trigger

```
Sync
```

### What It Does

1. Fetches `Knowledge_Vault/Protocols/sync-curriculum.md`
2. Compares the current state of `Knowledge_Vault/Curriculum/` against the upstream curriculum source
3. Detects:
   - **New lessons** — lessons in the curriculum not yet present in `Knowledge_Vault/`
   - **Updated lessons** — lessons where curriculum content has changed since the last sync (new exercises, revised explanations, etc.)
   - **No changes** — lessons already up to date
4. Updates `Knowledge_Vault/Curriculum/` with newly discovered or changed lesson files
5. Reports findings in chat

Sync does **not** begin teaching new content automatically. It only updates curriculum files.

### Output Format

```
Sync Report
───────────────────────────────────────
Last sync: 2026-03-01 10:00

✅ New lessons discovered: 2
  - Lesson 3.24 — Advanced Orchestration Patterns
  - Lesson 3.25 — Error Recovery Strategies

🔄 Updated lessons: 1
  - Lesson 3.1 — Hook Architecture (exercises updated)

✓ Up to date: 22 lessons

Knowledge_Vault updated. Type "lesson 3.24" to start a new lesson.
───────────────────────────────────────
```

### What Sync Does NOT Do

- Start teaching new content automatically
- Change your progress, checkpoints, or revision notes
- Overwrite existing notes or presentations

### When to Use Sync

- When new lessons may have been added to the course
- At the start of a new chapter to ensure the curriculum is current
- When `Verify` reports topics that seem missing from curriculum files
- Periodically (every few weeks) to stay current with course updates

---

## Compare Command

### Trigger

```
Compare
```

### What It Does

1. Fetches `Knowledge_Vault/Protocols/compare-diff.md`
2. Prompts you to choose what to compare
3. Generates a structured diff and displays it in chat

No files are written — output is chat-only.

### Compare Options

| Option | What It Compares |
|--------|-----------------|
| Two checkpoint layers | Shows what changed between L1 and L2, L2 and L3, etc. |
| Checkpoint vs. curriculum | Shows what topics are covered in your notes vs. the official curriculum |
| Two lessons | Shows conceptual overlap and differences between two separate lessons |

### Interactive Prompt

After typing `Compare`, Professor Agent presents a menu:

```
Professor Agent:
What would you like to compare?

1. Two checkpoint layers (e.g., L1 vs L2)
2. A checkpoint against the official curriculum
3. Two lessons against each other

Your choice (1/2/3):
```

### Example — Comparing Two Checkpoint Layers

```
You: Compare
You: 1

Professor Agent:
Which layers? (e.g., L1 vs L2)

You: L1 vs L2

Professor Agent:
Diff: Lesson 3.1 — L1 vs L2
─────────────────────────────────────────────
L1 (Hook Architecture — Fundamentals):
  + Hook System overview
  + Lifecycle phases (init, execute, cleanup)
  + Basic registration pattern

L2 (Custom Hooks — Intermediate):
  + Custom hook creation
  + Composition strategies
  + Hook chaining patterns
  ← Builds on L1: Uses lifecycle knowledge from L1

Overlap: None (clean separation of concerns)
─────────────────────────────────────────────
```

### Example — Checkpoint vs. Curriculum

```
You: Compare
You: 2

Professor Agent:
Curriculum coverage diff for Lesson 3.1:

Covered in checkpoints (✅) vs. Curriculum topics:
✅ Hook System Architecture
✅ Lifecycle Events
✅ Custom Patterns
❌ Debugging Strategies (in curriculum — not in your notes)
❌ Version Migration (in curriculum — not in your notes)

Recommendation: 2 gaps found. Consider reviewing before running Finish.
```

### When to Use Compare

- To understand how checkpoint layers build on each other
- To identify coverage gaps before running `Finish` (similar to `Verify` but more visual)
- To see what knowledge was added between two lessons
- After `Rewind` — to see what the new teaching path adds versus the original

---

## Related Commands

| Command | See Also |
|---------|----------|
| `Finish` | Generates HTML, flashcards, and cheatsheet that `Export` bundles |
| `Verify` | Checks curriculum coverage; `Compare` option 2 provides a more visual version of this |
| `Rewind` | Roll back to a checkpoint; use `Compare` afterward to diff the new path against the old |
| `Status` | Overview of lesson progress and completion |
