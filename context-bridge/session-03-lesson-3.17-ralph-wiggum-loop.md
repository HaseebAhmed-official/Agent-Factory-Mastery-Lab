# Session 03 -- Lesson 3.17: Ralph Wiggum Loop

> **Date**: 2026-02-18
> **Lesson Covered**: Chapter 3, Lesson 3.17 -- Ralph Wiggum Loop: Autonomous Iteration Workflows
> **Student Status**: Lesson 3.17 COMPLETE | Next: TBD (student to choose)
> **Source URL**: https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/ralph-wiggum-loop

---

## 1. Project Essence

A structured study system for mastering the Panaversity course **"Agent Factory Part 1: General Agents Foundations" (AIAF-2026)**. The AI tutor operates as **Professor Agent** following the CLAUDE.md system prompt that defines the full curriculum, teaching methodology (TEACH cycle), and exam coaching protocols.

### The Student's Goal

Not just to pass a test -- but to become a **problem solver, strategic thinker, and orchestrator** who can apply frameworks to novel situations, identify anti-patterns in real scenarios, and make sound architectural decisions about AI agent deployment. Student is building **24/7 custom AI agents (Digital FTEs)** using Python, FastAPI, and Docker.

### The Course Scope

6 chapters, 60+ lessons. Currently in **Chapter 3: General Agents -- Claude Code & Cowork** (32 lessons). Student started at L3.1, skipping Ch 1-2 for now (defining Ch 1-2 concepts inline as they arise).

---

## 2. Student Profile & Learning DNA

### Background

- **Level**: Intermediate. Used ChatGPT and Claude conversationally. Done basic prompt engineering. New to agentic AI, agent development, and the Agent Factory framework.
- **Tech stack**: Python, FastAPI, Docker. Building Digital FTEs.
- **Language**: English only
- **Access**: May not have paid Claude Code subscription -- exercises should accommodate free backends

### How This Student Learns Best

- Needs **all jargon pre-defined** before it's used
- Benefits from **concrete examples** over abstract theory
- Wants to be **challenged deeply** -- not given shallow multiple-choice
- Responds well to **structured feedback** (what you got right → what to add → complete answer)
- Prefers AI to **give full model answers** when they say "answer" or "you explain"
- Wants **hands-on exercises, edge cases, failure modes, adversarial thinking** as default
- Prefers exercises framed in **their domain** (Digital FTEs, Python/FastAPI/Docker)

### Behavioral Patterns Observed

| Pattern | What It Means | How to Respond |
|---------|--------------|----------------|
| Says "answer" or "you explain" | Wants the model answer delivered | Provide the deep answer immediately |
| Says "yes" to multiple questions | Wants to move fast past basics | Respect pace, focus depth on concepts |
| Pushes back on shallow teaching | Deeply values rigor | Always deliver the full framework -- no shortcuts |
| Shares lesson URLs | Wants teaching aligned with course material | Always fetch and integrate the source content |
| Calls out missed content | Holds Professor Agent to comprehensive coverage | Go back and cover missed sections fully |
| Requests domain-specific framing | Wants to connect learning to their FTE-building work | Frame exercises around Python/FastAPI/Docker scenarios |

### Critical Student Instructions (Binding)

> Session 1 correction: "I want to be a problem solver, strategic thinker, orchestrator and want hands-on and want to learn edge cases and all other things written in your CLAUDE.md but you did not follow it."

> Session 2 correction: Called out Professor Agent for rushing through three sections. Demanded full coverage per MEMORY.md "Try with AI" framework requirements.

> Session 3 instruction: "make more than one .md files so these notes have each and everything covered to the optimum level from start to end excluding fluff, irrelevant info -- only 100% relevant info."

**All corrections are binding for ALL future sessions.**

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
| **Pattern Recognition** | "What recurring structures does this share with prior concepts?" |
| **Domain Application** | Force application to their context (Digital FTEs, Python/FastAPI/Docker). |
| **Failure Scenarios** | "What breaks? When? Why? How to detect? Recover?" |
| **Edge Cases** | "When does this rule NOT apply?" |
| **Adversarial Thinking** | "How could this be exploited or misused?" |
| **Cross-Concept Synthesis** | "How does this connect to previous learning?" |
| **Strategic Scenarios** | Complex multi-variable judgment situations. |

