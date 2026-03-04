# Review Command Protocol

> **Purpose**: Generate interactive quizzes from assessment files, score responses, track progress
> **Version**: 1.0
> **Created**: 2026-03-03

---

## Command Trigger

**User types**: `Review`

**Alternative forms**: `review`, `Quiz`, `quiz`, `Test me`, `test`

**Optional parameters**:
- `Review 3.1` - Review specific lesson
- `Review Chapter 3` - Review entire chapter
- `Review all` - Review all completed lessons
- `Review recent` - Review last 3 lessons

---

## Workflow

### STAGE 1: Scope Selection

**If user provided scope** (e.g., `Review 3.1`):
- Skip to STAGE 2 with specified lesson

**If no scope provided** (just `Review`):

1. **Scan for available assessments**:
   - Check `assessments/` directory
   - Find all `lesson-{X.Y}-quiz.md` files
   - Cross-reference with completed lessons (check context bridge)

2. **Present options**:
   ```
   📚 REVIEW QUIZ

   Which lessons would you like to review?

   1️⃣ LESSON 3.1 - Origin Story
      Completed: 2026-03-01
      Last reviewed: Never
      Questions: 8

   2️⃣ LESSON 3.15 - Hooks and Extensibility
      Completed: 2026-03-02
      Last reviewed: Never
      Questions: 10

   3️⃣ LESSON 3.17 - Ralph Wiggum Loop
      Completed: 2026-03-03
      Last reviewed: Never
      Questions: 7

   4️⃣ CHAPTER 3 - All lessons (25 questions)

   5️⃣ ALL COMPLETED LESSONS (42 questions)

   Your choice (1/2/3/4/5 or cancel):
   ```

3. **User selects option**

---

### STAGE 2: Load Assessment File

**Locate assessment file**:
- Path: `assessments/lesson-{X.Y}-quiz.md`
- If not found → Check if assessment exists in curriculum (may need sync)
- If still not found → Offer to generate quiz from lesson notes

**Example assessment file structure**:

```markdown
# Lesson 3.1 - Origin Story Quiz

---

## Question 1: Explain-Back

**Type**: open-ended
**Points**: 5
**Difficulty**: fundamental

**Question**:
Explain what the "Hook System" is in Claude Code and why it's important for extensibility.

**Rubric**:
- ✅ Full credit (5 pts): Mentions lifecycle events, callback registration, extensibility, examples
- 🟡 Partial credit (3 pts): Correct definition but missing key benefits
- ❌ No credit (0 pts): Incorrect or off-topic

**Model answer**:
The Hook System is a mechanism in Claude Code that allows users to execute custom code at specific lifecycle events (e.g., before tool execution, after response generation). It's important for extensibility because it enables users to customize behavior without modifying core code, such as logging, validation, or integration with external systems.

---

## Question 2: Application

**Type**: scenario
**Points**: 5
**Difficulty**: intermediate

**Question**:
You want to log every tool execution to a file. Which hook would you use, and how would you register it?

**Rubric**:
- ✅ Full credit (5 pts): Identifies correct hook (`before_tool_execution`), shows registration syntax, correct file writing logic
- 🟡 Partial credit (3 pts): Correct hook but incomplete implementation
- ❌ No credit (0 pts): Wrong hook or missing implementation

**Model answer**:
Use the `before_tool_execution` hook. Register in `.claude/hooks/before_tool_execution.sh`:
```bash
#!/bin/bash
echo "[$(date)] Tool: $TOOL_NAME" >> /path/to/tool-log.txt
```

---

[... more questions ...]
```

**Parse assessment file**:
- Extract all questions
- Store rubric criteria
- Store model answers (for reference, NOT shown to student initially)

---

### STAGE 3: Generate Quiz Using AskUserQuestion

**For each question in assessment**:

1. **Present question via AskUserQuestion tool**:

   **For open-ended questions (explain-back, failure analysis)**:
   - Use AskUserQuestion with 2 placeholder options:
     - Option 1: "Provide your answer below" (description: "Type your full explanation")
     - Option 2: "Skip this question" (description: "Move to next question")
   - Student selects Option 1 → Types answer in text field
   - Student answer captured in `answers` field

   **For scenario/application questions**:
   - Use AskUserQuestion with real options if multiple choice
   - Or use open-ended format if requires written response

   **For compare-contrast questions**:
   - Use AskUserQuestion with structured options:
     - Option 1: "They are the same" (description: "No meaningful difference")
     - Option 2: "Different in purpose" (description: "Explain the difference")
     - Option 3: "Different in implementation" (description: "Explain how they differ technically")

