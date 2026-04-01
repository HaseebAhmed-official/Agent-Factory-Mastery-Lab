# Teaching Commands Reference

Commands typed in the Claude Code chat window to drive your lesson sessions. These control what the agent teaches, how fast it goes, how deep it digs, and how it responds to your understanding.

---

## Quick Reference

| Command | One-Line Description |
|---------|----------------------|
| `start` / `begin` | Start from Chapter 1, Lesson 1 |
| `Teach me Chapter X` | Start teaching from the beginning of a chapter |
| `lesson X.Y` | Jump directly to a specific lesson |
| `continue` | Resume from where you left off |
| `Next` | Advance to the next concept in the current lesson |
| `I understand, move on` | Signal readiness to proceed |
| `Go slower` / `simplify` | Re-explain with simpler terms and a new analogy |
| `go deeper` | Add more depth, edge cases, and advanced detail |
| `Give me another example` / `exercise` | Get an additional practice exercise |
| `explain [term]` | Full explanation of any vocabulary term |
| `connect [A] to [B]` | Explain the relationship between two concepts |
| `show connections` | Show how the current topic connects to all other chapters |
| `anti-patterns` | List all anti-patterns relevant to the current chapter |

---

## Background: What Happens During Teaching

Every teaching response follows the **TEACH cycle**. Understanding it helps you use the commands below more effectively.

| Step | What It Means |
|------|---------------|
| **T — Terminology First** | Every term is defined before it is used |
| **E — Explain with Depth** | What it is / Why it matters / How it works / Where it fits / What can go wrong |
| **A — Analogize and Visualize** | Real-world analogy + ASCII diagram or table |
| **C — Check Understanding** | Open-ended question (never yes/no) — agent waits for your answer |
| **H — Hands-On Practice** | Immediately executable exercise with expected output |

The agent will not skip steps. If you want to skip straight to practice, use `exercise`. If you want to skip the check and move on, use `Next` or `I understand, move on`.

---

## Starting Commands

---

### `start` / `begin`

**Syntax**: `start` or `begin` (case-insensitive)

**What it does**: Triggers a fresh lesson session beginning at Chapter 1, Lesson 1. The agent runs the Cold-Start Recovery Protocol first (reads `context-bridge/status.json`), then greets you and begins teaching from the very beginning of the curriculum.

**When to use it**: First time ever using the system, or when you want to restart from scratch regardless of any saved progress.

**What the agent does in response**:
1. Checks `context-bridge/status.json` for existing progress
2. If progress is found, warns you before overriding (offers to `Resume` instead)
3. If no progress (or you confirm), loads Chapter 1 curriculum module
4. Delivers the lesson opening using the TEACH cycle — starting with Terminology

**Example**:

```
You: start

Agent:
──────────────────────────────────────────────
📍 Cold-start check complete — no prior session found.
──────────────────────────────────────────────

Welcome to Agent Factory Part 1. We're starting from Chapter 1, Lesson 1.

**Lesson 1.1 — What Is an Agent?**

Before we dive in, let's define our first term:

**Agent** — A software entity that perceives its environment, makes decisions,
and takes actions to achieve a goal. Unlike a simple function that runs once
and returns, an agent loops: observe → decide → act → observe again.

Think of it like a thermostat, but one that can read email, call APIs,
and write code...
```

**Notes**:
- If a session is already in progress (bridge file exists), the agent will ask whether you want to resume or start fresh — it will not silently overwrite your progress.
- `begin` is an exact alias for `start`. Either works.

---

### `Teach me Chapter X`

**Syntax**: `Teach me Chapter 1`, `Teach me Chapter 3`, etc. (number is required)

**What it does**: Begins teaching from Lesson 1 of the specified chapter. Useful when you want to skip ahead to a chapter without knowing the exact lesson number.

**When to use it**: When you've already finished earlier chapters and want to jump to a new chapter, or when you want to revisit an entire chapter from its beginning.

**What the agent does in response**:
1. Loads the curriculum module for that chapter from `Knowledge_Vault/Curriculum/chapter-{N}-*.md`
2. Identifies the first lesson of the chapter
3. Begins the TEACH cycle for that lesson, starting with chapter-level context (what this chapter covers, how it connects to prior chapters)

