# Checkpoint Readiness Signals

> **Purpose**: Detection heuristics for proactive checkpoint suggestions
> **Used by**: Teaching agent to identify natural semantic boundaries
> **Cross-refs**: [Checkpoint Synthesis](../Protocols/checkpoint-synthesis.md) | [TEACH Cycle](../Pedagogy/teach-cycle.md)

---

## DIRECTIVE

**Do NOT auto-checkpoint without user permission** (unless explicitly configured in user settings).

**DO suggest checkpoints proactively** when strong or moderate signals appear, using the phrasing templates below.

**Philosophy**: Checkpoints should occur at **semantic boundaries** -- natural completion points where the student has mastered a cohesive unit of knowledge.

---

## SIGNAL TAXONOMY

### 🟢 Strong Signals (High Confidence)

Suggest checkpoint immediately when ANY of these appear:

#### 1. TEACH Cycle Complete for Major Concept

**Criteria**:
- ✅ **T**erminology: All terms defined
- ✅ **E**xplain: What/Why/How/Where/What Goes Wrong covered
- ✅ **A**nalogize: Real-world analogy provided
- ✅ **C**heck Understanding: Comprehension question asked AND **student passed**
- ✅ **H**ands-On: Exercise completed successfully

**Example scenario**:
- Taught "Hook Architecture" concept
- Defined: Hook, Lifecycle, Registration, Callback
- Explained: What hooks are, why they matter, how they work, where they fit, failure modes
- Analogy: "Like event listeners in JavaScript..."
- Comprehension check: Asked "Explain hook lifecycle in your own words" → Student answered correctly
- Exercise: "Register a simple hook" → Student completed successfully

**Trigger**: All 5 TEACH components complete ✅

**Suggestion phrasing**:
```
🎯 Strong checkpoint opportunity

We've completed the full TEACH cycle for {Concept Name}:
✅ Terminology defined
✅ Depth explanation delivered
✅ Analogy provided
✅ Comprehension check passed
✅ Hands-on exercise completed successfully

This is a natural checkpoint. Type 'Checkpoint' to save progress and refresh context, or continue to {next concept}.
```

---

#### 2. User Explicitly Requests Save

**Triggers**:
- User says: "Checkpoint"
- User says: "Save progress"
- User says: "Let's pause here"
- User says: "Can we save this?"

**Action**: Execute checkpoint immediately (no suggestion needed)

---

#### 3. Natural Curriculum Boundary

**Criteria**:
- Completed a **numbered subsection** from official curriculum
- Finished a **framework introduction + application**
- Completed a **major thematic unit** (e.g., "Fundamentals" → ready to move to "Intermediate")

**Detection**:
- Check if current concept maps to a subsection heading in curriculum
- Verify subsection is complete (all sub-topics covered)

**Example**: Official curriculum shows:
```
3.1 Hook Architecture
  3.1.1 Hook Basics
  3.1.2 Lifecycle Management
  3.1.3 Registration Patterns
3.2 Custom Hooks
```

If just completed 3.1.3, suggest checkpoint before moving to 3.2.

**Suggestion phrasing**:
```
📚 Curriculum checkpoint

We've completed subsection {X.Y.Z} ({Subsection Name}). This is a natural boundary in the official curriculum.

Checkpoint here before moving to {Next Subsection}?
```

---

#### 4. Depth Layer Transition

**Criteria**:
- Student has mastered **fundamentals** (L1 content)
- Ready to move to **intermediate** (L2 content)
- OR: Completed intermediate, ready for **advanced** (L3)

**Detection**:
- Concepts taught so far are foundational (definitions, basic usage)
- Next concept introduces complexity (optimization, edge cases, advanced patterns)

**Suggestion phrasing**:
```
🚀 Layer transition detected

You've mastered the fundamentals (L1). Ready to checkpoint and move to intermediate concepts (L2)?

This creates a clean break between foundational and advanced material.
```

---

### 🟡 Moderate Signals (Suggest but Don't Push)

Suggest checkpoint when **2 or more** moderate signals appear together:

#### 1. Context Window Accumulation

**Criteria**:
- Estimated **30k+ tokens** in conversation (~60% of 50k window)
- **40+ message exchanges** since last checkpoint (or session start)

**Detection**:
- Track message count since last checkpoint
- Estimate tokens (rough heuristic: 1 message ≈ 500-1000 tokens)

**Why moderate, not strong**:
- Context window pressure alone shouldn't force checkpoint
- But combined with other signals, indicates good time to refresh

---

#### 2. Conceptual Closure

**Criteria**:
- Just finished **"What Goes Wrong"** analysis (failure modes covered)
- Completed **strategic scenario** challenge
- Student successfully **applied concept independently** (without prompting)

