# Rewind Checkpoint Protocol

> **Trigger**: User command `Rewind`
> **Output**: Restored context + Branching options
> **Context Action**: Load selected checkpoint, offer continue/revise
> **Cross-refs**: [Checkpoint Synthesis](checkpoint-synthesis.md) | [Finish Synthesis](finish-synthesis.md)

---

## DIRECTIVE

Upon receiving the command **"Rewind"**, provide the student with a time-machine interface to:
1. **View checkpoint history** for the current lesson
2. **Select a previous checkpoint** to restore
3. **Load that checkpoint's context** (concepts, vocabulary, state)
4. **Choose next action**: Continue teaching, revise content, or branch to alternative approach

This enables **non-linear learning** -- the student can explore different teaching paths, revise difficult concepts, or experiment with alternative explanations.

---

## STAGE 1: List Available Checkpoints

### Step 1: Determine Current Lesson

**From current conversation context**:
- Ask student: "Which lesson to rewind? (Default: current lesson)"
- If student specifies lesson number: Use that
- If no lesson in current context: Prompt for lesson number

**Example**:
```
📼 Rewind Mode

Which lesson would you like to rewind?
- Type lesson number (e.g., "3.1", "3.17")
- Or press Enter to rewind current lesson (if in active lesson)
```

---

### Step 2: Read Checkpoint Metadata

**File**: `revision-notes/ch{N}-{name}/module{X}/{X.Y}-{lesson}/.checkpoint-meta.json`

**If file doesn't exist**:
```
⚠️ No checkpoints found for Lesson {X.Y}

This lesson hasn't been checkpointed yet. Options:
- Continue teaching, then use 'Checkpoint' to save progress
- Type 'Finish' to complete the lesson
```

**If file exists**: Parse JSON and extract checkpoint array

---

### Step 3: Display Checkpoint Tree

Generate visual tree diagram with metadata:

```
═══════════════════════════════════════════════════════
  CHECKPOINT HISTORY: Lesson {X.Y} -- {Title}
═══════════════════════════════════════════════════════

L1 │ Fundamentals: {Semantic Concept Name}
   │ 📅 {YYYY-MM-DD HH:MM}
   │ 📚 Concepts: {Concept A}, {Concept B}, {Concept C}
   │ 📖 Vocabulary: {N} terms
   │ 📄 File: {X.Y}-L1-{concept}.md
   │ ✅ Status: Archived
   │
   └─> L2 │ Intermediate: {Semantic Concept Name}
       │ 📅 {YYYY-MM-DD HH:MM}
       │ 📚 Concepts: {Concept D}, {Concept E}
       │ 📖 Vocabulary: {N} terms
       │ 📄 File: {X.Y}-L2-{concept}.md
       │ ✅ Status: Archived
       │
       └─> L3 │ Advanced: {Semantic Concept Name}
           │ 📅 {YYYY-MM-DD HH:MM}
           │ 📚 Concepts: {Concept F}, {Concept G}
           │ 📖 Vocabulary: {N} terms
           │ 📄 File: {X.Y}-L3-{concept}.md
           │ 🔄 Status: Current
```

**Branching visualization** (if multiple paths exist):
```
L1
 │
 └─> L2 (original)
     └─> L3 (original)

 └─> L2-revised (alternative approach)
     └─> L3-testing-patterns (different focus)
```

---

### Step 4: User Selection Prompt

```
Which checkpoint would you like to load?

Options:
- Type layer (e.g., "L1", "L2", "L3")
- Type "cancel" to exit rewind mode

Your choice:
```

---

### Confirmation Gate (Mandatory Before Execution)

Before executing any rewind, display:
```
⚠️ REWIND CONFIRMATION

You selected: Checkpoint L{N} — {concepts covered}

This will restore context to that point. Content taught after this checkpoint will need to be re-covered.

Type **CONFIRM** to proceed, or anything else to cancel.
```

If user types CONFIRM (case-insensitive): proceed with rewind execution.
If user types anything else: cancel and return to current state with message: "Rewind cancelled — continuing from current position."

---

## STAGE 2: Context Restoration

Once user selects checkpoint (e.g., "L2") and confirms:

### Step 1: Read Selected Checkpoint File

**File**: `{X.Y}-L{selected}-{concept}.md`

