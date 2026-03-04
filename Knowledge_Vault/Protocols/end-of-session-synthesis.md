# End-of-Session Knowledge Synthesis Protocol

> **Trigger**: User command `End`
> **Cross-refs**: [Session Management](session-management.md) | [Formatting Templates](../Pedagogy/formatting-templates.md)

---

## DIRECTIVE

Upon receiving the command **"End"**, halt all teaching activity and execute the following three-tier archival workflow. You are now operating as a **Senior Knowledge Architect** -- your goal is to distill the entire session into permanent, structured knowledge assets with **zero information loss** and **zero conversational noise**.

---

## STAGE 1: Meticulous Session Audit

Before producing any output, perform a full transcript analysis:

1. **Scan** every message from the session's first exchange to the `End` trigger.
2. **Extract**: Core lessons delivered, methodologies applied, frameworks used, vocabulary introduced, exercises completed, student performance signals, anti-patterns discussed, comprehension check results, key moments, and course corrections.
3. **Discard**: Administrative commands (`/clear`, `/compact`, `/context`), greetings without content, unrelated side-questions, repeated false starts, and meta-discussion about the teaching process itself (unless it produced a binding protocol change).
4. **Identify**: Session number (increment from last context-bridge file), lesson(s) covered, and next lesson.

---

## STAGE 2: Tier 1 -- Master Lesson Documentation (Deep Archive)

**Output location**: `revision-notes/ch{N}-{chapter-kebab-name}/{X.Y}-{lesson-kebab-title}.md`

**Purpose**: An exhaustive, standalone revision guide. The student must be able to rely on this document alone to recall every nuance of the lesson without revisiting the chat.

### Required Structure

```markdown
# Chapter {N} | Lesson {X.Y}: {Lesson Title} -- Complete Revision Guide

---

## Table of Contents
[Auto-generate based on sections below]

---

## 1. Key Vocabulary
| Term | Definition |
|------|-----------|
[Every term introduced or reinforced in this session, with plain-language definitions]

## 2-N. [One section per major concept taught]
For each concept, include:
- **What it is** -- precise definition
- **Why it matters** -- stakes, motivation
- **How it works** -- mechanics, step-by-step
- **Where it fits** -- connection to curriculum
- **What can go wrong** -- failure modes, anti-patterns
- Analogies used
- ASCII diagrams / tables / visual aids produced
- Edge cases discussed
- Adversarial analysis (if conducted)

## N+1. Anti-Patterns & Failure Modes
[All anti-patterns taught or reinforced, with "What Goes Wrong" four-axis analysis where applicable]

## N+2. Key Formulas & Mental Models
[Distilled frameworks in compact form]

## N+3. Quiz Bank: Self-Test Questions
[All comprehension check questions from the session + model answers]
[All quiz questions asked + student's performance + correct answers]

## N+4. Connection Map
- **Builds on**: [previous lessons/concepts]
- **Connects to**: [parallel concepts in other chapters]
- **Leads to**: [next lesson/concept]
```

### Quality Criteria
- Depth must match or exceed the session's teaching depth
- Every analogy, diagram, table, and exercise from the session must be preserved
- Student-specific insights (what they struggled with, what clicked) should be noted inline
- Tone: Technical, authoritative, matching the established teaching style

---

## STAGE 3: Tier 2 -- Context Bridge (Concise Routing)

**Output location**: `context-bridge/session-{NN}-lesson-{X.Y}-{lesson-kebab-title}.md`

**Purpose**: A concise file that gives a future Claude session full situational awareness. It must fit comfortably in a small context window while preserving all continuity-critical information.

### Required Structure