**Example**:
- Taught anti-pattern: "Conditional hook registration"
- Analyzed: Misapplication, Omission, Excess, Interaction Failure
- Student identified anti-pattern in example code independently

**Detection**:
- "What Goes Wrong" section completed
- OR strategic scenario with student demonstrating mastery

---

#### 3. Student Momentum Shift

**Criteria**:
- Student completed exercise **faster than expected** (high confidence)
- OR: Student **paused/struggled**, then succeeded (hard-won victory worth cementing)

**Why suggest**:
- High confidence: Capitalize on momentum, lock in success
- Hard-won victory: Checkpoint reinforces achievement, prevents re-teaching

**Detection**:
- Student answered comprehension check in 1-2 messages (fast)
- OR: Student took 5+ attempts but finally succeeded (struggle → success)

---

## SUGGESTION PHRASING TEMPLATES

### Template 1: Moderate Signals (Gentle Suggestion)

```
💡 Checkpoint suggestion

{Reason}: {Specific signal description}

This might be a good place to checkpoint. Type 'Checkpoint' to save and refresh context, or continue.
```

**Example**:
```
💡 Checkpoint suggestion

We've covered {N} concepts over {M} message exchanges. Context window is ~60% full.

This might be a good place to checkpoint. Type 'Checkpoint' to save and refresh context, or continue to {next concept}.
```

---

### Template 2: Strong Signals (Confident Recommendation)

```
🎯 Natural checkpoint detected

{Reason}: {Specific signal description}

This is a semantic boundary -- a natural completion point. Checkpoint recommended.

Type 'Checkpoint' to save progress, or continue if you prefer.
```

**Example**:
```
🎯 Natural checkpoint detected

TEACH cycle complete for "Hook Architecture":
✅ All terms defined
✅ Full explanation (What/Why/How/Where/Failure modes)
✅ Analogy provided (event listeners)
✅ Comprehension check passed
✅ Exercise completed successfully

This is a semantic boundary. Checkpoint recommended before moving to "Custom Hooks".
```

---

### Template 3: Critical (Context Window Pressure)

**Only use if context window is critically full** (80%+ estimated):

```
⚠️ Context window alert

Estimated token usage: ~80% of capacity ({N}k tokens)

**Recommended**: Checkpoint now to prevent context overflow.

Type 'Checkpoint' to save progress and refresh context.
```

---

## ANTI-SIGNALS (Do NOT Suggest Checkpoint)

### ❌ Mid-Concept Teaching

