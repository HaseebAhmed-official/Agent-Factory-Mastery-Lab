# Agent Factory Part 1: Elite Tutoring System

Professional learning management system for Panaversity's **"Agent Factory Part 1: General Agents Foundations"** (AIAF-2026) course.

## Overview

This repository implements a comprehensive tutoring system powered by Claude Code, featuring:
- **Progressive checkpoint system** with semantic versioning (L1/L2/L3 depth layers)
- **Multi-format outputs**: Revision notes, HTML presentations, flashcards, quick references
- **Automated workflows**: Git integration, search indexing, discovery systems
- **Spaced repetition support**: Anki-compatible flashcard exports

## Quick Start

1. **System Instructions**: See `CLAUDE.md` for complete system behavior
2. **User Guides**: Browse `guide/` for checkpoint system, git integration, advanced features
3. **Start Learning**: Launch Claude Code and begin with any lesson

## Commands

- **`Checkpoint`** - Save progress mid-lesson, clear context, resume fresh
- **`Finish`** - Complete lesson with full synthesis (notes + HTML + flashcards + quick ref)
- **`Rewind`** - Rollback to previous checkpoint, explore alternative paths
- **`Status`** - View progress dashboard with metrics and recommendations
- **`Sync`** - Discover new lessons from curriculum website
- **`Review {X.Y}`** - Quiz yourself on completed lesson
- **`Export {X.Y}`** - Bundle lesson for sharing (PDF/HTML/ZIP)

## Directory Structure

```
/
├── CLAUDE.md                   # Main system instructions (AI behavior)
├── curriculum-manifest.json    # Course structure metadata
├── guide/                      # User-facing documentation
│   ├── CHECKPOINT-SYSTEM-README.md
│   ├── GIT-INTEGRATION-GUIDE.md
│   ├── GITHUB-PAGES-SETUP.md
│   ├── OBSIDIAN-GUIDE.md
│   └── PHASE-5-EXTENSIONS-GUIDE.md
├── dev-docs/                   # Development documentation
│   ├── IMPLEMENTATION-PROGRESS.md
│   └── SYSTEM-COMPLETE.md
├── Knowledge_Vault/            # Teaching protocols, curriculum, frameworks
├── revision-notes/             # Lesson notes (generated via Checkpoint/Finish)
├── context-bridge/             # Session state files (cumulative bridges)
├── visual-presentations/       # Interactive HTML presentations
├── quick-reference/            # Condensed cheatsheets (2-3 pages)
├── flashcards/                 # Anki-compatible flashcard decks
├── exercises/                  # Hands-on practice exercises
├── quiz-bank/                  # Assessment questions
├── progress-tracking/          # Study metrics and analytics
├── scripts/                    # Automation scripts (search, export, sync)
├── search-index/               # Full-text and tag indexes (auto-generated)
└── templates/                  # File templates for generation
```

## Workflows

### Learning a Lesson

1. **Start**: User requests lesson (e.g., "Teach me lesson 3.17")
2. **Learn**: Professor Agent teaches using TEACH cycle (Terminology → Explain → Analogize → Check → Hands-On)
3. **Checkpoint**: Save progress at semantic boundaries (mid-lesson)
4. **Finish**: Complete lesson → generates notes, HTML, flashcards, quick ref
5. **Review**: Quiz yourself later with `Review 3.17`

### Checkpoint System

- **L1 (Fundamentals)**: Core concepts, essential vocabulary, basic patterns
- **L2 (Intermediate)**: Advanced patterns, integration, composition
- **L3 (Advanced)**: Edge cases, failure modes, strategic thinking

Each checkpoint creates versioned part files: `{X.Y}-L{depth}-{semantic-concept}.md`

### Git Integration (Automatic)

- **On Checkpoint**: Auto-commit checkpoint files with semantic messages
- **On Finish**: Auto-tag lesson completion (`lesson-{X.Y}`), push to remote
- **Quality Gates**: Pre-commit hooks validate checkpoint quality (70/100 minimum)

## Features

### Content Generation
- Master lesson documentation (markdown)
- Interactive HTML presentations (slide-based, arrow-key navigation)
- Quick reference cheatsheets (2-3 pages, condensed)
- Anki-compatible flashcard decks (spaced repetition)
- Cumulative context bridges (session state preservation)

### Discovery Systems
- Full-text search index (TF-IDF ranking)
- Tag-based navigation
- Concept map visualization (interactive graph)
- Auto-generated master INDEX.md

### Export & Sharing
- PDF export (via pandoc)
- HTML export (standalone)
- Anki .apkg export (flashcards)
- Lesson bundles (ZIP)

### Analytics (Optional)
- Progress tracking dashboard
- Study time estimation
- Streak tracking
- Performance metrics

## Technology Stack

- **AI**: Claude Code (Sonnet 4.5)
- **Languages**: Python 3.7+, Bash
- **Dependencies**: PyYAML, pandoc (optional)
- **Version Control**: Git
- **Flashcards**: Anki-compatible JSON

## Documentation

- **User Guides**: See `guide/` directory
- **System Behavior**: See `CLAUDE.md`
- **Development Status**: See `dev-docs/`
- **Script Documentation**: See `scripts/README.md`

## Getting Started

1. Open this project in Claude Code
2. Say: "Start with lesson 3.1" (or any lesson)
3. Professor Agent will begin teaching
4. Use `Checkpoint` to save progress mid-lesson
5. Use `Finish` when lesson complete

## Support

For issues or questions:
- Check `guide/` documentation
- Review `CLAUDE.md` for system behavior
- Use `/help` command in Claude Code

---

**Built for**: Panaversity Agent Factory Part 1 (AIAF-2026)
**Powered by**: Claude Code (Anthropic)
**Version**: 1.0
