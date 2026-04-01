# Navigation & Status Commands — Reference

## Quick Reference

| Command | Type in chat | Writes files? | Scope |
|---------|-------------|--------------|-------|
| `Status` | `Status` | No | Entire curriculum |
| `Verify` | `Verify` | No | Current lesson |
| `where am I?` | `where am I?` | No | Current lesson/layer |
| `what should I know so far?` | `what should I know so far?` | No | Everything covered so far |

**What these commands have in common:** All four are read-only. They display information in chat only. None of them create, modify, or delete any files.

---

## Status Command

### Trigger

Type `Status` in chat.

### Purpose

Generate a full progress dashboard showing where you are in the curriculum, what you have completed, and what comes next. This is the broadest view available — it spans the entire course.

### What It Does

1. Fetches `Knowledge_Vault/Protocols/status-dashboard.md`
2. Reads `context-bridge/master-cumulative.md` and `context-bridge/status.json`
3. Generates a progress dashboard showing:
   - Current lesson and layer
   - Overall curriculum completion percentage
   - Chapters completed vs. in progress vs. not started
   - Checkpoints created (count + list)
   - Concepts covered (total count)
   - Vocabulary bank size
   - Next steps
4. Displays in chat only — no files written

### What You See

```
📊 Progress Dashboard
─────────────────────────────────────────────────
Lesson:     3.1 — Hook Architecture
Layer:      L2 (Intermediate)
Checkpoint: 2 checkpoints saved (L1, L2)

Curriculum Progress:
  Chapter 1: ✅ Complete
  Chapter 2: ✅ Complete
  Chapter 3: 🔄 In Progress (Lesson 3.1 of 23)
  Chapters 4–6: ⬜ Not started

Overall: 12% complete (2 of 17 lessons done)

Concepts covered this lesson: 8
Vocab bank entries: 23 terms

Next steps:
  → Continue Lesson 3.1 (L2 → L3)
  → Then: Lesson 3.2
─────────────────────────────────────────────────
```

### When to Use Status

- You have lost track of where you are in the curriculum
- You want to see the overall completion percentage for the course
- The recovery banner showed something unexpected and you want to verify the full picture
- Before starting a new session to orient yourself before resuming
- You want to know how many vocab terms or concepts have been accumulated across all sessions

### What Status Does NOT Do

- Does not sync new curriculum content (use `Sync` for that)
- Does not run quizzes or assessments (use `Review X.Y` or `quiz me`)
- Does not show detailed coverage gaps within a lesson (use `Verify` for that)
- Does not write or update any files

---

## Verify Command

### Trigger

Type `Verify` in chat.

### Purpose

Compare what has been covered in your checkpoint notes against the official curriculum for the current lesson. Identifies topics the curriculum lists that have not yet appeared in any checkpoint. Shows a coverage percentage and a gap list.

### What It Does

1. Fetches `Knowledge_Vault/Protocols/verify-coverage.md`
2. Reads the official curriculum module for the current lesson
3. Reads all checkpoint part files for the current lesson from `revision-notes/`
4. Compares curriculum topics against checkpoint content
5. Identifies coverage gaps — topics present in the curriculum that do not appear in checkpoints
6. Generates a coverage report with percentage and gap list
7. Displays in chat only — no files written

### What You See

```
📋 Coverage Report — Lesson 3.1
────────────────────────────────────────
Curriculum topics: 12
Covered in checkpoints: 9
Coverage: 75%

✅ Covered:
  - Hook System Architecture
  - Lifecycle Events
  - Registration Patterns
  - Custom Hook Patterns
  - Composition Strategies
  - Error Boundaries
  - Performance Optimization
  - Testing Hooks
  - Hook Anti-Patterns

⚠️ Not yet covered:
  - Advanced Debugging Techniques
  - Hook Versioning
  - Migration Patterns

Recommendation: 3 topics remain. Checkpoint when complete for full coverage.
────────────────────────────────────────
```

### When to Use Verify

- Before running `Finish` — confirm you have not skipped major topics before generating the final artifacts
- After `Rewind` — to understand what coverage was lost by rolling back to an earlier checkpoint
- When you suspect the agent skipped or rushed past a topic
- During exam prep — identify gaps before starting review or quizzes
- Anytime coverage feels uncertain and you want a concrete gap list

### What Verify Does NOT Do

- Does not sync new curriculum content — it reads the existing curriculum only (use `Sync` to discover new lessons)
- Does not edit, update, or create any checkpoint files
- Does not change the teaching sequence or trigger re-teaching of gaps (that requires continuing the lesson normally)
- Does not operate across multiple lessons — scope is the current lesson only

---

## `where am I?` Command

### Trigger

Type `where am I?` in chat. Case-insensitive — `Where am I?` and `where am i?` also work.

### Purpose

Show your current position in the curriculum as a compact summary. More focused than `Status` — answers the immediate question of exactly where in the lesson you are right now, including the concept in progress, the layer, and how long since the last checkpoint.

