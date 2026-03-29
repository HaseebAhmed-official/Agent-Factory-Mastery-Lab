# Finish Synthesis Protocol

> **Trigger**: User command `Finish` (or `End` for backward compatibility)
> **Output**: Final part file + Final bridge + Comprehensive HTML + Quick Ref + Flashcards
> **Context Action**: Offer to continue to next lesson or end session
> **Cross-refs**: [Checkpoint Synthesis](checkpoint-synthesis.md) | [End-of-Session](end-of-session-synthesis.md) | [Formatting Templates](../Pedagogy/formatting-templates.md)

---

## DIRECTIVE

Upon receiving the command **"Finish"** or **"End"**, halt all teaching activity and execute the following **six-tier archival workflow**. You are now operating as a **Senior Knowledge Architect** -- your goal is to:

1. **Complete the lesson** with final checkpoint
2. **Generate comprehensive HTML presentation** covering ALL checkpoints
3. **Create quick reference materials** for rapid lookup
4. **Generate flashcards** for spaced repetition
5. **Update all discovery systems** (index, concept map)
6. **Prepare for next lesson** or session end

This is a **lesson completion** event -- different from mid-lesson checkpoints.

---

## STAGE 1: Session Audit (Since Last Checkpoint)

Identical to Checkpoint Protocol Stage 1:

1. **Identify last checkpoint timestamp** (from `.checkpoint-meta.json`)
2. **Extract teaching content** since that point
3. **Discard conversational noise**
4. **Determine final checkpoint metadata** (Layer L{N}, semantic concept)

If NO new content since last checkpoint (user says "Finish" immediately after checkpoint):
- Skip creating redundant final part file
- Proceed directly to HTML generation and Tier 4-6

---

## STAGE 2: Final Part File (Tier 2)

**Only if new content exists since last checkpoint.**

Create final versioned part: `{X.Y}-L{N}-{concept}.md`

**Process**: Identical to Checkpoint Protocol Stage 2
- Same structure, voice transformation, quality gates
- Mark as `status: "complete"` in YAML frontmatter
- Parent checkpoint: Previous layer (L{N-1})

---

## STAGE 3: Final Bridge Update (Tier 1)

**File**: `context-bridge/master-cumulative.md`

**Update mode**: Final updates + lesson completion marker

### Updates to Make

#### Mark lesson complete in "Next Steps":
```markdown
## 13. Next Steps
**Lesson {X.Y}**: ✅ COMPLETE

**Immediate Next**: Lesson {X.Z} -- {Next Lesson Title}

**Remaining in Module {X}**:
- Lesson {X.Z}
- Lesson {X.Z+1}
- ...
```

#### Add final checkpoint row:
```markdown
| L{N} | {timestamp} | {concepts} | {X.Y}-L{N}-{concept}.md | ✅ Lesson Complete |
```

#### Update "Repository Structure":
```markdown
revision-notes/
├─ ch{N}-{name}/
│  └─ module{X}-{name}/
│     └─ {X.Y}-{lesson}/
│        ├─ .checkpoint-meta.json
│        ├─ {X.Y}-L1-{concept}.md
│        ├─ {X.Y}-L2-{concept}.md
│        └─ {X.Y}-L{N}-{concept}.md  ← FINAL
visual-presentations/
└─ session-{NN}-lesson-{X.Y}-{title}.html  ← NEW
```

---

## STAGE 4: Interactive HTML Presentation (Tier 3)

**File**: `visual-presentations/session-{NN}-lesson-{X.Y}-{kebab-title}.html`

**Purpose**: Comprehensive interactive slide presentation covering **ALL checkpoints** for this lesson

### Content Aggregation Strategy

**CRITICAL**: Read ALL checkpoint part files for this lesson and merge content

1. **Scan lesson directory**: Glob `{X.Y}-L*-*.md` files
2. **Sort by depth**: L1, L2, L3, ... (lexicographic order)
3. **Parse each file**:
   - Extract YAML frontmatter
   - Extract vocabulary tables
   - Extract frameworks
   - Extract anti-patterns
   - Extract concepts (from headings and content)
   - Extract exercises

4. **Merge strategy**:
   - **Vocabulary**: Combine all vocab tables, deduplicate, alphabetize
   - **Frameworks**: Preserve teaching order (L1 frameworks first, then L2, etc.)
   - **Concepts**: One slide per major concept (chronological across layers)
   - **Anti-patterns**: Consolidate into single anti-patterns slide
   - **Exercises**: Combine into exercises slide (grouped by layer)
   - **Performance**: Use latest comprehension check results (from final part)

---

### Slide Structure (Master Navigation HTML)

