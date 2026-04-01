# Test Sequences Reference

Six complete end-to-end test scenarios for verifying the Agent Factory system works correctly. Run in order the first time — each sequence builds on the previous.

---

## Quick Reference

| Sequence | What it tests | Time | Prereqs |
|----------|--------------|------|---------|
| A | Full smoke test: health → teach → checkpoint → recovery | 15 min | None |
| B | Spaced review cold-start recall | 10 min | Sequence A |
| C | Finish: 6-tier synthesis + artifacts | 10 min | Sequence A |
| D | Rewind confirmation gate safety | 5 min | 2+ checkpoints |
| E | Mastery gate loop cap | 5 min | Active session |
| F | Atomic write failure detection | 3 min | None |

---

## How to Read These Sequences

- **TERMINAL** steps: run in bash
- **CHAT** steps: type in the Claude Code chat window
- **Look for**: what you should see if the test passes
- **PASS** / **FAIL** criteria are at the end of each sequence

---

## Recommended Test Order

```
A (15 min) → B (10 min) → C (10 min) → D (5 min) → E (5 min) → F (3 min)
Total: ~48 min for full system verification
```

For a quick smoke test: **A only** (15 min).

---

## Test Sequence A: Does everything work from scratch? (15 min)

**Purpose**: Full smoke test of the core workflow from health to checkpoint to recovery.

**Prerequisites**: None. Run this first.

---

**Step 1** — TERMINAL:
```bash
python3 scripts/health-check.py
```
Look for: `✅ HEALTHY — All 3 checks passed`

**Step 2** — TERMINAL:
```bash
python3 scripts/generate-html.py --demo
```
Look for: A new file appears in `visual-presentations/` with "demo" in the name.

**Step 3** — CHAT: Open Claude Code. Wait without typing anything.
Look for: A recovery banner (if prior progress exists) OR a fresh-start greeting. **Agent must NOT greet before checking the bridge.**

**Step 4** — CHAT: Type `Teach me the first concept in Chapter 1`
Look for: A vocabulary table at the top of the response, then a structured explanation following the TEACH cycle.

**Step 5** — CHAT: When the agent asks a comprehension question, type a weak answer: `I don't know`
Look for: Agent re-teaches using a **different approach**. It must NOT move on.

**Step 6** — CHAT: Give a proper answer in your own words (paraphrase what was just explained).
Look for: Agent confirms understanding, then provides a hands-on exercise.

**Step 7** — CHAT: Type `Checkpoint`
Look for: `Checkpoint L1 complete. Resuming from...`

**Step 8** — TERMINAL:
```bash
python3 scripts/health-check.py
```
Look for: `✅ HEALTHY` (still healthy after the checkpoint write)

**Step 9** — TERMINAL:
```bash
cat context-bridge/status.json
```
Look for: `lesson` field is NOT `"none"` — it should show the lesson you were just on.

**Step 10** — Close Claude Code completely. Open a new session.
Look for: A recovery banner that names your lesson and last checkpoint layer.

**PASS**: All 10 steps showed what was expected.

**Common failures**:

| Step | Failure | What it means |
|------|---------|--------------|
| Step 3 | Agent greets without checking bridge | Cold-start protocol not firing |
| Step 5 | Agent moves on after weak answer | Mastery gate not enforced |
| Step 7 | No confirmation message | Checkpoint workflow broken |
| Step 9 | lesson field still `"none"` | status.json write failed — run `Repair` |
| Step 10 | No recovery banner | Bridge write failed or status.json empty |

---

## Test Sequence B: Does spaced review work? (10 min)

**Purpose**: Verify that cold-start recall questions fire before new teaching.

**Prerequisites**: Sequence A must be completed first (need a checkpoint in the vocab bank).

---

**Step 1** — TERMINAL:
```bash
cat context-bridge/master-cumulative.md | grep -A 10 "## 7\."
```
Look for: Vocabulary bank has at least one row with a term name and a lesson reference.

**Step 2** — CHAT: Open a new Claude Code session. Do NOT type anything yet.
Look for: Before offering new teaching, the agent asks a cold recall question like "Before we continue — what is [term]?"

**Step 3** — CHAT: Give a weak answer to the recall question (e.g., `I'm not sure`)
Look for: Agent briefly re-explains the term, schedules it for tomorrow.

**Step 4** — CHAT: Give a strong answer to the next recall question (if there is one).
Look for: Agent confirms understanding and moves on to new content without re-explaining.

**PASS**: Spaced recall fired before new teaching, and weak/strong answers were handled differently.

**FAIL**: Agent jumps straight to new teaching without any recall question.

---

## Test Sequence C: Does Finish work? (10 min)

**Purpose**: Verify the 6-tier synthesis generates all expected artifacts.

