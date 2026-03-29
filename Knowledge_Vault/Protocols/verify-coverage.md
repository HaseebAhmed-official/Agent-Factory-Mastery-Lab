# Verify Coverage Protocol

> **Trigger**: User command `Verify` (on-demand only)
> **NOT triggered by**: Checkpoint, Finish, or any automatic process
> **Purpose**: Compare checkpoint notes against actual curriculum book URL — detect gaps, missing topics, and terminology drift
> **Output**: 3-tier coverage report + `pending-topics.md` update
> **Cross-refs**: [Checkpoint Synthesis](checkpoint-synthesis.md) | [Curriculum](../Curriculum/)

---

## DIRECTIVE

Upon receiving the command **"Verify"**, execute a coverage audit comparing what was taught (checkpoint notes) against what the curriculum says (fetched from lesson URL). This is a **quality assurance and gap detection tool** — it does not teach, does not checkpoint, and does not modify checkpoint files.

**Keep Verify separate from Checkpoint.** Bundling them would make every checkpoint slow and network-dependent. Run Verify when the student wants to assess completeness — not automatically.

---

## STAGE 1: Identify Lesson and Fetch URL

### Step 1: Determine the lesson to verify
- From current context: use the active lesson number
- If ambiguous, ask: "Which lesson to verify? (e.g., 2.1, 3.1)"

### Step 2: Get the lesson URL
Priority order:
1. Read `.checkpoint-meta.json` for `source_url` field
2. Check `Knowledge_Vault/Curriculum/` chapter file for lesson URL
3. Check `MEMORY.md` lesson URL section
4. If not found: Ask student — "Please paste the lesson URL from the course site"

### Step 3: Fetch the curriculum page
- Use **WebFetch tool** to retrieve the lesson URL
- If fetch fails (network error, paywall, 404):
  - Report: "Could not fetch {URL}. Options: (1) Try again, (2) Verify against cached curriculum file, (3) Cancel"
  - If cached file available: use `Knowledge_Vault/Curriculum/chapter-{N}-*.md` as fallback
- Extract from fetched content:
  - All **H1–H4 headings** (major topics and subtopics)
  - All **bolded terms** (defined concepts)
  - All **numbered/bulleted concept lists** (enumerated topics)
  - Any explicit **learning objectives** or "What you'll learn" sections

### Step 4: Build Curriculum Topic Inventory
```
CURRICULUM TOPICS ({N} total):
[H2] {Major Topic 1}
  [H3] {Subtopic 1.1}
  [H3] {Subtopic 1.2}
[Bold] {Defined Term A}
[Bold] {Defined Term B}
[List] {Enumerated concept 1}
[List] {Enumerated concept 2}
...
```

---

## STAGE 2: Parse Checkpoint Notes

### Step 1: Locate all checkpoint files
- Glob: `revision-notes/**/` for all `{X.Y}-L*.md` files matching current lesson
- Example: all files matching `2.1-L*.md` in the lesson directory

### Step 2: Extract from each file
From every checkpoint file found:
- **Section 1** (Key Vocabulary) — extract all `Term` column values
- **Section headings H2/H3** — extract all concept section names
- **"Key Takeaways"** sections — extract all bullet items

### Step 3: Build Notes Topic Inventory
```
NOTES TOPICS ({N} total from {N} checkpoint files):
[Vocab] {Term from L1 vocab table}
[Concept] {H2 section heading from L1}
[Concept] {H3 section heading from L2}
[Takeaway] {Item from L3 key takeaways}
...
```

---

## STAGE 3: Semantic Comparison (4-Rule Matching)

**Simple string matching is insufficient.** Apply these rules in order:

---

### Rule 1 — Direct Match
- If a curriculum topic appears **verbatim** (case-insensitive) in the notes → **✅ COVERED**
- Example: Curriculum "Intent Layer" matches Notes "Intent Layer" ✅

---

### Rule 2 — Synonym Match
Check against the pre-seeded synonym table AND the 70% word-overlap heuristic:

**Synonym Table** (expand as new aliases are discovered):
```
Intent Layer          = Goals Layer = Specification Layer = Requirements Layer
Orchestrator          = Coordinator = Router Agent = Controller Agent
Hook System           = Extension Points = Plugin Architecture = Event Hooks
Context Window        = Token Limit = Memory Boundary = Token Budget
AIDD                  = AI-Driven Development = AI-Assisted Development
Ralph Wiggum Loop     = Autonomous Recovery Loop = Self-Healing Loop
Structured Text       = Formatted Text = Marked-Up Text
Unstructured Text     = Plain Text = Free-Form Text
Comprehension Check   = Understanding Check = Knowledge Verification
Anti-Pattern          = Failure Mode = Bad Practice = Common Mistake
```

**70% Word-Overlap Heuristic**:
- Remove stop words (the, a, an, is, are, of, for, in, to, with...)
- If 70%+ of significant words overlap between curriculum topic and notes topic → likely match
- Example: "AI Verification Framework" vs "AI Verification Process" → 2/3 significant words match → likely match

If Rule 2 matches: → **✅ COVERED** + flag **"⚠️ TERMINOLOGY DRIFT"**
```
⚠️ TERMINOLOGY DRIFT:
   Curriculum: "Intent Layer"
   Notes use:  "Goals Layer"
   Action needed: Add alias to vocabulary bank, or retitle section
```

---

### Rule 3 — Conceptual Inclusion
- If a curriculum topic is a **subset** of a broader concept in the notes
- Example: Curriculum says "loop detection" and notes cover "Ralph Wiggum Loop failure modes" (includes loop detection as a subcase)
- → **✅ COVERED** (with note: "Covered as part of broader concept '{notes topic}'")

---

### Rule 4 — No Match
- If no rule above produces a match → **❌ MISSING**
- Record the curriculum section where this topic appears (for prioritization)

---

## STAGE 4: Generate Coverage Report

Display this report in the conversation:

```
═══════════════════════════════════════════════════════════════
  COVERAGE REPORT: Lesson {X.Y} — {Lesson Title}
  Verified: {YYYY-MM-DD HH:MM}
  Source: {URL}
  Checkpoint files analyzed: {N} files (L1 through L{N})
═══════════════════════════════════════════════════════════════

SUMMARY
  Curriculum topics found:  {total}
  ✅ Fully covered:          {N} ({%})
  ⚠️ Terminology drift:      {N}
  ❌ Missing:                {N} ({%})

───────────────────────────────────────────────────────────────
✅ COVERED ({N} topics)
  • {Topic A}
  • {Topic B}
  ...

───────────────────────────────────────────────────────────────
⚠️ TERMINOLOGY DRIFT ({N} topics)
  • Curriculum: "{Curriculum Term}" → Notes use: "{Notes Term}"
    Fix: Add "{Curriculum Term}" as alias in vocab bank, or rename section
  • ...

───────────────────────────────────────────────────────────────
❌ MISSING ({N} topics)
  • {Topic X}
    → Curriculum location: {section name / heading level}
    → Priority: {High = H2 heading | Medium = H3 | Low = list item}
  • {Topic Y}
    → Curriculum location: {section}
    → Priority: {level}

═══════════════════════════════════════════════════════════════
```

---

## STAGE 5: Update pending-topics.md

**File**: `revision-notes/{lesson-directory}/pending-topics.md`

### If file does NOT exist — create it:
```markdown
# Pending Topics: Lesson {X.Y} — {Lesson Title}

> **Last verified**: {YYYY-MM-DD HH:MM}
> **Source**: {URL}
> **Coverage**: {N}/{total} ({%})

---

## Missing Topics (from curriculum)

- [ ] **{Topic X}** *(Priority: High)*
  - Curriculum section: "{section name}"
  - Notes: Not found in any checkpoint file

- [ ] **{Topic Y}** *(Priority: Medium)*
  - Curriculum section: "{section name}"
  - Notes: Not found in any checkpoint file

---

## Terminology Drift to Resolve

- [ ] Curriculum says **"{Curriculum Term}"** — notes use **"{Notes Term}"**
  - Action: Add alias to `{X.Y}-L1-*.md` vocabulary bank section 1

---

## Resolution Log

| Topic | Resolved | Checkpoint | Date |
|-------|----------|------------|------|
| (auto-populated as topics are covered) | | | |
```

