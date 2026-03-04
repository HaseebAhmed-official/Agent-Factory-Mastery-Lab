# Session 01 -- Lesson 3.1: Claude Code Origin Story

> **Date**: 2026-02-16
> **Lesson Covered**: Chapter 3, Lesson 3.1 -- Claude Code Origin Story
> **Student Status**: Lesson 3.1 COMPLETE | Next: Lesson 3.2
> **Source URL**: https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/origin-story

---

## Table of Contents

1. [Project Essence](#1-project-essence)
2. [Student Profile & Learning DNA](#2-student-profile--learning-dna)
3. [Established Teaching Patterns](#3-established-teaching-patterns)
4. [Key Technical Decisions](#4-key-technical-decisions)
5. [Session Flow](#5-session-flow)
6. [Knowledge Graph -- What Was Learned](#6-knowledge-graph--what-was-learned)
7. [Vocabulary Bank -- Terms Introduced](#7-vocabulary-bank--terms-introduced)
8. [Anti-Patterns Covered](#8-anti-patterns-covered)
9. [Frameworks & Mental Models Internalized](#9-frameworks--mental-models-internalized)
10. [Student Strengths & Growth Areas](#10-student-strengths--growth-areas)
11. [Collaboration Style & Tone](#11-collaboration-style--tone)
12. [Repository Structure](#12-repository-structure)
13. [Next Steps](#13-next-steps)
14. [How to Use This File](#14-how-to-use-this-file)

---

## 1. Project Essence

### What This Is

A structured study system for mastering the Panaversity course **"Agent Factory Part 1: General Agents Foundations" (AIAF-2026)**. The AI tutor operates as **Professor Agent** following the CLAUDE.md system prompt that defines the full curriculum, teaching methodology (TEACH cycle), and exam coaching protocols.

### The Student's Goal

Not just to pass a test -- but to become a **problem solver, strategic thinker, and orchestrator** who can:
- Apply frameworks to novel situations
- Identify anti-patterns in real scenarios
- Make sound architectural decisions about AI agent deployment
- Think like an engineer, not a memorizer

### The Course Scope

6 chapters, 60+ lessons covering:
- Ch 1: The AI Agent Factory Paradigm
- Ch 2: Markdown -- Writing Instructions
- Ch 3: General Agents -- Claude Code & Cowork (32 lessons) ← **CURRENT**
- Ch 4: Effective Context Engineering
- Ch 5: Spec-Driven Development with Claude Code
- Ch 6: The Seven Principles of General Agent Problem Solving

---

## 2. Student Profile & Learning DNA

### Background

- **Level**: Intermediate. Has used ChatGPT and Claude conversationally. Done basic prompt engineering. New to agentic AI, agent development, and the Agent Factory framework.
- **Language**: English only
- **Access**: May not have paid Claude Code subscription -- exercises should accommodate free backends (OpenRouter, Gemini, DeepSeek)

### How This Student Learns Best

- Needs **all jargon pre-defined** before it's used
- Benefits from **concrete examples** over abstract theory
- Wants to be **challenged deeply** -- not given shallow multiple-choice
- Responds well to **structured feedback** (what you got right → what to add → complete answer)
- Prefers the AI to **give full model answers** when they say "answer" or "you explain"
- Wants **hands-on exercises, edge cases, failure modes, adversarial thinking** as default

### Behavioral Patterns Observed

| Pattern | What It Means | How to Respond |
|---------|--------------|----------------|
| Says "answer" or "you explain" | Wants the model answer delivered | Provide the deep answer, note value of attempting |
| Says "yes" to multiple questions | Wants to move fast past basics | Respect pace, focus depth on concepts |
| Pushes back on shallow teaching | Deeply values rigor | Always deliver the full framework -- no shortcuts |
| Asks creative strategic questions | Genuinely engaged | Match the depth and creativity of their question |
| Shares lesson URLs | Wants teaching aligned with course material | Always fetch and integrate the source content |

### Critical Student Instruction (Binding)

> "I want to be a problem solver, strategic thinker, orchestrator and want hands-on and want to learn edge cases and all other things written in your CLAUDE.md but you did not follow it."

**This was a course correction.** The student explicitly demanded the full CLAUDE.md methodology. This is a binding instruction for ALL future sessions.

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

### Question & Quiz Protocol

- **ALWAYS use AskUserQuestion tool** for all comprehension checks, quizzes, and questions
- Use **open-ended explain-back questions** (not shallow multiple-choice)
- Question types: Explain-Back, Application, Failure Analysis, Compare-Contrast, Edge Case, Strategic
- After answers: structured feedback (What you got right → What to add → Complete answer → Why it matters)

### Revision File Protocol

- After each lesson, create a detailed `.md` revision file
- Naming: `{lesson-number}-{kebab-case-title}.md`
- Location: `revision-notes/ch{N}-{chapter-name}/`

### Source Material Protocol

- When student shares a lesson URL, **always fetch and integrate**
- Supplement with deeper analysis but never contradict the source

---

## 4. Key Technical Decisions

### File & Directory Conventions

| Decision | Choice |
|----------|--------|
| Revision file naming | `3.1-claude-code-origin-story.md` |
| Chapter directory naming | `ch3-general-agents-claude-code-cowork/` |
| Session context naming | `session-01-lesson-3.1-origin-story.md` |
| Monorepo approach | Single repo with organized subdirectories |

---

## 5. Session Flow

### What Happened This Session

1. **Greeting & Orientation** -- Student said `start`
2. **Diagnostic Questions** -- Student answered "yes" to all
3. **Chapter Selection** -- Student chose Chapter 3 (skipping Ch 1-2 for now)
4. **Lesson 3.1 Initial Delivery** -- Vocabulary, explanation, analogy, basic questions
5. **COURSE CORRECTION** -- Student called out shallow teaching, demanded full CLAUDE.md adherence
6. **Lesson 3.1 Re-delivered at Full Depth:**
   - Deep OODA loop analysis with failure modes
   - OODA diagnostic exercise (3 scenarios -- student scored 2/3)
   - Source URL fetched and integrated (Boris Cherny story, adoption stats)
   - Detailed ChatGPT vs Claude Code debugging workflow comparison
   - O(n²) vs O(1) scaling analysis
   - Three future Product Overhang examples
   - Adversarial analysis on filesystem safety
   - 5-question hard quiz
7. **"Try with AI" Framework Established** -- Student requested proactive deep exploration as default
8. **Revision File Created** -- `3.1-claude-code-origin-story.md`
9. **Context Bridge Requested** -- This file

### Key Moments

- **Strongest moment**: Correctly identified that missing tests break the OODA loop at Observe
- **Growth edge**: Tends to request model answers on strategic/edge case questions rather than attempting
- **Teaching correction**: Professor Agent was initially too shallow. Student corrected. Now at full depth.

---

## 6. Knowledge Graph -- What Was Learned

### Lesson 3.1: Claude Code Origin Story -- COMPLETE

```
CONCEPTS MASTERED:
├── Origin Story (Boris Cherny, Sept 2024, filesystem experiment)
├── Product Overhang (capability + missing interface = unlock)
├── Adoption Stats (20%→50%→80%, 5 PRs/day, 90% self-written)
├── Passive vs Agentic Model (chatbot vs agent, execution vs judgment)
├── Two Interfaces (Claude Code terminal vs Cowork desktop)
├── General vs Custom Agents (factory vs product)
├── OODA Loop (Observe→Orient→Decide→Act, autonomous cycling)
├── OODA as Diagnostic Tool (which step broke?)
├── Agent Skills preview (encoded expertise, SKILL.md)
├── Anti-Patterns (Unverified Trust, Monolithic Decomposition, Staying Passive, Over-Distrust)
├── Trust Spectrum (no trust ← balanced → blind trust)
├── Scaling Analysis (O(n²) copy-paste vs O(1) agentic)
├── Product Overhang Pattern Recognition (3 future examples)
├── Edge Cases (when chatbot wins: security, air-gap, learning, quick questions)
└── Adversarial Analysis (filesystem danger: valid concerns + counter-arguments)

CONCEPTS FROM CH1/CH2 INTRODUCED INLINE:
├── Agent Maturity Model (General → Custom)
├── Five Powers (See, Hear, Reason, Act, Remember)
├── Three LLM Constraints (Statelessness, Probabilistic, Context Window) -- mentioned
├── OODA Loop (full framework)
├── Orchestrator role
├── Small Reversible Decomposition (Chapter 6 preview)
├── Verification as Core Step (Chapter 6 preview)
└── Constraints and Safety (Chapter 6 preview)
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

---

## 8. Anti-Patterns Covered

### Fully Taught

| Anti-Pattern | Chapter | How Taught |
|-------------|---------|------------|
| Unverified Trust | 3.1 | Scenarios + trust spectrum |
| Monolithic Decomposition | 3.1 | "Build everything" failure |
| Staying Passive | 3.1 | Copy-paste vs agentic comparison |
| Over-Distrust | 3.1 | Developer rewriting all output |

### Mentioned But Not Yet Fully Taught

Premature Specialization, Perpetual Incubation, Skipping Incubation (Ch.1), Vibe Coding (Ch.5), Context Stuffing, Context Starvation, Workflow Drift (Ch.4)

---

## 9. Frameworks & Mental Models Internalized

```
1. Product Overhang Formula:
   Existing Capability + Missing Interface = Massive Unlock

2. Agentic Success Requirements:
   Filesystem Access + Test Suite + Small Steps + Human Review = Success
   Remove ANY one = Failure

3. OODA Diagnostic:
   Wrong output → ORIENT | Missing info → OBSERVE | Blocked → ACT | Wrong strategy → DECIDE

4. Trust Spectrum:
   Over-distrust (typist) ←── Balanced (orchestrator) ──→ Blind trust (dangerous)

5. Scaling:
   Copy-paste: O(n) to O(n²) | Agentic: O(1) human, O(log n) agent

6. "What Goes Wrong" (4 Lenses):
   Misapplication | Omission | Excess | Interaction Failure
```

---

## 10. Student Strengths & Growth Areas

### Strengths

- **Recall**: Correctly remembered adoption stats
- **Core concepts**: Immediately grasped "chatbot answers, agent acts"
- **Trust analysis**: Identified Over-Distrust anti-pattern correctly
- **OODA application**: 2/3 on diagnostic scenarios
- **Strategic curiosity**: Independently asked about future Product Overhangs
- **Quality demand**: Won't accept shallow teaching

### Growth Areas

- **Articulating strategic analysis**: Tends to request answers on open-ended questions -- needs gradual push toward attempting
- **Observe vs Orient distinction**: Missed nuance in OODA Scenario A -- reinforce in future lessons
- **Edge case generation**: Needs more scaffolded practice (hints → attempt → model answer)

---

## 11. Collaboration Style & Tone

### Rules

- **Be direct.** No filler.
- **Be deep.** Full depth always. Student rejected shallow teaching.
- **Be structured.** Tables, ASCII diagrams, clear headers.
- **Be honest.** If answer is incomplete, say so. Give complete version.
- **Respect "answer" requests.** Deliver full model answer without re-prompting.
- **Push strategically.** Challenge on their terms via AskUserQuestion.
- **No emojis** unless requested.
- **Fetch source URLs** when shared.
- **Create revision files** after every lesson.

### Student Intent Signals

| They Say | They Mean |
|----------|----------|
| "answer" / "you explain" / "you give" | Deliver model answer now |
| "I need a hint" | Nudge, not full answer |
| "Let me type" | They'll attempt -- wait |
| Shares a URL | Fetch and align with source |
| "quiz me" / "quiz me hard" | Challenging questions via AskUserQuestion |
| Pushes back on approach | Adjust immediately |

---

## 12. Repository Structure

```
Agent-Factory-Part 1-test-prep/              ← ROOT (monorepo)
│
├── CLAUDE.md                                ← System prompt (Professor Agent)
│
├── context-bridge/                          ← Session continuity
│   ├── session-01-lesson-3.1-origin-story.md    ← THIS FILE
│   ├── session-02-lesson-3.2-installing.md      ← (future)
│   └── ...
│
├── revision-notes/                          ← Per-lesson revision guides
│   ├── ch1-ai-agent-factory-paradigm/
│   ├── ch2-markdown-writing-instructions/
│   ├── ch3-general-agents-claude-code-cowork/
│   │   ├── 3.1-claude-code-origin-story.md      ← DONE
│   │   ├── 3.2-installing-authenticating.md     ← (next)
│   │   └── ...
│   ├── ch4-effective-context-engineering/
│   ├── ch5-spec-driven-development/
│   └── ch6-seven-principles/
│
├── quiz-bank/                               ← Accumulated quiz questions
│   └── ch3-quiz-bank.md                     ← (future)
│
├── exercises/                               ← Hands-on exercises & solutions
│   └── ch3-exercises/                       ← (future)
│
└── progress-tracking/                       ← Curriculum progress
    └── PROGRESS.md                          ← (future)
```

---

## 13. Next Steps

### Immediate Next

- **Lesson 3.2: Installing and Authenticating Claude Code**
- Student should share the lesson URL if available
- Apply full TEACH cycle + "Try with AI" proactive framework

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

---

## 14. How to Use This File

1. Start a new session with Professor Agent
2. Share this file at the beginning
3. Say: **"Load context bridge and continue from where we left off"**
4. Professor Agent will:
   - Recognize all established patterns and protocols
   - Know your learning style and preferences
   - Resume at Lesson 3.2
   - Apply the full TEACH cycle + "Try with AI" framework
   - Use AskUserQuestion for all questions
   - Create revision files after each lesson

---

*Session 01 complete | 2026-02-16 | Lesson 3.1 done | Next: Lesson 3.2*
