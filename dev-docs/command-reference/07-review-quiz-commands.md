# Review & Quiz Commands Reference

> Test your knowledge of material you've already covered. All review and quiz commands output to chat only — no files are written.

---

## Quick Reference

| Command | Questions | Scope | Depth | Files Written? |
|---------|-----------|-------|-------|---------------|
| `quiz me` | 5 | Current lesson | Recent checkpoints | No |
| `quiz me on chapter X` | 10 | Full chapter | All completed checkpoints | No |
| `Review X.Y` | Variable | Specific lesson | All lesson checkpoints | No |
| `review chapter X` | Comprehensive | Full chapter | All lessons | No |
| `exam prep` | Intensive | All chapters | Everything | No |

---

## Commands

### `quiz me`

**Trigger:** `quiz me`

Generates 5 practice questions on the most recently covered material (current lesson and checkpoint).

**Behavior:**
- Uses all six question types (see [Question Types](#question-types) below)
- Agent waits for your answer before showing the next question
- Weak answer: agent re-explains the concept using a different approach, then continues (3-attempt mastery gate applies — see [Mastery Gate](#mastery-gate-in-review-mode))
- Strong answer: agent confirms and advances to the next question
- Ends with a brief score summary and a recommendation to continue or review specific topics

**Best used when:** You just finished a checkpoint and want a quick knowledge check before moving on.

---

### `quiz me on chapter X`

**Trigger:** `quiz me on chapter 1`, `quiz me on chapter 3`, etc.

Generates 10 practice questions spanning all lessons in the specified chapter.

**Behavior:**
- Covers material from all completed checkpoints for that chapter
- Same question types and mastery gate behavior as `quiz me`
- Ends with a score summary and recommendations

**Best used when:** You've finished a chapter and want to confirm overall mastery before advancing.

---

### `Review X.Y`

**Trigger:** `Review 3.1`, `Review 3.17`, etc.

**Fetches:** `Knowledge_Vault/Protocols/review-quiz.md`

Quizzes you on a specific completed lesson by reading all checkpoint files for lesson X.Y.

**Behavior:**
- Generates questions targeting the specific vocabulary, concepts, anti-patterns, and frameworks from that lesson
- Question difficulty scales with checkpoint depth:
  - L1 questions — foundational vocabulary and definitions
  - L2 questions — intermediate application and comparison
  - L3+ questions — advanced edge cases and strategic reasoning
- Same mastery gate behavior applies
- Ends with a mastery summary for that lesson and spaced repetition scheduling (see [Spaced Repetition](#spaced-repetition-scheduling))

**Best used when:** You haven't touched a lesson in a while and need to reactivate that knowledge.

---

### `review chapter X`

**Trigger:** `review chapter 1`, `review chapter 3`, etc.

Runs the Full Chapter Review Protocol for the specified chapter.

**Behavior:**
- Fetches the chapter curriculum module and all checkpoint files for that chapter
- Generates a comprehensive review covering all lessons
- More thorough than `quiz me on chapter X` — includes concept synthesis, not just Q&A
- Ends with a chapter mastery rating and recommendations for weak areas

**Best used when:** You want deep synthesis across an entire chapter, not just a spot-check quiz.

---

### `exam prep`

**Trigger:** `exam prep`

**Fetches:** `Knowledge_Vault/Protocols/` (exam-relevant protocols)

Enters intensive exam preparation mode covering all completed chapters.

**Behavior:**
- Coverage: all completed checkpoints across all lessons and chapters
- Format: mixed question types, timed sections, scenario challenges
- Includes Failure Analysis scenarios, "What Goes Wrong" framework questions, and strategic decision problems
- Ends with an overall readiness score, weak area report, and recommended review order

**Best used when:** An exam is coming up and you need a full-coverage intensive review.

---

## Question Types

All review and quiz commands draw from the same six question types:

| Type | Description | Example |
|------|-------------|---------|
| **Explain-Back** | Restate a concept in your own words | "Explain what a hook lifecycle is." |
| **Application** | Apply a concept to a real scenario | "You need to register a post-processing hook. What do you do?" |
| **Failure Analysis** | Identify what goes wrong in a given scenario | "What happens if you call a hook before registration?" |
| **Compare-Contrast** | Distinguish between two related things | "What's the difference between L1 and L2 hook patterns?" |
| **Edge Case** | Handle an unusual or boundary scenario | "What happens with a hook that throws an exception?" |
| **Strategic** | High-level decision-making | "When would you choose orchestration over direct chaining?" |

---

## Mastery Gate in Review Mode

The same 3-attempt loop cap that applies during teaching also applies during reviews:

| Attempt | Answer Quality | Agent Action |
|---------|---------------|--------------|
| Any | Strong | Confirm + move to next question |
| 1 | Weak | Re-explain using a different approach |
| 2 | Weak | Re-explain using a third approach |
| 3 | Weak | Flag `⚠️ NEEDS REVIEW` + move on (never loops a 4th time) |

Flagged concepts are collected and displayed in a review list at the end of the session.

---

## Spaced Repetition Scheduling

After `Review X.Y`, the agent schedules concepts for future review based on your performance:

| Performance | Next Review |
|-------------|-------------|
| Strong answer | Scheduled in 7 days |
| Weak answer | Scheduled for tomorrow |
| Flagged concept (`⚠️ NEEDS REVIEW`) | Added to next session's cold-start recall questions |

**Cold-start recall:** At the start of each new session, the agent asks cold recall questions for concepts that are due for review before starting any new teaching. This surfaces scheduled concepts automatically — no manual action needed.

---

## When to Use Each Command

| Situation | Recommended Command |
|-----------|---------------------|
| Just finished a checkpoint, want a quick check | `quiz me` |
| Finished a chapter, want a fast mastery check | `quiz me on chapter X` |
| Finished a chapter, want deep synthesis | `review chapter X` |
| Haven't touched a specific lesson in a while | `Review X.Y` |
| Exam is coming up | `exam prep` |

---

## Example Interaction — `quiz me`

```
You: quiz me

Professor Agent:
Quiz — Lesson 3.1, Layer L2 (5 questions)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Question 1 of 5 [Explain-Back]

In your own words, explain what the hook lifecycle is and why it matters.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You: [answer]

Professor Agent:
[feedback + next question, or re-explanation if answer was weak]
```

---

## Example Interaction — `Review 3.1`

```
You: Review 3.1

Professor Agent:
Loading review for Lesson 3.1 — Hook Architecture
Checkpoint files: L1 (13 concepts), L2 (9 concepts), L3 (11 concepts)
Total: 33 concepts to review

Starting with vocabulary recall (L1 fundamentals)...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Question 1 — Vocabulary [L1]

What is a "hook" in the context of Agent Factory? Give a one-sentence definition.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You: [answer]

Professor Agent:
[feedback + spaced repetition note + next question]
```
