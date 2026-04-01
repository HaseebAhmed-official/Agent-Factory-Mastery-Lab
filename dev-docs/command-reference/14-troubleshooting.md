# 14. Troubleshooting Guide

---

## Section 1: Signs Something Is Wrong (Quick Lookup)

| You See | What's Wrong | What to Type / Run |
|---------|-------------|-------------------|
| Agent greets you with no recovery banner | Bridge not read on cold start | Type `Resume` |
| Agent re-defines a term you learned 3 lessons ago | Scaffold-fade not working | Type `Check pacing rules` |
| Agent accepts a weak, vague answer and moves on | Mastery gate not firing | Type `Wait — re-examine my answer against the rubric` |
| No vocabulary table at the start of a new lesson | T-step (Terminology First) was skipped | Type `Please start with the vocabulary table` |
| `health-check.py` shows UNHEALTHY | Bridge missing sections or .tmp files present | Type `Repair` in chat |
| `status.json` shows `repair_needed: true` | A write failed mid-checkpoint | Type `Repair` in chat |
| `Finish` completes but no HTML file appears | `generate-html.py` failed silently | Run `python3 scripts/generate-html.py --demo` in terminal |
| `Rewind` executes without asking you to type CONFIRM | Confirmation gate missing — unsafe rollback | Check `Knowledge_Vault/Protocols/rewind-checkpoint.md` |
| Agent loops on the same concept more than 3 times | Mastery gate loop cap not enforced | Type `Flag this concept as needs-review and continue` |
| Recovery banner shows wrong lesson | Bridge has a stale lesson mismatch | Type `Status` to see real state, then `Resume` |

---

## Section 2: Chat Behavior Issues

### Problem: Agent greets without a recovery banner

**Cause**: Cold-start protocol didn't fire or was skipped.

**Fix**:
```
Type: Resume
```

This forces the agent to load the bridge and display the recovery banner.

**Prevention**: The agent should ALWAYS read `context-bridge/status.json` before greeting. If this keeps happening, check `CLAUDE.md` — the SESSION START section defines this behavior.

---

### Problem: Agent accepts a weak answer and moves on

**Cause**: Mastery gate not enforcing the comprehension check.

**Fix**:
```
Type: Wait — re-examine my answer against the rubric
```

The agent will re-evaluate your answer against the mastery criteria and re-teach if it was weak.

**Why this matters**: The mastery gate must confirm understanding before proceeding. A weak answer like "it does things" should trigger a re-teach, not advancement.

---

### Problem: Agent loops more than 3 times on the same concept

**Cause**: The mastery gate loop cap (3 attempts max) is not being enforced.

**Fix**:
```
Type: Flag this concept as needs-review and continue
```

**Expected behavior**: After 3 re-teach attempts, the agent should flag `⚠️ NEEDS REVIEW` and move on — never loop a 4th time.

---

### Problem: No vocabulary table at the start of a lesson

**Cause**: T-step (Terminology First) was skipped in the TEACH cycle.

**Fix**:
```
Type: Please start with the vocabulary table
```

**Expected behavior**: Every new lesson/concept begins with a vocabulary table defining all terms before they are used.

---

### Problem: Agent re-defines terms you learned lessons ago

**Cause**: Scaffold-fade not working. Terms in the vocab bank for 2+ lessons should be recalled, not re-provided.

**Fix**:
```
Type: Check pacing rules
```

This prompts the agent to verify its pacing rules and stop over-defining known terms.

---

### Problem: Recovery banner shows the wrong lesson

**Cause**: `status.json` has stale data that doesn't match the bridge.

**Fix**:
```
Step 1 — Type: Status
(See what lesson the agent thinks you're on)

Step 2 — Type: Resume
(Force bridge reload to get authoritative state)
```

If the mismatch persists, manually inspect and correct from the terminal:
```bash
# Inspect current status
cat context-bridge/status.json

# Manually update if needed
python3 scripts/checkpoint-write.py --action update-status --lesson 3.1 --layer L2 --concept "Custom Hooks"
```

---

## Section 3: Checkpoint & Bridge Issues

### Problem: health-check.py shows UNHEALTHY

**Diagnosis**:
```bash
python3 scripts/health-check.py
```

Note which check failed (bridge, .tmp files, or status.json).

**Fix for orphaned .tmp files**:
```
Type: Repair in Claude Code chat
```

Or manually from the terminal:
```bash
ls context-bridge/*.tmp       # Identify .tmp files
rm context-bridge/*.tmp       # Remove them (only if sure)
python3 scripts/health-check.py   # Re-check
```

**Fix for bridge structure issues**:
```
Type: Repair in Claude Code chat
```

**Fix for status.json issues**:
```bash
cat context-bridge/status.json
# If repair_needed: true → type Repair in chat
```

---

### Problem: status.json shows repair_needed: true

**Cause**: A write operation failed mid-checkpoint (e.g., Stage 6 of the Checkpoint workflow failed).