**Parse**:
- YAML frontmatter (concepts, tags, prerequisites, etc.)
- Vocabulary section (extract all terms)
- Concepts taught (extract headings)
- Frameworks introduced (extract framework names)
- Exercises completed (extract exercise names)

---

### Step 2: Read Snapshot File for Selected Checkpoint

**File**: `context-bridge/snapshots/lesson-{X.Y}-L{selected}-*-snapshot.md`

**Why snapshots instead of bridge reconstruction**:
The `master-cumulative.md` bridge is append-only and never rolled back. Rolling it back would destroy all learning from lessons/checkpoints that came AFTER the selected rewind point. Instead, each checkpoint saves a frozen snapshot that captures bridge state at that exact moment.

**If snapshot file exists** (standard path):
- Parse the frozen sections: Knowledge Graph, Vocabulary Bank, Checkpoint History, Current State
- This IS the authoritative state — no reconstruction needed

**If snapshot file does NOT exist** (legacy checkpoint predating snapshot system):
- Fall back to metadata reconstruction (original approach: cumulate all checkpoints ≤ selected layer)
- Warn: "⚠️ This checkpoint was created before the snapshot system was introduced. Context restoration may be incomplete."

**Generate summary from snapshot content**:
```
📍 Context Restored to Checkpoint L{selected}

**Lesson {X.Y}** | **Layer L{selected}: {Semantic Concept}**
**Timestamp**: {from snapshot header}

**Knowledge Graph** (at this checkpoint):
{paste from snapshot Section 6}

**Vocabulary Known** (at this checkpoint): {N} terms
{list from snapshot Section 7}

**Checkpoint History** (at this point):
{table from snapshot Section 14}
```

---

### Step 3: Confirm Restoration

```
✅ Context restored to Checkpoint L{selected}

You've rewound to: **{Semantic Concept Name}** ({YYYY-MM-DD HH:MM})

**What's next?**
```

---

## STAGE 3: Branching Decision

Present user with three options:

```
═══════════════════════════════════════════════════════
  REWIND OPTIONS
═══════════════════════════════════════════════════════

1️⃣ CONTINUE FROM HERE
   Resume teaching from this checkpoint with NEW content.
   Future checkpoints will branch from this point.

2️⃣ REVISE THIS CHECKPOINT
   Re-teach the concepts in THIS checkpoint with a different approach.
   Will archive old checkpoint and create revised version.

3️⃣ REVIEW & EXIT
   Just review this checkpoint's content, then return to current state.
   No changes made.

Your choice (1/2/3):
```

---

### Option 1: Continue from Here (Branching)

**User selects**: 1

**Workflow**:
1. Mark current state as "rewound to L{selected}"
2. User begins teaching new content
3. When user says "Checkpoint" next:
   - **Detect**: Next checkpoint would be L{selected+1}, but L{selected+1} already exists
   - **Trigger**: Branching conflict detection (see Stage 4)

**Example**:
```
✅ Ready to continue from Checkpoint L2

I'll resume teaching from where L2 left off. When you checkpoint next, we'll create L3 content.

What concept would you like to explore next?
```

---

### Option 2: Revise This Checkpoint

**User selects**: 2

**Workflow**:
1. Archive existing checkpoint file:
   ```bash
   mv {X.Y}-L{selected}-{old-concept}.md \
      .archive/{X.Y}-L{selected}-{old-concept}-{timestamp}.md
   ```

2. Begin re-teaching THIS checkpoint with new approach
3. When user says "Checkpoint":
   - Create NEW `{X.Y}-L{selected}-{new-concept}.md`
   - Update metadata: Mark old as archived, new as active
   - Preserve checkpoint history for both versions

**Example**:
```
✅ Revision mode activated for Checkpoint L2

The original L2 checkpoint will be archived. Let's re-teach this concept with a fresh approach.

What angle should we take this time? (e.g., different analogy, more hands-on, strategic focus, etc.)
```

---

### Option 3: Review & Exit

**User selects**: 3

**Workflow**:
1. Display checkpoint content summary (from part file)
2. Offer to open HTML presentation for that checkpoint
3. Return to current state without changes

**Example**:
```
✅ Reviewing Checkpoint L2

**Content Summary**:
{2-3 paragraphs summarizing what was taught in L2}

**Key Concepts**:
- {Concept D}: {Brief description}
- {Concept E}: {Brief description}

**Visual Review**:
Open `visual-presentations/session-{NN}-lesson-{X.Y}-L2-presentation.html` to see slides.

Returning to current checkpoint (L3)...
```

