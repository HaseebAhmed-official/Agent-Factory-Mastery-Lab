# Session 02 -- Lesson 3.18: The Creator's Workflow

> **Date**: 2026-02-17
> **Lesson Covered**: Chapter 3, Lesson 3.18 -- The Creator's Workflow: Claude Code Best Practices
> **Student Status**: Lesson 3.18 COMPLETE | Next: TBD (student to choose)
> **Source URL**: https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/creator-workflow

---

## 1. Project Essence

A structured study system for mastering the Panaversity course **"Agent Factory Part 1: General Agents Foundations" (AIAF-2026)**. The AI tutor operates as **Professor Agent** following the CLAUDE.md system prompt that defines the full curriculum, teaching methodology (TEACH cycle), and exam coaching protocols.

### The Student's Goal

Not just to pass a test -- but to become a **problem solver, strategic thinker, and orchestrator** who can apply frameworks to novel situations, identify anti-patterns in real scenarios, and make sound architectural decisions about AI agent deployment.

### The Course Scope

6 chapters, 60+ lessons. Currently in **Chapter 3: General Agents -- Claude Code & Cowork** (32 lessons). Student started at L3.1, skipping Ch 1-2 for now (defining Ch 1-2 concepts inline as they arise).

---

## 2. Student Profile & Learning DNA

### Background

- **Level**: Intermediate. Used ChatGPT and Claude conversationally. Done basic prompt engineering. New to agentic AI, agent development, and the Agent Factory framework.
- **Language**: English only
- **Access**: May not have paid Claude Code subscription -- exercises should accommodate free backends (OpenRouter, Gemini, DeepSeek)

### How This Student Learns Best

- Needs **all jargon pre-defined** before it's used
- Benefits from **concrete examples** over abstract theory
- Wants to be **challenged deeply** -- not given shallow multiple-choice
- Responds well to **structured feedback** (what you got right -> what to add -> complete answer)
- Prefers the AI to **give full model answers** when they say "answer" or "you explain"
- Wants **hands-on exercises, edge cases, failure modes, adversarial thinking** as default

### Behavioral Patterns Observed

| Pattern | What It Means | How to Respond |
|---------|--------------|----------------|
| Says "answer" or "you explain" | Wants the model answer delivered | Provide the deep answer immediately |
| Says "yes" to multiple questions | Wants to move fast past basics | Respect pace, focus depth on concepts |
| Pushes back on shallow teaching | Deeply values rigor | Always deliver the full framework -- no shortcuts |
| Asks creative strategic questions | Genuinely engaged | Match the depth and creativity of their question |
| Shares lesson URLs | Wants teaching aligned with course material | Always fetch and integrate the source content |
| Calls out missed content | Holds Professor Agent to comprehensive coverage | Go back and cover missed sections fully |

### Critical Student Instructions (Binding)

> Session 1 correction: "I want to be a problem solver, strategic thinker, orchestrator and want hands-on and want to learn edge cases and all other things written in your CLAUDE.md but you did not follow it."

> Session 2 correction: Called out Professor Agent for rushing through three sections (Subagents, Prompting, Data Analysis). Demanded full coverage per MEMORY.md "Try with AI" framework requirements.

**Both corrections are binding for ALL future sessions. Never rush through content. Every section gets the full "Try with AI" treatment.**

---

## 3. Established Teaching Patterns

### The TEACH Cycle (Mandatory for Every Concept)

| Step | What | Status |
|------|------|--------|
| **T** - Terminology First | Define every term in a Key Vocabulary table before using it | ACTIVE |
| **E** - Explain with Depth | What / Why / How / Where it fits / What can go wrong | ACTIVE |
| **A** - Analogize & Visualize | Real-world analogy + ASCII diagrams/tables | ACTIVE |
| **C** - Check Understanding | Open-ended questions via AskUserQuestion tool | ACTIVE |
| **H** - Hands-On Practice | Executable exercise every lesson | ACTIVE |

### The "Try with AI" Proactive Framework (Binding Operating Mode)

For EVERY concept, automatically generate:

| Dimension | What to Do |
|-----------|-----------|
| **Friction Analysis** | Show real-world friction. Make them feel the pain of doing it wrong. |
| **Product Overhang Recognition** | "What's locked inside this that most people miss?" |
| **Domain Application** | Force application to their context. |
| **Failure Scenarios** | "What breaks? When? Why? How to detect? Recover?" |
| **Edge Cases** | "When does this rule NOT apply?" |
| **Adversarial Thinking** | "Strongest argument against this? How respond?" |
| **Cross-Concept Synthesis** | "How does this connect to previous learning?" |
| **Strategic Scenarios** | Complex multi-variable judgment situations. |

