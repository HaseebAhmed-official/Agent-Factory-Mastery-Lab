# Mastery Rubrics — Behavioral Pass Criteria

> **Purpose**: Define what "passing" means at each depth layer before TEACH cycle marks completion
> **Used by**: TEACH cycle C-step, Chapter Assessment protocol
> **Cross-refs**: [TEACH Cycle](../Pedagogy/teach-cycle.md) | [Chapter Assessment](../Protocols/chapter-assessment.md)

---

## DIRECTIVE

After every "C — Check Understanding" step in the TEACH cycle, evaluate the student's response against the rubric for the current depth layer. Do NOT mark the concept as understood unless the minimum layer threshold is met.

**Re-teach rule**: If student fails, re-teach using a DIFFERENT approach (different analogy, different entry point, simpler sub-concept). Max 3 re-teach loops. After 3 failures: flag concept as ⚠️ NEEDS REVIEW and allow continuation.

---

## LAYER RUBRICS

### L1 — Fundamentals (Required before any L2 teaching)
**Bloom's Level**: Remember + Understand (1-2)

Pass Criteria (ALL required):
- ✅ Can define the concept in their OWN words (not verbatim recitation)
- ✅ Can explain WHY it matters with real-world stakes
- ✅ Can identify at least one example in context
- ✅ Response is not scaffolded by hints in the question

Fail Indicators:
- ❌ Pure verbatim recitation of the definition
- ❌ Cannot explain why it matters without prompting
- ❌ Requires multiple follow-up questions for basic description

---

### L2 — Intermediate (Required before Chapter Assessment)
**Bloom's Level**: Apply + Analyze (3-4)

Pass Criteria (ALL required):
- ✅ Can apply concept correctly to a NEW scenario not seen in the lesson
- ✅ Can identify which concept applies when given a problem (not told which)
- ✅ Can describe at least one failure mode or anti-pattern
- ✅ Can compare this concept to a related concept

Fail Indicators:
- ❌ Can only apply to examples already seen in the lesson
- ❌ Cannot identify the concept without being told "this is about X"
- ❌ No awareness of failure modes

---

### L3 — Advanced (Required for lesson marked 'Expert Complete')
**Bloom's Level**: Evaluate + Create (5-6)

Pass Criteria (ALL required):
- ✅ Can identify the correct concept from an unlabeled scenario
- ✅ Can evaluate trade-offs: "Why choose X over Y?"
- ✅ Can identify edge cases the lesson did not cover
- ✅ Can design a simple solution from scratch

---

### L4 — Expert (Optional deep-dive)
**Bloom's Level**: Create + Teach (6+)

Pass Criteria:
- ✅ Can teach the concept to a hypothetical beginner without notes
- ✅ Can identify cross-chapter connections
- ✅ Can handle adversarial edge cases

---

## RE-TEACH STRATEGIES

When a student fails, do NOT repeat the same explanation. Use one of:
1. **Simpler Analogy**: Different real-world comparison
2. **Concrete Example First**: Example → definition (reversed order)
3. **Socratic Decomposition**: Break into smaller answerable questions, build up
4. **Failure Mode Entry**: Start from what goes WRONG instead of what goes RIGHT
5. **Connect to Prior Knowledge**: "You know X from lesson Y — this is similar because..."

Track which strategy was used in bridge Section 10 (Growth Areas).

---

## MASTERY GATE FLOW

```
C — Check Understanding
│
├── Ask open-ended question
├── Evaluate against rubric for current layer
├── PASS → Proceed to H (Hands-On) ✅
└── FAIL → Select different re-teach strategy
         → Re-explain using alternative approach
         → Ask DIFFERENT comprehension question
         → Evaluate again (max 3 loops)
         → After 3 failures: flag ⚠️ NEEDS REVIEW, allow continuation
```

---

## FLAG PROTOCOL

When flagged ⚠️ NEEDS REVIEW after 3 failures:
1. Add to bridge Section 10 under "Growth Areas"
2. Set NextReviewDue = tomorrow in vocabulary bank
3. Continue teaching — do NOT permanently block
4. Pre-lesson retrieval MUST include this concept first next session
5. If student passes on retry: remove flag, update to ✅

---

## SUCCESS CRITERIA

✅ Every TEACH cycle C-step evaluated against this rubric
✅ Re-teach loops fire on failure (max 3, different approach each time)
✅ Flagged concepts prioritized in pre-lesson retrieval
✅ Layer transitions require passing appropriate rubric level
✅ Chapter completion requires L2 mastery of all chapter concepts

---

## EXAMPLE RESPONSES (Pass vs Fail)

These examples help calibrate consistent LLM evaluation across sessions.

### L1 Example: Hook Architecture

**Question**: "What is a hook, and when would you use one?"

**PASS response** ✅:
> "A hook is basically a way to plug your own code into specific moments of an agent's lifecycle without touching the core agent. Like, instead of modifying the agent itself, you register a function that fires automatically when a certain event happens — like before a tool call or after a response. You'd use one when you want to add logging, monitoring, or custom behavior to an existing agent."

Why it passes: Own words, explains WHY (extensibility without modification), gives a concrete use case, not verbatim from the lesson.

**FAIL response** ❌:
> "A hook is a callback function registered at a specific lifecycle point in an agent's execution."

Why it fails: Verbatim recitation of the definition. No own-words processing, no WHY, no example.

---

### L2 Example: Hook Architecture

**Question**: "You're building an agent that needs to notify a Slack channel every time it makes a tool call. How would you implement this?"

**PASS response** ✅:
> "I'd use a post-tool-call hook — register a callback that fires after every tool execution. Inside the callback, call the Slack API with the tool name and result. I'd need to be careful about async handling so the hook doesn't block the agent, and I'd add error handling so a Slack failure doesn't crash the agent itself."

Why it passes: Applies to a new scenario (Slack, not from lesson), identifies the correct hook type, identifies a failure mode (async blocking), unprompted by hints.

**FAIL response** ❌:
> "I would add a hook like we did in the exercise."

Why it fails: References only the lesson example, no adaptation to new scenario, no failure mode awareness.

---

### Evaluator Note

When in doubt between PASS and FAIL: ask one follow-up question ("Can you give me a concrete example?"). If the student can expand their answer with specifics, it's a PASS. If they cannot add anything substantive, it's a FAIL.