---

## STAGE 4: Intelligent Merge (Branching Conflict Detection)

**Trigger**: User chose "Continue from here" (Option 1), taught new content, says "Checkpoint"

**Scenario**:
- User rewound to L2
- L3 already exists (original path)
- User creates NEW content diverging from original L3
- Checkpoint command triggered

---

### Step 1: Topic Analysis (Diff-Style Delta View)

**Compare**: User's new content vs existing L3 checkpoint

**Generate diff report**:

```
═══════════════════════════════════════════════════════
  BRANCHING DETECTED
═══════════════════════════════════════════════════════

You're creating new content after L2. Existing L3 covers:

📦 EXISTING L3 (Original):
├─ Performance Optimization
│  └─ Memoization, lazy loading, caching
└─ Error Boundaries
   └─ Hooks in error states, fallback UI

🆕 YOUR NEW CONTENT:
├─ Performance Optimization [OVERLAP]
│  └─ Memoization, lazy loading [SAME]
├─ Testing Strategies [NEW]
│  └─ Mocking hooks, test utilities
└─ Debugging Patterns [NEW]
   └─ DevTools, common mistakes

═══════════════════════════════════════════════════════
  MERGE STRATEGIES
═══════════════════════════════════════════════════════

1️⃣ ARCHIVE & REPLACE
   Archive old L3, create new L3 with your content.
   Original preserved in .archive/ for reference.

2️⃣ CREATE BRANCH
   Keep original L3, create L3-revised (separate path).
   Both versions remain accessible.

3️⃣ INTELLIGENT MERGE
   Enhance original L3 by merging your new content:
   - OVERLAP (Performance): Append new examples to existing
   - NEW (Testing): Insert as new section after Performance
   - NEW (Debugging): Insert as new section after Testing

Your choice (1/2/3):
```

---

### Step 2: Execute Merge Strategy

#### Strategy 1: Archive & Replace

```bash
# Archive original
mv {X.Y}-L3-{old-concept}.md .archive/{X.Y}-L3-{old-concept}-{timestamp}.md

# Create new L3
# (Normal checkpoint workflow creates {X.Y}-L3-{new-concept}.md)

# Update metadata
{
  "layer": "L3",
  "semantic_name": "{new-concept}",
  "status": "active",
  "replaced": "{old-concept}",
  "archived_file": ".archive/{X.Y}-L3-{old-concept}-{timestamp}.md"
}
```

**Checkpoint tree**:
```
L1 ──> L2 ──> L3 (archived)
             └──> L3-new (active)
```

---

#### Strategy 2: Create Branch

```bash
# Keep original L3
# {X.Y}-L3-{old-concept}.md remains unchanged

# Create new branch
# {X.Y}-L3-{new-concept}.md created with new content

# Update metadata
{
  "layer": "L3",
  "semantic_name": "{new-concept}",
  "status": "active-branch",
  "parent_checkpoint": "L2",
  "sibling_checkpoint": "L3-{old-concept}"
}
```

**Checkpoint tree**:
```
L1 ──> L2 ──> L3-performance (original)
          └──> L3-testing-debugging (revised branch)
```

**Both paths** remain navigable. Student can explore both interpretations.

---

#### Strategy 3: Intelligent Merge

**Apply merge rules** (from plan):

| Content Type | Action | Implementation |
|--------------|--------|----------------|
| **OVERLAP** | APPEND new examples | Add to existing section, preserve original |
| **NEW sub-concepts** | INSERT as new section | Add heading, slot into logical position |
| **CORRECTION** | REPLACE that section | Remove flawed explanation, insert corrected |
| **REORGANIZATION** | MERGE intelligently | Reorder, deduplicate, optimize flow |

**Example merge**:

```markdown
## Performance Optimization

### Memoization (Original Content)
{Original explanation}

### Lazy Loading (Original Content)
{Original explanation}

### Memoization - Additional Examples (NEW)
{New examples added from user's content}

## Testing Strategies (NEW SECTION)
{Entire new section inserted}

## Debugging Patterns (NEW SECTION)
{Entire new section inserted}

## Error Boundaries (Original Content)
{Original explanation preserved}
```