**Navigation Philosophy**: Master HTML is **overview + navigation hub** linking to individual checkpoint HTMLs

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson {X.Y}: {Title} - Complete Presentation</title>
  <style>
    /* DESIGN SYSTEM: Use exact theme from end-of-session-synthesis.md */
    /* Color palette, typography, slide structure - follow specification exactly */
  </style>
</head>
<body>

<!-- SLIDE 1: TITLE SLIDE -->
<div class="slide active" id="slide-title">
  <div class="slide-content">
    <h1 class="lesson-title gradient-text">Lesson {X.Y}: {Title}</h1>
    <p class="subtitle">Complete Interactive Presentation</p>
    <div class="meta-badges">
      <span class="badge">Session {NN}</span>
      <span class="badge">Chapter {N}</span>
      <span class="badge">{Date}</span>
    </div>
    <div class="stats-pills">
      <div class="pill">{N} Checkpoints</div>
      <div class="pill">L1-L{N} Layers</div>
      <div class="pill">{M} Concepts</div>
      <div class="pill">{V} Vocab Terms</div>
    </div>
    <p class="nav-hint">Use arrow keys, click edges, or dots below to navigate</p>
  </div>
</div>

<!-- SLIDE 2: CHECKPOINT NAVIGATION DASHBOARD -->
<div class="slide" id="slide-navigation">
  <div class="slide-content">
    <h2>Lesson Overview & Navigation</h2>
    <p class="intro">This lesson was taught in {N} checkpoint layers. Click any card to open its focused presentation.</p>

    <div class="checkpoint-grid">
      <!-- L1 Card -->
      <div class="checkpoint-card layer-l1" onclick="openCheckpoint('L1')">
        <div class="layer-badge">L1: Fundamentals</div>
        <h3>{L1 Semantic Concept Title}</h3>
        <ul class="concepts-list">
          <li>{Concept A}</li>
          <li>{Concept B}</li>
          <li>{Concept C}</li>
        </ul>
        <div class="card-footer">
          <span class="timestamp">{HH:MM}</span>
          <button class="btn-open">Open L1 →</button>
        </div>
      </div>

      <!-- L2 Card -->
      <div class="checkpoint-card layer-l2" onclick="openCheckpoint('L2')">
        <div class="layer-badge">L2: Intermediate</div>
        <h3>{L2 Semantic Concept Title}</h3>
        <ul class="concepts-list">
          <li>{Concept D}</li>
          <li>{Concept E}</li>
        </ul>
        <div class="card-footer">
          <span class="timestamp">{HH:MM}</span>
          <button class="btn-open">Open L2 →</button>
        </div>
      </div>

      <!-- Repeat for L3, L4, etc. -->
    </div>
  </div>
</div>

<!-- SLIDE 3: LESSON OVERVIEW (Aggregated) -->
<div class="slide" id="slide-overview">
  <div class="slide-content">
    <div class="hero-card accent-left-indigo">
      <h2>Lesson Overview</h2>
      <p class="overview-text">{2-3 sentence summary of entire lesson}</p>

      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-number">{N}</div>
          <div class="stat-label">Concepts</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{V}</div>
          <div class="stat-label">Vocab Terms</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{F}</div>
          <div class="stat-label">Frameworks</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{A}</div>
          <div class="stat-label">Anti-Patterns</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- SLIDE 4+: CONCEPT SLIDES (Aggregated from all checkpoints) -->
<!-- One slide per major concept, chronological order across layers -->
<div class="slide" id="slide-concept-1">
  <div class="slide-content">
    <h2>{Concept Name}</h2>
    <div class="layer-indicator">From: Layer L{X}</div>

    <!-- Visual diagram using CSS (NOT ASCII) -->
    <div class="concept-diagram">
      {CSS-drawn flowchart, node graph, pipeline, or comparison}
    </div>

    <!-- Expandable accordion for details -->
    <div class="accordion">
      <input type="checkbox" id="acc-concept-1">
      <label for="acc-concept-1">
        <span>Show Details</span>
        <span class="chevron">▼</span>
      </label>
      <div class="accordion-content">
        <p><strong>What it is:</strong> {Definition}</p>
        <p><strong>Why it matters:</strong> {Motivation}</p>
        <p><strong>How it works:</strong> {Mechanics}</p>
      </div>
    </div>
  </div>
</div>