**Example**:

```
You: Teach me Chapter 3

Agent:
Chapter 3 focuses on Hook Architecture — one of the most critical patterns
in the Agent Factory system. Before we begin Lesson 3.1, let me orient you:

What you already know (from Chapters 1–2):
- What agents are and why they matter
- The basic loop: observe → decide → act

What Chapter 3 adds:
- How to intercept and modify agent behavior at runtime
- The hook lifecycle and event system
- Composing hooks without conflicts

Starting with Lesson 3.1: Hook Fundamentals...
```

**Notes**:
- Chapter numbers must be valid (1–6). If you specify a chapter that doesn't exist, the agent will tell you the valid range.
- If you are mid-lesson in a prior chapter, the agent may ask whether you want to `Checkpoint` first before jumping.

---

### `lesson X.Y`

**Syntax**: `lesson 3.1`, `lesson 2.4`, `lesson 5.12` — chapter number dot lesson number

**What it does**: Jumps directly to a specific lesson anywhere in the curriculum. The agent immediately loads that lesson's curriculum module and begins teaching from its first concept.

**When to use it**: When you know exactly which lesson you want. Useful for targeted review, picking up after a break, or skipping to a specific topic.

**What the agent does in response**:
1. Parses the chapter and lesson numbers
2. Fetches `Knowledge_Vault/Curriculum/chapter-{N}-*.md` and navigates to that lesson
3. Provides a brief context bridge ("In prior lessons you learned X — this lesson builds on that")
4. Starts the TEACH cycle for the first concept of that lesson

**Example**:

```
You: lesson 3.17

Agent:
──────────────────────────────────────────────
Jumping to Lesson 3.17 — Orchestration Patterns
──────────────────────────────────────────────

Context: By now you've covered Hook Architecture (3.1–3.16), including the
hook lifecycle, event system, and composition rules. Lesson 3.17 introduces
orchestration: how multiple hooks coordinate to produce emergent behavior.

First term we need:

**Orchestration Pattern** — A design strategy that governs how two or more
hooks interact when handling the same event...
```

**Notes**:
- If you jump to a lesson that references vocabulary from earlier lessons and those terms are already in your vocabulary bank (≥2 lessons), the agent will test recall rather than re-explain — this is intentional scaffold-fade behavior (see the Scaffold-Fade section below).
- You can combine with `Checkpoint` before jumping if you want to save your current position first.

---

## Continuation Commands

---

### `continue`

**Syntax**: `continue` (case-insensitive)

**What it does**: Resumes teaching from exactly where the last session ended. The agent reads the context bridge (`context-bridge/master-cumulative.md` and `context-bridge/status.json`) to determine the last lesson, layer, and concept, then picks up from there.

**When to use it**: After reopening Claude Code following a previous session. This is the standard "I'm back, let's keep going" command.

**What the agent does in response**:
1. Reads `context-bridge/status.json` for instant state (lesson, layer, last concept)
2. Loads `context-bridge/master-cumulative.md` for full context
3. Displays a brief recovery banner showing where you left off
4. Resumes the lesson from the next concept after the last checkpoint

**Example**:

```
You: continue

Agent:
──────────────────────────────────────────────
Resuming Session
Last saved: Lesson 3.17, Checkpoint L2 — Orchestration Patterns
Concepts covered so far this lesson: hook-event-dispatch, listener-chains
──────────────────────────────────────────────

Picking up where we left off. You've covered how listeners chain when
an event fires. Next up: conflict resolution when two listeners claim
the same event priority...
```

**Notes**:
- If no context bridge exists, the agent will tell you there's nothing to resume and offer to `start` instead.
- `continue` is distinct from `Resume` — `continue` is casual and used mid-flow; `Resume` is the formal protocol command that runs full Cold-Start Recovery. Both end up at the same place, but `Resume` does more verification work.

---

### `Next`

**Syntax**: `Next` (capital N is conventional but not required)

**What it does**: Advances to the next concept within the current lesson. Skips the current concept's Check Understanding step if the agent is waiting for your answer, or advances from the current concept to the next if you've already answered.

