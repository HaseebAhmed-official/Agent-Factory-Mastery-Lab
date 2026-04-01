# Compare Command Protocol

> **Purpose**: Compare checkpoints, curriculum versions, or notes vs official content
> **Version**: 1.0
> **Created**: 2026-03-03

---

## Command Trigger

**User types**: `Compare`

**Alternative forms**: `compare`, `Diff`, `diff`, `What changed`

**With parameters**:
- `Compare L1 L2` - Compare two checkpoint layers
- `Compare 3.1 curriculum` - Compare local notes vs official curriculum
- `Compare 3.1 3.15` - Compare two lessons
- `Compare old new` - Compare before/after versions

---

## Workflow

### STAGE 1: Scope Selection

**If user provided scope** (e.g., `Compare L1 L2`):
- Parse parameters
- Skip to appropriate comparison type

**If no scope provided** (just `Compare`):

1. **Present comparison types**:
   ```
   🔍 COMPARE TOOL

   What would you like to compare?

   1️⃣ CHECKPOINT LAYERS
      Compare different depth layers (L1 vs L2 vs L3)
      Shows conceptual progression and added depth

   2️⃣ CURRICULUM VS NOTES
      Compare your local notes vs official curriculum
      Detect missing content, extra content, differences

   3️⃣ TWO LESSONS
      Compare two different lessons side-by-side
      Identify overlapping concepts, differences

   4️⃣ BEFORE/AFTER CHECKPOINT
      Compare content before and after a Rewind or revision
      See what changed in rewrites

   5️⃣ SYNC DIFF (from last sync)
      Review what changed in last curriculum sync
      See new, updated, deprecated lessons

   Your choice (1/2/3/4/5 or cancel):
   ```

2. **User selects comparison type**

---

## Comparison Type 1: Checkpoint Layers

**Purpose**: Compare L1 vs L2 vs L3 to see conceptual depth progression

### Workflow

1. **Select lesson**:
   - Prompt user: "Which lesson?" (e.g., "3.1")
   - Scan for all checkpoint files: `3.1-L*-*.md`

2. **Load checkpoint files**:
   - Read YAML frontmatter + content for each layer
   - Extract:
     - Concepts covered (from frontmatter)
     - Vocabulary terms
     - Frameworks introduced
     - Anti-patterns discussed
     - Word count

