# Resume Protocol (Cold-Start Recovery)

> **Trigger**: Automatically at EVERY new conversation start, before any greeting
> **Also triggered by**: User command `Resume` or `Repair`
> **Purpose**: Detect context loss, recover seamlessly, surface repair needs
> **Cross-refs**: [Checkpoint Synthesis](checkpoint-synthesis.md) | [Session Management](session-management.md)

---

## FAST START (Run First)

Before reading master-cumulative.md, read `context-bridge/status.json`:
```json
// Single file read → instant state:
// lesson, layer, concept, last_checkpoint, status
```
Display recovery banner immediately from status.json. Then load full bridge for detail.

Run health check: `python3 scripts/health-check.py`
If UNHEALTHY: surface specific issues before proceeding.

---

## DIRECTIVE

At the **START of every conversation**, before greeting the student or taking any other action, execute this detection and recovery workflow **silently** (no tool-call permission prompts visible to user). This entire stage takes under 5 seconds and is invisible unless recovery is needed.

**This protocol is the solution to the `/clear` black hole.** After a student types `/clear`, the conversation history is gone — but this protocol reads the file system to restore full context before teaching resumes.

---

## STAGE 1: Cold-Start Detection

Run these checks silently before displaying anything:

### Step 1: Check for master bridge
- Does `context-bridge/master-cumulative.md` exist?
  - **No** → Skip all stages. Execute normal Session Start from `session-management.md`. Done.
  - **Yes** → Continue to Step 2.

### Step 2: Parse the bridge
Read the following sections from `master-cumulative.md`:
- **Section 13** (Next Steps) — what was planned next
- **Section 14** (Checkpoint History) — last 3 rows only
- **Section 15** (Current Checkpoint State) — active layer, timestamp, concepts since last checkpoint
- **Section 1** header — current lesson number

Extract: `active_layer`, `last_checkpoint_timestamp`, `concepts_since_last_checkpoint`, `current_lesson`

### Step 3: Check teaching log
- Does `revision-notes/**/teaching-log-current.md` exist with non-empty content?
  - **Yes** → Set flag: `has_unsaved_teaching_log = true`. Read concept list from file.
  - **No** → `has_unsaved_teaching_log = false`

### Step 4: Scan for repair needs
- Scan Section 14 of bridge for rows containing `⚠️ Meta failed`
- Check all lesson directories for orphaned `.checkpoint-meta.tmp.json` files (using Glob)
  - Set flag: `has_repair_needs = true/false`
  - Record affected checkpoint layers if found

### Step 5: Check for lesson mismatch
- If student's first message mentions a **different lesson** than what's in the bridge header:
  - Set flag: `lesson_mismatch = true`

---

## STAGE 2: Display Recovery Banner

Based on detection results, display the appropriate banner **before the greeting**:

---

### Case A — Clean State (no unsaved content, no repair needs, no mismatch)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📂 Context Restored
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Lesson: {X.Y} | Layer: L{N} | Last checkpoint: {date}

  Concepts covered (last checkpoint):
  • {concept 1}
  • {concept 2}
  (or: "Clean checkpoint — no concepts listed")

  Next step: {section 13 value}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Continuing from Lesson {X.Y} Layer L{N}...
