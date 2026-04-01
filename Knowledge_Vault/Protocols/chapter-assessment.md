# Chapter Assessment Protocol

> **Trigger**: Completion of the final lesson in each chapter (Finish command on last lesson)
> **Purpose**: Verify integrated mastery before marking chapter complete
> **Cross-refs**: [Mastery Rubrics](../Assessment/mastery-rubrics.md) | [Finish Synthesis](finish-synthesis.md)

---

## DIRECTIVE

After student completes the final lesson of a chapter, execute this assessment BEFORE marking the chapter complete. The chapter is NOT complete until the assessment passes.

---

## WHAT MAKES IT DIFFERENT FROM LESSON CHECKS

- **No scaffolding**: No vocabulary table, no "we learned about X" context
- **Multi-concept**: Requires integrating 3+ concepts from different lessons
- **Open-ended**: Full written response — no multiple choice
- **No hints**: If student asks for hints, respond: "Try your best — I'll give full feedback after."

---

## PROCEDURE

### Step 0: Prerequisite Validation

Before announcing the assessment, verify all lessons in this chapter are complete.

Check bridge Section 13 (Next Steps) and Section 14 (Checkpoint History) for completed lessons.

**If all lessons complete**: Proceed to Step 1.

**If lessons missing**:
```
⚠️ Chapter {N} Assessment — Prerequisites Not Met

The following lessons in this chapter have not been completed:
- Lesson {X.Y}: [title]
- Lesson {X.Z}: [title]

Complete these lessons first, then the chapter assessment will run automatically after your final Finish.

Continuing with current lesson instead.
```
Cancel the assessment and return to normal teaching flow.

### Step 1: Announce
```
📋 Chapter [N] Assessment

You've completed all lessons in Chapter [N]: [Title].

Final integration check before we mark this chapter complete.
No hints — apply what you've learned to a real situation.

Ready? Type 'Yes' to begin.
```

### Step 2: Present Scenario
Use scenario from this file's SCENARIOS section below (or generate a new one following the rules).

**Scenario Design Rules**:
1. Realistic situation (not abstract "explain concept X")
2. At least 3 concepts from the chapter without naming them
3. Clear success/failure outcome
4. At least one red herring or complexity layer
5. No terminology that gives away which concept applies

### Step 3: Wait (No Hints)
Do not prompt or hint. If asked for hints: "This is the assessment — give it your best shot."

### Step 4: Evaluate

| Criterion | Weight | Pass Threshold |
|-----------|--------|----------------|
| Correct diagnosis (identified right concepts) | 40% | ≥2 of 3 concepts correct |
| Correct solution (applied concepts properly) | 30% | Core solution must be correct |
| Failure mode awareness | 20% | ≥1 post-fix risk identified |
| Strategic reasoning | 10% | Bonus |

**Pass**: All thresholds met
**Fail**: Misses diagnosis entirely OR solution fundamentally wrong

### Step 5: Feedback (Always — pass or fail)
1. What they got RIGHT (specific)
2. What they MISSED (specific)
3. Complete model answer
4. Overall: PASSED ✅ or NEEDS REVIEW ⚠️

### Step 6: Pass → Mark Chapter Complete
Update bridge Section 13 + status.json.

### Step 7: Fail → Remediation
Re-teach the missed concepts, then offer ONE retry. After retry, mark chapter complete with a note regardless of outcome.

---

## BUILT-IN SCENARIOS

### Chapter 1: The New Paradigm
A company wants to replace their customer service chatbot with an AI agent that "does everything automatically." They handle 500 queries/day. They're excited about zero human involvement.

Tasks: (1) Diagnose the unrealistic expectations. (2) Prescribe a realistic transition plan. (3) Identify what could still fail after your plan.

*Tests*: Agent vs. chatbot distinction, digital FTE concept, agent maturity framework, realistic capability framing

### Chapter 2: Markdown & Specification
A developer shows you a CLAUDE.md that is 3000 lines of dense prose, no section headers, 200+ mixed behavioral rules and background context. Agents behave unpredictably.

Tasks: (1) Diagnose the problems. (2) Prescribe a rewrite strategy. (3) What will still go wrong after your fix?

*Tests*: CLAUDE.md structure, formatting principles, cognitive load for LLMs, specification quality

### Chapter 3: Claude Code
An agent fails silently every Monday morning — no errors, tool calls stop being logged after 9am, recovers by noon. No weekend code changes.

Tasks: (1) Diagnose the failure. (2) What would you check first? (3) What mechanism is likely involved?

*Tests*: Hook architecture, lifecycle management, failure mode analysis

---

## SUCCESS CRITERIA

✅ Chapter assessment triggers after final lesson Finish
✅ No scaffolding or hints during assessment
✅ Rubric criteria applied explicitly
✅ Model answer always provided regardless of outcome
✅ Failed assessments trigger targeted re-teaching, not permanent blocking
✅ Bridge updated with chapter completion + assessment result