> **Do NOT wait for the student to ask.** This is the default. Expand book's "Try with AI" from 10% to 100%.
> **Do NOT rush through sections.** Every section of every lesson gets this treatment. Student corrected on this in Session 02.

### Question & Quiz Protocol

- **ALWAYS use AskUserQuestion tool** for all comprehension checks, quizzes, and questions
- Use **open-ended explain-back questions** (not shallow multiple-choice)
- Question types: Explain-Back, Application, Failure Analysis, Compare-Contrast, Edge Case, Strategic
- After answers: structured feedback (What you got right -> What to add -> Complete answer -> Why it matters)

### Revision File Protocol

- After each lesson, create a detailed `.md` revision file
- Naming: `{lesson-number}-{kebab-case-title}.md`
- Location: `revision-notes/ch{N}-{chapter-name}/`

### Source Material Protocol

- When student shares a lesson URL, **always fetch and integrate**
- Supplement with deeper analysis but never contradict the source

### End-of-Session Protocol

- Triggered by user command `End`
- Three-tier archival: Master Lesson Doc + Context Bridge + HTML Visual Synthesis
- Defined in `Knowledge_Vault/Protocols/end-of-session-synthesis.md`

---

## 4. Key Technical Decisions

### File & Directory Conventions

| Decision | Choice |
|----------|--------|
| Revision file naming | `3.18-creators-workflow.md` |
| Chapter directory naming | `ch3-general-agents-claude-code-cowork/` |
| Session context naming | `session-02-lesson-3.18-creators-workflow.md` |
| Monorepo approach | Single repo with organized subdirectories |

---

## 5. Session Flow

### What Happened This Session