3. **Build comparison table**:

   ```markdown
   ═══════════════════════════════════════════════════════
   CHECKPOINT COMPARISON: Lesson 3.1 - Origin Story
   ═══════════════════════════════════════════════════════

   ## Overview

   | Metric | L1 (Fundamentals) | L2 (Intermediate) | L3 (Advanced) |
   |--------|-------------------|-------------------|---------------|
   | **Concepts** | 5 | +3 (8 total) | +2 (10 total) |
   | **Vocabulary** | 12 terms | +6 (18 total) | +4 (22 total) |
   | **Frameworks** | 2 | +1 (3 total) | +2 (5 total) |
   | **Anti-Patterns** | 3 | +2 (5 total) | +3 (8 total) |
   | **Word Count** | 2,500 | +1,800 (4,300) | +1,200 (5,500) |

   ═══════════════════════════════════════════════════════

   ## Concept Progression

   ### L1: Fundamentals
   1. Hook System (what it is)
   2. Lifecycle Events (when hooks fire)
   3. Hook Registration (how to register)
   4. Built-in Hooks (pre-defined hooks)
   5. Hook Execution Order (sequence)

   ### L2: Intermediate (NEW concepts)
   6. Custom Hook Patterns (creating your own)
   7. Hook Composition (combining multiple hooks)
   8. Hook Parameters (passing data to hooks)

   ### L3: Advanced (NEW concepts)
   9. Performance Optimization (efficient hooks)
   10. Error Handling in Hooks (graceful failures)

   ═══════════════════════════════════════════════════════

   ## Vocabulary Depth

   ### L1: Fundamentals (12 terms)
   Hook, Lifecycle Event, Registration, Callback, Lifecycle Stage, ...

   ### L2: Adds (6 terms)
   Custom Hook, Hook Composition, Hook Chain, Parameter Passing, ...

   ### L3: Adds (4 terms)
   Hook Optimization, Error Boundary, Async Hook, Performance Profiling

   ═══════════════════════════════════════════════════════

   ## Framework Depth

   ### L1: Fundamentals
   - Hook System Architecture (diagram)
   - Lifecycle Event Model (flow)

   ### L2: Adds
   - Custom Hook Pattern Formula (when/how to create)

   ### L3: Adds
   - Performance Trade-off Matrix (speed vs flexibility)
   - Error Handling Decision Tree (when to fail/fallback)

   ═══════════════════════════════════════════════════════

   ## Anti-Patterns (What Goes Wrong)

   ### L1: Fundamentals
   1. Forgetting to register hook
   2. Wrong lifecycle event chosen
   3. Hook execution order confusion

   ### L2: Adds
   4. Hook composition creates circular dependency
   5. Parameter passing without validation

   ### L3: Adds
   6. Performance bottleneck from heavy hook
   7. Unhandled async errors crash system
   8. Error boundary too broad (hides real issues)

   ═══════════════════════════════════════════════════════

   ## Conceptual Depth Analysis

   **L1 → L2 Progression**:
   - L1 teaches WHAT and WHY
   - L2 teaches HOW TO USE in practice
   - Shift from theory to application
   - +75% content increase

   **L2 → L3 Progression**:
   - L2 teaches common patterns
   - L3 teaches expert techniques and edge cases
   - Shift from patterns to optimization & robustness
   - +28% content increase

   **Overall L1 → L3**:
   - 120% total content increase
   - 10 concepts covered (5 → 8 → 10)
   - Progressive depth: Fundamentals → Patterns → Optimization

   ═══════════════════════════════════════════════════════

   ## Gap Analysis

   ✅ **Well Covered**:
   - Hook fundamentals thoroughly explained (L1)
   - Custom patterns with examples (L2)
   - Performance considerations addressed (L3)

   ⚠️ **Could Be Enhanced**:
   - L2 could include more composition examples
   - L3 could cover testing strategies for hooks

   💡 **Recommended Additions** (for revision):
   - L2: Add "Hook Composition Patterns" (3-4 examples)
   - L3: Add "Testing Custom Hooks" section

   ═══════════════════════════════════════════════════════
   ```

4. **Present options**:
   ```
   What would you like to do?

   1. View detailed L1 content
   2. View detailed L2 content
   3. View detailed L3 content
   4. Export comparison as markdown
   5. Return to main menu
   ```

---

## Comparison Type 2: Curriculum vs Notes

**Purpose**: Compare local lesson notes vs official curriculum lesson

### Workflow

1. **Select lesson**:
   - Prompt user: "Which lesson?" (e.g., "3.15")

2. **Load local notes**:
   - Read all `3.15-L*-*.md` files
   - Extract concepts, vocabulary, frameworks

3. **Fetch official curriculum**:
   - Check `curriculum-manifest.json` for lesson URL
   - Fetch official content using WebFetch
   - Extract concepts (scan for headings, key terms)

4. **Compute diff**:

   **Content Categories**:
   - **COVERED**: In both local notes and official curriculum
   - **EXTRA**: In local notes but NOT in official curriculum (good! additional depth)
   - **MISSING**: In official curriculum but NOT in local notes (gap!)