(Greeting follows immediately below)
```

---

### Case B — Teaching Log Has Unsaved Content

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📂 Context Restored — ⚠️ Unsaved Progress Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Last Checkpoint: L{N} ({date})

  UN-CHECKPOINTED CONTENT (from teaching log):
  • {concept from log 1}
  • {concept from log 2}
  • {concept from log N}

  These concepts were taught AFTER the last checkpoint
  but the session ended before they were saved.

  Options:
  1. Recover → Run Checkpoint now (captures from log)
  2. Discard → Continue from last checkpoint (L{N})

  Your choice (1/2):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Wait for student input before proceeding.**

---

### Case C — Repair Needed

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📂 Context Restored — 🔧 Repair Needed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Last Checkpoint: L{N} ({date})

  INCOMPLETE CHECKPOINT METADATA:
  The following checkpoints have incomplete metadata
  (notes and bridge are intact — only JSON is missing):

  • L{N} — {timestamp} — {⚠️ Meta failed}
  • (list all affected)

  Options:
  1. Auto-repair (recommended) → Rebuild from frontmatter
  2. Skip → Continue teaching (repair later with `Repair`)

  Your choice (1/2):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Wait for student input before proceeding.**

---

### Case D — Lesson Mismatch

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📂 Bridge Found — Different Lesson Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Bridge shows: Lesson {X.Y} (L{N})
  You mentioned: Lesson {new lesson}

  Options:
  1. Continue Lesson {X.Y} from bridge
  2. Start Lesson {new lesson} fresh (bridge preserved)

  Your choice (1/2):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## STAGE 3: Auto-Repair (if student selects repair in Case C)

For each checkpoint with `⚠️ Meta failed` status:

1. **Locate the checkpoint file**: Glob `revision-notes/**/lesson-dir/{X.Y}-L{N}-*.md`
2. **Parse YAML frontmatter**: Extract `lesson`, `layer`, `depth`, `semantic_name`, `concepts`, `vocab_count`, `date`
3. **Read existing `.checkpoint-meta.json`**: Load current content
4. **Reconstruct the missing entry**:
   ```json
   {
     "layer": "L{N}",
     "depth": {N},
     "semantic_name": "{from frontmatter}",
     "timestamp": "{from frontmatter date}",
     "concepts": ["{from frontmatter concepts list}"],
     "vocab_count": {from frontmatter},
     "file": "{filename}",
     "context_state": "Repaired from frontmatter",
     "parent_checkpoint": "L{N-1}"
   }
   ```
5. **Write updated `.checkpoint-meta.json`** with reconstructed entry
6. **Update bridge row**: Change `⚠️ Meta failed` → `✓ Archived (repaired {date})`
7. **Handle orphaned .tmp files**: If `.checkpoint-meta.tmp.json` exists:
   - Compare modification times with `.checkpoint-meta.json`
   - If .tmp is newer: offer "Promote .tmp to replace .json?"
   - If .json is newer: offer "Delete .tmp (safe)?"

**Confirm completion**:
```
✅ Repair complete: {N} checkpoint(s) repaired
   Bridge rows updated: ⚠️ → ✓ Archived (repaired)
   Metadata files reconstructed from frontmatter.
```

---

## STAGE 4: Teaching Log Recovery (if student selects recover in Case B)

1. **Read `teaching-log-current.md` in full**
2. **Use as Stage 1 audit source** — treat as if it were conversation history for the checkpoint
3. **Execute full Checkpoint workflow** (Stages 1-6 of `checkpoint-synthesis.md`) using log content as the source material
4. **After successful checkpoint**: Truncate `teaching-log-current.md` (overwrite with empty content)
5. **Confirm**:
   ```
   ✅ Teaching log recovered: {N} concepts checkpointed
      New part file: {X.Y}-L{N}-{concept}.md
      teaching-log-current.md cleared
   ```
6. **Resume teaching** from after the recovered concepts

---

## COMMAND: `Resume`

When user types `Resume` explicitly (not at session start):

1. Execute Stages 1-2 of this protocol (detect + display banner)
2. If clean state: "Already up to date. Here's where we left off: {state}"
3. If unsaved content or repair: show appropriate Case B/C banner
4. Resume teaching

---

## COMMAND: `Repair`

When user types `Repair` explicitly:

1. Execute Stage 1 Steps 3-4 only (check for repair needs)
2. If repair found: Execute Stage 3
3. If no repair found: "No incomplete checkpoints detected. All metadata is intact."

---

## CONSTRAINTS

- **Silent execution**: Run all file checks without displaying tool-call confirmations
- **Banner before greeting**: Recovery banner always appears BEFORE the standard Professor Agent greeting
- **Never force recovery**: Always offer skip/discard option. Student decides.
- **Bridge immutability during Rewind**: This protocol never rolls back the master bridge — it only reads forward
- **Lesson mismatch guard**: If bridge lesson ≠ student's stated new topic, ALWAYS ask before loading
- **No greeting if repair pending**: If repair is needed, wait for student decision before proceeding with greeting
- **Fast path for clean state**: Case A adds minimal overhead — just displays a 5-line banner

---

## SUCCESS CRITERIA

✅ After `/clear`, next session opens with recovery banner (not blank greeting)
✅ Un-checkpointed teaching log content is surfaced and recoverable
✅ Repair needs are detected and fixable without manual JSON editing
✅ Lesson mismatch is caught before wrong context is loaded
✅ Clean sessions add < 5 seconds and 5 lines of overhead
✅ Student can always skip recovery and start fresh

---

## RELATED PROTOCOLS

- **Checkpoint workflow**: `checkpoint-synthesis.md`
- **Teaching log format**: See Stage 4 and `checkpoint-synthesis.md` CONSTRAINTS
- **Rewind**: `rewind-checkpoint.md` (uses snapshots, not this protocol)
- **Session management**: `session-management.md`
