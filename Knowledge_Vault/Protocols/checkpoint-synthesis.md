# Checkpoint Synthesis Protocol

> **Trigger**: User command `Checkpoint`
> **Output**: Versioned lesson part file + Updated cumulative bridge
> **Context Action**: Auto-reload from bridge
> **Cross-refs**: [Finish Synthesis](finish-synthesis.md) | [Rewind](rewind-checkpoint.md) | [Formatting Templates](../Pedagogy/formatting-templates.md)

---

## COMMAND NORMALIZATION

The Checkpoint command is recognized under the following conditions:

**Recognized forms** (all equivalent):
- `Checkpoint` / `checkpoint` / `CHECKPOINT` (case-insensitive)
- Command at start of message: "Checkpoint but also..." → execute checkpoint first, then handle remainder
- Phrases: "Save progress", "Quick checkpoint", "Let's checkpoint"

**NOT recognized** when embedded in an interrogative:
- Preceded by: "what is", "explain", "define", "how does", "about", "does", "why"
- Message contains "?" AND command word is not at the message start

**Detection rule**: If "checkpoint" appears as an imperative (standalone, or first word of sentence), trigger workflow. If embedded inside a question or explanation request, suppress.

---

## DIRECTIVE

Upon receiving the command **"Checkpoint"**, halt teaching and execute the following **two-tier archival workflow**. You are capturing progress at a semantic boundary to:
1. **Prevent context window bloat** via periodic archival
2. **Enable rollback** to earlier teaching states
3. **Support branching narratives** (explore alternative teaching paths)

**This is NOT a session end** -- you will resume teaching immediately after saving.

---

## STAGE 1: Session Audit (Since Last Checkpoint)

Before producing any output, analyze content **since the last checkpoint** (or session start if this is the first checkpoint):

1. **Identify last checkpoint timestamp**:
   - Read `.checkpoint-meta.json` from current lesson directory
   - If file doesn't exist, this is Checkpoint 1 (start = session beginning)
   - If file exists, find latest checkpoint timestamp

2. **Read teaching log first** (primary source — survives `/clear`):
   - Check for `{lesson-directory}/teaching-log-current.md`
   - **If file exists and has content**: Use as the authoritative record of concepts taught since last checkpoint. This file persists through `/clear` because it lives on disk, not in conversation memory.
   - **If file does not exist**: Fall back to conversation history (normal for very first checkpoint of a session before any teaching log was written)
   - **After Stage 5 completes successfully**: Truncate `teaching-log-current.md` to empty content (new concepts start fresh for next checkpoint interval)

   **Teaching log format** (written by Professor Agent after each TEACH cycle step):
   ```
   ## Concept: {Name}
   **Taught**: {ISO timestamp}
   **TEACH coverage**: T✓ E✓ A✓ C✓ H✓  (mark each as ✓ complete or ~ partial)
   **Key points**:
   - {point 1}
   - {point 2}
   **Vocab introduced**: {term1}, {term2}
   **Exercises completed**: {exercise name or "none"}
   ```

   **Extract from log or conversation** (same categories regardless of source):
   - **Concepts introduced**: Major ideas, definitions, explanations
   - **Vocabulary defined**: All new terms with definitions
   - **Frameworks taught**: Mental models, decision trees, formulas
   - **Exercises completed**: Hands-on practice with student work
   - **Anti-patterns discussed**: Failure modes, "What Goes Wrong" analysis
   - **Comprehension check results**: Questions asked + student performance
   - **Analogies used**: Real-world comparisons
   - **Visual aids**: Diagrams, tables, ASCII art produced
   - **Edge cases explored**: Boundary conditions, corner cases
   - **Strategic scenarios**: Orchestrator-level thinking exercises

3. **Discard conversational noise**:
   - Greetings and pleasantries
   - Administrative commands
   - Repeated false starts
   - Meta-discussion about teaching process
   - Unrelated side-questions
   - "Let me explain...", "Great!", "That's correct!" (artifacts)