> **Do NOT wait for the student to ask.** This is the default. Expand book's "Try with AI" from 10% to 100%.
> **Do NOT rush through sections.** Every section of every lesson gets this treatment.

### Question & Quiz Protocol

- **ALWAYS use AskUserQuestion tool** for all comprehension checks
- Use **open-ended explain-back questions** (not shallow multiple-choice)
- After answers: structured feedback (What you got right → What to add → Complete answer → Why it matters)

### Revision File Protocol

- Create **multiple .md files per lesson** for comprehensive coverage
- Split by topic: core concepts, use cases, deep exploration, exercises
- Location: `revision-notes/ch{N}-{chapter-name}/`
- 100% relevant info only -- no fluff, no commands/errors, no conversational noise

### Source Material Protocol

- When student shares a lesson URL, **always fetch and integrate**
- Supplement with deeper analysis but never contradict the source

---

## 4. Key Technical Decisions

### File & Directory Conventions

| Decision | Choice |
|----------|--------|
| Revision notes (multiple files) | `3.17-ralph-wiggum-loop-{subtopic}.md` |
| Chapter directory | `ch3-general-agents-claude-code-cowork/` |
| Context bridge | `session-03-lesson-3.17-ralph-wiggum-loop.md` |
| HTML presentation | `session-03-lesson-3.17-ralph-wiggum-loop.html` |

---

## 5. Session Flow

### What Happened This Session

1. **Lesson URL shared** -- Student provided L3.17 URL (Ralph Wiggum Loop)
2. **Source fetched** -- Full lesson content retrieved from agentfactory.panaversity.org
3. **Vocabulary delivered** -- 7 key terms defined (Iteration Fatigue, Stop Hook, Completion Promise, Max Iterations, Loop Prompt, Embedded Promise Pattern, Ralph Loop)
4. **Core explanation** -- What/Why/How/Where it fits, full architecture diagram, four components
5. **Analogy** -- Night Shift Factory Supervisor (green flag = promise, 50 runs = max iterations, supervisor = loop)
6. **What Goes Wrong** -- Full four-axis analysis (Misapplication, Omission, Excess, Interaction Failure)
7. **"Try with AI" deep exploration** -- All 8 dimensions: friction, patterns, domains (CI/CD, robotics, business), failures, edges, adversarial, synthesis, strategic
8. **Comprehension Q1** -- "Why plugin not built-in?" -- Student chose "You explain" -- model answer delivered
9. **Comprehension Q2** -- False positive scenario (tests still failing after loop exits) -- Student partially answered (identified premature exit correctly) -- full model answer with 4 root causes delivered
10. **Hands-on exercises attempted** -- 3 prompt design exercises offered, student chose "You explain"
11. **Good vs Poor Use Cases deep dive requested** -- Student wanted deeper coverage of this section
12. **Source sections fetched** -- Retrieved specific #good-use-cases and #poor-use-cases sections
13. **Full use case analysis delivered** -- Each good/poor case dissected with hidden risks, edge cases, the gaming risk, convergent vs divergent distinction
14. **Decision tree delivered** -- 6-step flowchart for "should I use Ralph Loop?"
15. **More exercises requested** -- Student wanted hands-on exercises
16. **Exercise 1: Judgment Call** -- 6 scenarios (A-F) for Ralph Loop/Manual/Hybrid classification
17. **Exercise reframed for student's domain** -- All exercises rewritten for Python/FastAPI/Docker/Digital FTE context
18. **Exercise 3: Multi-Loop Campaign** -- Pydantic v1→v2 migration campaign design (4 loops)
19. **Exercise 4: FTE Builder Scenarios** -- 6 Digital FTE scenarios classified with reasoning
20. **Exercise 2: Prompt Surgery** -- 7 problems found in bad command, corrected version written
21. **End-of-session synthesis triggered** -- Student requested multiple .md files, 100% relevant info

### Key Moments