```markdown
# Session {NN} -- Lesson {X.Y}: {Lesson Title}

> **Date**: {YYYY-MM-DD}
> **Lesson Covered**: Chapter {N}, Lesson {X.Y} -- {Title}
> **Student Status**: Lesson {X.Y} COMPLETE | Next: Lesson {X.Z}
> **Source URL**: {if provided during session}

---

## 1. Project Essence
[2-3 sentences: what this project is, student goal, current chapter]

## 2. Student Profile & Learning DNA
### Background
[Level, language, access constraints]
### How This Student Learns Best
[Bullet list of observed preferences and binding instructions]
### Behavioral Patterns Observed
[Table: Pattern | What It Means | How to Respond]

## 3. Established Teaching Patterns
[TEACH cycle status, "Try with AI" framework, question protocol, revision file protocol, source material protocol -- carry forward from previous bridge + any updates]

## 4. Key Technical Decisions
[File naming conventions, directory structure choices]

## 5. Session Flow
### What Happened This Session
[Numbered timeline of the session's key events]
### Key Moments
[2-3 bullet points: strongest moment, growth edge, any course corrections]

## 6. Knowledge Graph -- What Was Learned
[ASCII tree of all concepts mastered, organized hierarchically]
[Separate section for concepts from other chapters introduced inline]

## 7. Vocabulary Bank -- Terms Introduced
[Table: Term | First Introduced | Defined?]
[Cumulative across all sessions]

## 8. Anti-Patterns Covered
### Fully Taught
[Table: Anti-Pattern | Chapter | How Taught]
### Mentioned But Not Yet Fully Taught
[List]

## 9. Frameworks & Mental Models Internalized
[Compact numbered list of all frameworks taught so far, cumulative]

## 10. Student Strengths & Growth Areas
### Strengths
[Bullet list with evidence]
### Growth Areas
[Bullet list with guidance for next session]

## 11. Collaboration Style & Tone
### Rules
[Bullet list of binding interaction rules]
### Student Intent Signals
[Table: They Say | They Mean]

## 12. Repository Structure
[ASCII tree of current project state]

## 13. Next Steps
### Immediate Next
[Next lesson + instructions]
### Remaining in Current Module
[List of upcoming lessons]
### Open Questions
[Anything unresolved]

## 14. How to Use This File
[Instructions for loading in next session]
```

### Quality Criteria
- Must be **self-contained** -- a new Claude session reading ONLY this file + CLAUDE.md should have full context
- Cumulative: carry forward vocabulary, anti-patterns, frameworks, and student observations from ALL prior bridges
- Concise but complete: every section present, no padding

---

## STAGE 4: Tier 3 -- Interactive Slide-Based Visual Presentation

**Output**: A standalone HTML file **saved to `visual-presentations/session-{NN}-lesson-{X.Y}-{lesson-kebab-title}.html`** using the Write tool.

**Purpose**: A beautiful, interactive slide-based presentation the student can navigate like a keynote, open in any browser, and use as a polished revision tool.

### Design Specification (Persistent Across All Sessions)

The HTML must follow this **exact, consistent design system** for every session. This is a **BINDING specification** -- do not deviate.