5. **Build comparison report**:

   ```markdown
   ═══════════════════════════════════════════════════════
   CURRICULUM COMPARISON: Lesson 3.15 - Hooks and Extensibility
   ═══════════════════════════════════════════════════════

   ## Summary

   | Category | Count | Status |
   |----------|-------|--------|
   | **COVERED** (in both) | 12 concepts | ✅ Good |
   | **EXTRA** (only in notes) | 5 concepts | 💡 Bonus depth |
   | **MISSING** (only in curriculum) | 2 concepts | ⚠️ Gap detected |

   ═══════════════════════════════════════════════════════

   ## ✅ COVERED Concepts (12)

   Concepts present in BOTH local notes and official curriculum:

   1. Hook System Overview
   2. Lifecycle Events
   3. Hook Registration
   4. Built-in Hooks
   5. Custom Hook Creation
   6. Hook Parameters
   7. Hook Composition
   8. Error Handling
   9. Performance Considerations
   10. Best Practices
   11. Common Pitfalls
   12. Real-World Examples

   **Analysis**: Excellent coverage! All core concepts from curriculum are in your notes.

   ═══════════════════════════════════════════════════════

   ## 💡 EXTRA Concepts (5)

   Concepts in local notes but NOT in official curriculum (bonus depth):

   1. **Hook Testing Strategies** (L3)
      - Your notes include testing patterns
      - Official curriculum doesn't cover this
      - GOOD: Extra practical depth

   2. **Performance Profiling for Hooks** (L3)
      - Detailed optimization techniques in your notes
      - Not in official curriculum
      - GOOD: Advanced application

   3. **Hook Composition Patterns** (L2)
      - 4 composition patterns in your notes
      - Official curriculum mentions composition but no patterns
      - GOOD: Pattern library you built

   4. **Async Hook Error Boundaries** (L3)
      - Advanced error handling in your notes
      - Official curriculum has basic error handling only
      - GOOD: Edge case coverage

   5. **Real-World Case Studies** (L2)
      - 3 case studies in your notes from practice exercises
      - Not in official curriculum
      - GOOD: Hands-on experience captured

   **Analysis**: Great! You've gone beyond curriculum with practical depth.

   ═══════════════════════════════════════════════════════

   ## ⚠️ MISSING Concepts (2)

   Concepts in official curriculum but NOT in local notes (gaps to fill):

   1. **Hook Debugging Techniques**
      - Official curriculum has section on debugging hooks
      - NOT found in your notes
      - RECOMMENDED: Add to next review session

   2. **MCP Integration with Hooks**
      - Curriculum covers MCP (Model Context Protocol) integration
      - NOT in your notes
      - RECOMMENDED: Study this topic

   **Analysis**: Minor gaps. Consider reviewing these topics.

   ═══════════════════════════════════════════════════════

   ## Content Depth Comparison

   | Aspect | Official Curriculum | Your Notes | Assessment |
   |--------|---------------------|------------|------------|
   | **Coverage** | 14 concepts | 17 concepts | ✅ More comprehensive |
   | **Depth** | Introductory | Intermediate to Advanced | ✅ Deeper |
   | **Examples** | 5 examples | 12 examples | ✅ More examples |
   | **Exercises** | None | 8 hands-on | ✅ More practice |
   | **Vocab** | 15 terms | 22 terms | ✅ More thorough |

   **Overall**: Your notes are MORE comprehensive than official curriculum. Well done!

   ═══════════════════════════════════════════════════════

   ## Recommendations

   ### High Priority
   1. **Fill gaps**: Study "Hook Debugging Techniques" and "MCP Integration"
   2. **Verify understanding**: Quiz yourself on MISSING concepts

   ### Low Priority (Optional)
   3. **Contribute back**: Consider sharing your EXTRA content (case studies, patterns) with community
   4. **Refine notes**: Ensure EXTRA concepts align with curriculum scope (Parts 0–3, 5–7)

   ═══════════════════════════════════════════════════════

   ## Next Steps

   1. Add "Hook Debugging Techniques" to notes
   2. Add "MCP Integration with Hooks" to notes
   3. Optional: Review extra concepts to ensure accuracy
   4. Re-compare after filling gaps

   ═══════════════════════════════════════════════════════
   ```

6. **Present options**:
   ```
   What would you like to do?

   1. Fill gaps now (study missing concepts)
   2. Export comparison as markdown
   3. Update notes with missing content
   4. Return to main menu
   ```

---

## Comparison Type 3: Two Lessons Side-by-Side

**Purpose**: Compare two different lessons to find overlaps, differences

### Workflow

