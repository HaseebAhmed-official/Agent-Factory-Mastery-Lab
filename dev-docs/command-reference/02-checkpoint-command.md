# Checkpoint Command Reference

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────────┐
│  CHECKPOINT — Mid-Lesson Save                                        │
│                                                                      │
│  Trigger:   Checkpoint  |  Save progress  |  Quick checkpoint        │
│  Effect:    Saves current progress, continues teaching               │
│  Ends session? NO                                                    │
│                                                                      │
│  Creates:   revision-notes/{lesson}/{X.Y}-L{N}-{concept}.md         │
│             context-bridge/master-cumulative.md  (appended)         │
│             context-bridge/status.json           (updated)          │
│             context-bridge/backup/master-cumulative-{DATE}.md       │
│             context-bridge/snapshots/lesson-{X.Y}-L{N}-*.md        │
│                                                                      │
│  Analogy:   Save game mid-level (vs. Finish = level complete)       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Trigger Words

The following phrases trigger a checkpoint (case-insensitive):

| Trigger | Example |
|---------|---------|
| `Checkpoint` | "Checkpoint" |
| `Save progress` | "Save progress here" |
| `Quick checkpoint` | "Quick checkpoint before we move on" |

### NOT triggered by:

Questions that contain the word but are not commands:

- "What is a checkpoint?"
- "How does checkpointing work?"
- "Should I checkpoint here?"

---

## Full 8-Step Workflow

When you trigger a checkpoint, the agent executes these steps in order:

**Step 1 — Backup**
Runs `python3 scripts/checkpoint-write.py --action backup`. Creates a dated backup of `context-bridge/master-cumulative.md` before any writes occur. This ensures the bridge is always recoverable.

**Step 2 — Synthesis**
Fetches and executes `Knowledge_Vault/Protocols/checkpoint-synthesis.md`. Synthesizes all teaching content since the last checkpoint into structured notes: concepts, vocabulary, frameworks, anti-patterns, and connections.

**Step 3 — Create part file**
Writes the synthesized content to a versioned part file in `revision-notes/`:

```
revision-notes/{lesson}/{X.Y}-L{depth}-{semantic-concept}.md
```

Layer depth is assigned by deterministic rules (see Depth Layers below), not subjective judgment.

**Step 4 — Update master bridge**
Appends new content to `context-bridge/master-cumulative.md`. This is a living document — never replaced. Adds: vocabulary terms, knowledge graph nodes, anti-patterns, frameworks, and a new row in Section 14 (Checkpoint History).

**Step 5 — Write frozen snapshot**
Creates an immutable snapshot of the bridge state at this moment:

```
context-bridge/snapshots/lesson-{X.Y}-L{depth}-{concept}-snapshot.md
```

Used by `Rewind` to restore exact state at any past checkpoint.

**Step 6 — Update status.json**
Updates `context-bridge/status.json` with current lesson, layer, and concept. Uses 3-attempt retry logic. If all 3 attempts fail, status is marked `⚠️ Meta failed — repair needed` in Section 14 of the bridge.

**Step 7 — Reload context**
Truncates `teaching-log-current.md` to clear accumulated context. Auto-reloads summary from master bridge. Keeps the agent operating efficiently without losing any content.

**Step 8 — Confirm and continue**
Displays confirmation message and resumes teaching immediately. Does NOT end the session.

### Confirmation message format:

```
Checkpoint L{depth} complete. Resuming from {last concept taught}...
```

---

## Files Created / Updated

| File | Action | Notes |
|------|--------|-------|
| `revision-notes/{lesson}/{X.Y}-L{N}-{concept}.md` | Created | New part file with synthesized content |
| `context-bridge/master-cumulative.md` | Appended | Never replaced — sections 14, 15, 17, 18 updated |
| `context-bridge/status.json` | Updated | Current lesson/layer/concept |
| `context-bridge/backup/master-cumulative-{DATE}.md` | Created | Safety backup made before any writes |
| `context-bridge/snapshots/lesson-{X.Y}-L{N}-{concept}-snapshot.md` | Created | Frozen state for Rewind use |

---

## File Naming Convention

**Format:** `{X.Y}-L{depth}-{semantic-concept}.md`

| Component | Rules |
|-----------|-------|
| `{X.Y}` | Lesson number (e.g., `3.1`, `3.17`) |
| `L{depth}` | Layer number — L1, L2, L3, L4, ... (no cap) |
| `{semantic-concept}` | Kebab-case primary concept name, max 50 chars |

**Examples:**

```
3.1-L1-hook-architecture.md
3.17-L2-orchestration-patterns.md
3.1-L3-advanced-patterns.md
```

**Rules:**
- Layers represent conceptual depth, not strict sequence
- You can skip layers (L1 → L3) if content jumps in complexity
- You can branch (L2a, L2b) for parallel conceptual tracks
- Layer assignment is deterministic from content, not chosen arbitrarily

---

## Depth Layers

| Layer | Meaning | Typical Content |
|-------|---------|-----------------|
| **L1: Fundamentals** | Core concepts, definitions, basic usage | "What it is", "Why it matters", basic examples |
| **L2: Intermediate** | Advanced usage, composition, patterns | "How to combine", "Common patterns", real-world applications |
| **L3: Advanced** | Optimization, edge cases, expert techniques | "Performance", "Error handling", complex scenarios |
| **L4+: Expert** | Research-level depth, system design | Architecture tradeoffs, cross-system integration |

Layers describe conceptual depth, not a rigid sequence. The agent assigns the layer by analyzing the content being synthesized.

---

## Proactive Checkpoint Suggestions