**When to use it**: When you feel solid on the current concept and want to move forward without completing the full check. Or when the agent has posed its understanding question and you want to skip answering.

**What the agent does in response**:
1. Acknowledges the skip (no judgment)
2. Marks the current concept as "passed / skipped" in session state
3. Loads the next concept in the lesson sequence
4. Begins the TEACH cycle for that concept

**Example**:

```
Agent (mid-lesson):
Before we continue, I want to check your understanding:
"In your own words, what is the difference between a hook and a middleware?"

You: Next

Agent:
Got it — moving on.

Next concept: **Hook Priorities**
When multiple hooks respond to the same event, priority determines
execution order...
```

**Notes**:
- Using `Next` frequently means your mastery gates are being skipped. The agent tracks this. At `Finish` time, skipped concepts are flagged in the synthesis output so you know what to review.
- `Next` does not trigger a checkpoint. Use `Checkpoint` if you also want to save progress.

---

### `I understand, move on`

**Syntax**: Exact phrase or close variants (e.g., "I get it, move on", "understood, continue")

**What it does**: Signals explicit readiness to proceed after an explanation. Functionally similar to `Next` but communicates confidence rather than a skip. The agent treats this as a soft mastery pass and advances.

**When to use it**: After reading an explanation and feeling genuinely confident before the agent has asked its check question, or after a question you chose not to answer formally.

**What the agent does in response**:
1. Acknowledges your signal
2. Optionally asks one quick confirming question if the concept is marked as critical in the curriculum (flagged concepts require at least a brief check)
3. For non-critical concepts: advances immediately to the next concept

**Example**:

```
Agent: ...and that's how the event dispatcher routes to registered listeners.

You: I understand, move on

Agent:
Great. Next: **Priority Conflicts** — what happens when two listeners
register at the same priority level for the same event...
```

**Notes**:
- For concepts flagged as critical in the curriculum, the agent may still ask one quick question before advancing. This is intentional and cannot be overridden by this command — use `Next` if you want a hard skip.

---

## Pacing Commands

---

### `Go slower` / `simplify`

**Syntax**: `Go slower`, `simplify`, `slow down`, `that's too fast` (all recognized)

**What it does**: Triggers a full re-explanation of the current concept using a completely different approach — new analogy, simpler vocabulary, more broken-down steps. This is **not** a repeat. The agent must use a different teaching angle.

**When to use it**: When an explanation felt too abstract, used unfamiliar terms, or moved through too many ideas at once. Use it as many times as needed on the same concept.

**What the agent does in response**:
1. Acknowledges the request
2. Selects a different analogy and entry point for the same concept
3. Re-delivers the E and A steps of the TEACH cycle (Explain + Analogize) using simpler language
4. Re-issues the Check Understanding question at the end

**Example**:

```
Agent:
The hook lifecycle consists of pre-execution, execution, and post-execution
phases, each with its own event envelope and context mutation rules...

You: Go slower

Agent:
Let me try a different angle.

Imagine you're a security guard at a concert venue. Every person who
enters goes through three checkpoints:
  1. Before they reach the gate (pre-execution) — you can turn them away
  2. At the gate (execution) — you scan their ticket
  3. After they've passed (post-execution) — you log who entered

A hook is just code that runs at one of those three checkpoints.
Pre = intercept before. Post = observe after. That's the whole lifecycle.

Does that make more sense? Tell me what you think the "pre-execution" phase
is responsible for in your own words.
```

**Notes**:
- Each call to `Go slower` uses a fresh analogy. The agent does not repeat its previous explanation.
- If you use `Go slower` three times on the same concept and still aren't confident, the mastery gate loop cap activates — the agent flags `⚠️ NEEDS REVIEW` and allows continuation. See the Mastery Gate section below.

---

### `go deeper`

**Syntax**: `go deeper`, `more depth`, `advanced detail`, `tell me more` (all recognized)

**What it does**: Expands the current concept with edge cases, failure modes, advanced implementation detail, and connections to adjacent concepts. Assumes you've grasped the fundamentals and want to go further.

**When to use it**: When the base explanation clicked but you want to understand the full picture — including what can go wrong and how experts think about the topic.