1. **Select lessons**:
   - Prompt: "First lesson?" (e.g., "3.1")
   - Prompt: "Second lesson?" (e.g., "3.15")

2. **Load both lessons**:
   - Read all checkpoint files for both
   - Extract concepts, vocabulary, frameworks

3. **Find overlaps and differences**:

   **Categories**:
   - **SHARED**: Concepts in both lessons
   - **UNIQUE to Lesson A**: Only in first lesson
   - **UNIQUE to Lesson B**: Only in second lesson
   - **RELATED**: Concepts that build on each other

4. **Build comparison**:

   ```markdown
   ═══════════════════════════════════════════════════════
   LESSON COMPARISON
   ═══════════════════════════════════════════════════════

   **Lesson A**: 3.1 - Origin Story
   **Lesson B**: 3.15 - Hooks and Extensibility

   ═══════════════════════════════════════════════════════

   ## Concept Overlap

   ### SHARED Concepts (5)

   Concepts covered in BOTH lessons:

   1. **Hook System** (both discuss fundamentals)
   2. **Lifecycle Events** (both cover event model)
   3. **Registration** (both explain how to register)
   4. **Built-in Hooks** (both reference pre-defined hooks)
   5. **Best Practices** (both include guidelines)

   **Analysis**: Lesson 3.15 builds on foundation from 3.1

   ═══════════════════════════════════════════════════════

   ### UNIQUE to 3.1: Origin Story (8)

   Concepts ONLY in Lesson 3.1:

   1. Claude Code History
   2. Design Philosophy
   3. Core Architecture
   4. Tool System Overview
   5. Agent Loops
   6. Context Window Management
   7. Initial Setup
   8. Getting Started Tutorial

   **Analysis**: 3.1 is broader introduction, covers entire system

   ═══════════════════════════════════════════════════════

   ### UNIQUE to 3.15: Hooks and Extensibility (7)

   Concepts ONLY in Lesson 3.15:

   1. Custom Hook Creation (deep dive)
   2. Hook Composition Patterns
   3. Hook Parameters (detailed)
   4. Advanced Error Handling
   5. Performance Optimization
   6. MCP Integration
   7. Hook Debugging

   **Analysis**: 3.15 is focused deep-dive on hooks specifically

   ═══════════════════════════════════════════════════════

   ## Vocabulary Overlap

   ### SHARED Terms (10)
   Hook, Lifecycle, Event, Callback, Registration, Execution, Tool, Agent, Context, Command

   ### UNIQUE to 3.1 (15)
   Claude Code, Claude Desktop, Tool Use, Agentic Loop, Token Budget, ...

   ### UNIQUE to 3.15 (12)
   Custom Hook, Hook Chain, Composition, Parameter Binding, Async Hook, ...

   ═══════════════════════════════════════════════════════

   ## Relationship Analysis

   **Dependency**: 3.15 assumes knowledge from 3.1
   - Hook fundamentals from 3.1 are prerequisite
   - 3.15 expands on hook concepts introduced in 3.1

   **Progression**: 3.1 (broad intro) → 3.15 (focused deep-dive)
   - 3.1 covers 20% hooks, 80% other topics
   - 3.15 covers 100% hooks only

   **Overlap Type**: Foundational + Extension
   - 3.1 provides foundation
   - 3.15 extends with advanced patterns

   ═══════════════════════════════════════════════════════

   ## Study Recommendations

   **If you haven't studied 3.1 yet**:
   - Start with 3.1 first (foundation)
   - Then study 3.15 (builds on foundation)

   **If you've studied both**:
   - Review SHARED concepts to reinforce
   - Ensure understanding of how 3.15 extends 3.1

   **For exam prep**:
   - Understand the relationship (foundation → extension)
   - Don't confuse 3.1 hook basics with 3.15 advanced patterns

   ═══════════════════════════════════════════════════════
   ```

---

## Comparison Type 4: Before/After Checkpoint

**Purpose**: Compare content before and after a Rewind + revision

### Workflow

1. **Detect revisions**:
   - Scan for archived checkpoints in `.archive/`
   - Find pairs: original vs revised