- **Domain context revealed**: Student disclosed they're building 24/7 Digital FTEs with Python/FastAPI/Docker. All future exercises should be framed in this context.
- **Partial answer on false positive Q**: Correctly identified premature exit as root cause but needed the full taxonomy (4 root causes). Shows good instinct, needs more practice on exhaustive failure analysis.
- **Multi-file revision notes requested**: Student explicitly asked for multiple .md files covering everything "to the optimum level" with "100% relevant info" -- no fluff.
- **Consistent "You explain" pattern**: Student continues to prefer model answers over attempting. Growth area carried forward.

---

## 6. Knowledge Graph -- What Was Learned

### Lesson 3.1: Claude Code Origin Story -- COMPLETE (Session 01)

```
CONCEPTS MASTERED:
├── Origin Story, Product Overhang, Adoption Stats
├── Passive vs Agentic Model, Two Interfaces
├── General vs Custom Agents, OODA Loop
├── Anti-Patterns (4), Trust Spectrum, Scaling Analysis
└── Edge Cases, Adversarial Analysis
```

### Lesson 3.18: The Creator's Workflow -- COMPLETE (Session 02)

```
CONCEPTS MASTERED:
├── Fundamental Constraint (context window)
├── Five Principles (Context, Parallelization, Plan Mode, Self-Evolving Docs, Verification)
├── Subagents (context isolation, permission routing, trust calibration)
├── Prompting (challenge prompts, elegant solution, detailed briefs)
├── Research & Data Analysis (NL interface, safety layers)
├── Skills for Workflow Automation
├── Supporting Practices (model selection, session mgmt, permissions, hooks, learning, voice)
└── Failure Patterns (Kitchen Sink, Correction Spiral, Over-Specified CLAUDE.md, etc.)
```

### Lesson 3.17: Ralph Wiggum Loop -- COMPLETE (Session 03)

```
CONCEPTS MASTERED:
├── Iteration Fatigue (3 hidden costs, ~10 iteration threshold)
├── Ralph Loop Architecture
│   ├── Stop Hook interception mechanism
│   ├── Completion Promise (static, exact match, immutable)
│   ├── Max Iterations (safety ceiling)
│   ├── Loop Prompt (continuation template)
│   └── Embedded Promise Pattern (recommended over natural tool output)
│
├── Good Use Cases (deeply analyzed)
│   ├── Framework upgrades (deterministic build output)
│   ├── Test-driven refactoring (BEST use case -- tests as specification)
│   ├── Linting/type error resolution (highest gaming risk)
│   └── Deployment debugging (riskiest -- external state)
│
├── Poor Use Cases (deeply analyzed)
│   ├── Human judgment tasks (subjective, no tool verification)
│   ├── Exploratory research (divergent, no done-state)
│   ├── Creative work (no ceiling, no objective measurement)
│   ├── Multi-goal tasks (single-promise bottleneck)
│   └── External input tasks (no pause-and-ask mechanism)
│
├── Convergent vs Divergent Task Distinction
│   └── Ralph Loop = convergent tasks only (error count → zero)
│
├── The Gaming Risk
│   ├── @ts-ignore, any, eslint-disable, deleting code, changing config
│   └── Anti-gaming prompt template
│
├── Decision Tree (6-step: tool-verifiable → single signal → >10 iterations → convergent → no human input needed → contained side effects)
│
├── Multi-Loop Campaign Design
│   ├── Bottom-up ordering (dependencies first)
│   ├── Scope isolation per loop
│   ├── Git checkpoints between loops
│   └── Pydantic v1→v2 example (4 loops)
│
├── Failure Scenarios (advanced)
│   ├── Cascading fix spiral (coupled errors oscillate)
│   ├── Scope creep accumulator (Claude "improves" beyond task)
│   ├── Silent corruption (technically passes, architecturally broken)
│   └── False positive taxonomy (4 root causes)
│
├── Edge Cases
│   ├── Promise string in source code
│   ├── Claude needs to ask mid-loop (no pause mechanism)
│   ├── 90% complete at max iterations (resumable with seam)
│   └── Concurrent loops on same files (race conditions)
│
├── Adversarial Analysis
│   ├── Malicious CLAUDE.md (exfiltration amplified by autonomy)
│   ├── Cost attack via vague task
│   └── Dependency injection via npm/pip install
│
├── Cross-Concept Synthesis
│   ├── Composability (CLAUDE.md + Hooks + Plugins = Ralph Loop)
│   ├── Escalating Autonomy Ladder (Level 0-5)
│   ├── Verification-Trust Inversion
│   ├── OODA mapping (all 4 steps automated)
│   └── Digital FTE connection (Ralph Loop = simplest FTE pattern)
│
├── Historical Context
│   ├── Geoffrey Huntley (creator, summer 2025)
│   ├── Boris Cherny (formalizer, late 2025)
│   ├── Plugin-not-built-in philosophy
│   └── 14-hour autonomous sessions
│
├── Cost Management
│   ├── $10-20 (simple), $20-50 (medium), $80-150 (complex)
│   ├── Always set max-iterations
│   └── Monitor every 15 min, cancel indicators
│
└── The FTE Builder's Rule
    ├── DESIGN decisions → Manual
    ├── MECHANICAL replication → Ralph Loop
    └── MIXED tasks → Hybrid

DOMAIN APPLICATION (mapped to student's stack):
├── CI/CD pipelines (Stop Hook = webhook, Promise = health check)
├── Robotics/control systems (closed-loop feedback)
├── Business process automation (exception-handling loops)
├── Docker dependency conflicts (Ralph Loop)
├── Pydantic migration (multi-loop campaign)
├── FastAPI rate limiting (manual -- design task)
├── Docker Compose config errors (Ralph Loop cautious)
└── Agent error responses (hybrid -- design once, replicate with loop)
```