**What the agent does in response**:
1. Confirms you've grasped the base concept (brief acknowledgment)
2. Adds the "What Goes Wrong" framework (Misapplication, Omission, Excess, Interaction Failure)
3. Covers edge cases and non-obvious behavior
4. Optionally adds an advanced exercise that tests the deeper understanding

**Example**:

```
You: go deeper

Agent:
Good — you've got the hook lifecycle down. Let's go deeper.

**What Goes Wrong (Four Failure Modes)**

| Failure Mode | What It Looks Like | Example |
|---|---|---|
| Misapplication | Using post-execution to block events | Blocking after the action already ran |
| Omission | Forgetting to call `next()` | Hook silently swallows all events |
| Excess | Registering identical hooks twice | Double side-effects on every event |
| Interaction Failure | Two hooks mutating the same context key | Last-write-wins, first hook's changes lost |

**Edge Case: Re-entrant hooks**
What happens if a hook fires an event that triggers the same hook?
By default: stack overflow. The fix is a re-entrancy guard...
```

**Notes**:
- `go deeper` is additive — it does not replace the previous explanation, it builds on it.
- You can chain `go deeper` calls on the same topic. Each call adds another layer.
- After `go deeper`, the mastery gate check will be harder — expect application-level or failure-analysis questions.

---

## Practice Commands

---

### `Give me another example` / `exercise`

**Syntax**: `Give me another example`, `exercise`, `practice`, `give me an exercise` (all recognized)

**What it does**: Provides an additional practice exercise on the current concept. The exercise is different from any previously given in the session and comes with expected output so you can self-check.

**When to use it**: After the built-in H step (Hands-On Practice) in the TEACH cycle, when you want more repetition before moving on. Also useful if the first exercise felt too abstract.

**What the agent does in response**:
1. Selects a practice exercise not yet used this session
2. States the scenario and what you should try to produce
3. Lists the expected outcome explicitly so you can check yourself
4. Waits — does not give the answer until you attempt it

**Example**:

```
You: Give me another example

Agent:
Here's another exercise on hook composition:

**Scenario**: You have two hooks: `auth-hook` (checks credentials) and
`rate-limit-hook` (limits requests per minute). Both run on the `request`
event.

**Task**: Write the registration calls that ensure auth always runs before
rate limiting. Then write what happens if auth fails — does rate-limit
still run?

**Expected outcome**:
- `auth-hook` registered with priority 10
- `rate-limit-hook` registered with priority 20 (higher number = later)
- If auth returns `reject`, the event chain stops — rate-limit never executes

Try it out, then share what you wrote.
```

**Notes**:
- The agent will not give the answer until you share an attempt. If you're stuck, use `Go slower` to revisit the underlying concept, then try again.
- Each `exercise` call provides a genuinely different scenario. The agent tracks which exercises have been used this session.

---

### `explain [term]`

**Syntax**: `explain hook lifecycle`, `explain orchestration`, `explain context mutation` — the word "explain" followed by the term or phrase

**What it does**: Delivers a full, standalone explanation of any vocabulary term in the curriculum — complete with definition, analogy, diagram (where applicable), and examples. Works for any term regardless of what lesson you're currently in.

**When to use it**: When the agent uses a term you don't recognize, when you want a refresher on something from a prior lesson, or when you encounter a term in an exercise and need clarification.

**What the agent does in response**:
1. Checks the vocabulary bank — if the term is already defined there, retrieves and presents it
2. If not in the bank, fetches from `Knowledge_Vault/Vocabulary/` or derives from curriculum context
3. Delivers: formal definition → plain-language restatement → analogy → example in code or pseudocode
4. Does NOT move the lesson forward — you return to where you were after the explanation

**Example**:

```
You: explain context mutation

Agent:
**Term: Context Mutation**

**Formal definition**: The act of modifying the shared data object (`context`)
that is passed between hooks during event processing. Each hook in the chain
reads the context, may modify it, and passes it to the next hook.

**Plain language**: Think of `context` as a baton in a relay race. Each runner
(hook) can write their name on it before passing it. By the end of the race,
the baton has notes from everyone who touched it.

**What can mutate**: Any key in the context object. Common mutations include
adding auth data, tagging requests with IDs, or appending to a log array.

**Risk**: If two hooks write to the same key, the second write wins silently.
This is an Interaction Failure (see: What Goes Wrong framework).

**Example**:
```python
def auth_hook(context, next):
    context['user'] = authenticate(context['token'])  # mutation
    return next(context)