2. **Capture response**:
   - Store student answer
   - Timestamp
   - Question ID

---

### STAGE 4: Score Responses

**For each student answer**:

1. **Apply rubric**:
   - Read rubric criteria from assessment file
   - Compare student answer to rubric tiers (Full / Partial / No credit)

2. **Use AI-assisted scoring**:
   - For open-ended answers:
     - Analyze student response semantically
     - Check for key concepts mentioned in rubric
     - Assign score tier (Full / Partial / None)
   - For structured answers:
     - Exact match against model answer
     - Assign score

3. **Generate feedback**:
   - **If Full Credit**:
     ```
     ✅ Excellent! (5/5 points)

     Your answer correctly identifies {key concepts}.

     Model answer:
     {show model answer for comparison}
     ```

   - **If Partial Credit**:
     ```
     🟡 Partial Credit (3/5 points)

     Your answer is on the right track, but missing:
     - {missing concept 1}
     - {missing concept 2}

     Model answer:
     {show model answer}

     What you got right:
     - {correct concepts identified}
     ```

   - **If No Credit**:
     ```
     ❌ Incorrect (0/5 points)

     Your answer:
     {student answer}

     The correct answer:
     {model answer}

     Key misconception:
     {explain what went wrong}

     Let's clarify:
     {brief re-teaching moment}
     ```

4. **Show feedback immediately** after each question:
   - Display score
   - Display feedback
   - Option to "Continue" or "Review this concept more"

---

### STAGE 5: Quiz Summary

**After all questions answered**:

1. **Calculate scores**:
   ```
   📊 QUIZ COMPLETE: Lesson 3.1 - Origin Story

   ═══════════════════════════════════════════════════════

   Your Score: 32 / 40 points (80%)

   ═══════════════════════════════════════════════════════

   Breakdown by Type:

   📝 Explain-Back (3 questions):
      ✅ Q1: Hook System (5/5)
      🟡 Q2: Lifecycle Events (3/5)
      ✅ Q3: Registration Process (5/5)
      Subtotal: 13/15 (87%)

   🎯 Application (2 questions):
      ✅ Q4: Logging Hook (5/5)
      ❌ Q5: Custom Validation (0/5)
      Subtotal: 5/10 (50%)

   🔍 Failure Analysis (2 questions):
      ✅ Q6: Hook Not Firing (5/5)
      🟡 Q7: Infinite Loop (3/5)
      Subtotal: 8/10 (80%)

   🔄 Compare-Contrast (1 question):
      ✅ Q8: Hooks vs Tools (5/5)
      Subtotal: 5/5 (100%)

   ═══════════════════════════════════════════════════════

   Grade: B+ (80-89%)

   ═══════════════════════════════════════════════════════

   Strengths:
   ✅ Strong grasp of hook fundamentals
   ✅ Excellent at failure analysis
   ✅ Perfect compare-contrast reasoning

   Areas to Review:
   ⚠️ Application scenarios (50% - needs work)
   ⚠️ Custom validation patterns (missed Q5)

   Recommended Action:
   1. Re-study "Custom Hook Patterns" section
   2. Practice: Write 3 custom hook scenarios
   3. Re-take quiz in 2-3 days to reinforce

   ═══════════════════════════════════════════════════════
   ```

2. **Update context bridge**:
   - Add new section: "15. Quiz Performance"
   - Record:
     - Lesson reviewed
     - Score achieved
     - Timestamp
     - Weak areas identified
     - Recommended actions

   **Example bridge entry**:
   ```markdown
   ## 15. Quiz Performance

   | Lesson | Date | Score | Grade | Weak Areas |
   |--------|------|-------|-------|------------|
   | 3.1 | 2026-03-03 | 32/40 (80%) | B+ | Application scenarios |
   | 3.15 | 2026-03-04 | 38/45 (84%) | B+ | Edge cases |
   ```

3. **Save quiz results**:
   - Create `assessments/results/lesson-{X.Y}-result-{timestamp}.json`:
   ```json
   {
     "lesson": "3.1",
     "quiz_date": "2026-03-03T16:45:00Z",
     "questions": [
       {
         "id": "Q1",
         "type": "explain-back",
         "points_possible": 5,
         "points_earned": 5,
         "student_answer": "...",
         "score_tier": "full",
         "feedback": "..."
       }
     ],
     "summary": {
       "total_points_possible": 40,
       "total_points_earned": 32,
       "percentage": 80,
       "grade": "B+",
       "weak_areas": ["Application scenarios"],
       "recommended_actions": [...]
     }
   }
   ```