```
═══════════════════════════════════════════════════════════
  ARCHITECTURE: FULLSCREEN SLIDE-BASED PRESENTATION
═══════════════════════════════════════════════════════════

FORMAT:
- Standalone HTML (all CSS inline in <style>, all JS inline in <script>)
- NO external dependencies (no CDNs, no frameworks, no imports)
- Fullscreen slide-based layout: each section is one slide (100vh)
- Slides are navigated via arrow keys, click, or dot indicators
- Smooth animated transitions between slides (CSS transform + opacity)
- Elements within each slide animate in on arrival (staggered fade+slide)
- Hover reveals, expandable accordions, and interactive cards within slides

═══════════════════════════════════════════════════════════
  THEME: LIGHT PROFESSIONAL
═══════════════════════════════════════════════════════════

COLOR PALETTE:
- Background: #f8f9fc (off-white)
- Surface/cards: #ffffff with subtle shadow
- Text primary: #1e293b (slate-800)
- Text secondary: #64748b (slate-500)
- Text muted: #94a3b8 (slate-400)
- Accent primary: #6366f1 (indigo-500)
- Accent secondary: #06b6d4 (cyan-500)
- Success: #10b981 (emerald-500)
- Warning: #f59e0b (amber-500)
- Danger: #ef4444 (red-500)
- Card border: #e2e8f0 (slate-200)
- Dividers: #f1f5f9 (slate-100)
- Code background: #f1f5f9

TYPOGRAPHY:
- Font stack: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif
- Monospace: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace
- Slide title: 2.5rem, font-weight 800, color slate-800, letter-spacing -0.03em
- Slide subtitle: 1.1rem, font-weight 400, color slate-500
- Body text: 1rem, line-height 1.7, color slate-700
- Labels/badges: 0.75rem, font-weight 600, uppercase, letter-spacing 0.05em
- Card titles: 1.05rem, font-weight 700

═══════════════════════════════════════════════════════════
  SLIDE STRUCTURE (in order)
═══════════════════════════════════════════════════════════

SLIDE 1 -- TITLE SLIDE:
- Large centered lesson title with gradient text (indigo→cyan)
- Session number, date, chapter info as subtle badges
- Animated entrance: title scales up from 0.9, subtitle fades in delayed
- "Use arrow keys or click to navigate" hint at bottom

SLIDE 2 -- SESSION OVERVIEW:
- Clean hero card with left accent border (indigo)
- 2-3 sentence summary of what was covered
- Key stats as pill badges (concepts count, vocab count, frameworks count)
- Content fades in from bottom on slide entry

SLIDE 3+ -- CONCEPT SLIDES (one slide per major concept OR grouped 2-3):
- Each concept gets a visual treatment:
  * Flowcharts using CSS flexbox/grid with colored nodes and arrows
  * Diagrams using styled divs (not ASCII -- use actual CSS shapes)
  * Step sequences as horizontal pipeline with numbered circles
  * Comparisons as side-by-side cards with vs divider
- Hover cards: brief label visible, full explanation appears on hover
- Accordion sections: click to expand deeper detail (CSS-only using checkbox hack)
- Staggered animation: elements appear one by one (0.1s delay each)

VOCABULARY SLIDE:
- Interactive card grid (NOT a plain table)
- Each term is a flip card or hover-reveal card:
  * Front: term name + category badge
  * Back/hover: full definition
- Grid layout: 3 columns on desktop, 2 on tablet, 1 on mobile
- Cards have subtle colored left border cycling through palette

FRAMEWORKS SLIDE:
- Visual numbered list with large step numbers (styled circles)
- Each framework has a compact formula/equation display
- Key frameworks get mini-diagrams (CSS-drawn, not ASCII)
- Hover to highlight connections between frameworks

ANTI-PATTERNS SLIDE:
- Warning cards with red/amber gradient left border
- Each card has: icon, name, one-line description
- Click/hover to expand: full explanation + "Fix" callout in green
- Cards arranged in responsive grid

PERFORMANCE SLIDE:
- Two-column layout: Strengths (green accent) | Growth Areas (amber accent)
- Each item has a colored dot indicator
- Clean, minimal -- no walls of text

CONNECTION MAP SLIDE:
- Visual node-and-line diagram using CSS (NOT monospace pre blocks)
- Lesson nodes as colored pills, connection lines as styled borders/pseudo-elements
- Related chapters as colored clusters
- Hover a node to highlight its connections

NEXT SESSION SLIDE:
- Clean call-to-action card centered on slide
- Next lesson title prominently displayed
- Gradient background (indigo→cyan, subtle)
- "Load context bridge to continue" instruction

═══════════════════════════════════════════════════════════
  INTERACTIVE FEATURES (JavaScript)
═══════════════════════════════════════════════════════════

SLIDE NAVIGATION:
- Arrow keys (Left/Right) navigate between slides
- Click anywhere on left/right 20% of screen navigates
- Dot indicators at bottom: clickable, show current position
- Slide transitions: transform translateX + opacity, 0.5s ease
- Current slide tracked via JS variable, slides shown/hidden via class toggle
- Mobile: swipe support via touch events (touchstart/touchend delta)

ON-SLIDE ANIMATIONS:
- Elements with class .animate-in start at opacity:0, translateY(30px)
- When slide becomes active, elements transition to opacity:1, translateY(0)
- Staggered: each .animate-in gets increasing transition-delay (0.1s increments)
- Use CSS transitions triggered by adding .active class to parent slide

HOVER INTERACTIONS:
- Cards: translateY(-4px) lift + shadow increase on hover
- Flip cards for vocabulary: CSS 3D transform rotateY(180deg)
- Expandable sections: CSS max-height transition from 0 to auto (use large max-height value)
- Tooltip-style reveals: opacity transition on nested .detail element

ACCORDION (CSS-ONLY WHERE POSSIBLE):
- Use hidden checkbox + label + sibling selector pattern
- Smooth max-height transition
- Chevron icon rotates on open

═══════════════════════════════════════════════════════════
  RESPONSIVE DESIGN
═══════════════════════════════════════════════════════════

- Mobile (≤640px): single column, smaller fonts, stack all grids vertically
- Tablet (641-1024px): two-column grids, slightly reduced spacing
- Desktop (1025px+): full layout, 3-column grids where specified
- Slides always 100vh regardless of viewport
- Content within slides: max-width 900px, centered, with overflow-y auto for long slides
- Nav dots: fixed bottom center, always visible

═══════════════════════════════════════════════════════════
  QUALITY BAR
═══════════════════════════════════════════════════════════

EVERY presentation must feel like a POLISHED KEYNOTE, not a document:
- NO walls of text -- break everything into visual chunks
- NO plain tables -- use card grids, flip cards, or styled mini-tables
- NO ASCII art -- use CSS-drawn diagrams with colored divs and borders
- EVERY concept should have a VISUAL (flowchart, diagram, pipeline, comparison)
- Animations should be SMOOTH and PURPOSEFUL, not gratuitous
- White space is a feature -- don't cram slides
- Maximum ~6-8 visual elements per slide -- split into multiple slides if needed
- Print: @media print should produce clean output (hide nav, show all slides stacked)
```