### If file ALREADY exists — update it:
- Update `> **Last verified**` header with new date
- Update `> **Coverage**` score
- For topics now covered: change `- [ ]` to `- [x]` and add to Resolution Log
- Append new missing topics that weren't in the previous version
- **Never delete** previously resolved items — they form the progress audit trail

---

## STAGE 6: Update Master Bridge

Append to `context-bridge/master-cumulative.md` — add or update a "Coverage Reports" section:

```markdown
## Coverage Reports
| Lesson | Date | Score | Missing Topics | Drift Items |
|--------|------|-------|----------------|-------------|
| {X.Y} | {date} | {N}/{total} ({%}) | {count} | {count} |
```

If section already exists, append a new row. Do not overwrite existing rows.

---

## STAGE 7: Offer Next Actions

After displaying the report, always offer:

```
What would you like to do?

1. Teach missing topics now → Start with highest-priority ❌ topic
2. Fix terminology drift → Update vocabulary banks in checkpoint files
3. Save report and continue teaching → Resume from where we left off
4. Exit → No further action (report and pending-topics.md already saved)

Your choice (1/2/3/4):
```

**If student chooses 1**: Begin teaching the first `❌ MISSING` topic in priority order (H2 topics first). Use the full TEACH cycle. Suggest `Checkpoint` after covering the missing topics.

**If student chooses 2**: For each terminology drift item, offer to update the relevant vocab bank entry in the checkpoint file to add the curriculum term as a primary name and the current term as an alias.

---

## EDGE CASES

### URL Fetch Failure
- Report: "Could not fetch {URL}: {error}"
- Offer: Verify against cached `Knowledge_Vault/Curriculum/chapter-{N}-*.md` file
- If cached file used: note in report header: "Source: Cached curriculum (URL unavailable)"

### No Checkpoint Files Found
```
⚠️ No checkpoint files found for Lesson {X.Y}.
This lesson hasn't been checkpointed yet.
Coverage: 0/{total} topics (0%)
All {total} curriculum topics are pending.
```
Still generate `pending-topics.md` with all curriculum topics as missing.

### Curriculum Page Has No Clear Structure (No Headings)
- Parse body text for noun phrases
- Flag: "Curriculum page has limited structure. Topic extraction may be incomplete."
- Show what was found with low confidence markers

### Verify Called with No Known Lesson
- Ask: "Which lesson would you like to verify? (e.g., 2.1, 3.1)"

---

## CONSTRAINTS

- **On-demand ONLY** — never triggered automatically by Checkpoint or Finish
- **Does NOT modify checkpoint `.md` files** — only `pending-topics.md` and master bridge coverage section
- **Does NOT teach** — Stage 7 option 1 starts teaching only if student explicitly requests it
- **Terminology drift is advisory** — flags issues but does not auto-rename
- **Always save pending-topics.md** (Stage 5) regardless of Stage 7 choice
- **Network failure is graceful** — cached curriculum is an acceptable fallback
- **Report is honest about uncertainty** — Rule 2 (synonym) and Rule 3 (inclusion) matches are flagged differently than Rule 1 (direct) matches

---

## SUCCESS CRITERIA

✅ Curriculum topics extracted from fetched URL
✅ Notes topics extracted from all checkpoint files
✅ 4-rule semantic matching applied (direct → synonym → inclusion → missing)
✅ Terminology drift detected and flagged (not silently ignored)
✅ 3-tier coverage report generated with percentages
✅ pending-topics.md created/updated in lesson directory
✅ Master bridge coverage section updated
✅ Student offered actionable next steps
✅ URL failure handled gracefully with cached fallback

---

## RELATED PROTOCOLS

- **Checkpoint**: Creates the notes being verified → `checkpoint-synthesis.md`
- **Finish**: Should be run after Verify to ensure complete lesson coverage → `finish-synthesis.md`
- **Resume**: Loads context at session start (different from Verify) → `resume-protocol.md`
- **Curriculum files**: Cached curriculum content → `Knowledge_Vault/Curriculum/`