---

## 7. Vocabulary Bank -- Terms Introduced

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
| **Iteration Fatigue** | **3.17** | **Yes** |
| **Stop Hook** | **3.17** | **Yes** |
| **Completion Promise** | **3.17** | **Yes** |
| **Max Iterations** | **3.17** | **Yes** |
| **Loop Prompt** | **3.17** | **Yes** |
| **Embedded Promise Pattern** | **3.17** | **Yes** |
| **Ralph Loop** | **3.17** | **Yes** |

---

## 8. Anti-Patterns Covered

### Fully Taught

| Anti-Pattern | Chapter | How Taught |
|-------------|---------|------------|
| Unverified Trust | 3.1 | Scenarios + trust spectrum |
| Monolithic Decomposition | 3.1 | "Build everything" failure |
| Staying Passive | 3.1 | Copy-paste vs agentic comparison |
| Over-Distrust | 3.1 | Developer rewriting all output |
| Kitchen Sink Session | 3.18 | Mixed tasks → context pollution |
| Correction Spiral | 3.18 | Failed approaches poisoning context |
| Over-Specified CLAUDE.md | 3.18 | Signal buried in noise |
| Trust-Then-Verify Gap | 3.18 | No feedback loops |
| Infinite Exploration | 3.18 | Unbounded investigation |
| **Ralph Loop Misapplication** | **3.17** | **Subjective tasks, divergent tasks, multi-goal tasks** |
| **Missing Guardrails** | **3.17** | **No max-iterations, no checkpoint, vague promise** |
| **Over-Reliance on Autonomy** | **3.17** | **Overnight runs, small tasks, multi-goal in one loop** |
| **Gaming/Silent Corruption** | **3.17** | **@ts-ignore, any type, eslint-disable shortcuts** |
| **Cascading Fix Spiral** | **3.17** | **Coupled errors oscillating across iterations** |
| **Scope Creep in Loops** | **3.17** | **Claude "improving" beyond the task scope** |

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

3. OODA Diagnostic:
   Wrong output → ORIENT | Missing info → OBSERVE | Blocked → ACT | Wrong strategy → DECIDE

4. Trust Spectrum:
   Over-distrust (typist) <-- Balanced (orchestrator) --> Blind trust (dangerous)

5. Scaling:
   Copy-paste: O(n²) | Agentic: O(1) human, O(log n) agent

6. "What Goes Wrong" (4 Lenses):
   Misapplication | Omission | Excess | Interaction Failure

-- FROM SESSION 02 --