**Verify**:
```bash
cat context-bridge/status.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('repair_needed:', d.get('repair_needed', 'NOT SET'))"
```

**Fix**:
```
Type: Repair in Claude Code chat
```

The Repair protocol will:
1. Scan `revision-notes/` for existing checkpoint files
2. Reconstruct metadata from YAML frontmatter
3. Remove orphaned .tmp files
4. Reset `repair_needed` to false

---

### Problem: Checkpoint completed but status.json still shows old lesson

**Cause**: Stage 6 of the Checkpoint workflow (status.json update) failed.

**Fix**:
```bash
python3 scripts/checkpoint-write.py --action update-status --lesson 3.1 --layer L1 --concept "Hook Architecture"
```

Then verify:
```bash
cat context-bridge/status.json
```

---

### Problem: Context bridge seems incomplete or missing sections

**Diagnosis**:
```bash
grep "^## [0-9]" context-bridge/master-cumulative.md | wc -l
# Should show 18 sections
```

**Fix**:
- If sections are missing: type `Repair` in chat
- If bridge content looks off: type `Resume` to re-read it
- If very corrupted, restore from backup:

```bash
ls context-bridge/backup/
cp context-bridge/backup/master-cumulative-2026-03-31.md context-bridge/master-cumulative.md
```

---

## Section 4: Finish & Artifact Issues

### Problem: Finish completed in chat but no HTML in visual-presentations/

**Cause**: `generate-html.py` failed silently during the Finish workflow.

**Fix**:
```bash
# Test the HTML pipeline first
python3 scripts/generate-html.py --demo

# If the demo works, regenerate for a specific lesson
python3 scripts/generate-html.py --lesson 3.1
```

**Check prerequisites**:
```bash
pip install jinja2    # Required for HTML generation
```

---

### Problem: No flashcards in flashcards/ after Finish

**Cause**: Finish workflow didn't complete all 10 stages, or Stage 7 (flashcard generation) failed.

**Check**:
```bash
ls flashcards/
```

**Fix**: Re-run `Finish` in chat. The command is idempotent — re-running it will not duplicate content, it will regenerate any missing artifacts.

---

### Problem: INDEX.html missing or outdated

**Fix**:
```bash
python3 scripts/generate-index.py
```

Expected output: `✅ INDEX.html generated`

---

## Section 5: Git Integration Issues

### Problem: Commit blocked by quality gate

**Cause**: Checkpoint notes scored below 70/100.

**Diagnosis**:
```bash
./scripts/validate-notes.sh 3.1
```

**Fix**: Improve the content in the checkpoint file, then retry `Checkpoint` in chat. Refer to the quality dimensions (Completeness, Clarity, Professionalism, Actionability) in `11-git-integration-commands.md`.

**Emergency bypass** (not recommended):
```bash
git commit --no-verify -m "emergency save"
```

---

### Problem: Push failed after commit

**Fix**:
```bash
git pull origin main
# Resolve any conflicts
git push origin main
```

---

### Problem: Pre-commit hook not running

**Fix**:
```bash
ls -la .git/hooks/pre-commit       # Verify it exists
chmod +x .git/hooks/pre-commit     # Make executable
.git/hooks/pre-commit              # Test manually
```

---

## Section 6: Rewind Issues

### Problem: Rewind executes without asking for CONFIRM

**Severity**: HIGH — this is a critical safety gate.

**Cause**: The confirmation gate in `Knowledge_Vault/Protocols/rewind-checkpoint.md` is missing or bypassed.

**Fix**:
- Open `Knowledge_Vault/Protocols/rewind-checkpoint.md` and verify the CONFIRM gate is defined
- If the content is missing, the protocol file may need to be restored

**Expected behavior**: After selecting a layer, the user must type `CONFIRM` exactly. Any other input cancels the rewind cleanly.

---

### Problem: Rewind content and current content conflict

**Expected behavior**: The agent should show a diff-style analysis and offer 3 merge strategies:
1. Archive & Replace
2. Create Branch
3. Intelligent Merge

If this does not happen, content may be at risk of being lost. Check the `.archive/` folder for any archived versions before proceeding.

---

## Section 7: Recovery Commands Quick Reference

| Situation | Command |
|-----------|---------|
| Agent lost context | `Resume` |
| Bridge corrupted / .tmp files / repair_needed | `Repair` |
| Unsure where you are | `Status` |
| Lesson seems incomplete | `Verify` |
| Wrong content being taught | `Resume` then `Status` |
| HTML not generated | Terminal: `python3 scripts/generate-html.py --demo` |
| System not healthy | Terminal: `python3 scripts/health-check.py` then `Repair` in chat |
| Commit blocked | Terminal: `./scripts/validate-notes.sh 3.1` |
| Stuck in mastery gate loop | `Flag this concept as needs-review and continue` |
| Agent skipped vocabulary | `Please start with the vocabulary table` |
