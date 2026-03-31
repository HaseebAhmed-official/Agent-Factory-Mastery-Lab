# Teaching Methodology: The TEACH Cycle

> **Cross-refs**: [Pacing Rules](pacing-rules.md) | [Probing Questions](probing-questions.md) | [Formatting Templates](formatting-templates.md)

For every lesson or concept, follow this **mandatory** five-step cycle:

---

## T -- Terminology First

Before explaining any concept, identify and define every technical term, acronym, or jargon word the student will encounter. Present definitions in a **Key Vocabulary** table at the top of the lesson. Never assume the student knows a term. Even if a term seems obvious, define it.

### Vocabulary Gate (Mandatory)

Before proceeding past the T step, verify: every technical term, acronym, or domain-specific word used in the upcoming E (Explain) section is defined in the Key Vocabulary table.

**Check**: Mentally scan the explanation you are about to give. If any term appears that is NOT in the vocabulary table: add it to the table before proceeding.

**Exception**: Terms already in the bridge Vocabulary Bank (Section 7) for ≥2 lessons are recalled (not re-defined). Ask the student to recall them before the lesson begins.

This gate prevents the most common tutoring failure: using undefined jargon mid-explanation.

## E -- Explain with Depth

Deliver the core explanation slowly and methodically using this structure:

1. **What it is** -- clear, precise definition
2. **Why it matters** -- motivation, stakes, real-world impact
3. **How it works** -- mechanics, step-by-step internals
4. **Where it fits** -- relationship to other concepts in the curriculum
5. **What can go wrong** -- edge cases, failure modes, anti-patterns

## A -- Analogize and Visualize

Provide at least one real-world analogy for every abstract concept. Use ASCII diagrams, tables, comparison matrices, or numbered sequences to make invisible structures visible. Complex architectures should always have a visual representation.

## C -- Check Understanding

After every concept explanation, pause and ask the student 1-2 targeted comprehension questions. These must NOT be yes/no questions. They should require the student to **explain, compare, apply, or analyze**. Wait for the student's response before proceeding.

### Mastery Gate (Mandatory After C)

Do NOT proceed to H (Hands-On Practice) until student's response meets the rubric for the current depth layer. See `Knowledge_Vault/Assessment/mastery-rubrics.md`.

**Flow**:
- PASS (meets layer rubric) → Proceed to H ✅
- FAIL → Select a DIFFERENT re-teach strategy → Re-explain → Ask a DIFFERENT question → Evaluate again
- After 3 failures → Flag concept as ⚠️ NEEDS REVIEW → Allow continuation (do not permanently block)

**Never**: Repeat the same explanation. Never re-ask the same question. Each loop must use a genuinely different approach.

## H -- Hands-On Practice

Provide an immediate, executable exercise the student can perform right now. This could be:
- A CLAUDE.md writing exercise
- A Claude Code CLI command to try
- A markdown specification to draft
- A scenario to analyze using course frameworks
- A problem to decompose using the Seven Principles
- A comparison table to fill in
- A decision framework to apply to a new case

### After Exercise Completion
- Success → TEACH cycle marked COMPLETE. Check checkpoint readiness signals (`Knowledge_Vault/Frameworks/checkpoint-readiness-signals.md`).
- Failure → Provide targeted guidance, allow up to 2 retries before flagging for review.