### What It Does

Reads `context-bridge/status.json` and displays current position with a within-lesson layer breakdown. No external protocol fetch required — this is a lightweight read of instant state.

### What You See

```
📍 Current Position
─────────────────────────────────────────
Lesson: 3.1 — Hook Architecture
Chapter: 3 — General Agents
Layer: L2 (Intermediate)
Concept: Custom Hook Patterns

Progress within lesson:
  L1 ✅ Fundamentals (Hook System, Lifecycle, Registration)
  L2 🔄 Intermediate — in progress
  L3 ⬜ Advanced — not started

Last checkpoint: 2026-03-31 14:30
Messages since checkpoint: 12
─────────────────────────────────────────
```

### When to Use `where am I?`

- You have lost track of which concept is currently in progress within the lesson
- You want to know how many messages have passed since the last checkpoint (to decide if it is time to checkpoint soon)
- A quick orientation check that does not need the full curriculum-wide view of `Status`
- After a distraction or break mid-lesson and you want to re-anchor before continuing

### Difference from `Status`

| | `where am I?` | `Status` |
|---|---|---|
| Scope | Current lesson only | Full curriculum |
| Shows chapter/layer/concept | Yes | Yes (at a higher level) |
| Shows within-lesson layer breakdown | Yes | No |
| Shows overall % complete | No | Yes |
| Shows vocab bank size | No | Yes |
| Shows messages since last checkpoint | Yes | No |
| Data source | `status.json` only | `status.json` + `master-cumulative.md` |

---

## `what should I know so far?` Command

### Trigger

Type `what should I know so far?` in chat.

### Purpose

Generate a cumulative review synthesis of all material covered up to this point — across all checkpoints, all lessons, and all completed chapters. This is not a quiz. It is a narrative summary of the full body of knowledge you have built, pulled from the vocab bank and checkpoint history in the context bridge.

### What It Does

1. Reads `context-bridge/master-cumulative.md` — specifically the Vocabulary Bank, Knowledge Graph, Anti-Patterns, and Frameworks sections
2. Reads checkpoint history to determine scope (all completed checkpoints)
3. Generates a structured synthesis covering everything in the record
4. Displays in chat only — no files written

### What You See

A structured summary covering all of the following, drawn from your actual checkpoint record:

- **Key vocabulary terms** — every term in the vocab bank with its definition
- **Core concepts and frameworks** — the central ideas from each lesson and how they work
- **Anti-patterns covered** — what to avoid and why
- **Connections between topics** — how concepts from different lessons relate to each other
- **Chapter-by-chapter progression** — how each chapter built on the previous one

The output is organized as a narrative synthesis, not a raw dump. It reads like a structured study guide built from your specific learning history.

### When to Use It

- Before starting a new chapter — consolidate and reinforce everything from the chapters before it
- When returning after a long break — rebuild context quickly before resuming
- During exam prep — see the full scope of what you are expected to know
- When concepts feel disconnected and you want to see how everything fits together
- Before a `Finish` — to verify your mental model matches the checkpoint record before generating final artifacts

### Difference from Quiz and Review Commands

| Command | What it does | Questions? |
|---------|-------------|------------|
| `what should I know so far?` | Narrative synthesis of everything covered | No |
| `quiz me` | 5 questions on most recently covered material | Yes |
| `Review X.Y` | Quiz on specific lesson X.Y | Yes |
| `review chapter X` | 10 questions spanning a full chapter | Yes |
| `exam prep` | Full exam simulation across all covered lessons | Yes |

Use `what should I know so far?` when you want to **read and absorb**. Use the quiz and review commands when you want to **test yourself**.

### What It Does NOT Do

- Does not ask questions or require responses
- Does not update the bridge or any files
- Does not synthesize content that was taught but never checkpointed — it reads from the checkpoint record only. If a concept was covered conversationally but you never ran `Checkpoint`, it may not appear here. This is a reason to checkpoint regularly.

---

## Choosing the Right Command

```
I want to know...
│
├── "Where exactly am I in THIS lesson, right now?"
│     → where am I?
│
├── "How much of the WHOLE COURSE have I completed?"
│     → Status
│
├── "Did I miss any topics in the current lesson?"
│     → Verify
│
└── "What is everything I should know at this point?"
      → what should I know so far?
```

---

## Related Commands

| Command | When to follow up |
|---------|------------------|
| `Checkpoint` | After `Verify` shows gaps — finish the remaining topics, then checkpoint before `Finish` |
| `Resume` | If `Status` shows an unexpected lesson (bridge may not have loaded correctly) |
| `Repair` | If `Status` shows corrupted or incomplete checkpoint data |
| `Verify` | After `Rewind` to see what coverage was rolled back |
| `Review X.Y` | After `what should I know so far?` to test yourself on the material you just reviewed |