7. The Fundamental Constraint:
   Context window fills → Performance degrades → Every practice manages this

8. Five Principles of the Creator's Workflow:
   Context | Parallelization | Plan Mode | Self-Evolving Docs | Verification

9. Context Window Lifecycle:
   Fresh (0%) → Productive (~30%) → Degrading (~70%) → Polluted (~90%+)

10. Plan Mode Economics:
    Planning tokens (cheap) << Correction tokens (expensive)

11. Self-Writing Compound Interest:
    Each 30-second CLAUDE.md update prevents same error × N future sessions

12. Subagent Context Savings:
    Main context cost = summary lines only, not raw file reads

13. Specificity Equation:
    Vague (1 min + 4 corrections = 21 min) vs Specific (5 min + 0 = 5 min)

14. Right Slow > Wrong Fast:
    Total task time = response time × iteration count

15. Product Overhang for Data:
    Existing Data + Missing NL Interface = Democratized Access

16. Trust Calibration for Subagents:
    Low stakes → trust | Medium → verify key refs | High → verify everything

17. Notes/ Three-Zone Strategy:
    Zone 1: CLAUDE.md index | Zone 2: specific file (on-demand) | Zone 3: irrelevant (0 tokens)

18. Team Compounding:
    Individual (notes/): linear growth | Team (@.claude): multiplied by team size

-- FROM SESSION 03 --

19. Ralph Loop Selection Principle:
    Success must be measurable by automated tools, not human judgment

20. Convergent vs Divergent Tasks:
    Convergent (errors → 0) = loop-able | Divergent (scope expands) = manual only

21. Escalating Autonomy Ladder:
    Basic (L0) → CLAUDE.md (L1) → Skills (L2) → Hooks (L3) → Ralph Loop (L4) → Agent Teams (L5)

22. Verification-Trust Inversion:
    More autonomy → more critical verification criteria

23. The FTE Builder's Rule:
    DESIGN → Manual | MECHANICAL → Ralph Loop | MIXED → Hybrid

24. Multi-Loop Campaign Pattern:
    Bottom-up order + scope isolation + git checkpoints + specific tests per loop

25. Anti-Gaming Prompt Design:
    Explicit constraints on what NOT to do (no @ts-ignore, no any, no deleting, no config changes)

26. Composability Principle:
    Independent capabilities (CLAUDE.md + Hooks + Plugins) combine into emergent capability (Ralph Loop)