<!-- VOCABULARY SLIDE (Aggregated, deduplicated) -->
<div class="slide" id="slide-vocabulary">
  <div class="slide-content">
    <h2>Complete Vocabulary</h2>
    <p class="subtitle">All terms from layers L1-L{N} (alphabetized)</p>

    <!-- Interactive flip cards (NOT plain table) -->
    <div class="vocab-grid">
      <div class="flip-card">
        <div class="flip-card-inner">
          <div class="flip-card-front">
            <div class="term-name">{Term A}</div>
            <div class="category-badge">Fundamental</div>
          </div>
          <div class="flip-card-back">
            <p>{Definition}</p>
            <span class="source">From L{X}</span>
          </div>
        </div>
      </div>

      <!-- Repeat for all vocab terms -->
    </div>
  </div>
</div>

<!-- FRAMEWORKS SLIDE (Aggregated, teaching order) -->
<div class="slide" id="slide-frameworks">
  <div class="slide-content">
    <h2>Frameworks & Mental Models</h2>

    <div class="frameworks-list">
      <div class="framework-card">
        <div class="framework-number">1</div>
        <div class="framework-content">
          <h3>{Framework Name}</h3>
          <div class="formula">{Compact formula/pattern}</div>
          <div class="mini-diagram">
            {CSS-drawn mini-diagram if applicable}
          </div>
          <p class="application">{When to use}</p>
          <span class="source-badge">Layer L{X}</span>
        </div>
      </div>

      <!-- Repeat for all frameworks -->
    </div>
  </div>
</div>

<!-- ANTI-PATTERNS SLIDE (Aggregated) -->
<div class="slide" id="slide-antipatterns">
  <div class="slide-content">
    <h2>Anti-Patterns & Failure Modes</h2>

    <div class="antipattern-grid">
      <div class="antipattern-card">
        <div class="warning-icon">⚠️</div>
        <h3>{Anti-Pattern Name}</h3>
        <p class="description">{One-line description}</p>

        <!-- Click to expand -->
        <input type="checkbox" id="ap-1">
        <label for="ap-1" class="expand-btn">Show Details ▼</label>
        <div class="expanded-content">
          <div class="what-goes-wrong">
            <h4>What Goes Wrong</h4>
            <ul>
              <li><strong>Misapplication:</strong> {Description}</li>
              <li><strong>Omission:</strong> {Description}</li>
            </ul>
          </div>
          <div class="fix-callout">
            <h4>✅ Fix</h4>
            <p>{Correct approach}</p>
          </div>
        </div>
        <span class="source-badge">Layer L{X}</span>
      </div>

      <!-- Repeat for all anti-patterns -->
    </div>
  </div>
</div>

<!-- CHECKPOINT TIMELINE SLIDE (NEW) -->
<div class="slide" id="slide-timeline">
  <div class="slide-content">
    <h2>Checkpoint Timeline</h2>
    <p class="subtitle">How this lesson unfolded</p>

    <div class="timeline">
      <div class="timeline-item layer-l1">
        <div class="timeline-marker">L1</div>
        <div class="timeline-content">
          <h3>{L1 Semantic Concept}</h3>
          <div class="concepts-taught">
            <span class="concept-pill">{Concept A}</span>
            <span class="concept-pill">{Concept B}</span>
          </div>
          <div class="timestamp">{HH:MM}</div>
        </div>
      </div>

      <div class="timeline-connector"></div>

      <div class="timeline-item layer-l2">
        <div class="timeline-marker">L2</div>
        <div class="timeline-content">
          <h3>{L2 Semantic Concept}</h3>
          <div class="concepts-taught">
            <span class="concept-pill">{Concept C}</span>
            <span class="concept-pill">{Concept D}</span>
          </div>
          <div class="timestamp">{HH:MM}</div>
        </div>
      </div>

      <!-- Repeat for all checkpoints, CSS draws connecting lines -->
    </div>
  </div>
</div>

<!-- EXERCISES SLIDE (Aggregated) -->
<div class="slide" id="slide-exercises">
  <div class="slide-content">
    <h2>Hands-On Exercises</h2>

    <div class="exercises-grid">
      <!-- Grouped by layer -->
      <div class="layer-group">
        <h3 class="layer-heading">Layer L1: Fundamentals</h3>

        <div class="exercise-card">
          <div class="exercise-number">Exercise 1</div>
          <h4>{Exercise Name}</h4>
          <p class="objective">{Objective}</p>

          <div class="accordion-wrapper">
            <input type="checkbox" id="ex-1">
            <label for="ex-1">Show Instructions ▼</label>
            <div class="accordion-content">
              <pre><code>{Step-by-step instructions}</code></pre>
              <div class="expected-outcome">
                <h5>Expected Outcome:</h5>
                <p>{What success looks like}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Repeat for other layers -->
    </div>
  </div>
</div>