```

Back to where we were — you were working on hook composition...
```

**Notes**:
- `explain` can be used on multi-word terms: `explain pre-execution phase`, `explain event envelope`.
- If a term has been in your vocabulary bank for 2+ lessons, the agent uses scaffold-fade — it may ask you to recall the definition first before providing it. This is intentional. See the Scaffold-Fade section below.

---

## Connection Commands

---

### `connect [A] to [B]`

**Syntax**: `connect hooks to lifecycle`, `connect orchestration to event dispatch`, `connect chapter 2 to chapter 3`

**What it does**: Produces a focused explanation of the relationship between two concepts, showing how they depend on, enable, or contrast with each other. More targeted than `show connections`.

**When to use it**: When you sense two concepts are related but can't articulate how. Also valuable before a checkpoint to consolidate understanding, or when studying for exams.

**What the agent does in response**:
1. Identifies both concepts
2. Explains the directional relationship (does A require B? Does A enable B? Do they conflict?)
3. Shows a concrete example where both concepts appear together
4. Notes where the connection can break (failure mode of the relationship)

**Example**:

```
You: connect hooks to lifecycle

Agent:
**Connection: Hooks ↔ Hook Lifecycle**

Relationship type: **hooks are governed by the lifecycle** — the lifecycle
defines when hooks can run; hooks are what fills those slots.

How they relate:
- The lifecycle defines three phases: pre / exec / post
- A hook registers itself into one of these phases
- Without the lifecycle, hooks have no execution order
- Without hooks, the lifecycle is an empty framework doing nothing

They are not interchangeable — lifecycle is the container, hook is the content.

**Where this connection breaks**:
If a hook is registered to a phase that never fires (e.g., a post-execution
hook for an event that always fails pre-execution), the hook never runs.
This is a silent omission failure.

**Example together**:
```python
# lifecycle: pre-execution phase
@hook(phase='pre', event='request')
def validate_input(context, next):
    ...
```
```

**Notes**:
- Either order works: `connect A to B` and `connect B to A` produce the same output.
- You can connect across chapters: `connect chapter 2 concepts to chapter 4`.

---

### `show connections`

**Syntax**: `show connections` (exact phrase)

**What it does**: Shows a map of how the current topic (lesson or concept) connects to all other chapters in the curriculum. Provides a bird's-eye view of where you are in the knowledge graph.

**When to use it**: After finishing a major concept, before a checkpoint, or when you feel lost about why the current topic matters in the bigger picture.

**What the agent does in response**:
1. Identifies the current lesson and concept
2. Maps its connections to each of the six chapters
3. Uses a table or ASCII diagram to show relationship types (feeds into, depends on, contrasts with, is used by)
4. Briefly explains why each connection matters

**Example**:

```
You: show connections

Agent:
**Connection Map: Hook Architecture (Chapter 3)**

| Chapter | Connection | Why It Matters |
|---------|-----------|----------------|
| Ch 1: Agent Foundations | Depends on | Hooks are extensions of the agent loop |
| Ch 2: Event System | Feeds into | Hooks register to events defined in Ch 2 |
| Ch 4: Pipelines | Is used by | Pipelines are built from composed hooks |
| Ch 5: Memory | Contrasts with | Memory persists state; hooks are stateless |
| Ch 6: Orchestration | Feeds into | Multi-agent orchestration uses hook coordination |

Reading this: You're building the wiring that everything else in the course
will plug into. Chapters 4 and 6 cannot be understood without Chapter 3.
```

**Notes**:
- The output adjusts to your current position. Running `show connections` in Chapter 5 produces a different map than running it in Chapter 2.

---

### `anti-patterns`

**Syntax**: `anti-patterns` (exact phrase)

**What it does**: Lists all documented anti-patterns relevant to the current chapter, using the "What Goes Wrong" framework. Shows real failure modes that students and practitioners commonly hit.

