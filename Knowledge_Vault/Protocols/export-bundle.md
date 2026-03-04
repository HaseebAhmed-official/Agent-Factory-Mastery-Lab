# Export Command Protocol

> **Purpose**: Package lessons/chapters into exportable bundles (PDF, HTML, ZIP, Markdown)
> **Version**: 1.0
> **Created**: 2026-03-03

---

## Command Trigger

**User types**: `Export`

**Alternative forms**: `export`, `Package`, `package`, `Bundle`

**With parameters**:
- `Export 3.1` - Export single lesson
- `Export Chapter 3` - Export entire chapter
- `Export all` - Export all completed lessons
- `Export 3.1 pdf` - Export as PDF
- `Export 3.1 html` - Export as standalone HTML

---

## Workflow

### STAGE 1: Scope & Format Selection

**If user provided scope** (e.g., `Export 3.1 pdf`):
- Parse lesson/chapter
- Parse format (pdf, html, zip, markdown)
- Skip to STAGE 2

**If no scope provided** (just `Export`):

1. **Present export scope options**:
   ```
   📦 EXPORT TOOL

   What would you like to export?

   1️⃣ SINGLE LESSON
      Package one lesson with all materials
      Example: Lesson 3.1 (notes, HTML, flashcards, quiz)

   2️⃣ FULL CHAPTER
      Package entire chapter with all lessons
      Example: Chapter 3 (12 lessons + index)

   3️⃣ ALL COMPLETED LESSONS
      Package everything you've studied so far
      Example: All lessons + progress tracking

   4️⃣ CUSTOM SELECTION
      Choose specific lessons to export
      Example: 3.1, 3.15, 3.22 only

   Your choice (1/2/3/4 or cancel):
   ```

2. **If single lesson**: Prompt "Which lesson?" (e.g., "3.1")
3. **If full chapter**: Prompt "Which chapter?" (e.g., "3")
4. **If custom**: Use AskUserQuestion with multiSelect to choose lessons

5. **Present format options**:
   ```
   📄 EXPORT FORMAT

   How would you like to export?

   1️⃣ PDF
      Polished PDF document (requires Pandoc)
      Best for: Printing, offline reading, sharing

   2️⃣ HTML (Standalone)
      Single HTML file with embedded styles
      Best for: Web viewing, interactive, no dependencies

   3️⃣ ZIP Bundle
      Complete package: markdown + HTML + PDFs + extras
      Best for: Backup, archiving, transferring

   4️⃣ Markdown Only
      Pure markdown files in folder structure
      Best for: Importing to other tools, editing

   5️⃣ ALL FORMATS
      Generate PDF + HTML + Markdown bundle
      Best for: Maximum compatibility

   Your choice (1/2/3/4/5 or cancel):
   ```

6. **User selects format**

---

### STAGE 2: Gather Export Contents

**For selected scope, collect**:

1. **Master Notes**:
   - All checkpoint files: `{X.Y}-L*-*.md`
   - Merge into single document or keep separate (user choice)

2. **Visual Presentations**:
   - Master HTML: `session-NN-lesson-{X.Y}-*.html`
   - Individual checkpoint HTMLs

3. **Quick Reference**:
   - Cheatsheet: `lesson-{X.Y}-cheatsheet.md`

4. **Flashcards**:
   - Anki deck: `lesson-{X.Y}-deck.json`

5. **Assessments** (if available):
   - Quiz: `lesson-{X.Y}-quiz.md`
   - Results: `lesson-{X.Y}-result-*.json` (latest)

6. **Metadata**:
   - Checkpoint metadata: `.checkpoint-meta.json`

7. **Extras**:
   - Context bridge excerpt (relevant sections)
   - Progress summary (if exporting multiple lessons)