<!-- PERFORMANCE SLIDE (Latest Assessment) -->
<div class="slide" id="slide-performance">
  <div class="slide-content">
    <h2>Performance Assessment</h2>

    <div class="performance-grid">
      <div class="strengths-column accent-left-green">
        <h3>Strengths</h3>
        <ul class="strength-list">
          <li><span class="dot green"></span>{Strength 1}</li>
          <li><span class="dot green"></span>{Strength 2}</li>
        </ul>
      </div>

      <div class="growth-column accent-left-amber">
        <h3>Growth Areas</h3>
        <ul class="growth-list">
          <li><span class="dot amber"></span>{Growth area 1}</li>
          <li><span class="dot amber"></span>{Growth area 2}</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<!-- CONNECTION MAP SLIDE (CSS-drawn graph) -->
<div class="slide" id="slide-connections">
  <div class="slide-content">
    <h2>Connection Map</h2>

    <div class="connection-diagram">
      <!-- CSS-drawn node graph (NOT ASCII pre block) -->
      <div class="connection-node prerequisite">
        <span class="node-label">{Previous Lesson}</span>
      </div>

      <div class="connection-line"></div>

      <div class="connection-node current">
        <span class="node-label">Lesson {X.Y}</span>
      </div>

      <div class="connection-line"></div>

      <div class="connection-node next">
        <span class="node-label">{Next Lesson}</span>
      </div>

      <!-- Parallel connections to other chapters -->
      <div class="parallel-connections">
        <div class="parallel-node">
          <span>{Related Concept} (Ch {N})</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- NEXT LESSON SLIDE (Final) -->
<div class="slide" id="slide-next">
  <div class="slide-content">
    <div class="next-lesson-card gradient-bg-indigo-cyan">
      <h2>Next Up</h2>
      <h3 class="next-lesson-title">Lesson {X.Z}: {Next Lesson Title}</h3>

      <div class="next-steps">
        <div class="step">
          <div class="step-number">1</div>
          <p>Load cumulative context bridge for continuity</p>
          <code>context-bridge/master-cumulative.md</code>
        </div>

        <div class="step">
          <div class="step-number">2</div>
          <p>Review quick reference cheatsheet (optional)</p>
          <code>quick-reference/lesson-{X.Y}-cheatsheet.md</code>
        </div>

        <div class="step">
          <div class="step-number">3</div>
          <p>Start Lesson {X.Z}</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- NAVIGATION CONTROLS -->
<div class="nav-dots">
  <span class="dot active" onclick="goToSlide(0)"></span>
  <span class="dot" onclick="goToSlide(1)"></span>
  <!-- One dot per slide -->
</div>

<script>
// Slide navigation logic
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.nav-dots .dot');

function goToSlide(n) {
  slides[currentSlide].classList.remove('active');
  dots[currentSlide].classList.remove('active');

  currentSlide = n;
  if (currentSlide >= slides.length) currentSlide = 0;
  if (currentSlide < 0) currentSlide = slides.length - 1;

  slides[currentSlide].classList.add('active');
  dots[currentSlide].classList.add('active');
}

// Arrow key navigation
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') goToSlide(currentSlide + 1);
  if (e.key === 'ArrowLeft') goToSlide(currentSlide - 1);
});

// Click edge navigation
document.addEventListener('click', (e) => {
  const clickX = e.clientX;
  const windowWidth = window.innerWidth;

  if (clickX < windowWidth * 0.2) goToSlide(currentSlide - 1);
  if (clickX > windowWidth * 0.8) goToSlide(currentSlide + 1);
});

// Touch swipe support
let touchStartX = 0;
document.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
});

document.addEventListener('touchend', (e) => {
  const touchEndX = e.changedTouches[0].clientX;
  const delta = touchEndX - touchStartX;

  if (delta > 50) goToSlide(currentSlide - 1);
  if (delta < -50) goToSlide(currentSlide + 1);
});

// Open individual checkpoint HTML
function openCheckpoint(layer) {
  const url = `session-{NN}-lesson-{X.Y}-${layer}-presentation.html`;
  window.open(url, '_blank');
}