4. **Determine checkpoint metadata** (deterministic rules — no subjective judgment):

   **Layer Assignment Algorithm** — read `.checkpoint-meta.json`, apply first matching rule:

   | Condition | Assign Layer |
   |-----------|-------------|
   | No prior checkpoints exist for this lesson | **L1** |
   | Content is exclusively definitions/vocabulary (no procedures) | **L1** |
   | L1 exists AND content includes mechanics/procedures/how-it-works | **L2** |
   | L2 exists AND content includes any of: anti-patterns, edge cases, strategic scenarios, failure analysis | **L3** |
   | L3 exists (or any LN exists) | **L{N+1}** (increment from last — no cap) |

   **Mixed-depth content** (single checkpoint spans multiple levels):
   - Assign the **HIGHEST depth level present**
   - Add to YAML frontmatter: `contains_layers: [L1, L2, L3]`

   **Semantic concept name**: Primary noun phrase most repeated in content. Kebab-case. Max 50 characters.

   **File existence check**: Glob `{X.Y}-L*-*.md`. If a file with the same layer already exists, append `-b` suffix: `{X.Y}-L2-hooks.md` → `{X.Y}-L2-hooks-b.md`

---

## STAGE 2: Master Lesson Documentation (Versioned Part)

**File naming pattern**: `{X.Y}-L{depth}-{semantic-concept}.md`

**Examples**:
- `3.1-L1-hook-architecture.md` (Lesson 3.1, Layer 1, fundamentals)
- `3.1-L2-custom-hooks.md` (Lesson 3.1, Layer 2, intermediate)
- `3.17-L3-orchestration-patterns.md` (Lesson 3.17, Layer 3, advanced)

**Output location**: `revision-notes/ch{N}-{chapter-kebab-name}/module{X}-{module-name}/{X.Y}-{lesson-name}/`

**Purpose**: A complete, standalone revision guide for THIS checkpoint's content only. Focused on the concepts taught since the last checkpoint.

### Required Structure

