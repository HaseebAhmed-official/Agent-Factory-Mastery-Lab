# Student Profile Evolution Protocol

> **Trigger**: Layer transition events (L1→L2 mastery confirmed, L2→L3 mastery confirmed)
> **Purpose**: Update student profile as competence grows — prevent treating an advancing student like a beginner
> **Cross-refs**: [Student Profile](profile.md) | [Mastery Rubrics](../Assessment/mastery-rubrics.md) | [Checkpoint Synthesis](../Protocols/checkpoint-synthesis.md)

---

## DIRECTIVE

When a student consistently demonstrates mastery at a new layer level, update their profile in `Knowledge_Vault/Student/profile.md`. Do NOT keep treating an L3-capable student with L1 scaffolding.

**Trigger condition**: Student passes L2 mastery rubric on 3+ consecutive concepts → profile evolves to "Advanced Learner" mode.

---

## EVOLUTION MILESTONES

### Milestone 1: L1 Mastery Confirmed (Foundations Complete)
**Trigger**: Student passes L1 rubric for all concepts in at least 2 lessons.

**Profile updates**:
- Level: `Intermediate` → `Intermediate-Advanced`
- Scaffolding: Reduce vocabulary table frequency — only new terms, never repeated
- Pacing: Allow student to suggest skipping sub-concepts they already know

**Banner to display**:
```
🎯 Milestone: Foundations Confirmed
You're consistently demonstrating L1 mastery.
Adjusting teaching style: reduced scaffolding, increased pace.
```

---

### Milestone 2: L2 Mastery Confirmed (Application Ready)
**Trigger**: Student passes L2 rubric on 3+ consecutive concepts.

**Profile updates**:
- Level: `Intermediate-Advanced` → `Advanced`
- Scaffolding: No vocabulary tables for previously covered terms
- Analogies: Student generates analogy first; tutor refines
- Exercises: Start with open transfer (no hint about which concept applies)
- Pacing: Student may request accelerated mode

**Banner to display**:
```
🚀 Milestone: Application Mastery Confirmed
You're consistently applying concepts to new scenarios.
Switching to advanced mode: less scaffolding, more challenge.
```

---

### Milestone 3: L3 Mastery Confirmed (Strategic Thinker)
**Trigger**: Student passes L3 rubric on 2+ concepts OR passes a Chapter Assessment without hints.

**Profile updates**:
- Level: `Advanced` → `Expert`
- Scaffolding: None unless explicitly requested
- Teaching style: Socratic-first (questions before explanations)
- Exercises: Design-from-scratch challenges only
- Pacing: Student drives pace entirely

**Banner to display**:
```
⭐ Milestone: Strategic Mastery Confirmed
You're identifying and applying concepts independently.
Full expert mode: Socratic teaching, design challenges, no scaffolding.
```

---

## HOW TO APPLY EVOLUTION

When a milestone is reached:

1. Display the appropriate banner
2. Update `Knowledge_Vault/Student/profile.md` — edit the Level and Style fields
3. Record the milestone in bridge Section 10 (Student Strengths & Growth Areas):
   ```
   **Milestones**: L1 Confirmed [date] | L2 Confirmed [date] | L3 Confirmed [date]
   ```
4. Update bridge Section 3 (Established Teaching Patterns) to note reduced scaffolding
5. Continue teaching with the updated profile — do NOT revert to prior scaffolding

---

## REGRESSION HANDLING

If student struggles after a milestone (fails 2+ L2 rubrics after L2 milestone):
- Do NOT demote the profile permanently
- Temporarily increase scaffolding for the struggling concept only
- Note in bridge Section 10 under "Growth Areas"
- After passing: resume evolved profile

---

## SUCCESS CRITERIA

✅ Profile evolves automatically at layer transition milestones
✅ Student is never over-scaffolded after demonstrating higher mastery
✅ Milestones recorded in bridge with dates
✅ Regression handled gracefully (temporary, concept-specific, not permanent demotion)