**Example for Lesson 3.1**:
```
Gathered content for export:

📚 Master Notes (3 files):
  - 3.1-L1-hook-architecture.md (2,500 words)
  - 3.1-L2-custom-hooks.md (1,800 words)
  - 3.1-L3-advanced-patterns.md (1,200 words)

🎨 Visual Presentations (4 files):
  - session-01-lesson-3.1-origin-story.html (master)
  - session-01-lesson-3.1-L1-presentation.html
  - session-01-lesson-3.1-L2-presentation.html
  - session-01-lesson-3.1-L3-presentation.html

📋 Quick Reference (1 file):
  - lesson-3.1-cheatsheet.md (3 pages)

🃏 Flashcards (1 file):
  - lesson-3.1-deck.json (25 cards)

📝 Assessments (2 files):
  - lesson-3.1-quiz.md (8 questions)
  - lesson-3.1-result-20260303.json (latest score: 80%)

Total: 11 files, ~5,500 words
```

---

### STAGE 3: Execute Export (Format-Specific)

## Format 1: PDF Export

**Requirements**: Pandoc installed (`pandoc --version`)

**If Pandoc not found**:
```
⚠️ Pandoc not installed

PDF export requires Pandoc.
Install: https://pandoc.org/installing.html

Alternative: Export as HTML or Markdown instead?
```

**PDF Generation Workflow**:

1. **Merge checkpoint files**:
   - Concatenate all `{X.Y}-L*-*.md` files
   - Add page breaks between layers
   - Add table of contents
   - Add frontmatter (title, author, date)

2. **Run Pandoc**:
   ```bash
   pandoc merged-notes.md \
     --output exports/lesson-3.1-complete.pdf \
     --from markdown \
     --to pdf \
     --template templates/note-template.tex \
     --toc \
     --toc-depth=3 \
     --number-sections \
     --highlight-style tango \
     --pdf-engine=xelatex \
     -V geometry:margin=1in \
     -V fontsize=11pt \
     -V documentclass=article
   ```

3. **Add metadata page**:
   ```markdown
   ---
   title: "Lesson 3.1 - Origin Story: Complete Study Guide"
   author: "Professor Agent (Panaversity)"
   date: "2026-03-03"
   subject: "Agent Factory Part 1 - General Agents Foundations"
   keywords: [hooks, claude code, extensibility, lifecycle events]
   ---

   # Lesson 3.1: Origin Story
   ## Complete Study Guide

   **Generated**: 2026-03-03
   **Checkpoint Layers**: L1, L2, L3
   **Total Content**: 5,500 words
   **Study Time**: ~3-4 hours

   ---

   [Table of Contents auto-generated]

   ---

   [Content follows]
   ```

4. **Confirm**:
   ```
   ✅ PDF exported successfully!

   File: exports/lesson-3.1-complete.pdf
   Size: 2.3 MB
   Pages: 42

   Open PDF now? (yes/no)
   ```

---

## Format 2: HTML (Standalone)

**HTML Generation Workflow**:

1. **Create standalone HTML**:
   - Convert markdown to HTML (Pandoc or internal)
   - Embed CSS styles (no external dependencies)
   - Include syntax highlighting
   - Add navigation menu