```markdown
---
lesson: "{X.Y}"
layer: "L{depth}"
depth: {1|2|3}
semantic_name: "{kebab-case-concept}"
title: "{Human-Readable Concept Title}"
concepts: ["{Concept 1}", "{Concept 2}", "{Concept 3}"]
tags: ["{tag1}", "{tag2}", "{tag3}"]
keywords: ["{keyword1}", "{keyword2}", "{keyword3}"]
prerequisites: ["{lesson.prerequisite}"]
difficulty: "{easy|intermediate|advanced}"
estimated_time: "{N}min"
date: "{YYYY-MM-DD}"
status: "complete"
parent_checkpoint: "L{N-1}"
---

# Lesson {X.Y} | Layer L{depth}: {Concept Title}

> **Checkpoint Part {N}** | {Date} | Session {NN}
> **Focus**: {One-sentence summary of this checkpoint's scope}

---

## Table of Contents
[Auto-generate based on sections below]

---

## 1. Key Vocabulary

| Term | Definition | Category |
|------|-----------|----------|
| {Term 1} | {Plain-language definition} | {Fundamental/Technical/Framework} |
| {Term 2} | {Plain-language definition} | {Fundamental/Technical/Framework} |

**Note**: Only terms introduced or reinforced **in this checkpoint**.

---

## 2-N. [One section per major concept taught in this checkpoint]

For each concept, include all five dimensions:

### {Concept Name}

#### What It Is
{Precise definition, 2-3 sentences}

#### Why It Matters
{Stakes, motivation, real-world impact}

#### How It Works
{Mechanics, step-by-step breakdown}

**Procedure**:
```
Step 1: {Action}
Step 2: {Action}
Step 3: {Action}
```

#### Where It Fits
{Connection to overall curriculum, this chapter, previous lessons}

#### What Can Go Wrong
{Failure modes, anti-patterns, edge cases}

**Common Pitfalls**:
- ❌ **{Anti-pattern name}**: {What happens}
  - ✅ **Fix**: {Correct approach}

**Visual Aids**:
[Include any diagrams, tables, or ASCII art used to explain this concept]

**Analogies**:
> {Real-world analogy used in teaching}

**Edge Cases**:
- {Edge case 1}: {How to handle}
- {Edge case 2}: {How to handle}

---

## N+1. Hands-On Exercises

### Exercise {N}: {Exercise Name}

**Objective**: {What student practices}

**Instructions**:
```
{Step-by-step procedure}
```

**Expected Outcome**:
```
{What success looks like}
```

**Student Performance**:
- {What the student did}
- {Mistakes made (if any)}
- {Corrections applied}

---

## N+2. Anti-Patterns & Failure Modes

### {Anti-Pattern Name}

**Pattern**: {Description of the anti-pattern}

**What Goes Wrong** (Four-Axis Analysis):
1. **Misapplication**: {How it's used incorrectly}
2. **Omission**: {What's left out}
3. **Excess**: {What's overdone}
4. **Interaction Failure**: {How it conflicts with other patterns}

**Fix**:
{Correct approach, step-by-step}

---

## N+3. Frameworks & Mental Models

### Framework {N}: {Framework Name}

**Formula/Pattern**:
```
{Compact representation}
```

**Components**:
1. **{Component 1}**: {Definition}
2. **{Component 2}**: {Definition}

**Application**:
{When and how to use this framework}

---

## N+4. Comprehension Check Results

### Question {N}
**Asked**: {Question text}

**Student Response**: {What student answered}

**Assessment**: {Pass/Partial/Fail}

**Model Answer**:
{Correct answer with explanation}

---

## N+5. Strategic Scenarios (If Applicable)

### Scenario {N}: {Scenario Name}

**Context**: {Setup}

**Challenge**: {What student had to solve}

**Student Approach**:
{What student did}

**Analysis**:
{Evaluation of approach, what worked, what didn't}

---

## N+6. Connection Map (Checkpoint-Scoped)

**Builds on** (from earlier checkpoints or lessons):
- {Concept A} (Lesson {X.Y}, L{N})
- {Concept B} (Lesson {X.Y}, L{N})

**Connects to** (parallel concepts):
- {Concept C} (Chapter {N})

**Enables** (future concepts):
- {Concept D} (next checkpoint or lesson)

---

## Appendix: Cross-References

**Previous Checkpoints**:
- L{N-1}: {semantic-name} -- {brief description}

**Related Lessons**:
- Lesson {X.Y}: {Title} -- {relationship}

**Source Material**:
- Official curriculum: {URL if provided}
```

---

### Voice Transformation Rules

**CRITICAL**: Transform all conversational teaching language into professional documentation voice.

| Content Type | Voice | Example |
|--------------|-------|---------|
| **Instructions** | Imperative | "Run the command...", "Check the output..." |
| **Concepts** | Third-person or passive | "The hook system registers...", "State is managed by..." |
| **General truths** | Passive voice | "Callbacks are invoked when..." |
| **Direct quotes** | Preserve as-is | Code comments, student questions |

**NEVER use**:
- Second-person "you/your" (except in direct quotes)
- Conversational artifacts ("Let me explain...", "Great job!", "As I mentioned...")
- Questions directed at reader (transform into statements or instructions)

**Examples**:
- ❌ "You should register your hook before calling it"
- ✅ "Register the hook before invoking it"

- ❌ "Let me show you how this works"
- ✅ "The following demonstrates the mechanism"

---

### Quality Gates (Must Pass Before Saving)

Run these checks before atomic write:

✅ **Completeness**: All concepts from Stage 1 audit appear in documentation
✅ **Clarity**: Standalone readable without conversation context
✅ **Professionalism**: Consistent headings, no conversational artifacts
✅ **Actionability**: At least 3 executable examples/procedures included

**Validation Script** (if implemented): `scripts/validate-notes.sh`

If quality gate fails, revise content before proceeding to Stage 3.

---

## STAGE 3: Cumulative Bridge Update

**File**: `context-bridge/master-cumulative.md`

**Update mode**: **APPEND** to existing sections (do NOT rewrite entire file)

### Pre-Write: Rolling Backup