**When to use it**: After completing a lesson or chapter, as exam prep, or when you want to understand where things break in practice.

**What the agent does in response**:
1. Fetches `Knowledge_Vault/Frameworks/` for the current chapter's anti-patterns
2. Organizes them by the four failure modes: Misapplication, Omission, Excess, Interaction Failure
3. For each anti-pattern: name, description, symptom (what you'd observe), and fix

**Example**:

```
You: anti-patterns

Agent:
**Anti-Patterns: Hook Architecture (Chapter 3)**

| Category | Anti-Pattern | Symptom | Fix |
|----------|-------------|---------|-----|
| Misapplication | Using post-hooks to cancel events | Event already ran, cancel is ignored | Move logic to pre-hook |
| Omission | Forgetting `next()` call | Event chain silently stops | Always call `next()` unless intentionally blocking |
| Omission | Unregistered hook | Hook never fires, no error | Verify registration at startup |
| Excess | Duplicate hook registration | Side effects run twice | Check for existing registration before adding |
| Excess | Hook modifying global state | Hard-to-debug concurrency issues | Keep hooks pure; use context for state |
| Interaction Failure | Two hooks writing to same context key | Second write silently overwrites first | Namespace your context keys |
| Interaction Failure | Priority collision | Non-deterministic execution order | Assign explicit, spaced priorities (10, 20, 30) |
```

**Notes**:
- Running `anti-patterns` in later chapters will show more entries as the knowledge graph grows.
- Anti-patterns also appear during `go deeper` calls — this command is a focused summary view.

---

## Mastery Gate Behavior

Understanding the mastery gate makes all the teaching commands more predictable.

After every concept, the agent asks an open-ended check question (the C step of the TEACH cycle). Your answer is evaluated against a rubric from `Knowledge_Vault/Assessment/mastery-rubrics.md`. The gate works as follows:

| Attempt | Agent Behavior |
|---------|---------------|
| 1st answer — strong | Advances to next concept |
| 1st answer — weak | Re-teaches using a different approach, asks again |
| 2nd answer — still weak | Re-teaches with a third approach, asks again |
| 3rd answer — still weak | Flags `⚠️ NEEDS REVIEW`, allows continuation regardless |

The gate **never loops more than 3 times** on the same concept. If you hit the loop cap, the concept is marked for later review and you continue.

### Troubleshooting the Mastery Gate

**Problem**: The agent accepted a vague or incomplete answer and moved on.

```
You: Wait — re-examine my answer against the rubric
```

The agent will re-evaluate your last answer using the mastery rubric explicitly and either confirm the pass or re-open the gate.

**Problem**: The agent is looping on the same concept more than 3 times.

```
You: Flag this concept as needs-review and continue
```

This forces the loop cap, marks the concept `⚠️ NEEDS REVIEW`, and advances to the next concept.

---

## Scaffold-Fade Behavior

As you progress through lessons, vocabulary terms accumulate in your vocabulary bank (`context-bridge/master-cumulative.md`, Vocabulary Bank section). Once a term has appeared in 2 or more lessons, the agent stops re-providing its definition automatically.

Instead, when that term comes up, the agent may:
- Use the term without defining it (assuming you remember)
- Ask you to define it before using it in an explanation

This is intentional. It mirrors how real expertise works — you shouldn't need definitions for foundational terms after you've used them repeatedly.

**If scaffold-fade surprises you**: Use `explain [term]` at any time to get the full definition. The agent will provide it and then note how many lessons that term has appeared in.

---

## Command Interaction Notes

| Scenario | Recommended Command |
|----------|---------------------|
| Just opened Claude Code, want to keep learning | `continue` |
| Know exactly which lesson you want | `lesson X.Y` |
| Explanation was too abstract | `Go slower` |
| Want to dig deeper after understanding basics | `go deeper` |
| Want another chance to practice | `exercise` |
| Agent used an unfamiliar word | `explain [term]` |
| Want to see the big picture | `show connections` |
| Confident and ready to move on | `Next` or `I understand, move on` |
| Want to understand failure modes | `anti-patterns` or `go deeper` |
| Felt like mastery gate let you slide by | `Wait — re-examine my answer against the rubric` |