---

### STAGE 6: Post-Quiz Options

**Present next steps**:

```
What would you like to do next?

1️⃣ REVIEW WEAK AREAS
   Re-study "Application scenarios" with focused exercises

2️⃣ RETRY MISSED QUESTIONS
   Answer only the 2 questions you got wrong

3️⃣ TAKE ANOTHER QUIZ
   Review a different lesson

4️⃣ CONTINUE LEARNING
   Resume with next lesson (3.2)

5️⃣ END SESSION
   Save progress and exit

Your choice (1/2/3/4/5):
```

**If student chooses "Review Weak Areas"**:
- Load lesson notes for weak concepts
- Present focused mini-lesson (5-10 min)
- Provide additional practice exercises
- Offer to retry quiz after review

**If student chooses "Retry Missed Questions"**:
- Present only questions with score < full credit
- Score again
- Compare old vs new score
- Update quiz results

---

## Edge Cases & Error Handling

### Case 1: Assessment File Not Found

**Scenario**: User requests `Review 3.5` but `assessments/lesson-3.5-quiz.md` doesn't exist

**Handling**:
1. Check if lesson exists in curriculum
2. If yes → Offer to generate quiz from lesson notes:
   ```
   ⚠️ No assessment file found for Lesson 3.5

   I can generate a quiz from your lesson notes:
   - Source: revision-notes/.../3.5-*.md
   - Auto-generate 8-10 questions (mix of types)
   - Save to assessments/ for future use

   Generate quiz now? (yes/no)
   ```

3. If no → Suggest syncing curriculum or checking lesson number

### Case 2: Student Skips All Questions

**Scenario**: Student selects "Skip" for every question

**Handling**:
1. After 3 consecutive skips:
   ```
   🤔 You've skipped 3 questions in a row.

   This might mean:
   - Lesson material is still unclear
   - You're not ready for a quiz yet
   - Different review format would help

   What would you like to do?
   1. End quiz and review lesson notes
   2. Continue quiz (I'll try my best)
   3. Switch to flashcard review instead
   ```

### Case 3: Answer Too Short/Vague

**Scenario**: Student provides 1-word answer to explain-back question

**Handling**:
1. Detect low word count (< 10 words for explain-back)
2. Prompt for elaboration:
   ```
   Your answer: "hooks"

   ⚠️ This answer is too brief. Please elaborate:
   - What are hooks?
   - Why are they important?
   - How do they work?

   Try again (or skip):
   ```

### Case 4: Off-Topic Answer

**Scenario**: Student answer is completely unrelated to question

**Handling**:
1. Detect semantic mismatch (AI-assisted)
2. Gentle redirect:
   ```
   🤔 Your answer seems off-topic.

   Question was: {question text}

   Your answer discussed: {detected topic}

   Would you like to:
   1. Try again
   2. See a hint
   3. Skip this question
   ```

### Case 5: Quiz Interrupted Mid-Way

**Scenario**: Session crashes after answering 3/8 questions

**Handling**:
1. **Auto-save progress**:
   - After each question answered
   - Save partial results to `assessments/results/.temp/lesson-{X.Y}-in-progress.json`

2. **Resume on next session**:
   ```
   📋 Incomplete quiz detected

   Lesson 3.1 - Origin Story
   Progress: 3/8 questions answered
   Started: 2026-03-03 16:30

   Resume this quiz? (yes/no)
   ```

3. If yes → Load partial results, continue from Q4
4. If no → Archive partial results, start fresh

---

## Quiz Generation from Notes (Fallback)

**If assessment file doesn't exist**, generate quiz from lesson notes:

1. **Read lesson notes**:
   - Load all `{X.Y}-L*-*.md` files for lesson
   - Extract key concepts, frameworks, vocabulary

2. **Generate questions**:
   - **Explain-Back** (2-3 questions):
     - "Explain {concept} and why it matters."
   - **Application** (2-3 questions):
     - "You need to {scenario}. How would you use {concept}?"
   - **Failure Analysis** (1-2 questions):
     - "What goes wrong if you {misuse pattern}?"
   - **Compare-Contrast** (1-2 questions):
     - "Compare {concept A} and {concept B}."

3. **Generate rubrics**:
   - Extract model answers from lesson notes
   - Create 3-tier rubric (Full / Partial / None) for each question

