#!/usr/bin/env python3
"""
Build Full-Text Search Index
=============================

Creates an inverted index for fast full-text search across all markdown files.

Features:
- Inverted index (word → document locations)
- TF-IDF ranking for relevance scoring
- Heading proximity boosting (words in headings ranked higher)
- Recency boosting (newer content ranked higher)
- Search snippet generation (context around matches)

Usage:
    python scripts/build-search-index.py

Output:
    search-index/fulltext-index.json
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import math


class FullTextIndexer:
    """Builds full-text search index with TF-IDF ranking."""

    def __init__(self, notes_dir: str = "revision-notes"):
        self.notes_dir = Path(notes_dir)
        self.inverted_index = defaultdict(list)  # word → [(doc_id, positions, context)]
        self.documents = {}  # doc_id → metadata
        self.doc_word_counts = defaultdict(Counter)  # doc_id → {word: count}
        self.total_docs = 0
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self) -> set:
        """Load common English stopwords to exclude from indexing."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

    def extract_text_with_metadata(self, file_path: Path) -> Tuple[str, dict]:
        """Extract text from markdown file with section metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove YAML frontmatter
            content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

            # Extract headings for proximity boosting
            headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

            # Get file modification time for recency
            mtime = file_path.stat().st_mtime

            metadata = {
                'path': str(file_path.relative_to(Path.cwd())),
                'title': headings[0] if headings else file_path.stem,
                'headings': headings,
                'mtime': mtime,
                'word_count': len(content.split())
            }

            return content, metadata

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return "", {}

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words (lowercase, alphanumeric only)."""
        # Convert to lowercase
        text = text.lower()

        # Extract words (alphanumeric + hyphens)
        words = re.findall(r'\b[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\b', text)

        # Remove stopwords and short words
        words = [w for w in words if w not in self.stopwords and len(w) >= 3]

        return words

    def index_document(self, doc_id: str, content: str, metadata: dict):
        """Index a single document."""
        words = self.tokenize(content)

        # Build word positions and contexts
        for i, word in enumerate(words):
            # Get context window (5 words before/after)
            context_start = max(0, i - 5)
            context_end = min(len(words), i + 6)
            context = ' '.join(words[context_start:context_end])

            # Check if word appears in headings (boost score)
            in_heading = any(word in self.tokenize(h) for h in metadata.get('headings', []))

            # Store position and context
            self.inverted_index[word].append({
                'doc_id': doc_id,
                'position': i,
                'context': context,
                'in_heading': in_heading
            })

            # Update word count for TF-IDF
            self.doc_word_counts[doc_id][word] += 1

        # Store document metadata
        self.documents[doc_id] = metadata

    def scan_files(self):
        """Scan all markdown files and build index."""
        if not self.notes_dir.exists():
            print(f"⚠️  Directory not found: {self.notes_dir}")
            return

        md_files = list(self.notes_dir.rglob("*.md"))

        if not md_files:
            print(f"⚠️  No markdown files found in {self.notes_dir}")
            return

        print(f"📂 Indexing {len(md_files)} markdown files...")

        for file_path in md_files:
            # Skip INDEX.md and README.md
            if file_path.name in ['INDEX.md', 'README.md']:
                continue

            content, metadata = self.extract_text_with_metadata(file_path)
            if not content:
                continue

            doc_id = str(file_path.relative_to(Path.cwd()))
            self.index_document(doc_id, content, metadata)
            self.total_docs += 1

        print(f"✅ Indexed {self.total_docs} documents")
        print(f"✅ Found {len(self.inverted_index)} unique terms")

    def compute_idf(self, word: str) -> float:
        """Compute Inverse Document Frequency for a word."""
        doc_freq = len(set(entry['doc_id'] for entry in self.inverted_index.get(word, [])))
        if doc_freq == 0:
            return 0.0
        return math.log(self.total_docs / doc_freq)

    def build_index(self) -> dict:
        """Build the complete search index structure."""
        index = {
            'generated': self._get_timestamp(),
            'total_documents': self.total_docs,
            'total_terms': len(self.inverted_index),
            'documents': {},
            'inverted_index': {}
        }

        # Add document metadata
        for doc_id, metadata in self.documents.items():
            index['documents'][doc_id] = metadata

        # Add inverted index with IDF scores
        for word, entries in sorted(self.inverted_index.items()):
            idf = self.compute_idf(word)

            # Group by document for cleaner structure
            docs_data = defaultdict(list)
            for entry in entries:
                docs_data[entry['doc_id']].append({
                    'position': entry['position'],
                    'context': entry['context'],
                    'in_heading': entry['in_heading']
                })

            index['inverted_index'][word] = {
                'idf': round(idf, 4),
                'doc_frequency': len(docs_data),
                'occurrences': {
                    doc_id: {
                        'count': len(positions),
                        'positions': positions[:3]  # Store first 3 positions only
                    }
                    for doc_id, positions in docs_data.items()
                }
            }

        return index

    def save_index(self, output_path: str = "search-index/fulltext-index.json"):
        """Save search index to JSON file."""
        index = self.build_index()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"💾 Full-text index saved to {output_path}")
        print(f"   - {index['total_documents']} documents")
        print(f"   - {index['total_terms']} unique terms")

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main execution."""
    print("="*60)
    print("  Full-Text Search Index Builder")
    print("="*60)

    indexer = FullTextIndexer(notes_dir="revision-notes")
    indexer.scan_files()
    indexer.save_index()

    print("\n✅ Search index complete!")


if __name__ == "__main__":
    main()
