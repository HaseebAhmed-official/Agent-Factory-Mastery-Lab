# Phase 0: Reliability Audit Protocol

> **Purpose**: Verify system foundation before adding features. Run this before trusting any Tier 2/3 improvements.
> **Time required**: ~30 minutes (5 sessions × ~6 minutes each)
> **Pass threshold**: 4/5 sessions fully correct

---

## WHY RUN THIS FIRST

The core reliability problem is: the system can APPEAR to work (no visible errors) while silently losing data. A checkpoint "succeeds" but writes incomplete content. Recovery "works" but restores the wrong state. This audit makes silent failures visible.

---

## SETUP

```bash
# From the repo root, verify scripts are ready:
python3 scripts/health-check.py
python3 scripts/session-start.py
```

Both should run without errors before proceeding.

---

## THE 5-SESSION TEST

### Session 1
1. Start a new Claude Code session in this repo
2. Ask Professor Agent: "Teach me the first concept in Chapter 1"
3. Let it teach for 5-10 minutes (at least one full TEACH cycle)
4. Type: `Checkpoint`
5. After checkpoint confirms, **manually open** `context-bridge/master-cumulative.md`

**Check** ✓/✗:
- [ ] All 18 sections present?
- [ ] Section 7 (Vocabulary Bank) has at least one new term row?
- [ ] Section 14 (Checkpoint History) has a new row?
- [ ] Section 15 shows the correct lesson and layer?
- [ ] `context-bridge/status.json` shows the correct lesson/concept?

---

### Session 2
1. Close the session completely
2. Open a NEW Claude Code session in this repo
3. Wait for cold-start recovery (do not type anything until Professor Agent greets you)

**Check** ✓/✗:
- [ ] Did Professor Agent display a recovery banner?
- [ ] Does the banner show the correct lesson from Session 1?
- [ ] Does the banner show the correct layer and concept?
- [ ] Did it offer to continue from the right place (not restart from scratch)?
- [ ] Did health-check show HEALTHY?

---

### Session 3
1. In the Session 2 window (or a new session), teach 2 more concepts
2. Type `Checkpoint` after each concept (2 checkpoints total)

**Check** ✓/✗:
- [ ] Second checkpoint appended to Section 14 (not replaced)?
- [ ] Third checkpoint appended (cumulative, not overwritten)?
- [ ] Bridge file size grew (not shrunk or stayed same)?
- [ ] No .tmp orphan files in context-bridge/?

---

### Session 4
1. Open a NEW session
2. Type `Rewind`
3. Select L1 (first checkpoint)
4. Type CONFIRM when prompted

**Check** ✓/✗:
- [ ] Did Rewind show a confirmation gate before executing?
- [ ] Did it restore to the correct checkpoint state?
- [ ] Was a snapshot file present in context-bridge/snapshots/?
- [ ] Did it offer the 3 branching options (Continue / Revise / Review)?

---

### Session 5
1. Open a NEW session
2. Teach 1 more concept fully (complete TEACH cycle)
3. Type `Finish`
4. Type YES when prompted for confirmation

**Check** ✓/✗:
- [ ] Did Finish show a confirmation dialog?
- [ ] Was an HTML file created in visual-presentations/?
- [ ] Was a cheatsheet created in quick-reference/?
- [ ] Was a flashcard JSON created in flashcards/?
- [ ] Did INDEX.html get updated in visual-presentations/?

---

## SCORING

| Sessions Passed | Result | Action |
|-----------------|--------|--------|
| 5/5 | ✅ FOUNDATION SOLID | Proceed to Tier 2/3 improvements |
| 4/5 | ✅ MOSTLY SOLID | Fix the one failure, retest, then proceed |
| 3/5 | ⚠️ NEEDS WORK | Debug failures before adding any features |
| <3/5 | ❌ FOUNDATION BROKEN | Run bridge-update.py and checkpoint-write.py diagnostics first |

---

## DIAGNOSING FAILURES

**Bridge sections missing after checkpoint**:
```bash
python3 scripts/health-check.py
python3 scripts/bridge-update.py --section 14 --content "| test | $(date) | test | test | ✓ |"
```

**Recovery banner not showing correct state**:
```bash
cat context-bridge/status.json
python3 scripts/session-start.py
```

**Orphaned .tmp files**:
```bash
find context-bridge/ -name "*.tmp"
# Inspect each, then remove if incomplete
```

**HTML not generated**:
```bash
python3 scripts/generate-html.py --demo
# Should create demo HTML in visual-presentations/
```

---

## RECORD YOUR RESULTS

Add a row to this table after each audit run:

| Date | Sessions Passed | Failures Found | Action Taken |
|------|-----------------|----------------|--------------|
| 2026-03-29 | _/5 | | |