4. **Save generated quiz**:
   - Write to `assessments/lesson-{X.Y}-quiz.md`
   - Mark as `auto-generated: true` in frontmatter
   - Ready for use

---

## Scoring Rubric Guidelines

**Full Credit (100%)**:
- Answer addresses all rubric criteria
- Key concepts correctly identified
- Examples provided (if asked)
- No major misconceptions

**Partial Credit (60-70%)**:
- Answer partially correct
- Missing 1-2 key concepts
- Minor misconceptions present
- Incomplete examples

**No Credit (0%)**:
- Answer incorrect or off-topic
- Major misconceptions
- Misses all key concepts
- Blank or skipped

**AI-Assisted Scoring**:
- Use semantic similarity to model answer
- Check for presence of rubric keywords
- Flag edge cases for manual review
- Err on side of partial credit (generous grading)

---

## Integration with CLAUDE.md

**Add to CLAUDE.md under "Commands" section**:

```markdown
### Review Command

**Usage**: `Review [lesson|chapter|all]`

**Purpose**: Generate interactive quiz from assessment files, score responses, track progress

**Examples**:
- `Review` - Choose from available quizzes
- `Review 3.1` - Quiz on Lesson 3.1
- `Review Chapter 3` - All Chapter 3 quizzes
- `Review recent` - Last 3 completed lessons

**Workflow**:
1. Select quiz scope
2. Answer questions via AskUserQuestion tool
3. Receive immediate feedback with model answers
4. See quiz summary with score breakdown
5. Update context bridge with performance data
6. Choose next steps (review weak areas, retry, continue)

**Use cases**:
- Test comprehension after completing lesson
- Identify weak areas before exam
- Spaced repetition review
- Track learning progress over time
```

---

## Quiz Types Reference

| Type | Description | Rubric Focus | Example |
|------|-------------|--------------|---------|
| **Explain-Back** | Explain concept in own words | Completeness, clarity, key concepts | "Explain the Hook System" |
| **Application** | Apply concept to scenario | Correct usage, implementation | "Log tool executions using hooks" |
| **Failure Analysis** | Identify what goes wrong | Root cause, fix strategy | "Hook doesn't fire - why?" |
| **Compare-Contrast** | Differentiate concepts | Similarities, differences | "Hooks vs Tools" |
| **Edge Case** | Handle unusual scenarios | Edge awareness, robustness | "What if hook throws error?" |
| **Strategic** | Make architectural choice | Trade-offs, justification | "When to use Hook vs Tool?" |

---

## Performance Tracking

**Track over time**:

```markdown
## 15. Quiz Performance (Context Bridge)

### Overall Stats
- Quizzes taken: 5
- Average score: 82%
- Strongest area: Fundamentals (92%)
- Weakest area: Application (65%)

### History
| Lesson | Date | Score | Grade | Improvement |
|--------|------|-------|-------|-------------|
| 3.1 | 2026-03-01 | 80% | B+ | Baseline |
| 3.1 (retry) | 2026-03-03 | 95% | A | +15% ⬆️ |
| 3.15 | 2026-03-05 | 84% | B+ | -- |
| 3.17 | 2026-03-07 | 88% | B+ | +4% ⬆️ |

### Recommendations
- Keep reinforcing weak areas (Application scenarios)
- Consider review quiz before moving to Chapter 4
- Strong fundamentals - ready for advanced topics
```

---

## Future Enhancements

**Phase 4+ (Not in current scope)**:

- **Adaptive quizzing**: Harder questions if student doing well
- **Timed quizzes**: Simulate exam conditions
- **Multi-lesson quizzes**: Cumulative assessments
- **Peer comparison**: Anonymous percentile ranking
- **Confidence rating**: "How confident are you?" before answering
- **Explanation quality scoring**: Not just correctness, but clarity

---

## Summary

**Review command provides**:
- ✅ Interactive quiz generation from assessment files
- ✅ AI-assisted scoring with rubrics
- ✅ Immediate feedback with model answers
- ✅ Score tracking in context bridge
- ✅ Weak area identification
- ✅ Retry and review workflows
- ✅ Fallback: auto-generate quiz from notes

**User experience**:
1. Type `Review`
2. Select lesson
3. Answer questions interactively
4. See score + feedback immediately
5. Review weak areas or continue
6. Track progress over time

**Spaced repetition + weak area focus = deep retention.**

---

**END OF PROTOCOL**