**Before any append to the bridge**, execute backup:

1. **Read** `context-bridge/master-cumulative.md`
2. **Write copy** to `context-bridge/backup/master-cumulative-{YYYY-MM-DD}.md`
3. **Prune**: List all files in `context-bridge/backup/`. If count > 3, delete the file with the oldest date in its filename.
4. **Archive check**: Count lines in `master-cumulative.md`. If > 300:
   - Move Section 5 (Session Flow) older entries and Section 14 rows older than the 5 most recent into `context-bridge/archive/master-cumulative-archived-{YYYY-MM-DD}.md`
   - Append to master: `> See archive/master-cumulative-archived-{YYYY-MM-DD}.md for earlier content.`

Only then proceed with the append operations below.

### Sections to Update

#### Add to "Checkpoint History" table:
```markdown
| L{depth} | {YYYY-MM-DD HH:MM} | {Concepts covered} | {X.Y}-L{depth}-{concept}.md | ⏳ Saving... |
```

**Important**: Write status as `⏳ Saving...` now. After Stage 4 completes successfully, return to this row and update: `⏳ Saving...` → `✓ Archived`

If Stage 4 fails after all retries: update status to `⚠️ Meta failed — repair needed`

#### Append to "Vocabulary Bank":
```markdown
| {New Term} | {X.Y}-L{depth} | ✓ |
```
(Deduplicate: skip if term already in table)

#### Expand "Knowledge Graph":
```markdown
{X.Y}-L{depth}: {Concept Name}
    ├─ {Sub-concept A}
    └─ {Sub-concept B}
```

#### Add to "Anti-Patterns Covered":
```markdown
| {Anti-Pattern Name} | {X.Y} | Checkpoint L{depth} |
```

#### Append to "Frameworks Internalized":
```markdown
{N+1}. **{Framework Name}** ({X.Y}-L{depth}): {One-line summary}
```

#### Update "Current Checkpoint State":
```markdown
**Active Part**: L{depth}
**Last Checkpoint**: {YYYY-MM-DD HH:MM}
**Concepts Since Last Checkpoint**: [empty - just checkpointed]
**Context Window Status**: {message count since last checkpoint} messages
```

#### Update "Session History" (Section 17):
- If this is a new session (different date than last row), append a new row
- If same session (same date), update the checkpoint count in the existing row

#### Update "Backup Log" (Section 18):
```markdown
| backup/master-cumulative-{YYYY-MM-DD}.md | {YYYY-MM-DD HH:MM} | Checkpoint L{depth} |
```

---

### Snapshot Write (Rewind Support)

After ALL section updates above are complete, write a frozen snapshot:

**File**: `context-bridge/snapshots/lesson-{X.Y}-L{depth}-{semantic-concept}-snapshot.md`

**Content**:
```markdown
# Snapshot: Lesson {X.Y} Layer L{depth}
> **Frozen at**: {ISO8601 timestamp}
> **Semantic concept**: {kebab-case-name}
> **Purpose**: Read-only. Used by Rewind protocol. Do not modify.
> **Master bridge row**: L{depth} | {timestamp} | ⏳ Saving...

---

{Copy verbatim from master-cumulative.md at this moment:}

## Knowledge Graph (Section 6 snapshot)
{paste section 6 content}

## Vocabulary Bank (Section 7 snapshot)
{paste section 7 content}

## Checkpoint History (Section 14 snapshot)
{paste section 14 content — including the new ⏳ row just added}

## Current Checkpoint State (Section 15 snapshot)
{paste section 15 content}
```

This snapshot is **immutable** after creation. Never modify it.

---

### Full Bridge Structure (for reference)

If creating a NEW cumulative bridge (first checkpoint ever), use this template:

```markdown
# Session {NN} -- Cumulative Learning Progress

> **Started**: {YYYY-MM-DD}
> **Current Lesson**: {X.Y}
> **Current Layer**: L{depth}
> **Last Updated**: {YYYY-MM-DD HH:MM}

---

## 1. Project Essence
{2-3 sentences: what this project is, student goal, current chapter}

## 2. Student Profile & Learning DNA
[Same as end-of-session context bridge]

## 3. Established Teaching Patterns
[TEACH cycle, Try with AI framework, question protocols]

## 4. Key Technical Decisions
**File Naming**: `{X.Y}-L{depth}-{semantic-concept}.md`
**Directory Structure**: `revision-notes/ch{N}-{name}/module{X}/{lesson}/`

## 5. Session Flow
[Timeline of session events -- update with each checkpoint]

## 6. Knowledge Graph -- Concepts Mastered
```
Chapter {N}
├─ Lesson {X.Y}
│  ├─ L1: {Concept A}
│  ├─ L2: {Concept B}
│  └─ L3: {Concept C}
└─ Lesson {X.Z}
   └─ L1: {Concept D}
```

## 7. Vocabulary Bank -- Terms Introduced
| Term | First Introduced | Defined? |
|------|-----------------|----------|
| {Term A} | {X.Y}-L1 | ✓ |
| {Term B} | {X.Y}-L2 | ✓ |

## 8. Anti-Patterns Covered
| Anti-Pattern | Lesson | Checkpoint |
|-------------|--------|-----------|
| {Pattern A} | {X.Y} | L1 |

## 9. Frameworks Internalized
1. **{Framework A}** ({X.Y}-L1): {Summary}
2. **{Framework B}** ({X.Y}-L2): {Summary}

## 10. Student Strengths & Growth Areas
[Update based on comprehension checks in this checkpoint]

## 11. Collaboration Style & Tone
[Carry forward established rules]

## 12. Repository Structure
```
revision-notes/
├─ ch{N}-{name}/
│  └─ module{X}-{name}/
│     └─ {X.Y}-{lesson}/
│        ├─ .checkpoint-meta.json
│        ├─ {X.Y}-L1-{concept}.md
│        └─ {X.Y}-L2-{concept}.md
```

## 13. Next Steps
**Immediate Next**: Continue Lesson {X.Y} to L{depth+1} or next concept

## 14. Checkpoint History
| Layer | Timestamp | Concepts Covered | File | Status |
|-------|-----------|------------------|------|--------|
| L1 | {timestamp} | {concepts} | {file} | ✓ Archived |
| L2 | {timestamp} | {concepts} | {file} | ✓ Archived |

## 15. Current Checkpoint State
**Active Part**: L{depth}
**Last Checkpoint**: {timestamp}
**Concepts Since Last Checkpoint**: []
**Context Window Status**: {estimate}

## 16. How to Use This File
1. Load this file at session start: "Read context-bridge/session-{NN}-cumulative.md"
2. Review checkpoint history to see progress
3. Resume from "Current Checkpoint State"
```

---

## STAGE 4: Checkpoint Metadata (Atomic Write)

**File**: `revision-notes/ch{N}-{name}/module{X}/{X.Y}-{lesson}/.checkpoint-meta.json`

**Purpose**: Track checkpoint tree structure, enable Rewind command

### Write Process (With Retry)

1. **Write to temporary file**: `.checkpoint-meta.tmp.json`
2. **Build JSON structure**:

```json
{
  "lesson": "{X.Y}",
  "session": "{NN}",
  "last_updated": "{ISO8601 timestamp}",
  "checkpoints": [
    {
      "layer": "L1",
      "depth": 1,
      "semantic_name": "{kebab-case-concept}",
      "timestamp": "{ISO8601}",
      "concepts": ["{Concept A}", "{Concept B}"],
      "vocab_count": {N},
      "file": "{X.Y}-L1-{concept}.md",
      "context_state": "{Brief description}",
      "parent_checkpoint": null
    },
    {
      "layer": "L2",
      "depth": 2,
      "semantic_name": "{kebab-case-concept}",
      "timestamp": "{ISO8601}",
      "concepts": ["{Concept C}", "{Concept D}"],
      "vocab_count": {N},
      "file": "{X.Y}-L2-{concept}.md",
      "context_state": "{Brief description}",
      "parent_checkpoint": "L1"
    }
  ],
  "checkpoint_tree": "L1 ──> L2 ──> L3"
}
```