### Content Rules
- **Only document what was actually taught** -- no speculative content, no approaches or patterns not discussed
- Replace all text-heavy explanations with **visual representations**: flowcharts, node diagrams, pipeline sequences, comparison cards, or structured grids
- Tone: Technical, authoritative, matching established teaching style
- This is a **premium revision tool** -- it should feel like opening a polished product, not reading a document
- Each slide should be digestible in 10-15 seconds of viewing
- **Vocabulary**: use flip-card or hover-reveal pattern, never a plain table
- **Frameworks**: show as visual formulas or mini-diagrams, never just a numbered list
- **Anti-patterns**: show as expandable warning cards, never just paragraphs
- **Connections**: show as a visual node graph, never a monospace pre block

---

## EXECUTION ORDER

When the student says `End`:

1. Acknowledge the trigger: "Initiating End-of-Session Knowledge Synthesis..."
2. Perform the Session Audit (Stage 1) silently
3. **Write** the Master Lesson Documentation file (Stage 2) using the Write tool
4. **Write** the Context Bridge file (Stage 3) using the Write tool
5. **Write** the Interactive HTML Presentation (Stage 4) to `visual-presentations/` using the Write tool -- this MUST be saved as a file, never only shown in chat
6. Confirm completion: "Session archived. Three artifacts created: [list paths]. Open the HTML in a browser for the interactive slide presentation."

---

## CONSTRAINTS

- **Zero information loss**: The Master Lesson Documentation must capture everything taught
- **Zero noise**: Strip all conversational filler, administrative commands, and meta-discussion
- **Pedagogical consistency**: Match the teaching tone established during the session
- **Format persistence**: The HTML design MUST be identical across all sessions for visual consistency
- **Cumulative bridges**: Each context bridge builds on all prior ones -- never lose prior session data
