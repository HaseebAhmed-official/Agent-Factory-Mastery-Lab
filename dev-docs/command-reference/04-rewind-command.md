# Rewind Command Reference

## Quick Reference

| Item | Detail |
|------|--------|
| **Trigger** | Type `Rewind` in chat |
| **Purpose** | Roll back to a previous checkpoint layer and continue, revise, or review from there |
| **Safety gate** | Must type `CONFIRM` after selecting a layer — any other input cancels cleanly |
| **Data loss** | None — all strategies preserve original content |
| **Files read** | `Knowledge_Vault/Protocols/rewind-checkpoint.md`, `.checkpoint-meta.json` |
| **Files changed** | Depends on option chosen (see Files Touched table below) |

---

## Overview

`Rewind` is Git-style time travel for your learning session. It lets you load a previous checkpoint layer, then decide what to do from there: keep going with new content, redo the layer with a different approach, or just peek at it and return to where you were.

---

## Full Workflow (8 Steps)

1. Fetches `Knowledge_Vault/Protocols/rewind-checkpoint.md`
2. Reads `.checkpoint-meta.json` from the current lesson directory
3. Displays all checkpoints as a tree diagram — layer, timestamp, concepts covered, file path
4. User selects a checkpoint layer (e.g., `L2`)
5. **Confirmation gate** — shows `⚠️ CONFIRM REQUIRED`; user must type `CONFIRM` to proceed
6. Loads that checkpoint's content and bridge state at that time
7. Presents three post-rewind options (see below)
8. If continuing and a conflict exists (next layer already exists), offers merge strategies

---

## The Three Post-Rewind Options

| Option | Name | What Happens |
|--------|------|-------------|
| 1 | **Continue from here** | Resume teaching with new content from this checkpoint forward. Future checkpoints branch from this point. |
| 2 | **Revise this checkpoint** | Re-teach the concepts in this checkpoint with a different approach. Archives the old checkpoint, creates a revised version. |
| 3 | **Review & exit** | View this checkpoint's content, then return to current state. No files changed. |

---

## The Confirmation Gate

After selecting a layer, you **must** type `CONFIRM` exactly to proceed.

- Any other input — including `cancel`, `no`, `stop` — cancels the rewind cleanly
- Cancellation message: `Rewind cancelled — continuing from current position`
- This gate exists to prevent accidental rollbacks

> **Note for testers**: If the CONFIRM gate is missing, that is a known bug. The test for this behavior is Test Sequence D, Step 3 in `13-test-sequences.md`.

### Cancellation Example

```
You: Rewind
[checkpoint list displayed]
You: L2

Professor Agent:
⚠️ CONFIRM REQUIRED — type CONFIRM to proceed or anything else to cancel.

You: cancel

Professor Agent:
Rewind cancelled — continuing from current position.
```

---

## Branching and Conflict Detection

If you rewind to L2 and then checkpoint new content, but L3 already exists, a conflict is detected.

### Diff-Style Analysis

The agent shows a side-by-side breakdown:

```
EXISTING L3 (Original):
├─ Performance Optimization
└─ Error Boundaries

YOUR NEW CONTENT:
├─ Testing Strategies [NEW]
└─ Debugging Patterns [NEW]
```

### Three Merge Strategies

| Strategy | What It Does |
|----------|-------------|
| **Archive & Replace** | Moves old L3 to `.archive/` folder, replaces with new content |
| **Create Branch** | Keeps both: `L3-optimization` and `L3-testing` as separate files |
| **Intelligent Merge** | Combines old and new content — appends new material to the existing file |

Original content is **never deleted**. It is always archived or kept as a branch.

---

## Files Touched by Rewind

| Action | Files Affected |
|--------|---------------|
| Review & exit | No files changed |
| Continue from here (no conflict) | New checkpoint files created on the next `Checkpoint` command |
| Continue from here (conflict) | Old file archived to `.archive/` or kept as a parallel branch file |
| Revise this checkpoint | Old file archived, new file created with the same layer name |

---

## Example Interaction

```
You: Rewind

Professor Agent:
═══════════════════════════════════════════════════════
  CHECKPOINT HISTORY: Lesson 3.1 — Hook Architecture
═══════════════════════════════════════════════════════

L1 │ Fundamentals: Hook Architecture
   │ 📅 2026-03-03 14:32
   │ 📚 Concepts: Hook System, Lifecycle, Registration
   │ 📄 File: 3.1-L1-hook-architecture.md
   │ ✅ Status: Archived
   │
   └─> L2 │ Intermediate: Custom Hooks
       │ 📅 2026-03-03 15:15
       │ 📚 Concepts: Custom Patterns, Composition
       │ 📄 File: 3.1-L2-custom-hooks.md
       │ ✅ Status: Archived
       │
       └─> L3 │ Advanced: Performance Patterns
           │ 📅 2026-03-03 16:00
           │ 📚 Concepts: Optimization, Error Boundaries
           │ 📄 File: 3.1-L3-advanced-patterns.md
           │ 🔄 Status: Current

Which checkpoint would you like to load? (L1/L2/L3 or cancel)

You: L2

Professor Agent:
⚠️ CONFIRM REQUIRED
You are about to rewind to Checkpoint L2. This will restore context to:
  Lesson 3.1 | Layer L2: Custom Hooks
  Timestamp: 2026-03-03 15:15

Note: L3 already exists. If you continue from here, a conflict will be detected.

Type CONFIRM to proceed or anything else to cancel.

You: CONFIRM

Professor Agent:
✅ Context restored to Checkpoint L2

Lesson 3.1 | Layer L2: Custom Hooks
Timestamp: 2026-03-03 15:15

Concepts Covered (up to this checkpoint):
├─ L1: Hook System, Lifecycle, Registration
└─ L2: Custom Patterns, Composition

What's next?

1️⃣ CONTINUE FROM HERE
   Resume teaching from this checkpoint with NEW content.
   Future checkpoints will branch from this point.

2️⃣ REVISE THIS CHECKPOINT
   Re-teach the concepts in THIS checkpoint with a different approach.
   Will archive old checkpoint and create revised version.

3️⃣ REVIEW & EXIT
   Just review this checkpoint's content, then return to current state.

Your choice (1/2/3):
```

---

## Confirmation Message After Successful Rewind

```
Context restored to Checkpoint L{N}. {Concepts covered}. Ready to {continue/revise}?
```

---

## When to Use Rewind

- You want to re-explore a concept with a different teaching approach
- L3 went in the wrong direction and you want to try a different path
- You want to review earlier material without losing your current state (option 3)
- You want to branch your learning path and create `L3-a` and `L3-b` variants

---

## Best Practices

1. **Use option 3 (Review & exit) first** if you are unsure — it is fully non-destructive
2. **Use option 1 (Continue from here) + Create Branch** to keep both learning paths alive
3. **Never worry about data loss** — all three strategies preserve original content
4. Rewind works best when you have at least two checkpoints saved

---

## What Rewind Does NOT Do

- Does not delete any content — all strategies preserve originals
- Does not proceed without the CONFIRM gate — that gate is a required safety feature
- Does not create new files on its own — it only reads existing snapshots unless option 1 or 2 is chosen after confirmation