```

---

## 10. Student Strengths & Growth Areas

### Strengths

- **Recall**: Correctly remembered adoption stats (Session 1)
- **Core concepts**: Immediately grasped "chatbot answers, agent acts" (Session 1)
- **Trust analysis**: Identified Over-Distrust anti-pattern correctly (Session 1)
- **Quality demand**: Won't accept shallow teaching; corrected Professor Agent in Sessions 1 and 2
- **Pattern recognition**: Correctly identified notes/ pointer mechanism (Session 2)
- **Content vigilance**: Caught rushing through sections (Session 2)
- **Failure analysis instinct**: Correctly identified "premature exit / false positive" as first root cause (Session 3)
- **Domain clarity**: Clearly articulated their FTE-building context and requested domain-specific framing (Session 3)
- **Quality standards for revision materials**: Explicitly requested comprehensive, multi-file, no-fluff revision notes (Session 3)

### Growth Areas

- **Articulating strategic analysis**: Consistently requests model answers on open-ended questions. Needs gradual push toward attempting. (All 3 sessions)
- **Exhaustive failure analysis**: Identified one root cause correctly but needed the full taxonomy of four. Practice on "list ALL possible causes" type questions. (Session 3)
- **Architectural depth**: Partial answers on system design questions. Right direction but missing deeper implications. (Sessions 2 and 3)

---

## 11. Collaboration Style & Tone

### Rules

- **Be direct.** No filler.
- **Be deep.** Full depth always. Student rejected shallow teaching TWICE.
- **Be structured.** Tables, ASCII diagrams, clear headers.
- **Be honest.** If answer is incomplete, say so.
- **Respect "answer" requests.** Deliver full model answer without re-prompting.
- **Push strategically.** Challenge via AskUserQuestion.
- **No emojis** unless requested.
- **Fetch source URLs** when shared.
- **Create multiple revision files** after every lesson. 100% relevant info, no fluff.
- **Cover EVERY section.** Never rush. Full "Try with AI" on every section.
- **Frame exercises in student's domain.** Python, FastAPI, Docker, Digital FTEs.

### Student Intent Signals

| They Say | They Mean |
|----------|----------|
| "answer" / "you explain" | Deliver model answer now |
| "I need a hint" | Nudge, not full answer |
| "Let me type" | They'll attempt -- wait |
| Shares a URL | Fetch and align with source |
| "quiz me" / "quiz me hard" | Challenging questions via AskUserQuestion |
| Pushes back on approach | Adjust immediately |
| "move" / "move to the rest" | Continue with remaining content |
| Calls out missed content | Go back and cover fully |
| "End" | Execute end-of-session synthesis protocol |
| Requests domain-specific framing | Use Python/FastAPI/Docker/FTE examples |

---

## 12. Repository Structure

```
Agent-Factory-Part 1-test-prep/
├── CLAUDE.md
├── Knowledge_Vault/
│   ├── Curriculum/
│   ├── Pedagogy/
│   ├── Vocabulary/
│   ├── Protocols/
│   ├── Frameworks/
│   ├── Student/
│   └── Capabilities/
├── context-bridge/
│   ├── session-01-lesson-3.1-origin-story.md
│   ├── session-02-lesson-3.18-creators-workflow.md
│   └── session-03-lesson-3.17-ralph-wiggum-loop.md       <- THIS FILE
├── revision-notes/
│   └── ch3-general-agents-claude-code-cowork/
│       ├── 3.1-claude-code-origin-story.md
│       ├── 3.18-creators-workflow.md
│       ├── 3.17-ralph-wiggum-loop-core.md                 <- NEW
│       ├── 3.17-ralph-wiggum-loop-use-cases.md            <- NEW
│       ├── 3.17-ralph-wiggum-loop-deep-exploration.md     <- NEW
│       └── 3.17-ralph-wiggum-loop-exercises.md            <- NEW
├── visual-presentations/
│   ├── session-02-lesson-3.18-creators-workflow.html
│   └── session-03-lesson-3.17-ralph-wiggum-loop.html      <- NEW
├── quiz-bank/
├── exercises/
└── progress-tracking/
```

---

## 13. Next Steps

### Immediate Next

- **Student to choose next lesson**
- Apply full TEACH cycle + "Try with AI" proactive framework
- Cover EVERY section with full depth
- Frame exercises in Python/FastAPI/Docker/FTE context
- Create multiple .md revision files per lesson

### Lessons Completed So Far

```
3.1   Claude Code Origin Story                         <- COMPLETE (Session 01)
3.18  The Creator's Workflow: Best Practices            <- COMPLETE (Session 02)
3.17  Ralph Wiggum Loop: Autonomous Iteration Workflows <- COMPLETE (Session 03)
```

### Module D Remaining (Autonomous Workflows)

```
3.19  Plugins Exercises (15 hands-on exercises)
3.20  Agent Teams (multiple Claude sessions coordinating)
3.21  Agent Teams Exercises
```

### Open Questions

- Will you cover Chapters 1-2 at any point, or stay focused on Chapter 3?
- Which lesson next: continue Module D (3.19/3.20) or jump elsewhere?
- Should we create a PROGRESS.md tracker?

---

## 14. How to Use This File

1. Start a new session with Professor Agent
2. Share this file at the beginning
3. Say: **"Load context bridge and continue from where we left off"**
4. Professor Agent will:
   - Recognize all established patterns and protocols
   - Know your learning style and preferences
   - Know your tech stack (Python, FastAPI, Docker, Digital FTEs)
   - Resume at your chosen lesson
   - Apply the full TEACH cycle + "Try with AI" framework on EVERY section
   - Use AskUserQuestion for all questions
   - Create multiple revision files per lesson (100% relevant, no fluff)
   - Frame exercises in your domain
   - Execute End protocol when triggered

---

*Session 03 complete | 2026-02-18 | Lesson 3.17 done | Next: Student's choice*