**Prerequisites**: At least one checkpoint from Sequence A.

---

**Step 1** — CHAT: Type `Finish`
Look for: A confirmation dialog listing what will be created (HTML, cheatsheet, flashcards).

**Step 2** — CHAT: Type `YES`
Look for: Agent generates files and says "Lesson X.Y complete. 6-tier synthesis finished."

**Step 3** — TERMINAL: Run all three commands:
```bash
ls visual-presentations/
ls flashcards/
ls quick-reference/
```
Look for: At least one new file in each directory matching your lesson number.

**Step 4** — TERMINAL:
```bash
python3 scripts/generate-index.py
```
Look for: `✅ INDEX.html generated`

**Step 5** — Open `visual-presentations/INDEX.html` in a browser.
Look for: Your lesson card appears as a clickable tile. Click it — slides should navigate with arrow keys or clicks.

**PASS**: All three artifact directories have new files, INDEX.html opens, slides are interactive.

**Common failures**:

| Step | Failure | Fix |
|------|---------|-----|
| Step 1 | No confirmation dialog — just executes | Finish confirmation gate missing |
| Step 2 | No HTML file appears | Run `python3 scripts/generate-html.py --demo` to test pipeline |
| Step 3 | Missing flashcards or cheatsheet | Finish workflow incomplete — check chat output for errors |
| Step 5 | INDEX.html opens blank | Run `python3 scripts/generate-index.py` again |

---

## Test Sequence D: Does Rewind work safely? (5 min)

**Purpose**: Verify the Rewind confirmation gate works (prevents accidental rollback).

**Prerequisites**: At least two checkpoints (L1 and L2) from prior sequences.

---

**Step 1** — CHAT: Type `Rewind`
Look for: A numbered list of your checkpoints showing layer, timestamp, and concepts covered.

**Step 2** — CHAT: Type the layer you want to go back to (e.g., `L1`)
Look for: A **CONFIRMATION WARNING** asking you to type CONFIRM before proceeding.

**Step 3** — CHAT: Type anything OTHER than CONFIRM (e.g., `cancel`)
Look for: "Rewind cancelled — continuing from current position"

**Step 4** — CHAT: Type `Rewind` again, select a layer, then type `CONFIRM`
Look for: "Context restored to Checkpoint L{N}. {Concepts covered}. Ready to continue/revise?"

**PASS**: Step 3 cancelled cleanly (confirmation gate worked), Step 4 restored state (CONFIRM worked).

**FAIL (critical)**: If Rewind executes without asking you to type CONFIRM — the confirmation gate is missing. This is unsafe. Check `Knowledge_Vault/Protocols/rewind-checkpoint.md`.

---

## Test Sequence E: Does the mastery gate loop cap work? (5 min)

**Purpose**: Verify the agent never loops more than 3 times on the same concept.

**Prerequisites**: Be in an active teaching session.

---

**Step 1** — CHAT: Type `continue` to get to a new concept.

**Step 2** — CHAT: When the comprehension question appears, type: `I have no idea`
Look for: Agent re-teaches using a **different approach** (attempt 1 of re-teach).

**Step 3** — CHAT: Type: `Still don't understand`
Look for: Agent re-teaches again with a **third approach** (attempt 2 of re-teach).

**Step 4** — CHAT: Type: `I'm confused`
Look for: Either a third re-teach attempt (attempt 3) OR the flag `⚠️ NEEDS REVIEW` followed by a move to the next concept.

**PASS**: Agent does NOT loop a 4th time. It flags and continues.

**FAIL**:
- Agent loops again (4th+ time) without flagging — loop cap not enforced
- Agent gets stuck and won't continue — use the recovery phrase below

**Recovery phrase** if agent gets stuck:
```
Flag this concept as needs-review and continue
```

---

## Test Sequence F: Does atomic write failure detection work? (3 min)

**Purpose**: Verify that write failures are detected and surfaced as repair_needed.

**Prerequisites**: None.

---

**Step 1** — TERMINAL: Make the bridge file read-only, then try a backup:
```bash
chmod 444 context-bridge/master-cumulative.md
python3 scripts/checkpoint-write.py --action backup
chmod 644 context-bridge/master-cumulative.md
```
Look for: An error message from the script indicating write failure.

**Step 2** — TERMINAL:
```bash
cat context-bridge/status.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('repair_needed:', d.get('repair_needed', 'NOT SET'))"
```
Look for: `repair_needed: True`

**Step 3** — CHAT: Open Claude Code.
Look for: Agent warns about `repair_needed` in the recovery banner before offering to teach.

**PASS**: The flag was set (Step 2) and surfaced in chat (Step 3).

**FAIL**:
- Step 2 shows `repair_needed: False` — failure not detected
- Step 3 shows no warning — recovery banner not checking `repair_needed`