2. **Select revision to compare**:
   ```
   REWIND REVISIONS DETECTED

   Lesson 3.1 - L2 (Custom Hooks):
   - Original: 3.1-L2-custom-hooks.md (2026-03-01 14:30)
   - Revised: 3.1-L2-custom-hooks.md (2026-03-03 16:00)
   - Archived: .archive/3.1-L2-custom-hooks-20260301.md

   Compare this revision? (yes/no)
   ```

3. **Load both versions**:
   - Original from `.archive/`
   - Revised from current location

4. **Compute diff**:

   **Line-by-line diff**:
   - Added content (green)
   - Removed content (red)
   - Changed content (yellow)
   - Unchanged content (gray)

5. **Build diff report**:

   ```markdown
   ═══════════════════════════════════════════════════════
   REVISION COMPARISON: Lesson 3.1-L2 - Custom Hooks
   ═══════════════════════════════════════════════════════

   **Original**: 2026-03-01 14:30 (archived)
   **Revised**: 2026-03-03 16:00 (current)

   ═══════════════════════════════════════════════════════

   ## Summary of Changes

   | Change Type | Count |
   |-------------|-------|
   | **Added** | 3 sections, 800 words |
   | **Removed** | 1 section, 200 words |
   | **Modified** | 2 sections, 300 words |
   | **Unchanged** | 4 sections, 1500 words |

   **Net change**: +600 words (+40% expansion)

   ═══════════════════════════════════════════════════════

   ## Detailed Diff

   ### ✅ ADDED Content

   **1. New Section: "Hook Composition Patterns"**
   - Location: After "Custom Hook Creation"
   - Content: 4 composition patterns with examples
   - Reason: Original lacked practical patterns

   **2. New Section: "Common Pitfalls"**
   - Location: Before conclusion
   - Content: 5 anti-patterns with fixes
   - Reason: Added "What Goes Wrong" framework

   **3. Enhanced Examples**
   - Added 3 more code examples
   - More realistic scenarios

   ═══════════════════════════════════════════════════════

   ### ❌ REMOVED Content

   **1. Removed Section: "Basic Hook Review"**
   - Reason: Redundant (already covered in L1)
   - Content moved to L1 instead

   ═══════════════════════════════════════════════════════

   ### 🔄 MODIFIED Content

   **1. Section: "Custom Hook Creation"**
   - BEFORE: Brief overview (150 words)
   - AFTER: Detailed walkthrough with step-by-step (400 words)
   - Change: +167% expansion, added more detail

   **2. Section: "Hook Parameters"**
   - BEFORE: Technical description
   - AFTER: Added analogy + visual diagram
   - Change: Improved clarity with TEACH cycle

   ═══════════════════════════════════════════════════════

   ## Quality Improvement Analysis

   **Improvements**:
   ✅ More practical examples (+3)
   ✅ Added "What Goes Wrong" framework
   ✅ Removed redundancy
   ✅ Better analogies and diagrams
   ✅ Followed TEACH cycle more rigorously

   **Trade-offs**:
   - Longer content (+40% words)
   - May take more time to study

   **Overall**: Revised version is significantly improved. Good revision!

   ═══════════════════════════════════════════════════════
   ```

---

## Comparison Type 5: Sync Diff

**Purpose**: Review changes from last curriculum sync

### Workflow

1. **Load last sync log**:
   - Read `logs/sync-{latest}.log`
   - Extract NEW, UPDATED, DEPRECATED lessons