**Scenario**: Halfway through TEACH cycle (explained "What it is" and "Why", but haven't covered "How" yet)

**Why not**: Incomplete unit of knowledge -- checkpoint would split concept awkwardly

---

### ❌ Immediately After Last Checkpoint

**Scenario**: User checkpointed 2 minutes ago, taught 1 small sub-point, no major progress

**Why not**: No substantial new content since last checkpoint

**Detection**: Time since last checkpoint < 5 minutes AND concepts taught < 1

---

### ❌ During Active Exercise

**Scenario**: Student is mid-exercise (working on hands-on practice)

**Why not**: Let student complete the exercise first -- checkpoint after success/failure

---

### ❌ During Comprehension Check

**Scenario**: Asked comprehension question, waiting for student response

**Why not**: Wait for answer, assess understanding, THEN checkpoint (if passed)

---

## CONTEXTUAL FACTORS

### Factor 1: Student Pace Preference

**Observed from student behavior**:
- **Fast pacer**: Checkpoints every 1-2 major concepts (20-30 min intervals)
- **Slow pacer**: Checkpoints every concept (10-15 min intervals)
- **Marathon learner**: Rare checkpoints, prefers long sessions (45+ min)

**Adjust**: Suggest checkpoints more/less frequently based on observed pace

---

### Factor 2: Lesson Complexity

**Simple lessons** (L1 fundamentals, definitions-heavy):
- Suggest checkpoint after **2-3 concepts**

**Complex lessons** (L3 advanced, many edge cases):
- Suggest checkpoint after **1 major concept** (more granular)

**Rationale**: Complex concepts benefit from more frequent checkpoints (easier to rewind/revise)

---

### Factor 3: Student Explicit Preference

**If student says**: "I prefer frequent checkpoints"
- Lower threshold: Suggest at moderate signals

**If student says**: "I prefer fewer checkpoints, longer sessions"
- Raise threshold: Only suggest at strong signals + context pressure

**Record in context bridge**: Update "Collaboration Style" section

---

## DETECTION ALGORITHM (Pseudocode)

```python
def should_suggest_checkpoint():
    # Strong signals (any one triggers suggestion)
    if teach_cycle_complete_for_major_concept():
        return ("strong", "TEACH cycle complete")

    if user_explicitly_requested():
        return ("execute", None)  # Just do it, no suggestion

    if natural_curriculum_boundary():
        return ("strong", "Curriculum subsection complete")

    if depth_layer_transition():
        return ("strong", "Layer transition (L1→L2 or L2→L3)")

    # Moderate signals (need 2+ to trigger)
    moderate_signals = []

    if context_window_usage() > 0.6:
        moderate_signals.append("Context window ~60% full")

    if conceptual_closure_achieved():
        moderate_signals.append("Conceptual closure (What Goes Wrong complete)")

    if student_momentum_shift():
        moderate_signals.append("Student demonstrated mastery")

    if len(moderate_signals) >= 2:
        return ("moderate", " + ".join(moderate_signals))

    # Critical signal (context overflow imminent)
    if context_window_usage() > 0.8:
        return ("critical", "Context window critically full")

    # No checkpoint needed
    return (None, None)


def handle_checkpoint_suggestion(signal_type, reason):
    if signal_type == "execute":
        execute_checkpoint()  # User said "Checkpoint"

    elif signal_type == "strong":
        suggest_checkpoint_strong(reason)

    elif signal_type == "moderate":
        suggest_checkpoint_moderate(reason)

    elif signal_type == "critical":
        warn_context_overflow(reason)

    else:
        continue_teaching()  # No suggestion
```

---

## EXAMPLES

### Example 1: Strong Signal Detected

**Scenario**:
- Taught: "Ralph Wiggum Loop" concept
- Defined: Loop, Autonomous, Failure Recovery
- Explained: What/Why/How/Where/What Goes Wrong
- Analogy: "Like a retry mechanism in fault-tolerant systems"
- Comprehension check: "Explain when Ralph Wiggum Loop is useful" → Student answered correctly
- Exercise: "Identify Ralph Wiggum Loop in example code" → Student succeeded

**Detection**: `teach_cycle_complete_for_major_concept()` = True

**Output**:
```
🎯 Natural checkpoint detected

TEACH cycle complete for "Ralph Wiggum Loop":
✅ All terms defined
✅ Full explanation (What/Why/How/Where/Failure modes)
✅ Analogy provided (retry mechanism)
✅ Comprehension check passed
✅ Exercise completed successfully

This is a semantic boundary. Checkpoint recommended before moving to "Creator's Workflow".

Type 'Checkpoint' to save progress, or continue if you prefer.
```

---

### Example 2: Moderate Signals (2 Combined)

**Scenario**:
- Context window: ~55% full (moderate accumulation)
- Just completed "What Goes Wrong" analysis for hook anti-patterns
- Student correctly identified anti-pattern in example code

**Detection**:
- `context_window_usage()` = 0.55 (moderate)
- `conceptual_closure_achieved()` = True ("What Goes Wrong" complete)
- `student_momentum_shift()` = True (demonstrated mastery)

**Moderate signals count**: 3 (threshold met)

**Output**:
```
💡 Checkpoint suggestion

Multiple completion signals:
- Context window ~55% full
- "What Goes Wrong" analysis complete
- Student demonstrated mastery (identified anti-pattern independently)

This might be a good place to checkpoint. Type 'Checkpoint' to save and refresh context, or continue to next concept.
```

---

### Example 3: No Checkpoint (Mid-Concept)

**Scenario**:
- Taught "What it is" and "Why it matters" for "Hooks & Extensibility"
- Haven't covered "How it works" yet
- Student hasn't done exercise

**Detection**:
- `teach_cycle_complete_for_major_concept()` = False (only 2/5 components)
- No other strong/moderate signals

**Output**: (No checkpoint suggestion, continue teaching)

---

## CONSTRAINTS

- **Never auto-checkpoint** without user command (unless explicit setting)
- **Always provide opt-out** ("or continue if you prefer")
- **Be specific** in reason (don't say "good time to checkpoint" without explanation)
- **Respect student preference** (adjust frequency based on observed pace)
- **Avoid suggestion spam** (at most 1 suggestion per 10 minutes or 1 per concept)

---

## SUCCESS CRITERIA

✅ Strong signals trigger confident recommendation
✅ Moderate signals require 2+ to trigger gentle suggestion
✅ Anti-signals prevent inappropriate checkpoint suggestions
✅ Phrasing templates used consistently
✅ Specific reasons provided (not vague "good time to checkpoint")
✅ Student can always decline suggestion and continue
✅ Context window pressure escalates suggestion urgency

---

## RELATED FRAMEWORKS

- **TEACH Cycle**: Defines concept completion → `../Pedagogy/teach-cycle.md`
- **What Goes Wrong**: Framework for failure analysis → `anti-patterns.md`
- **Checkpoint Protocol**: Execution workflow → `../Protocols/checkpoint-synthesis.md`