The agent monitors your session and suggests checkpoints when readiness signals are detected. You are never forced — you control the pace.

### Strong signals (immediate suggestion):

- TEACH cycle fully complete for a major concept (all 5 components: Terminology, Explain, Analogize, Check, Hands-On)
- Natural curriculum boundary reached (subsection or topic complete)
- Depth layer transition (L1 → L2 or L2 → L3)
- 25+ message exchanges since last checkpoint
- You explicitly request it

### Moderate signals (gentle suggestion — needs 2 or more to trigger):

- "What Goes Wrong" failure analysis completed for a concept
- Student demonstrates independent mastery (momentum shift observed)

### Declining a suggestion:

Just continue talking. The agent will not repeat the suggestion until another strong signal is detected.

---

## The Cumulative Context Bridge

`context-bridge/master-cumulative.md` is the central state file. It is ONE living document — never replaced, only appended. Each checkpoint adds rows and terms; it never removes them.

Relevant sections updated on every checkpoint:

```markdown
## 14. Checkpoint History
| Layer | Timestamp | Concepts Covered | File | Status |
|-------|-----------|------------------|------|--------|
| L1 | {timestamp} | {concepts} | {file} | ✓ Archived |

## 15. Current Checkpoint State
**Active Part**: L{N}
**Last Checkpoint**: {timestamp}
**Concepts Since Last Checkpoint**: []
**Context Window Status**: {message count} messages since last checkpoint

## 17. Session History
| Session | Date | Lessons Covered | Checkpoints | Notes |
|---------|------|-----------------|-------------|-------|

## 18. Backup Log
| Backup File | Created | Trigger |
|-------------|---------|---------|
| backup/master-cumulative-{date}.md | {timestamp} | Checkpoint L{N} |
```

### Status markers in Section 14:

| Marker | Meaning |
|--------|---------|
| `⏳ Saving...` | Checkpoint currently in progress |
| `✓ Archived` | Successfully saved and verified |
| `⚠️ Meta failed — repair needed` | Step 6 (status.json update) failed — use `Repair` command |

---

## Example Interaction

```
You: Checkpoint

Professor Agent:
⏳ Checkpoint L1 in progress...

Creating backup: context-bridge/backup/master-cumulative-2026-03-31.md ✓
Synthesizing content for L1...
Writing part file: revision-notes/ch3/3.1-L1-hook-architecture.md ✓
Updating master bridge... ✓
Writing snapshot... ✓
Updating status.json... ✓

✅ Checkpoint L1 complete. Resuming from Hook Architecture...

Files created:
- revision-notes/ch3/3.1-L1-hook-architecture.md
- context-bridge/backup/master-cumulative-2026-03-31.md
- context-bridge/snapshots/lesson-3.1-L1-hook-architecture-snapshot.md

Lesson 3.1 | Layer L1 complete
Concepts covered: Hook System, Lifecycle, Registration

Next: Custom Hook Patterns (L2)
Ready to continue?
```

---

## When to Checkpoint (Best Practices)

**Good times to checkpoint:**

- After a major concept is fully explained (full TEACH cycle complete)
- At natural curriculum boundaries (end of a subsection or topic)
- When moving from fundamentals to intermediate depth (L1 → L2)
- Every 25+ messages if no natural boundary has appeared
- Before a complex or unfamiliar topic (creates a clean restore point)

**Avoid checkpointing:**

- After only a partial explanation (synthesis will be incomplete)
- Mid-exercise — finish the exercise first, then checkpoint
- When no new content exists since the last checkpoint (agent will warn you)

---

## What Happens When There Is Nothing to Save

If you trigger a checkpoint but no new content has been taught since the last one:

```
⚠️ No new content to checkpoint yet.
Continue teaching, then checkpoint when ready.
```

No files are created. No writes occur. Teaching resumes immediately.

---

## Checkpoint vs. Finish

| | Checkpoint | Finish |
|---|---|---|
| Ends session? | No — continues teaching | Offers to continue or end |
| Creates HTML presentation? | No | Yes |
| Creates flashcards? | No | Yes |
| Creates quick-reference cheatsheet? | No | Yes |
| Updates context bridge? | Yes | Yes |
| Creates part file? | Yes | Yes (if new content exists) |
| Git auto-commit? | Yes | Yes (+ creates git tag) |
| Analogy | Save game mid-level | Level complete |

Use `Checkpoint` to save progress and keep going. Use `Finish` when a lesson is fully complete.

---

## Git Integration (Automatic)

After Step 7, if git is configured, the checkpoint is auto-committed without any action from you.

**Script called:**

```
python3 scripts/git-auto-push.py checkpoint {X.Y} L{N}
```

**What it does:**

1. Stages all checkpoint files created in this run
2. Creates a semantic commit message: `docs(checkpoint): lesson 3.1 layer L1`
3. Runs pre-commit hook — validates checkpoint quality (minimum score: 70/100)
4. Pushes to remote if a remote is configured

**If the quality gate fails:**

The commit is blocked. The agent reports the quality score and the specific areas that need improvement. Fix the content, then re-trigger the checkpoint.

See `11-git-integration-commands.md` for full configuration details, dry-run mode, and manual override options.

---

## Related Commands

| Command | When to use |
|---------|-------------|
| `Finish` | Lesson is complete — generate HTML, flashcards, cheatsheet |
| `Rewind` | Roll back to a previous checkpoint layer |
| `Resume` | Reload state after closing and reopening Claude Code |
| `Repair` | Fix a checkpoint whose Step 6 (status.json) failed |
| `Status` | View checkpoint history and current progress |