1. **Context Bridge Loaded** -- Student shared session-01 context bridge, said "let me know when ready"
2. **Lesson URL Shared** -- Student provided L3.18 URL (Creator's Workflow)
3. **Source Fetched and Integrated** -- Full lesson content retrieved from agentfactory.panaversity.org
4. **Vocabulary Delivered** -- 12 initial terms defined
5. **Core Explanation** -- Five Principles framework, fundamental constraint, each principle explained with diagrams
6. **Professional Kitchen Analogy** -- Counter space, mise en place, recipe binder, tasting, stations
7. **Key Practices Deep-Dive** -- Skills, autonomous problem solving, failure patterns
8. **Connection Map** -- Full curriculum cross-references
9. **Friction Analysis + Product Overhang + Edge Cases + Adversarial Thinking** -- For Five Principles
10. **Strategic Scenario** -- Solo developer with 3 workstreams in one session
11. **Comprehension Check 1** -- "Pick two practices, trace to context constraint" -- Student chose "You explain" -- Model answer delivered
12. **Deep Dive: Notes/ Directory Pattern** -- Individual compounding, architecture, three-zone strategy
13. **Deep Dive: @.claude Team Pattern** -- Organizational compounding, failure modes
14. **Comprehension Check 2** -- "12 files, 3000 lines, new developer" -- Student answered briefly (right direction, insufficient depth) -- Full model answer delivered
15. **Remaining Practices** -- Model selection, session management, permissions, hooks, learning mode, voice dictation, autonomous problem solving
16. **COURSE CORRECTION** -- Student called out rushing through Subagents, Prompting, and Data Analysis sections
17. **Subagents Section Re-delivered at Full Depth** -- Vocabulary, context isolation diagrams, "use subagents" directive, permission routing, friction analysis, pattern recognition, edge cases, adversarial thinking, strategic scenario, What Goes Wrong
18. **Prompting Section Re-delivered at Full Depth** -- Challenge prompts, elegant solution, detailed briefs, friction analysis, pattern recognition (OODA connection), domain application, edge cases, adversarial thinking, What Goes Wrong
19. **Data Analysis Section Re-delivered at Full Depth** -- Paradigm shift, domain applications, skill-building pattern, Product Overhang, friction analysis, edge cases, adversarial thinking, What Goes Wrong
20. **Hands-On Exercise Offered** -- Three-part exercise (subagent plan + challenge prompts + data skill)
21. **Lesson Summary** -- Five Principles recap, full practice table, connection map, failure patterns
22. **End Protocol Triggered** -- Three-tier archival initiated

### Key Moments

- **Course correction (Session 2)**: Student caught Professor Agent rushing through three sections and demanded full coverage. This reinforces Session 1 correction -- full depth is non-negotiable.
- **Architecture question partial answer**: Student correctly identified the notes/ pointer mechanism but missed the deeper problem (context budget, progressive disclosure, three-zone strategy). Shows right instincts but needs more practice on architectural reasoning.
- **Consistent "You explain" on comprehension checks**: Student continues to prefer model answers over attempting. Growth area carried forward from Session 1.

---

## 6. Knowledge Graph -- What Was Learned

### Lesson 3.1: Claude Code Origin Story -- COMPLETE (Session 01)

```
CONCEPTS MASTERED:
├── Origin Story (Boris Cherny, Sept 2024, filesystem experiment)
├── Product Overhang (capability + missing interface = unlock)
├── Adoption Stats (20%->50%->80%, 5 PRs/day, 90% self-written)
├── Passive vs Agentic Model (chatbot vs agent, execution vs judgment)
├── Two Interfaces (Claude Code terminal vs Cowork desktop)
├── General vs Custom Agents (factory vs product)
├── OODA Loop (Observe->Orient->Decide->Act, autonomous cycling)
├── OODA as Diagnostic Tool (which step broke?)
├── Agent Skills preview (encoded expertise, SKILL.md)
├── Anti-Patterns (Unverified Trust, Monolithic Decomposition, Staying Passive, Over-Distrust)
├── Trust Spectrum (no trust <-- balanced --> blind trust)
├── Scaling Analysis (O(n^2) copy-paste vs O(1) agentic)
├── Product Overhang Pattern Recognition (3 future examples)
├── Edge Cases (when chatbot wins: security, air-gap, learning, quick questions)
└── Adversarial Analysis (filesystem danger: valid concerns + counter-arguments)
```

### Lesson 3.18: The Creator's Workflow -- COMPLETE (Session 02)

```
CONCEPTS MASTERED:
├── The Fundamental Constraint (context window fills -> performance degrades)
├── Context Window Lifecycle (Fresh -> Productive -> Degrading -> Polluted)
├── The Five Principles (Context, Parallelization, Plan Mode, Self-Evolving Docs, Verification)
│
├── PRINCIPLE 1: Context is the Constraint
│   ├── /clear as strategic tool (not panic button)
│   ├── /statusline for monitoring
│   └── 10-20% session abandonment as healthy behavior
│
├── PRINCIPLE 2: Parallelization Over Optimization
│   ├── Parallel sessions ("single biggest productivity unlock")
│   ├── Git worktrees (developers)
│   ├── Multiple tabs/workspaces (knowledge workers)
│   └── O(1) context cost per task
│
├── PRINCIPLE 3: Plan Mode Discipline
│   ├── Plan Mode workflow (Shift+Tab x2, iterate, auto-accept, execute)
│   ├── Plan Mode economics (cheap text vs expensive execution)
│   ├── Recovery pattern (switch back to Plan Mode when sideways)
│   └── Claude-Reviews-Claude (fresh context catches blind spots)
│
├── PRINCIPLE 4: Self-Evolving Documentation
│   ├── Magic phrase ("Update your CLAUDE.md so you don't make that mistake again")
│   ├── Notes/ directory pattern (compounding project knowledge)
│   ├── Three-zone strategy for notes/ at scale (index -> on-demand -> never)
│   ├── @.claude team pattern (organizational learning via code review)
│   └── Individual + team compounding synthesis
│
├── PRINCIPLE 5: Verification Infrastructure
│   ├── 2-3x quality improvement from feedback loops
│   ├── Forms: tests, browser automation, hooks, subagents, bash
│   └── Connection to OODA Observe step
│
├── Specialized Subagents
│   ├── Boris's library (code-simplifier, verify-app, build-validator, code-architect)
│   ├── Context isolation mechanism (subagent reads -> summary report -> main context preserved)
│   ├── "use subagents" directive (parallel cognitive compute)
│   ├── Investigation pattern (explore in isolation, report findings)
│   ├── Permission routing through hooks
│   └── Trust calibration for subagent reports (low/medium/high stakes)
│
├── Level Up Your Prompting
│   ├── Challenge prompts (critique mode vs generate mode)
│   ├── Elegant solution prompt (context investment -> superior redo)
│   ├── Detailed briefs (specificity = quality)
│   └── Specificity equation (vague + corrections vs specific + zero corrections)
│
├── Research & Data Analysis
│   ├── Conversational data interface (NL replaces query languages)
│   ├── Product Overhang for data (existing data + missing NL interface = unlock)
│   ├── Skill-building pattern for data access
│   └── Safety layers for data queries (readonly, limits, replica, show query)
│
├── Skills for Workflow Automation
│   ├── Heuristic ("more than once a day -> skill")
│   ├── Session-end review skill (/session-review)
│   ├── Technical debt skill (/techdebt)
│   ├── Skill portfolio (commit, simplify, verify, context-dump)
│   └── Global vs project-specific storage
│
├── Supporting Practices
│   ├── Autonomous problem solving (give problem, not solution)
│   ├── Model selection (Opus 4.5: right slow > wrong fast)
│   ├── Session management (/clear, /rewind, Esc, --continue, --resume, /rename)
│   ├── Permissions vs skip (/permissions over --dangerously-skip-permissions)
│   ├── PostToolUse hooks (auto-format after write)
│   ├── Using Claude Code for learning (explanatory mode, HTML presentations)
│   └── Voice dictation (3x faster, more detail = better output)
│
└── Failure Patterns
    ├── Kitchen Sink Session (mixed tasks -> context pollution)
    ├── Correction Spiral (failed approaches poisoning context)
    ├── Over-Specified CLAUDE.md (signal buried in noise)
    ├── Trust-Then-Verify Gap (no feedback loops)
    ├── Infinite Exploration (unbounded investigation fills context)
    └── Meta-pattern: most failures = context pollution

CONCEPTS FROM CH1/CH2 REINFORCED:
├── LLM Constraint 3: Context Window -- now the CENTRAL constraint driving every practice
├── LLM Constraint 1: Statelessness -- notes/ and CLAUDE.md externalize memory
├── LLM Constraint 2: Probabilistic -- verification infrastructure addresses this
├── OODA Loop -- Plan Mode = Orient+Decide, Verification = Observe
├── Product Overhang -- applied to data access
├── Trust Spectrum -- applied to subagent reports
└── O(1) Scaling -- applied to context management via parallel sessions
```

---

## 7. Vocabulary Bank -- Terms Introduced

All terms below have been **defined and used in context**. In new sessions, use freely with brief inline reminders.

| Term | First Introduced | Defined? |
|------|-----------------|----------|
| Claude Code | 3.1 | Yes |
| Claude Cowork | 3.1 | Yes |
| CLI | 3.1 | Yes |
| General Agent | 3.1 | Yes |
| Custom Agent | 3.1 | Yes |
| Agentic AI | 3.1 | Yes |
| Product Overhang | 3.1 | Yes |
| OODA Loop | 3.1 | Yes |
| Filesystem Access | 3.1 | Yes |
| Permission Loop | 3.1 | Yes |
| Agent Skills | 3.1 | Yes (preview) |
| Digital FTE | 3.1 | Yes |
| Orchestrator | 3.1 | Yes |
| SKILL.md | 3.1 | Mentioned |
| Unverified Trust | 3.1 | Yes |
| Monolithic Decomposition | 3.1 | Yes |
| Creator's Workflow | 3.18 | Yes |
| Parallel Sessions | 3.18 | Yes |
| Git Worktree | 3.18 | Yes |
| Plan Mode | 3.18 | Yes |
| Claude-Reviews-Claude | 3.18 | Yes |
| Self-Writing CLAUDE.md | 3.18 | Yes |
| Notes Directory Pattern | 3.18 | Yes |
| @.claude Team Pattern | 3.18 | Yes |
| Session-End Review | 3.18 | Yes |
| Correction Spiral | 3.18 | Yes |
| Context Pollution | 3.18 | Yes |
| Kitchen Sink Session | 3.18 | Yes |
| PostToolUse Hook | 3.18 | Yes |
| Voice Dictation | 3.18 | Yes |
| Skill Portfolio | 3.18 | Yes |
| Subagent | 3.18 | Yes |
| code-simplifier | 3.18 | Yes |
| verify-app | 3.18 | Yes |
| build-validator | 3.18 | Yes |
| code-architect | 3.18 | Yes |
| "use subagents" directive | 3.18 | Yes |
| Challenge Prompts | 3.18 | Yes |
| Elegant Solution Prompt | 3.18 | Yes |
| Detailed Brief | 3.18 | Yes |
| Conversational Data Interface | 3.18 | Yes |

---

## 8. Anti-Patterns Covered

### Fully Taught

| Anti-Pattern | Chapter | How Taught |
|-------------|---------|------------|
| Unverified Trust | 3.1 | Scenarios + trust spectrum |
| Monolithic Decomposition | 3.1 | "Build everything" failure |
| Staying Passive | 3.1 | Copy-paste vs agentic comparison |
| Over-Distrust | 3.1 | Developer rewriting all output |
| Kitchen Sink Session | 3.18 | Mixed tasks -> context pollution + strategic scenario |
| Correction Spiral | 3.18 | Failed approaches poisoning context + /clear fix |
| Over-Specified CLAUDE.md | 3.18 | Signal buried in noise + prune rule |
| Trust-Then-Verify Gap | 3.18 | No feedback loops + verification infrastructure |
| Infinite Exploration | 3.18 | Unbounded investigation + subagent fix |

### Mentioned But Not Yet Fully Taught

Premature Specialization, Perpetual Incubation, Skipping Incubation (Ch.1), Vibe Coding (Ch.5), Context Stuffing, Context Starvation, Workflow Drift (Ch.4)

---

## 9. Frameworks & Mental Models Internalized

```
-- FROM SESSION 01 --

1. Product Overhang Formula:
   Existing Capability + Missing Interface = Massive Unlock

2. Agentic Success Requirements:
   Filesystem Access + Test Suite + Small Steps + Human Review = Success
   Remove ANY one = Failure

3. OODA Diagnostic:
   Wrong output -> ORIENT | Missing info -> OBSERVE | Blocked -> ACT | Wrong strategy -> DECIDE

4. Trust Spectrum:
   Over-distrust (typist) <-- Balanced (orchestrator) --> Blind trust (dangerous)

5. Scaling:
   Copy-paste: O(n) to O(n^2) | Agentic: O(1) human, O(log n) agent

6. "What Goes Wrong" (4 Lenses):
   Misapplication | Omission | Excess | Interaction Failure

-- FROM SESSION 02 --

7. The Fundamental Constraint:
   Context window fills -> Performance degrades -> Every practice manages this

8. Five Principles of the Creator's Workflow:
   Context | Parallelization | Plan Mode | Self-Evolving Docs | Verification

9. Context Window Lifecycle:
   Fresh (0%) -> Productive (~30%) -> Degrading (~70%) -> Polluted (~90%+)

10. Plan Mode Economics:
    Planning tokens (cheap text) << Correction tokens (code + undo + redo)

11. Self-Writing Compound Interest:
    Each 30-second CLAUDE.md update prevents same error x N future sessions

12. Subagent Context Savings:
    Main context cost = summary lines only, not raw file reads

13. Specificity Equation:
    Vague (1 min + 4 corrections = 21 min) vs Specific (5 min + 0 = 5 min)

14. Right Slow > Wrong Fast:
    Total task time = response time x iteration count

15. Product Overhang for Data:
    Existing Data + Missing NL Interface = Democratized Access

16. Trust Calibration for Subagents:
    Low stakes -> trust | Medium -> verify key refs | High -> verify everything

17. Notes/ Three-Zone Strategy:
    Zone 1: CLAUDE.md index (~150 tokens) | Zone 2: specific file (on-demand) | Zone 3: irrelevant (0 tokens)

18. Team Compounding:
    Individual (notes/): linear growth | Team (@.claude): multiplied by team size
```

---

## 10. Student Strengths & Growth Areas

### Strengths

- **Recall**: Correctly remembered adoption stats (Session 1)
- **Core concepts**: Immediately grasped "chatbot answers, agent acts" (Session 1)
- **Trust analysis**: Identified Over-Distrust anti-pattern correctly (Session 1)
- **OODA application**: 2/3 on diagnostic scenarios (Session 1)
- **Strategic curiosity**: Independently asked about future Product Overhangs (Session 1)
- **Quality demand**: Won't accept shallow teaching; corrected Professor Agent in BOTH sessions
- **Pattern recognition**: Correctly identified the notes/ pointer mechanism (Session 2)
- **Content vigilance**: Caught Professor Agent rushing through sections and demanded full coverage (Session 2)

### Growth Areas

- **Articulating strategic analysis**: Consistently requests model answers on open-ended questions -- needs gradual push toward attempting (both sessions)
- **Architectural depth**: Partial answer on notes/ architecture question -- right direction but missed deeper implications (progressive disclosure, three-zone strategy). Needs more practice reasoning about system design at scale.
- **Observe vs Orient distinction**: Missed nuance in OODA Scenario A (Session 1) -- reinforce in future lessons

---

## 11. Collaboration Style & Tone

### Rules

- **Be direct.** No filler.
- **Be deep.** Full depth always. Student rejected shallow teaching TWICE.
- **Be structured.** Tables, ASCII diagrams, clear headers.
- **Be honest.** If answer is incomplete, say so. Give complete version.
- **Respect "answer" requests.** Deliver full model answer without re-prompting.
- **Push strategically.** Challenge on their terms via AskUserQuestion.
- **No emojis** unless requested.
- **Fetch source URLs** when shared.
- **Create revision files** after every lesson.
- **Cover EVERY section.** Never rush through content. Full "Try with AI" framework on every section.

### Student Intent Signals

| They Say | They Mean |
|----------|----------|
| "answer" / "you explain" / "you give" | Deliver model answer now |
| "I need a hint" | Nudge, not full answer |
| "Let me type" | They'll attempt -- wait |
| Shares a URL | Fetch and align with source |
| "quiz me" / "quiz me hard" | Challenging questions via AskUserQuestion |
| Pushes back on approach | Adjust immediately |
| "move" / "move to the rest" | Continue with remaining content |
| Calls out missed content | Go back and cover fully |
| "End" | Execute end-of-session synthesis protocol |

---

## 12. Repository Structure

```
Agent-Factory-Part 1-test-prep/              <- ROOT (monorepo)
|
├── CLAUDE.md                                <- System prompt (Professor Agent)
|
├── Knowledge_Vault/                         <- Curriculum, pedagogy, protocols
│   ├── Curriculum/
│   ├── Pedagogy/
│   ├── Vocabulary/
│   ├── Protocols/
│   ├── Frameworks/
│   ├── Student/
│   └── Capabilities/
|
├── context-bridge/                          <- Session continuity
│   ├── session-01-lesson-3.1-origin-story.md        <- DONE
│   ├── session-02-lesson-3.18-creators-workflow.md   <- THIS FILE
│   └── ...
|
├── revision-notes/                          <- Per-lesson revision guides
│   ├── ch1-ai-agent-factory-paradigm/
│   ├── ch2-markdown-writing-instructions/
│   ├── ch3-general-agents-claude-code-cowork/
│   │   ├── 3.1-claude-code-origin-story.md          <- DONE
│   │   ├── 3.18-creators-workflow.md                 <- DONE
│   │   └── ...
│   ├── ch4-effective-context-engineering/
│   ├── ch5-spec-driven-development/
│   └── ch6-seven-principles/
|
├── quiz-bank/                               <- Accumulated quiz questions
│   └── ch3-quiz-bank.md                     <- (future)
|
├── exercises/                               <- Hands-on exercises & solutions
│   └── ch3-exercises/                       <- (future)
|
└── progress-tracking/                       <- Curriculum progress
    └── PROGRESS.md                          <- (future)
```

---

## 13. Next Steps

### Immediate Next

- **Student to choose next lesson** -- options include sequential (L3.2-3.7 Module A) or continuing with other advanced lessons
- Apply full TEACH cycle + "Try with AI" proactive framework
- Cover EVERY section with full depth -- no rushing

### Lessons Completed So Far

```
3.1   Claude Code Origin Story                    <- COMPLETE (Session 01)
3.18  The Creator's Workflow: Best Practices       <- COMPLETE (Session 02)
```

### Module A Remaining (Lessons 3.2 -- 3.7)

```
3.2  Installing and Authenticating Claude Code
3.3  Free Claude Code Setup (OpenRouter, Gemini, DeepSeek)
3.4  Hello Claude -- First Conversation (CLI basics, slash commands, permissions)
3.5  CLAUDE.md Context Files (persistent project context)
3.6  Practical Problem-Solving Exercises (27 exercises)
3.7  Teach Claude Your Way of Working
```

### Open Questions

- Will you cover Chapters 1-2 at any point, or stay focused on Chapter 3?
- Should we create a PROGRESS.md tracker?
- Which lesson next: sequential (3.2) or another advanced lesson?

---

## 14. How to Use This File

1. Start a new session with Professor Agent
2. Share this file at the beginning
3. Say: **"Load context bridge and continue from where we left off"**
4. Professor Agent will:
   - Recognize all established patterns and protocols
   - Know your learning style and preferences
   - Resume at your chosen lesson
   - Apply the full TEACH cycle + "Try with AI" framework on EVERY section
   - Use AskUserQuestion for all questions
   - Create revision files after each lesson
   - Execute End protocol when triggered

---

*Session 02 complete | 2026-02-17 | Lesson 3.18 done | Next: Student's choice*
