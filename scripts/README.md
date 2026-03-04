# Search & Discovery Scripts

This directory contains automated scripts for building search indexes and discovery systems.

## Scripts Overview

| Script | Purpose | Output | When to Run |
|--------|---------|--------|-------------|
| `extract-tags.py` | Extract tags from YAML frontmatter | `search-index/tags-index.json` | After Finish |
| `build-search-index.py` | Build full-text search index | `search-index/fulltext-index.json` | After Finish |
| `generate-index.py` | Auto-generate master INDEX.md | `revision-notes/INDEX.md` | After Finish |
| `generate-concept-map.py` | Build concept map graph data | `visual-presentations/concept-map-data.json` | After Finish |

## Installation

### Prerequisites

```bash
# Python 3.7+
python --version

# Install dependencies
pip install pyyaml
```

## Usage

### Automatic (Recommended)

All scripts are **automatically executed** when you use the `Finish` command in Professor Agent. You don't need to run them manually.

### Manual Execution

If you need to rebuild indexes manually (e.g., after editing notes):

```bash
# Run all scripts in sequence
python scripts/extract-tags.py
python scripts/build-search-index.py
python scripts/generate-index.py
python scripts/generate-concept-map.py
```

Or run individual scripts:

```bash
# Update tags index only
python scripts/extract-tags.py

# Update full-text search index only
python scripts/build-search-index.py

# Regenerate master INDEX.md only
python scripts/generate-index.py

# Update concept map data only
python scripts/generate-concept-map.py
```

## Script Details

### 1. extract-tags.py

**Purpose**: Extract tags from YAML frontmatter and build tags index.

**Features**:
- Scans all markdown files in `revision-notes/`
- Extracts tags from frontmatter (`tags`, `tag`, `keywords` fields)
- Builds co-occurrence matrix for related tags
- Computes tag frequencies

**Output Structure** (`search-index/tags-index.json`):
```json
{
  "generated": "2026-03-03T...",
  "total_tags": 25,
  "total_files": 12,
  "tags": {
    "hooks": {
      "frequency": 5,
      "files": [
        {
          "file": "revision-notes/.../3.1-L1-hook-architecture.md",
          "title": "Hook Architecture",
          "lesson": "3.1",
          "depth": "L1"
        }
      ],
      "related_tags": ["architecture", "lifecycle", "callbacks"]
    }
  }
}
```

**Use Cases**:
- Tag-based search: `Search tag:hooks` → instant file list
- Discover related concepts: `hooks` → `architecture`, `lifecycle`
- Tag frequency analysis

---

### 2. build-search-index.py

**Purpose**: Build full-text inverted index for fast keyword search.

**Features**:
- Tokenizes all markdown content (removes stopwords)
- Builds inverted index (word → document positions)
- Computes TF-IDF scores for relevance ranking
- Generates search snippets (context around matches)
- Heading proximity boosting (words in headings rank higher)
- Recency boosting (newer content ranks higher)

**Output Structure** (`search-index/fulltext-index.json`):
```json
{
  "generated": "2026-03-03T...",
  "total_documents": 12,
  "total_terms": 458,
  "documents": {
    "revision-notes/.../3.1-L1-hook-architecture.md": {
      "path": "...",
      "title": "Hook Architecture",
      "headings": ["Hook System", "Lifecycle"],
      "mtime": 1709481234.5,
      "word_count": 1250
    }
  },
  "inverted_index": {
    "lifecycle": {
      "idf": 1.2345,
      "doc_frequency": 3,
      "occurrences": {
        "revision-notes/.../3.1-L1-hook-architecture.md": {
          "count": 8,
          "positions": [
            {
              "position": 42,
              "context": "...hook system lifecycle begins when...",
              "in_heading": true
            }
          ]
        }
      }
    }
  }
}
```

**Use Cases**:
- Full-text keyword search with ranking
- Context snippet generation
- Relevance scoring (TF-IDF)

---

### 3. generate-index.py

**Purpose**: Auto-generate master `INDEX.md` from markdown frontmatter.

**Features**:
- Scans all markdown files in `revision-notes/`
- Extracts metadata from YAML frontmatter
- Builds hierarchical structure (Chapter → Module → Lesson)
- Creates concept, framework, and anti-pattern indexes
- **Overwrites** `revision-notes/INDEX.md`