3. **Write with retry** (3 attempts):
   - **Attempt 1**: Write `.checkpoint-meta.json` immediately
   - **If fails**: Wait 1 second, retry (Attempt 2)
   - **If fails again**: Wait 2 seconds, retry (Attempt 3)
   - **All 3 fail**:
     a. Keep `.checkpoint-meta.tmp.json` intact (do NOT delete)
     b. Update bridge row status: `⏳ Saving...` → `⚠️ Meta failed — repair needed`
     c. Alert user:
        ```
        ⚠️ Stage 4 failed after 3 attempts.
        Notes and bridge are saved safely.
        Metadata could not be written.

        Options:
        - Type 'Repair' next session to auto-fix
        - Manually rename: .checkpoint-meta.tmp.json → .checkpoint-meta.json
        ```
     d. Continue to Stage 5 using `.tmp` file data (do NOT block teaching)

### Error Handling

- If all retries fail: Keep `.tmp` file, update bridge with `⚠️` status, continue gracefully
- On session start (via Resume Protocol): Check for `.tmp` files and `⚠️` bridge rows, offer repair
- After successful write: Update bridge row `⏳ Saving...` → `✓ Archived`

---

## STAGE 5: Auto-Reload Protocol

After writing checkpoint files successfully:

1. **Acknowledge completion**:
   ```
   ✅ Checkpoint L{depth} saved

   Files created:
   - Master notes: {file-path}
   - Bridge updated: context-bridge/master-cumulative.md
   - Backup created: context-bridge/backup/master-cumulative-{YYYY-MM-DD}.md
   - Snapshot saved: context-bridge/snapshots/lesson-{X.Y}-L{depth}-{concept}-snapshot.md
   - Metadata: .checkpoint-meta.json
   - Bridge row: ✓ Archived
   ```

2. **Signal context refresh**:
   ```
   🔄 Refreshing context window...
   ```

3. **Reload from cumulative bridge**:
   - Read `context-bridge/master-cumulative.md`
   - Parse checkpoint history (Section 14)
   - Identify current state (Section 15)
   - Also truncate `teaching-log-current.md` to empty content (new concepts start fresh)

4. **Reinitialize teaching state**:
   ```
   📍 Context restored

   **Lesson {X.Y}** | **Layer L{depth} complete**

   **Concepts covered** (this checkpoint):
   - {Concept A}
   - {Concept B}

   **Next**: {Next concept or layer}

   Ready to continue?
   ```

5. **Resume teaching**:
   - Do NOT rehash already-taught concepts
   - Move forward to next concept
   - Treat bridge as authoritative "ground truth"

---

## STAGE 6: Git Integration (Optional Auto-Commit)

**Trigger**: After successful checkpoint save (Stages 1-5 complete)

**Purpose**: Automatically commit and push checkpoint files to version control

### Workflow

1. **Check if git integration is available**:
   - Verify git repository exists
   - Check if `scripts/git-auto-push.py` exists
   - Skip if either is missing (graceful degradation)

2. **Invoke auto-push script** (worktree-aware):
   ```bash
   python3 scripts/git-auto-push.py checkpoint {X.Y} L{depth} --worktree-aware
   ```

3. **Script handles**:
   - Auto-detect git context (worktree vs main repo) via `get_git_context()`
   - Stage checkpoint files:
     - `revision-notes/{lesson-dir}/{X.Y}-L{depth}-{concept}.md`
     - `context-bridge/master-cumulative.md`
     - `context-bridge/snapshots/lesson-{X.Y}-L{depth}-*.md`
     - `context-bridge/backup/master-cumulative-*.md`
     - `.checkpoint-meta.json`
   - Create semantic commit message
   - Run pre-commit quality hook (validates notes)
   - Push to remote if configured
   - Error handling and rollback

4. **User notification**:
   ```
   📦 Git auto-commit:
   - Files staged: {count}
   - Commit: "docs(checkpoint): lesson {X.Y} layer L{depth}"
   - Quality hook: ✓ Passed
   - Pushed to: origin/main
   ```