2. **Present sync summary**:

   ```markdown
   ═══════════════════════════════════════════════════════
   LAST SYNC: 2026-03-03 16:45
   ═══════════════════════════════════════════════════════

   ## Summary

   - NEW lessons: 3
   - UPDATED lessons: 2
   - DEPRECATED lessons: 1
   - UNCHANGED lessons: 36

   ═══════════════════════════════════════════════════════

   ## NEW Lessons (3)

   1. **3.25** - Advanced MCP Integration
      - Added to Chapter 3
      - Status: Not yet studied

   2. **4.8** - Custom Tool Development
      - Added to Chapter 4
      - Status: Not yet studied

   3. **5.12** - Multi-Agent Orchestration
      - Added to Chapter 5
      - Status: Not yet studied

   ═══════════════════════════════════════════════════════

   ## UPDATED Lessons (2)

   1. **3.15** - Hooks and Extensibility
      - Content hash changed
      - Status: You studied the OLD version
      - RECOMMENDED: Review new version

   2. **3.22** - CoWork Terminal to Desktop
      - Content hash changed
      - Status: Not yet studied
      - RECOMMENDED: Study updated version

   ═══════════════════════════════════════════════════════

   ## DEPRECATED Lessons (1)

   1. **3.5** - Legacy Integration Patterns
      - Removed from official curriculum
      - Archived to: .deprecated/3.5-legacy-integration.md
      - Status: No action needed (archived)

   ═══════════════════════════════════════════════════════

   ## Recommended Actions

   **High Priority**:
   1. Review updated Lesson 3.15 (you studied old version)
   2. Study new Lesson 3.25 (continues Chapter 3)

   **Low Priority**:
   3. Study new Lesson 4.8 (when you reach Chapter 4)
   4. Study new Lesson 5.12 (when you reach Chapter 5)
   5. Review updated Lesson 3.22

   ═══════════════════════════════════════════════════════
   ```

3. **Present options**:
   ```
   What would you like to do?

   1. View detailed diff for updated lessons
   2. Start studying new lessons
   3. Export sync report
   4. Return to main menu
   ```

---

## Edge Cases & Error Handling

### Case 1: No Checkpoints to Compare

**Scenario**: User requests `Compare L1 L2` but only L1 exists

**Handling**:
```
⚠️ Cannot compare L1 and L2

Only L1 checkpoint exists for this lesson.
L2 not yet created.

Suggestion: Complete L2 checkpoint first, then compare.
```

### Case 2: Lesson Not Found

**Scenario**: User requests `Compare 3.99 curriculum` (lesson doesn't exist)

**Handling**:
```
❌ Lesson 3.99 not found

Check lesson number and try again.
Available lessons: 3.1, 3.15, 3.17, 3.22, 3.23
```

### Case 3: Curriculum Fetch Fails

**Scenario**: Network error when fetching official curriculum

**Handling**:
```
❌ Cannot fetch official curriculum

Network error. Check internet connection.

Alternative: Compare using cached curriculum (last synced 2026-03-01)
```

---

## Integration with CLAUDE.md

**Add to CLAUDE.md under "Commands" section**:

```markdown
### Compare Command

**Usage**: `Compare [scope]`

**Purpose**: Compare checkpoints, curriculum, lessons, or revisions

**Examples**:
- `Compare` - Choose comparison type
- `Compare L1 L2` - Compare two checkpoint layers
- `Compare 3.1 curriculum` - Compare notes vs official
- `Compare 3.1 3.15` - Compare two lessons

**Workflow**:
1. Select comparison type or provide scope
2. Load content to compare
3. Compute diff (COVERED/EXTRA/MISSING or SHARED/UNIQUE)
4. Present detailed comparison report
5. Export as markdown or take action

**Use cases**:
- Track conceptual depth progression (L1 vs L2 vs L3)
- Verify notes match curriculum (gap analysis)
- Understand lesson relationships (dependencies, overlaps)
- Review revision impact (before/after)
- Check sync changes (NEW/UPDATED/DEPRECATED)
```

---

## Summary

**Compare command provides**:
- ✅ Checkpoint layer comparison (depth progression)
- ✅ Curriculum vs notes diff (gap analysis)
- ✅ Lesson-to-lesson comparison (relationships)
- ✅ Before/after revision diff (quality improvement)
- ✅ Sync diff review (curriculum changes)

**User experience**:
1. Type `Compare [scope]`
2. View detailed diff report
3. Identify gaps, overlaps, or changes
4. Take action (fill gaps, export, continue)

**Visibility into learning progress and content quality.**

---

**END OF PROTOCOL**