**Generated Sections**:
1. Table of Contents
2. Hierarchical Lesson Structure
3. Concept Index (alphabetical)
4. Framework Index (alphabetical)
5. Anti-Pattern Index (alphabetical)

**Use Cases**:
- Quick navigation to lessons
- Concept-to-file mapping
- Discover all usages of a concept

---

### 4. generate-concept-map.py

**Purpose**: Build graph data for interactive concept map visualization.

**Features**:
- Extracts concepts and frameworks from frontmatter
- Builds graph structure (nodes + edges)
- Infers relationships from frontmatter fields:
  - `prerequisites`: Creates "requires" edges
  - `related_concepts`: Creates "related" edges
  - Frameworks → concepts: Creates "applies_to" edges
- Co-located concepts: Creates "related" edges

**Output Structure** (`visual-presentations/concept-map-data.json`):
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

**Use Cases**:
- Interactive concept map visualization (`visual-presentations/concept-map.html`)
- Discover concept dependencies
- Filter by lesson, depth, or type

---

## Frontmatter Requirements

For scripts to work correctly, markdown files should include YAML frontmatter:

```yaml
---
title: "Hook Architecture"
lesson: "3.1"
depth: "L1"
chapter: "3"
module: "General Agents"
concepts:
  - Hook System
  - Lifecycle Management
  - Callback Registration
frameworks:
  - TEACH Framework
  - What Goes Wrong Framework
anti_patterns:
  - Skipping Hook Registration
  - Blocking Hook Execution
tags:
  - hooks
  - architecture
  - lifecycle
prerequisites:
  - Agent Basics
related_concepts:
  - Event Loop
  - Async Patterns
---
```

### Required Fields

- `title`: Lesson title (string)
- `lesson`: Lesson number (e.g., "3.1")
- `depth`: Layer depth ("L1", "L2", "L3")

### Optional Fields

- `chapter`: Chapter number or name
- `module`: Module name
- `concepts`: List of concepts taught
- `frameworks`: List of frameworks introduced
- `anti_patterns`: List of anti-patterns discussed
- `tags`: List of tags for categorization
- `prerequisites`: List of prerequisite concepts
- `related_concepts`: List of related concepts

---

## Troubleshooting

### Script fails with "No module named 'yaml'"

**Fix**:
```bash
pip install pyyaml
```

### No files found / empty indexes

**Cause**: No markdown files with frontmatter in `revision-notes/`

**Fix**: Complete a lesson with the `Finish` command first. This will create markdown files with proper frontmatter.

### INDEX.md not updating

**Cause**: Script may have failed silently

**Fix**: Run manually with verbose output:
```bash
python scripts/generate-index.py
```

### Concept map shows no nodes

**Cause**: Frontmatter missing `concepts` field

**Fix**: Add `concepts: [...]` to YAML frontmatter in your markdown files.

---

## Integration with Professor Agent

These scripts are automatically called during the **Finish** command workflow:

1. User types `Finish`
2. Professor Agent executes 6-tier synthesis
3. **STAGE 7**: Discovery System Updates (automated)
   - Runs `extract-tags.py`
   - Runs `build-search-index.py`
   - Runs `generate-index.py`
   - Runs `generate-concept-map.py`
4. Reports results to user

**No manual intervention needed** when using Professor Agent's `Finish` command.

---

## Future Enhancements (Phase 3+)

Planned for future phases:

- **Search query interface**: Interactive CLI for searching indexes
- **Curriculum sync**: Auto-discover new lessons from official website
- **Validation**: Check frontmatter completeness before indexing
- **Export to Algolia/ElasticSearch**: Full-featured search backend
- **Anki flashcard export**: Convert JSON flashcards to `.apkg` format

---

## See Also

- [guide/CHECKPOINT-SYSTEM-README.md](../guide/CHECKPOINT-SYSTEM-README.md) - Checkpoint system overview
- [dev-docs/IMPLEMENTATION-PROGRESS.md](../dev-docs/IMPLEMENTATION-PROGRESS.md) - Implementation phases
- [Knowledge_Vault/Protocols/finish-synthesis.md](../Knowledge_Vault/Protocols/finish-synthesis.md) - Finish protocol