// Staggered animations on slide entry
function animateSlideElements() {
  const activeSlide = slides[currentSlide];
  const animatedElements = activeSlide.querySelectorAll('.animate-in');

  animatedElements.forEach((el, index) => {
    setTimeout(() => {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, index * 100);
  });
}

// Watch for slide changes
const observer = new MutationObserver(() => {
  animateSlideElements();
});

slides.forEach(slide => {
  observer.observe(slide, { attributes: true, attributeFilter: ['class'] });
});
</script>

</body>
</html>
```

---

### Individual Checkpoint HTMLs

**ALSO generate**: Individual focused presentations for each checkpoint layer

**Files**: `session-{NN}-lesson-{X.Y}-L{N}-presentation.html`

**Purpose**: Student can review JUST the fundamentals (L1) or JUST the advanced concepts (L3) without all layers

**Structure**: Same design system, but content ONLY from that checkpoint's part file
- Includes: "Back to Master" button linking to master navigation HTML
- Smaller scope: 3-6 slides typically

---

## STAGE 5: Quick Reference Cheatsheet (Tier 4)

**File**: `quick-reference/lesson-{X.Y}-cheatsheet.md`

**Purpose**: 2-3 page condensed summary for rapid lookup

### Generation Process

1. **Read ALL checkpoint part files** for lesson
2. **Extract key elements**:
   - Vocabulary: All terms (deduplicate)
   - Frameworks: All numbered frameworks
   - Decision trees: "When to use X vs Y" sections
   - Key formulas: Condensed procedures
   - Common pitfalls: Top 5 anti-patterns

3. **Generate condensed cheatsheet**:

```markdown
---
lesson: "{X.Y}"
title: "Lesson {X.Y} Quick Reference: {Title}"
layers: [L1, L2, L{N}]
estimated_time: "5min"
---

# Lesson {X.Y} Quick Reference: {Title}

## At a Glance

- **Core Concept**: {One sentence summary}
- **When to Use**: {Brief criteria}
- **Difficulty**: {easy|intermediate|advanced}
- **Estimated Study Time**: {N} min
- **Layers Covered**: L1-L{N}

---

## Essential Vocabulary

| Term | Definition | Layer |
|------|-----------|-------|
| {Term A} | {One-line definition} | L1 |
| {Term B} | {One-line definition} | L2 |

---

## Key Frameworks

### 1. {Framework Name} (L{X})
```
{Compact formula or pattern}
```
**Use when**: {Brief criteria}

### 2. {Framework Name} (L{Y})
```
{Compact formula}
```
**Use when**: {Brief criteria}

---

## Decision Trees

### When to {Action A} vs {Action B}

```mermaid
graph TD
    A[Need {capability}?] -->|Yes| B[Use {Approach A}]
    A -->|No| C[Use {Approach B}]
    B --> D{Performance critical?}
    D -->|Yes| E[Add {optimization}]
    D -->|No| F[Standard approach]
```

---

## Common Pitfalls

| ❌ Anti-Pattern | ✅ Fix | Layer |
|----------------|--------|-------|
| {Anti-pattern 1} | {Correct approach} | L{X} |
| {Anti-pattern 2} | {Correct approach} | L{Y} |

---

## Quick Commands

```bash
# {Description}
{command or code snippet}

# {Description}
{command or code snippet}
```

---

## Where to Learn More

- **Full notes**: `revision-notes/.../3.{X}-L*-*.md` (all layers)
- **Visual presentation**: `visual-presentations/session-{NN}-lesson-{X.Y}-*.html`
- **Practice exercises**: See full notes, section "Hands-On Exercises"
- **Flashcards**: `flashcards/lesson-{X.Y}-deck.json`

---

## Connections

**Builds on**: {Previous lesson(s)}
**Leads to**: {Next lesson}
**Related**: {Parallel concepts in other chapters}
```

---

## STAGE 6: Flashcards for Spaced Repetition (Tier 6)

**File**: `flashcards/lesson-{X.Y}-deck.json`

**Purpose**: Anki-compatible flashcard deck for long-term retention

### Generation Process

1. **Read ALL checkpoint part files**
2. **Extract flashcard candidates**:
   - Vocabulary terms → vocab cards
   - Key concepts → concept cards
   - Anti-patterns → anti-pattern cards
   - Frameworks → framework cards

3. **Generate Anki-compatible JSON**:

```json
{
  "deck_name": "Agent Factory - Lesson {X.Y}: {Title}",
  "cards": [
    {
      "id": "{X.Y}-vocab-001",
      "type": "vocab",
      "front": "What is {Term} in the context of {domain}?",
      "back": "{Definition}",
      "tags": ["{X.Y}", "{topic}", "vocabulary", "fundamentals"],
      "difficulty": "easy",
      "source": "revision-notes/.../3.{X}-L1-{concept}.md#vocabulary",
      "layer": "L1"
    },
    {
      "id": "{X.Y}-concept-001",
      "type": "concept",
      "front": "Describe the {Concept Name} and its purpose.",
      "back": "{What it is + Why it matters + Brief how it works}",
      "tags": ["{X.Y}", "{topic}", "concept", "intermediate"],
      "difficulty": "medium",
      "source": "revision-notes/.../3.{X}-L2-{concept}.md#{section}",
      "layer": "L2"
    },
    {
      "id": "{X.Y}-antipattern-001",
      "type": "antipattern",
      "front": "What goes wrong if {specific misuse}?",
      "back": "{Problem description}<br><br><strong>Fix:</strong> {Correct approach}",
      "tags": ["{X.Y}", "anti-patterns", "debugging"],
      "difficulty": "hard",
      "source": "revision-notes/.../3.{X}-L2-{concept}.md#anti-patterns",
      "layer": "L2"
    },
    {
      "id": "{X.Y}-framework-001",
      "type": "framework",
      "front": "Explain the {Framework Name} framework.",
      "back": "{Formula/Pattern}<br><br>{Application guidance}",
      "tags": ["{X.Y}", "frameworks", "mental-models"],
      "difficulty": "medium",
      "source": "revision-notes/.../3.{X}-L1-{concept}.md#frameworks",
      "layer": "L1"
    }
  ],
  "metadata": {
    "lesson": "{X.Y}",
    "total_cards": {N},
    "created": "{ISO8601 timestamp}",
    "version": "1.0",
    "layers": ["L1", "L2", "L{N}"],
    "export_ready": true
  }
}
```

---

## STAGE 7: Discovery System Updates (Automated)

**Purpose**: Rebuild all search indexes and discovery systems to include the newly completed lesson.

### 7.1 Extract Tags Index

**Script**: `scripts/extract-tags.py`

**What it does**:
- Scans all markdown files in `revision-notes/` for YAML frontmatter
- Extracts tags and builds co-occurrence matrix for related tags
- Generates `search-index/tags-index.json`

**Command**: `python scripts/extract-tags.py`

**Expected Output**:
```
📂 Scanning {N} markdown files...
✅ Found {M} unique tags
💾 Tags index saved to search-index/tags-index.json
   - {M} tags
   - {N} files
```

---

### 7.2 Build Full-Text Search Index

**Script**: `scripts/build-search-index.py`

**What it does**:
- Tokenizes all markdown content
- Builds inverted index with TF-IDF scoring
- Generates search snippets with context
- Outputs `search-index/fulltext-index.json`

**Command**: `python scripts/build-search-index.py`

**Expected Output**:
```
📂 Indexing {N} markdown files...
✅ Indexed {N} documents
✅ Found {K} unique terms
💾 Full-text index saved to search-index/fulltext-index.json
   - {N} documents
   - {K} unique terms
```

---

### 7.3 Auto-Generate Master INDEX.md

**Script**: `scripts/generate-index.py`

**What it does**:
- Scans all markdown files and extracts frontmatter metadata
- Builds hierarchical structure (Chapter → Module → Lesson)
- Creates concept, framework, and anti-pattern indexes
- **Overwrites** `revision-notes/INDEX.md` with fresh content

**Command**: `python scripts/generate-index.py`

**Expected Output**:
```
📂 Scanning {N} markdown files...
✅ Found {C} chapters
💾 Master INDEX.md saved to revision-notes/INDEX.md
   - {C} chapters
   - {K} concepts
   - {F} frameworks
   - {A} anti-patterns
```

**Generated Structure**:
```markdown
# Agent Factory Part 1: Master Index

> **Auto-Generated**: This file is automatically generated by scripts/generate-index.py

## Table of Contents
- Chapter {N}
  - Module {X}
    - Lesson {X.Y}

## Chapter {N}
### Module {X}
#### Lesson {X.Y}

**🔷 Fundamentals**: [Title](path/to/{X.Y}-L1-*.md)
- Concepts: `concept-a`, `concept-b`
- Frameworks: `framework-a`

**🔶 Intermediate**: [Title](path/to/{X.Y}-L2-*.md)
- Concepts: `concept-c`, `concept-d`

## Concept Index
### Concept Name
- [file-path-1.md](file-path-1.md)
- [file-path-2.md](file-path-2.md)

## Framework Index
### Framework Name
- [file-path.md](file-path.md)

## Anti-Pattern Index
### Anti-Pattern Name
- [file-path.md](file-path.md)
```

---

### 7.4 Generate Concept Map Data

**Script**: `scripts/generate-concept-map.py`

**What it does**:
- Extracts concepts and frameworks from all markdown files
- Builds graph structure (nodes + edges)
- Infers relationships from frontmatter (prerequisites, related concepts)
- Outputs `visual-presentations/concept-map-data.json`

**Command**: `python scripts/generate-concept-map.py`

**Expected Output**:
```
📂 Scanning {N} markdown files...
✅ Created {M} nodes
✅ Created {E} edges
💾 Concept map data saved to visual-presentations/concept-map-data.json
   - {M} nodes
   - {E} edges
```

**Generated Structure**:
```json
{
  "generated": "2026-03-03T...",
  "metadata": {
    "total_nodes": 42,
    "total_edges": 38,
    "node_types": {
      "concept": 35,
      "framework": 7
    },
    "edge_types": {
      "related": 25,
      "requires": 8,
      "applies_to": 5
    }
  },
  "nodes": [
    {
      "id": 0,
      "label": "Hook System",
      "type": "concept",
      "lesson": "3.1",
      "depth": "L1",
      "chapter": "3",
      "file": "revision-notes/.../3.1-L1-hook-architecture.md",
      "tags": ["architecture", "lifecycle"]
    }
  ],
  "edges": [
    {
      "source": 5,
      "target": 2,
      "type": "requires"
    }
  ]
}
```

---

### 7.5 Execution Protocol

**When Professor Agent executes STAGE 7, follow this sequence**:

1. **Run all 4 scripts in order** (tags → fulltext → index → concept-map)
2. **Verify outputs**: Check that JSON files and INDEX.md were created
3. **Report results**: Display file paths and stats to user
4. **Handle errors gracefully**:
   - If Python not available: Skip automated indexing, warn user
   - If script errors: Log error, continue with rest of synthesis
   - If no markdown files exist yet: Scripts will output empty indexes (valid state)

**Example Execution Flow**:

```
🔧 Rebuilding discovery systems...

[1/4] Extracting tags...
✅ Tags index: 15 tags, 8 files

[2/4] Building full-text search index...
✅ Search index: 8 documents, 342 terms

[3/4] Generating master INDEX.md...
✅ INDEX.md: 1 chapter, 8 concepts, 3 frameworks

[4/4] Generating concept map data...
✅ Concept map: 12 nodes, 10 edges

💾 All discovery systems updated!
```

---

### 7.6 Fallback Strategy (No Python Available)

**If Python is not available or scripts fail**:

1. **Skip automated indexing**
2. **Warn user**:
   ```
   ⚠️ Discovery systems not updated (Python unavailable)

   To update manually:
   - Run: python scripts/extract-tags.py
   - Run: python scripts/build-search-index.py
   - Run: python scripts/generate-index.py
   - Run: python scripts/generate-concept-map.py
   ```
3. **Continue with rest of synthesis** (HTML, flashcards still generated)

---

## STAGE 8: Final Confirmation & Next Steps

After all files written successfully:

```
✅ Lesson {X.Y} complete -- 6-tier synthesis finished

**Files created**:

📚 Master Notes ({N} checkpoint parts):
  - {X.Y}-L1-{concept}.md
  - {X.Y}-L2-{concept}.md
  - {X.Y}-L{N}-{concept}.md

🌉 Context Bridge (updated):
  - context-bridge/master-cumulative.md

🎨 Visual Presentations:
  - session-{NN}-lesson-{X.Y}-{title}.html (master navigation)
  - session-{NN}-lesson-{X.Y}-L1-presentation.html
  - session-{NN}-lesson-{X.Y}-L2-presentation.html
  - session-{NN}-lesson-{X.Y}-L{N}-presentation.html

📋 Quick Reference:
  - quick-reference/lesson-{X.Y}-cheatsheet.md

🃏 Flashcards:
  - flashcards/lesson-{X.Y}-deck.json ({N} cards)

🔍 Discovery Systems (auto-updated):
  - revision-notes/INDEX.md (auto-generated)
  - search-index/tags-index.json
  - search-index/fulltext-index.json
  - visual-presentations/concept-map-data.json

---

**Next Steps**:

1. **Review the master HTML**: Open `visual-presentations/session-{NN}-lesson-{X.Y}-{title}.html` in browser
2. **Study with flashcards**: Import `flashcards/lesson-{X.Y}-deck.json` to Anki (or review online)
3. **Quick lookup**: Use `quick-reference/lesson-{X.Y}-cheatsheet.md` for rapid reference

**Continue learning?**
- Type `{X.Z}` to start next lesson: {Next Lesson Title}
- Type `Status` to see overall progress dashboard
- Type `Review {X.Y}` to quiz yourself on this lesson

**End session?**
- Context bridge saved -- you can resume anytime
```

---

## STAGE 9: Git Integration (Optional Auto-Commit & Tagging)

**Trigger**: After successful 6-tier synthesis (Stages 1-8 complete)

**Purpose**: Automatically commit lesson artifacts to version control and create a release tag

### Workflow

1. **Check if git integration is available**:
   - Verify git repository exists
   - Check if `scripts/git-auto-push.py` exists
   - Skip if either is missing (graceful degradation)

2. **Invoke auto-push script**:
   ```bash
   python3 scripts/git-auto-push.py finish {X.Y}
   ```

3. **Script handles**:
   - Auto-detect git remote
   - Stage all lesson artifacts:
     * All checkpoint part files (`{X.Y}-L*-*.md`)
     * Updated context bridge
     * Visual presentations (master + individual HTMLs)
     * Quick reference cheatsheet
     * Flashcards JSON
     * Updated INDEX.md and concept map data
     * Updated search indexes
   - Create semantic commit message (Conventional Commits format)
   - Run pre-commit quality hook (validates notes)
   - Create git tag: `lesson-{X.Y}` with message "Lesson {X.Y} complete (6-tier synthesis)"
   - Push commit and tags to remote if configured
   - Error handling and rollback

4. **User notification**:
   ```
   📦 Git auto-commit & tagging:
   - Files staged: {count}
   - Commit: "docs(lesson): complete lesson {X.Y}"
   - Tag created: lesson-{X.Y}
   - Quality hook: ✓ Passed
   - Pushed to: origin/main (with tags)
   ```

### Skip Conditions

- **No git repo**: "Git not initialized, skipping auto-commit"
- **No remote**: "Commit and tag saved locally (no remote configured)"
- **Quality failure**: "Quality checks failed, commit blocked (see pre-commit hook output)"
- **Push failure**: "Commit and tag saved locally (push failed - may need to pull first)"
- **Tag exists**: "Tag 'lesson-{X.Y}' already exists, skipping tag creation"

### User Control

- Users can disable auto-commit by removing the script
- Users can bypass quality hooks with `git commit --no-verify` (not recommended)
- Script supports `--dry-run` mode for testing
- Tags serve as lesson milestones and can trigger GitHub Actions (e.g., auto-deploy to GitHub Pages)

### Benefits

- **Version history**: Each lesson becomes a git commit with semantic message
- **Milestones**: Tags mark lesson completion for easy navigation (`git tag -l`)
- **GitHub integration**: Tags can trigger auto-deployment to GitHub Pages
- **Rollback**: Easy to revert to previous lesson state (`git checkout lesson-3.1`)
- **Collaboration**: Multiple students can fork and track their own progress

---

## EDGE CASES & HANDLING

### Edge Case 1: Finish Without Any Checkpoints

**Scenario**: User teaches entire lesson, says "Finish" without intermediate checkpoints

**Action**:
- Create single part file: `{X.Y}-L1-{primary-concept}.md` (entire lesson in one file)
- Proceed with normal 6-tier synthesis
- Metadata JSON has single checkpoint entry
- HTML timeline shows single checkpoint

### Edge Case 2: Finish Immediately After Last Checkpoint

**Scenario**: User checkpoints L3, immediately says "Finish" with no new teaching

**Action**:
- Skip creating redundant final part file
- Proceed directly to HTML generation (Stage 4)
- Use existing part files for aggregation
- Mark latest checkpoint as "Lesson Complete" in metadata

### Edge Case 3: No Visual Presentations Directory

**Action**:
- Create directory: `mkdir -p visual-presentations/`
- Proceed with normal HTML generation

---

## CONSTRAINTS

- **Aggregate HTML must cover ALL checkpoints** (read all L* files)
- **Individual checkpoint HTMLs** for each layer (focused presentations)
- **Zero information loss**: HTML, quick ref, flashcards capture everything taught
- **Consistent design**: HTML MUST use exact theme from specification
- **Quality bar**: HTML feels like polished keynote, not a document
- **Anki compatibility**: Flashcard JSON must be importable
- **Discovery updates**: Index and concept map MUST be updated

---

## SUCCESS CRITERIA

✅ Final part file created (if new content exists)
✅ Cumulative bridge marked lesson complete
✅ Master navigation HTML created with ALL checkpoint content
✅ Individual checkpoint HTMLs created (one per layer)
✅ Checkpoint timeline slide shows progression
✅ Quick reference cheatsheet generated (2-3 pages)
✅ Flashcards JSON generated (Anki-compatible)
✅ Master INDEX.md updated with new lesson
✅ Concept map data updated with new nodes
✅ User prompted with next steps (continue or end session)

---

## RELATED PROTOCOLS

- **Checkpoint**: Mid-lesson save → `checkpoint-synthesis.md`
- **Rewind**: Rollback to earlier checkpoint → `rewind-checkpoint.md`
- **End-of-Session**: Original protocol (backward compatibility) → `end-of-session-synthesis.md`
