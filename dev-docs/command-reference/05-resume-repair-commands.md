# Resume & Repair Commands — Reference

## Quick Reference

| Command | Type in chat | What it does |
|---------|-------------|--------------|
| `Resume` | `Resume` | Force-loads the context bridge and continues from last checkpoint |
| `Repair` | `Repair` | Fixes corrupted metadata, malformed bridge rows, and orphaned `.tmp` files |

**When to use which:**

| Symptom | Use |
|---------|-----|
| Agent greeted with no recovery banner | `Resume` |
| Recovery banner shows wrong lesson | `Status` then `Resume` |
| health-check shows UNHEALTHY | `Repair` |
| `status.json` has `repair_needed: true` | `Repair` |
| Bridge rows show `⚠️ Meta failed` | `Repair` |
| `.tmp` files exist in `context-bridge/` | `Repair` |
| Bridge seems complete but agent is lost | `Resume` |

---

## Resume Command

### Trigger

Type `Resume` in chat.

### Purpose

Explicitly load the context bridge and continue from the last checkpoint. Use this when the cold-start recovery banner did not fire, or when you want to force-reload the bridge mid-session.

### What It Does

1. Fetches `Knowledge_Vault/Protocols/resume-protocol.md`
2. Reads `context-bridge/status.json` (instant state — lesson/layer/concept)
3. Loads `context-bridge/master-cumulative.md` (full context)
4. Displays recovery banner with current lesson/layer/last-checkpoint
5. Surfaces any un-checkpointed teaching log content (offers recovery)
6. Surfaces any repair needs (`⚠️` bridge rows or orphaned `.tmp` files)
7. If lesson mismatch detected: asks before loading
8. Resumes teaching from last checkpoint

### Recovery Banner Format

```
📍 Context restored
Lesson {X.Y} | Layer L{N}
Last checkpoint: {timestamp}
Concepts covered: {list}

[any repair warnings if applicable]

Ready to continue from {last concept}?
```

### When to Use Resume

- Agent greeted you without showing a recovery banner (cold-start check didn't fire)
- You want to explicitly confirm the bridge was loaded correctly
- You're mid-session and want to reload from the bridge (e.g., after suspecting drift)
- After opening a new Claude Code session where the bridge was not shown automatically

### Cold-Start Recovery (Automatic — Background)

On **every** new conversation (including after `/clear`), the agent automatically runs the cold-start recovery protocol **before greeting you**:

1. Reads `context-bridge/status.json` first
2. Displays recovery banner with lesson/layer/last-checkpoint
3. Loads `context-bridge/master-cumulative.md` for full context
4. Executes `Knowledge_Vault/Protocols/resume-protocol.md` silently
5. Surfaces any repair needs
6. Only then greets you

**If the agent greeted you without a recovery banner**, the cold-start check failed. Type `Resume` to force it.

### Example Interaction

```
You: Resume

Professor Agent:
Loading context bridge...

📍 Context restored
Lesson 3.1 | Layer L2
Last checkpoint: 2026-03-31 14:30
Concepts covered: Hook System, Lifecycle, Custom Patterns

Bridge loaded: context-bridge/master-cumulative.md
No repair needs detected.

Ready to continue from Custom Hook Patterns (L2)?
Next concept: Composition Strategies
```

---

## Repair Command

### Trigger

Type `Repair` in chat.

### Purpose

Fix incomplete checkpoint metadata, corrupted bridge rows, orphaned `.tmp` files, or any state where `status.json` shows `repair_needed: true`.

### When to Use Repair

| Symptom | What's wrong |
|---------|-------------|
| `python3 scripts/health-check.py` shows `UNHEALTHY` | Bridge missing sections or `.tmp` files present |
| `context-bridge/status.json` shows `repair_needed: true` | A write failed mid-checkpoint (Stage 6 of checkpoint workflow) |
| Recovery banner shows `⚠️ repair needed` | Checkpoint metadata is incomplete |
| Section 14 of bridge has `⚠️ Meta failed — repair needed` | Stage 6 (status.json update) failed |

### What Repair Does

1. Fetches `Knowledge_Vault/Protocols/resume-protocol.md` (repair branch)
2. Scans `revision-notes/` for all `{X.Y}-L*-*.md` files
3. Extracts YAML frontmatter from each file
4. Reconstructs `.checkpoint-meta.json` from frontmatter
5. Removes orphaned `.tmp` files
6. Repairs bridge section rows that are malformed or incomplete
7. Resets `repair_needed` flag in `status.json` to `false`
8. Confirms: "Repair complete. Bridge restored to last known good state."
9. Warns if reconstruction was partial: "Checkpoint tree may be incomplete — some metadata was inferred"

### How `repair_needed` Gets Set (the failure scenario)

1. Checkpoint stages 1–5 complete successfully (backup → synthesis → part file → bridge update → snapshot)
2. Stage 6 (update `status.json`) fails — disk full, permission denied, or interrupted
3. The checkpoint write script detects the failure and sets `repair_needed: true` in `status.json`
4. Next session: recovery banner shows the warning
5. User types `Repair` → system reconstructs from the successfully written files

### What Happens If Metadata Is Corrupted

The agent scans the lesson directory for all checkpoint files and reconstructs the tree from their YAML frontmatter. This is a best-effort recovery — if frontmatter is also corrupted, the tree may be incomplete, but the content files themselves are preserved.

### Terminal Pre-Check Before Using Repair

```bash
# Check health first
python3 scripts/health-check.py

# Check repair flag
cat context-bridge/status.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('repair_needed:', d.get('repair_needed', 'NOT SET'))"

# Check for orphaned tmp files
ls context-bridge/*.tmp 2>/dev/null && echo "tmp files found" || echo "no tmp files"
```

### Test for Atomic Write Failure Detection (Test Sequence F)

```bash
# Make bridge read-only to simulate write failure
chmod 444 context-bridge/master-cumulative.md
python3 scripts/checkpoint-write.py --action backup
chmod 644 context-bridge/master-cumulative.md
# Should see error message and repair_needed: True in status.json
```

### Example Interaction

```
You: Repair

Professor Agent:
🔧 Running repair protocol...

Scanning revision-notes/ for checkpoint files...
Found: 3.1-L1-hook-architecture.md ✓
Found: 3.1-L2-custom-hooks.md ✓

Reconstructing .checkpoint-meta.json from frontmatter...
Checking for orphaned .tmp files...
Found: context-bridge/master-cumulative.md.tmp — removing ✓
Repairing bridge rows...
Resetting repair_needed flag...

✅ Repair complete. Bridge restored to last known good state.

⚠️ Note: Checkpoint tree was partially reconstructed from frontmatter.
   Some metadata may be inferred. Run 'Verify' to check coverage.

Ready to continue from Lesson 3.1, Layer L2?
```

---

## Related Commands

| Command | Use after |
|---------|-----------|
| `Status` | Confused about current lesson/layer before running `Resume` |
| `Verify` | After `Repair` to confirm coverage is correct |
| `Checkpoint` | After session drift is fixed and teaching resumes |
