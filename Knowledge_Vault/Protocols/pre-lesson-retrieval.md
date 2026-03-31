# Pre-Lesson Retrieval Protocol

> **Trigger**: Every session start, after cold-start recovery, before any new teaching
> **Purpose**: Combat forgetting curve; activate prior knowledge before new encoding
> **Cross-refs**: [Resume Protocol](resume-protocol.md) | [Mastery Rubrics](../Assessment/mastery-rubrics.md) | [Pacing Rules](../Pedagogy/pacing-rules.md)

---

## DIRECTIVE

Before teaching ANY new content, execute this protocol every session. Exception: if this is the student's very first session (bridge vocabulary bank is empty), skip and proceed to teaching.

---

## STEP 1: Load Due Concepts

From bridge Vocabulary Bank (Section 7), find concepts where `NextReviewDue <= today`.
Also include any concept flagged `⚠️ NEEDS REVIEW` (always appear first).

**Cap**: Maximum 5 concepts per session. Priority order:
1. ⚠️ NEEDS REVIEW flags first
2. Most overdue (NextReviewDue furthest in the past)
3. Lowest ReviewCount (least-reviewed)

---

## STEP 2: Cold Recall Questions

For each due concept, ask WITHOUT any context hint:

**BAD** ❌: "We learned about hooks last time. Can you explain what a hook is?"
**GOOD** ✅: "What is a hook, and when would you use one in an agent?"

Use question types from probing-questions.md. Rotate types across sessions:
Session 1 due → Explain-Back | Session 2 → Application | Session 3 → Failure Analysis | (cycle through all 6 types)

---

## STEP 3: Update Vocabulary Bank After Each Response

**Pass** (meets L1 rubric minimum):
- `LastReview = today`
- `ReviewCount += 1`
- `NextReviewDue` using Leitner intervals:
  - Count 1 → +1 day | Count 2 → +3 days | Count 3 → +7 days | Count 4 → +14 days | Count 5+ → +30 days
- Update `ConfidenceRating` (1=poor → 5=excellent) based on response quality

**Fail** (does not meet L1 rubric):
- Brief 2-3 sentence re-teach (different framing, NOT full TEACH cycle)
- `NextReviewDue = tomorrow`
- Flag as still-struggling in bridge

---

## STEP 4: Transition

After all due concepts reviewed:
```
Quick review complete. [N] concepts refreshed.
Now let's continue with [today's lesson/concept].
```
If nothing due: `No review items due today — straight to new content.`

---

## INTERLEAVED REVIEW (Every 3rd Session)

Sessions 3, 6, 9, 12... begin with a 10-minute cross-chapter retrieval block:
1. Announce: "Interleaved review session — 10 minutes across all completed lessons before new content."
2. Select 5-8 concepts randomly from ALL completed chapters
3. Cold recall questions (same format)
4. After 10 min: transition to regular session flow
5. These concepts follow the same spaced review scheduling rules

**Why**: Interleaved practice (mixing chapters) produces significantly better transfer and long-term retention than blocked practice.

---

## SPACED REVIEW INTERVALS

| Review Count | Days Until Next Review |
|--------------|----------------------|
| 1st | 1 day |
| 2nd | 3 days |
| 3rd | 7 days |
| 4th | 14 days |
| 5th+ | 30 days (maintenance) |

---

## SUCCESS CRITERIA

✅ Retrieval fires at EVERY session start (not just when remembered)
✅ Only due concepts surfaced (cap 5 per session)
✅ Cold recall format — no "we learned X" hints
✅ Bridge vocabulary bank updated after every retrieval
✅ ⚠️ NEEDS REVIEW concepts always prioritized
✅ Every 3rd session includes interleaved cross-chapter retrieval