2. **Structure**:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <title>Lesson 3.1 - Origin Story: Complete Study Guide</title>
     <style>
       /* Embedded CSS - clean professional theme */
       body { font-family: 'Georgia', serif; max-width: 800px; margin: 0 auto; padding: 20px; }
       h1 { color: #2c3e50; border-bottom: 3px solid #3498db; }
       code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
       /* ... more styles ... */
     </style>
   </head>
   <body>
     <header>
       <h1>Lesson 3.1: Origin Story</h1>
       <p class="meta">Generated: 2026-03-03 | Study Guide</p>
       <nav>
         <a href="#L1">L1: Fundamentals</a> |
         <a href="#L2">L2: Intermediate</a> |
         <a href="#L3">L3: Advanced</a>
       </nav>
     </header>

     <main>
       <section id="L1">
         <h2>Layer 1: Fundamentals</h2>
         <!-- L1 content -->
       </section>

       <section id="L2">
         <h2>Layer 2: Intermediate</h2>
         <!-- L2 content -->
       </section>

       <section id="L3">
         <h2>Layer 3: Advanced</h2>
         <!-- L3 content -->
       </section>
     </main>

     <footer>
       <p>Generated by Professor Agent | Panaversity Agent Factory Part 1</p>
     </footer>
   </body>
   </html>
   ```

3. **Run conversion** (using Pandoc):
   ```bash
   pandoc merged-notes.md \
     --output exports/lesson-3.1-complete.html \
     --from markdown \
     --to html5 \
     --standalone \
     --self-contained \
     --css templates/note-style.css \
     --toc \
     --toc-depth=3 \
     --highlight-style tango
   ```

4. **Confirm**:
   ```
   ✅ HTML exported successfully!

   File: exports/lesson-3.1-complete.html
   Size: 450 KB (standalone, no dependencies)

   Open in browser? (yes/no)
   ```

---

## Format 3: ZIP Bundle

**Bundle Contents**:

```
lesson-3.1-export-bundle.zip
├── README.md (what's in this bundle, how to use)
├── master-notes/
│   ├── 3.1-L1-hook-architecture.md
│   ├── 3.1-L2-custom-hooks.md
│   └── 3.1-L3-advanced-patterns.md
├── merged/
│   └── 3.1-complete.md (all layers merged)
├── presentations/
│   ├── lesson-3.1-master.html
│   ├── lesson-3.1-L1.html
│   ├── lesson-3.1-L2.html
│   └── lesson-3.1-L3.html
├── quick-reference/
│   └── lesson-3.1-cheatsheet.md
├── flashcards/
│   └── lesson-3.1-deck.json
├── assessments/
│   ├── lesson-3.1-quiz.md
│   └── lesson-3.1-result-latest.json
├── pdf/ (if Pandoc available)
│   └── 3.1-complete.pdf
└── metadata/
    ├── .checkpoint-meta.json
    └── export-manifest.json
```

**README.md** (auto-generated):

```markdown
# Lesson 3.1 - Origin Story: Export Bundle

**Generated**: 2026-03-03 by Professor Agent
**Course**: Agent Factory Part 1 - General Agents Foundations (AIAF-2026)
**Lesson**: 3.1 - Origin Story

---

## What's Included

### 📚 Master Notes (3 files)
- `master-notes/3.1-L1-hook-architecture.md` - Fundamentals (2,500 words)
- `master-notes/3.1-L2-custom-hooks.md` - Intermediate (1,800 words)
- `master-notes/3.1-L3-advanced-patterns.md` - Advanced (1,200 words)

### 📄 Merged Document
- `merged/3.1-complete.md` - All layers in one file (5,500 words)

### 🎨 Visual Presentations (4 HTML files)
- `presentations/lesson-3.1-master.html` - Interactive master presentation
- `presentations/lesson-3.1-L1.html` - L1 focused presentation
- `presentations/lesson-3.1-L2.html` - L2 focused presentation
- `presentations/lesson-3.1-L3.html` - L3 focused presentation

### 📋 Quick Reference
- `quick-reference/lesson-3.1-cheatsheet.md` - 3-page summary

### 🃏 Flashcards
- `flashcards/lesson-3.1-deck.json` - 25 Anki cards

### 📝 Assessments
- `assessments/lesson-3.1-quiz.md` - 8 questions with rubrics
- `assessments/lesson-3.1-result-latest.json` - Latest quiz score (80%)

### 📄 PDF (if available)
- `pdf/3.1-complete.pdf` - Polished PDF (42 pages)

---

## How to Use

**For studying**:
1. Start with `presentations/lesson-3.1-master.html` (overview)
2. Study `master-notes/` (deep dive)
3. Review `quick-reference/lesson-3.1-cheatsheet.md` (summary)
4. Test yourself with `assessments/lesson-3.1-quiz.md`
5. Use flashcards for spaced repetition

**For importing**:
- **Obsidian**: Import `master-notes/` folder
- **Notion**: Convert markdown to Notion format
- **Anki**: Import `flashcards/lesson-3.1-deck.json`

**For sharing**:
- Share entire ZIP bundle
- Or share individual files as needed

---

## Metadata

- **Checkpoint Layers**: 3 (L1, L2, L3)
- **Total Words**: 5,500
- **Estimated Study Time**: 3-4 hours
- **Quiz Performance**: 32/40 points (80%, B+)
- **Exported**: 2026-03-03

---

**Generated by**: Professor Agent
**Course**: Panaversity Agent Factory Part 1
**License**: Personal educational use

---
```

**ZIP Creation**:
```bash
cd exports
zip -r lesson-3.1-export-bundle.zip lesson-3.1-export-bundle/
```

**Confirm**:
```
✅ ZIP bundle created successfully!

File: exports/lesson-3.1-export-bundle.zip
Size: 3.2 MB (compressed)
Contents: 14 files

Extract and use on any device.
```

---

## Format 4: Markdown Only

**Markdown Export** (simple folder copy):

```
exports/lesson-3.1-markdown/
├── 3.1-L1-hook-architecture.md
├── 3.1-L2-custom-hooks.md
├── 3.1-L3-advanced-patterns.md
├── 3.1-complete.md (merged)
├── lesson-3.1-cheatsheet.md
└── README.md (export info)
```

**No conversion needed**, just copy files.

**Confirm**:
```
✅ Markdown files exported!

Folder: exports/lesson-3.1-markdown/
Files: 5 markdown files

Import to Obsidian, Notion, or any markdown editor.
```

---

## Format 5: All Formats

**Generate all 4 formats in one bundle**:

```
exports/lesson-3.1-all-formats/
├── markdown/
│   └── [markdown files]
├── html/
│   └── 3.1-complete.html
├── pdf/
│   └── 3.1-complete.pdf
├── presentations/
│   └── [HTML presentations]
├── flashcards/
│   └── lesson-3.1-deck.json
└── README.md
```

**Confirm**:
```
✅ ALL FORMATS exported!

Folder: exports/lesson-3.1-all-formats/
Formats: Markdown, HTML, PDF, Presentations
Size: 5.8 MB

Maximum compatibility. Use any format you prefer.
```

---

### STAGE 4: Post-Export Actions

**After export completes**:

1. **Open export location**:
   ```bash
   open exports/  # macOS
   xdg-open exports/  # Linux
   explorer exports\  # Windows
   ```

2. **Present summary**:
   ```
   ═══════════════════════════════════════════════════════
   EXPORT COMPLETE
   ═══════════════════════════════════════════════════════

   Lesson: 3.1 - Origin Story
   Format: ZIP Bundle
   Output: exports/lesson-3.1-export-bundle.zip

   ═══════════════════════════════════════════════════════

   Contents:
   - 3 master note files (L1, L2, L3)
   - 4 HTML presentations
   - 1 quick reference cheatsheet
   - 1 flashcard deck (25 cards)
   - 1 quiz with results
   - 1 PDF (42 pages)

   Total size: 3.2 MB (compressed)

   ═══════════════════════════════════════════════════════

   Next Steps:
   1. Extract ZIP bundle
   2. Read README.md for usage guide
   3. Import to your preferred tools
   4. Share with study group (if desired)

   ═══════════════════════════════════════════════════════
   ```

3. **Offer next actions**:
   ```
   What would you like to do?

   1. Open export folder
   2. Export another lesson
   3. Continue studying
   4. End session
   ```

---

## Export Scripts

**Create export helper scripts**:

### 1. `scripts/export-to-pdf.sh`

```bash
#!/bin/bash
# Export lesson notes to PDF using Pandoc
# Usage: ./export-to-pdf.sh 3.1

LESSON=$1
if [ -z "$LESSON" ]; then
  echo "Usage: ./export-to-pdf.sh <lesson>"
  echo "Example: ./export-to-pdf.sh 3.1"
  exit 1
fi

# Find checkpoint files
FILES=$(find revision-notes -name "${LESSON}-L*.md" | sort)

if [ -z "$FILES" ]; then
  echo "Error: No checkpoint files found for lesson $LESSON"
  exit 1
fi

# Merge files
echo "Merging checkpoint files..."
cat $FILES > /tmp/merged-${LESSON}.md

# Convert to PDF
echo "Converting to PDF..."
pandoc /tmp/merged-${LESSON}.md \
  --output exports/lesson-${LESSON}-complete.pdf \
  --from markdown \
  --to pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --highlight-style tango \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt

echo "✅ PDF exported: exports/lesson-${LESSON}-complete.pdf"
```

### 2. `scripts/export-to-html.sh`

```bash
#!/bin/bash
# Export lesson notes to standalone HTML using Pandoc
# Usage: ./export-to-html.sh 3.1

LESSON=$1
if [ -z "$LESSON" ]; then
  echo "Usage: ./export-to-html.sh <lesson>"
  exit 1
fi

FILES=$(find revision-notes -name "${LESSON}-L*.md" | sort)

if [ -z "$FILES" ]; then
  echo "Error: No checkpoint files found for lesson $LESSON"
  exit 1
fi

echo "Merging checkpoint files..."
cat $FILES > /tmp/merged-${LESSON}.md

echo "Converting to HTML..."
pandoc /tmp/merged-${LESSON}.md \
  --output exports/lesson-${LESSON}-complete.html \
  --from markdown \
  --to html5 \
  --standalone \
  --self-contained \
  --toc \
  --toc-depth=3 \
  --highlight-style tango

echo "✅ HTML exported: exports/lesson-${LESSON}-complete.html"
```

**Make scripts executable**:
```bash
chmod +x scripts/export-to-pdf.sh
chmod +x scripts/export-to-html.sh
```

---

## Edge Cases & Error Handling

### Case 1: Pandoc Not Installed

**Scenario**: User requests PDF export but Pandoc not found

**Handling**:
```
⚠️ Pandoc not installed

PDF export requires Pandoc.

Installation:
- macOS: brew install pandoc
- Linux: sudo apt install pandoc
- Windows: Download from https://pandoc.org

Alternative formats available:
1. HTML (no dependencies)
2. Markdown (no conversion)
3. ZIP bundle (includes HTML)

Choose alternative? (1/2/3 or cancel)
```

### Case 2: Export Folder Doesn't Exist

**Scenario**: `exports/` directory missing

**Handling**:
1. Auto-create directory:
   ```bash
   mkdir -p exports
   ```
2. Continue export

### Case 3: File Name Collision

**Scenario**: `lesson-3.1-complete.pdf` already exists

**Handling**:
```
⚠️ File already exists

File: exports/lesson-3.1-complete.pdf

Options:
1. Overwrite (replace existing)
2. Keep both (add timestamp: lesson-3.1-complete-20260303.pdf)
3. Cancel export

Your choice (1/2/3):
```

### Case 4: Large Export (>100MB)

**Scenario**: Exporting all completed lessons produces huge bundle

**Handling**:
```
⚠️ Large export detected

Estimated size: 150 MB
This may take 2-3 minutes.

Recommendations:
- Export by chapter instead (smaller bundles)
- Export specific lessons only

Continue with large export? (yes/no)
```

### Case 5: Missing Checkpoint Files

**Scenario**: Lesson has no checkpoint files (not completed yet)

**Handling**:
```
❌ Cannot export Lesson 3.5

No checkpoint files found. Lesson not yet studied.

Available lessons for export: 3.1, 3.15, 3.17, 3.22, 3.23
```

---

## Integration with CLAUDE.md

**Add to CLAUDE.md under "Commands" section**:

```markdown
### Export Command

**Usage**: `Export [scope] [format]`

**Purpose**: Package lessons/chapters into exportable bundles

**Examples**:
- `Export` - Choose scope and format interactively
- `Export 3.1` - Export single lesson (all formats)
- `Export Chapter 3` - Export entire chapter
- `Export 3.1 pdf` - Export as PDF only
- `Export all zip` - Export all lessons as ZIP

**Formats**:
- **PDF**: Polished document (requires Pandoc)
- **HTML**: Standalone web page (no dependencies)
- **ZIP**: Complete bundle (all materials)
- **Markdown**: Pure markdown files
- **All Formats**: Generate all formats

**Use cases**:
- Backup study materials
- Share notes with study group
- Print for offline review
- Import to other tools (Obsidian, Notion)
- Archive completed lessons
```

---

## Template Files

**Create export templates**:

### 1. `templates/note-template.tex` (LaTeX for PDF)

```latex
% Pandoc LaTeX template for lesson exports
\documentclass[$if(fontsize)$$fontsize$,$endif$article]{article}

% Packages
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{fancyhdr}

% Colors
\definecolor{codecolor}{HTML}{f4f4f4}

% Code highlighting
\lstset{
  backgroundcolor=\color{codecolor},
  basicstyle=\ttfamily\small,
  breaklines=true
}

% Headers/Footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{$title$}
\fancyhead[R]{\thepage}

\begin{document}

$if(title)$
\title{$title$}
$endif$

$if(author)$
\author{$author$}
$endif$

$if(date)$
\date{$date$}
$endif$

\maketitle

$if(toc)$
\tableofcontents
\newpage
$endif$

$body$

\end{document}
```

### 2. `templates/note-style.css` (CSS for HTML)

```css
/* Clean professional theme for exported HTML */

body {
  font-family: 'Georgia', 'Times New Roman', serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  line-height: 1.6;
  color: #333;
  background: #fff;
}

h1, h2, h3, h4 {
  font-family: 'Helvetica Neue', 'Arial', sans-serif;
  color: #2c3e50;
  margin-top: 1.5em;
}

h1 {
  border-bottom: 3px solid #3498db;
  padding-bottom: 0.3em;
}

h2 {
  border-bottom: 1px solid #bdc3c7;
  padding-bottom: 0.2em;
}

code {
  background: #f4f4f4;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 0.9em;
}

pre {
  background: #f4f4f4;
  border-left: 4px solid #3498db;
  padding: 15px;
  overflow-x: auto;
  border-radius: 4px;
}

pre code {
  background: none;
  padding: 0;
}

blockquote {
  border-left: 4px solid #3498db;
  padding-left: 15px;
  margin-left: 0;
  color: #555;
  font-style: italic;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px 12px;
  text-align: left;
}

th {
  background: #3498db;
  color: white;
  font-weight: bold;
}

tr:nth-child(even) {
  background: #f9f9f9;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

---

## Export Manifest Schema

**File**: `export-manifest.json` (included in exports)

```json
{
  "export_version": "1.0",
  "generated_at": "2026-03-03T16:45:00Z",
  "scope": "lesson",
  "lesson": "3.1",
  "title": "Origin Story",
  "formats": ["markdown", "html", "pdf", "zip"],
  "contents": {
    "master_notes": [
      "3.1-L1-hook-architecture.md",
      "3.1-L2-custom-hooks.md",
      "3.1-L3-advanced-patterns.md"
    ],
    "presentations": [
      "lesson-3.1-master.html",
      "lesson-3.1-L1.html",
      "lesson-3.1-L2.html",
      "lesson-3.1-L3.html"
    ],
    "quick_reference": ["lesson-3.1-cheatsheet.md"],
    "flashcards": ["lesson-3.1-deck.json"],
    "assessments": [
      "lesson-3.1-quiz.md",
      "lesson-3.1-result-latest.json"
    ]
  },
  "stats": {
    "total_files": 14,
    "total_words": 5500,
    "checkpoint_layers": 3,
    "flashcard_count": 25,
    "quiz_questions": 8,
    "quiz_score": "80%"
  }
}
```

---

## Summary

**Export command provides**:
- ✅ Multi-format export (PDF, HTML, ZIP, Markdown)
- ✅ Single lesson or full chapter bundling
- ✅ Complete materials package (notes + presentations + extras)
- ✅ Auto-generated README for bundles
- ✅ Helper scripts for command-line export
- ✅ Metadata tracking

**User experience**:
1. Type `Export [scope] [format]`
2. Select what to export and how
3. Wait ~30-60 seconds for generation
4. Receive bundle ready for use/sharing
5. Import to any tool or device

**Portable, shareable, professional-quality exports.**

---

**END OF PROTOCOL**