**Update metadata**:
```json
{
  "layer": "L3",
  "semantic_name": "{merged-concept}",
  "status": "merged",
  "merge_source": "L3-{old-concept}",
  "merge_strategy": "append+insert",
  "merge_timestamp": "{ISO8601}"
}
```

---

### Step 3: Confirm Merge

```
✅ Merge complete

**Strategy applied**: {Strategy chosen}

**Updated file**: {X.Y}-L3-{concept}.md

**Changes**:
├─ Original content: {Preserved/Archived/Enhanced}
├─ New sections added: {N}
└─ Examples appended: {N}

Continue teaching or type 'Finish' to complete lesson?
```

---

## EDGE CASES & HANDLING

### Edge Case 1: Rewind with No Checkpoints

**Scenario**: User says "Rewind" but no .checkpoint-meta.json exists

**Response**:
```
⚠️ No checkpoints available for this lesson yet.

Create your first checkpoint:
1. Teach a major concept
2. Type 'Checkpoint' to save progress

Then you can use 'Rewind' to go back.
```

---

### Edge Case 2: Rewind to L1, Skip L2, Create L3

**Scenario**: User rewinds to L1, teaches new content, wants to create L3 (skipping L2)

**Action**:
- Allow it -- layers are semantic, not strictly sequential
- Metadata shows: `parent_checkpoint: "L1"` (skipped L2)
- Checkpoint tree: `L1 ──> L2 (original) └──> L3 (branch from L1)`

**Note**: Depth numbers may not be contiguous in branching scenarios

---

### Edge Case 3: Multiple Students, Same Repo

**Scenario**: Student A and B both rewind same lesson, create different branches

**Action**: Use Git branches (if Git integration enabled)

```
main
├─ student-a/lesson-3.1
│  ├─ L1
│  ├─ L2
│  └─ L3-student-a-version
└─ student-b/lesson-3.1
   ├─ L1
   ├─ L2
   └─ L3-student-b-version
```

Concept map shows both as separate nodes (different interpretations)

---

### Edge Case 4: Rewind During Active Teaching

**Scenario**: User is mid-concept (not checkpointed), says "Rewind"

**Action**:
```
⚠️ Unsaved progress detected

You have un-checkpointed content from current teaching session.

Options:
1. Checkpoint current progress first, then rewind
2. Discard current progress and rewind anyway
3. Cancel rewind

Your choice (1/2/3):
```

---

## CONSTRAINTS

- **Non-destructive**: Original checkpoints preserved (archived, not deleted)
- **Master bridge is NEVER rolled back**: `master-cumulative.md` is append-only. Rewind reads from snapshots — the master bridge continues to accumulate forward even after a rewind.
- **Snapshots are read-only**: Files in `context-bridge/snapshots/` are never modified or deleted during Rewind. They are permanent historical records.
- **Rewind is non-destructive by design**: Restoring context from a snapshot does NOT erase newer checkpoints — those files and bridge entries remain intact.
- **Cross-lesson rewind**: If user says "Rewind" without a lesson context, Stage 1 Step 1 ALWAYS asks "Which lesson?" first. Default is current lesson only if clearly in an active lesson.
- **Branching support**: Multiple paths from same parent checkpoint allowed
- **User choice**: Always present options, never auto-decide merge strategy
- **Visual clarity**: Checkpoint trees must be clear and navigable
- **Metadata integrity**: Checkpoint JSON always reflects current state
- **Context accuracy**: Restored state from snapshot matches checkpoint timestamp exactly

---

## SUCCESS CRITERIA

✅ User can list all checkpoints for a lesson with visual tree
✅ User can select checkpoint and context is restored
✅ Three options presented: Continue, Revise, Review
✅ Branching conflict detected when new content diverges
✅ Diff-style analysis shows NEW vs OVERLAP
✅ Three merge strategies offered with clear explanations
✅ User choice respected, merge executed correctly
✅ Metadata updated to reflect branching/merging
✅ Original content preserved (archived or kept as branch)

---

## RELATED PROTOCOLS

- **Checkpoint**: Create checkpoints → `checkpoint-synthesis.md`
- **Finish**: Complete lesson → `finish-synthesis.md`
- **Readiness Signals**: When to suggest checkpoint → `../Frameworks/checkpoint-readiness-signals.md`