### Skip Conditions

- **No git repo**: "Git not initialized, skipping auto-commit"
- **No remote**: "Commit saved locally (no remote configured)"
- **Quality failure**: "Quality checks failed, commit blocked (see pre-commit hook output)"
- **Push failure**: "Commit saved locally (push failed - may need to pull first)"

### User Control

- Users can disable auto-commit by removing the script
- Users can bypass quality hooks with `git commit --no-verify` (not recommended)
- Script supports `--dry-run` mode for testing

---

## EDGE CASES & HANDLING

### Edge Case 1: Checkpoint Called with No New Content

**Detection**: No concepts taught since last checkpoint (or session start)

**Response**:
```
⚠️ No new content to checkpoint yet.

Options:
- Continue teaching, then checkpoint when ready
- Type 'Finish' if lesson is complete
```

### Edge Case 2: First Checkpoint (No Existing Directory)

**Action**:
1. Create directory structure: `revision-notes/ch{N}-{name}/module{X}/{X.Y}-{lesson}/`
2. Create new `.checkpoint-meta.json` with first entry
3. Create new cumulative bridge if none exists
4. Proceed with normal checkpoint workflow

### Edge Case 3: Quality Gate Failure

**Scenario**: Validation detects missing examples, incomplete sections

**Action**:
```
❌ Quality check failed: Actionability score 1/3 (need 3+)

Missing:
- Runnable examples/procedures

Please add examples to the current concept, then retry 'Checkpoint'.
```

Do NOT save checkpoint. Wait for more teaching content, then user can retry.

### Edge Case 4: Metadata Corruption

**Detection**: `.checkpoint-meta.json` parse fails

**Recovery**:
1. Scan lesson directory for all `{X.Y}-L*-*.md` files
2. Extract YAML frontmatter from each
3. Reconstruct metadata from frontmatter
4. Write fresh `.checkpoint-meta.json`
5. Warn: "Metadata reconstructed from file frontmatter. Checkpoint tree may be incomplete."

---

## CONSTRAINTS

- **No HTML generation** (checkpoint only does T1 + T2, skip T3)
- **Incremental**: Only document content since last checkpoint
- **Focused**: Each part file covers one depth layer or major concept
- **Voice transformation**: Always apply professional documentation voice
- **Retry writes**: Use `.tmp` files + 3-attempt retry for metadata JSON
- **Quality gates**: Validate before saving (fill checklist, do not self-pass)
- **Auto-reload**: Treat reload as fresh start with bridge context
- **Teaching log write**: Append to `{lesson-dir}/teaching-log-current.md` after each TEACH cycle step completes. This file is the fallback audit source if `/clear` occurs before checkpoint.
- **Teaching log truncate**: After Stage 5 (auto-reload) completes successfully, overwrite `teaching-log-current.md` with empty content. New teaching starts fresh.
- **Bridge is master-cumulative.md**: Never reference old session-numbered bridge files.
- **Snapshot is mandatory**: Always write snapshot to `context-bridge/snapshots/` in Stage 3. No exceptions.

---

## SUCCESS CRITERIA

✅ Part file created with correct naming: `{X.Y}-L{depth}-{concept}.md`
✅ YAML frontmatter complete with all required fields
✅ Content uses imperative/third-person voice (no "you/your")
✅ All concepts from audit appear in documentation
✅ At least 3 executable examples/procedures included
✅ Cumulative bridge updated (appended, not replaced)
✅ Checkpoint metadata JSON updated atomically
✅ Context reload confirms current state and next steps
✅ Teaching resumes without repeating checkpointed content

---

## RELATED PROTOCOLS

- **Finish**: When lesson is complete → `Knowledge_Vault/Protocols/finish-synthesis.md`
- **Rewind**: To rollback to previous checkpoint → `Knowledge_Vault/Protocols/rewind-checkpoint.md`
- **Readiness Signals**: When to suggest checkpoint → `Knowledge_Vault/Frameworks/checkpoint-readiness-signals.md`
