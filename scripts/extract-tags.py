#!/usr/bin/env python3
"""
Extract Tags from YAML Frontmatter
===================================

Scans all markdown files in revision-notes/ for YAML frontmatter,
extracts tags, and builds a tags-index.json mapping tags to files.

Features:
- Auto-discovery of tags from frontmatter
- Related tags inference (co-occurrence analysis)
- Tag frequency ranking
- File metadata extraction

Usage:
    python scripts/extract-tags.py

Output:
    search-index/tags-index.json
"""

import os
import json
import yaml
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set
import re


class TagExtractor:
    """Extracts tags from markdown files with YAML frontmatter."""

    def __init__(self, notes_dir: str = "revision-notes"):
        self.notes_dir = Path(notes_dir)
        self.tags_index = defaultdict(list)
        self.tag_frequencies = Counter()
        self.tag_cooccurrence = defaultdict(Counter)
        self.file_metadata = {}

    def extract_frontmatter(self, file_path: Path) -> dict:
        """Extract YAML frontmatter from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for YAML frontmatter (--- ... ---)
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter if isinstance(frontmatter, dict) else {}

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return {}

    def extract_tags_from_frontmatter(self, frontmatter: dict) -> List[str]:
        """Extract tags from frontmatter (handles multiple formats)."""
        tags = []

        # Format 1: tags: [tag1, tag2, tag3]
        if 'tags' in frontmatter:
            if isinstance(frontmatter['tags'], list):
                tags.extend([str(t).lower().strip() for t in frontmatter['tags']])
            elif isinstance(frontmatter['tags'], str):
                # Format 2: tags: "tag1, tag2, tag3"
                tags.extend([t.strip().lower() for t in frontmatter['tags'].split(',')])

        # Format 3: tag: single_tag
        if 'tag' in frontmatter:
            tags.append(str(frontmatter['tag']).lower().strip())

        # Format 4: keywords: [...]
        if 'keywords' in frontmatter:
            if isinstance(frontmatter['keywords'], list):
                tags.extend([str(k).lower().strip() for k in frontmatter['keywords']])

        return list(set(tags))  # Deduplicate

    def extract_metadata(self, frontmatter: dict, file_path: Path) -> dict:
        """Extract file metadata from frontmatter."""
        return {
            'title': frontmatter.get('title', file_path.stem),
            'lesson': frontmatter.get('lesson', ''),
            'depth': frontmatter.get('depth', ''),
            'concepts': frontmatter.get('concepts', []),
            'frameworks': frontmatter.get('frameworks', []),
            'anti_patterns': frontmatter.get('anti_patterns', []),
        }

    def scan_files(self):
        """Scan all markdown files in revision-notes directory."""
        if not self.notes_dir.exists():
            print(f"⚠️  Directory not found: {self.notes_dir}")
            return

        md_files = list(self.notes_dir.rglob("*.md"))

        if not md_files:
            print(f"⚠️  No markdown files found in {self.notes_dir}")
            return

        print(f"📂 Scanning {len(md_files)} markdown files...")

        for file_path in md_files:
            # Skip INDEX.md and README.md
            if file_path.name in ['INDEX.md', 'README.md']:
                continue

            frontmatter = self.extract_frontmatter(file_path)
            if not frontmatter:
                continue

            tags = self.extract_tags_from_frontmatter(frontmatter)
            if not tags:
                continue

            # Store metadata
            relative_path = str(file_path.relative_to(Path.cwd()))
            self.file_metadata[relative_path] = self.extract_metadata(frontmatter, file_path)

            # Build tags index
            for tag in tags:
                self.tags_index[tag].append({
                    'file': relative_path,
                    'title': self.file_metadata[relative_path]['title'],
                    'lesson': self.file_metadata[relative_path]['lesson'],
                    'depth': self.file_metadata[relative_path]['depth'],
                })
                self.tag_frequencies[tag] += 1

            # Build co-occurrence matrix (for related tags)
            for i, tag1 in enumerate(tags):
                for tag2 in tags[i+1:]:
                    self.tag_cooccurrence[tag1][tag2] += 1
                    self.tag_cooccurrence[tag2][tag1] += 1

        print(f"✅ Found {len(self.tags_index)} unique tags")

    def compute_related_tags(self, tag: str, top_n: int = 5) -> List[str]:
        """Find related tags based on co-occurrence."""
        if tag not in self.tag_cooccurrence:
            return []

        related = self.tag_cooccurrence[tag].most_common(top_n)
        return [t for t, count in related]

    def build_index(self) -> dict:
        """Build the complete tags index structure."""
        index = {
            'generated': self._get_timestamp(),
            'total_tags': len(self.tags_index),
            'total_files': len(self.file_metadata),
            'tags': {}
        }

        for tag, files in sorted(self.tags_index.items()):
            index['tags'][tag] = {
                'frequency': self.tag_frequencies[tag],
                'files': files,
                'related_tags': self.compute_related_tags(tag, top_n=5)
            }

        return index

    def save_index(self, output_path: str = "search-index/tags-index.json"):
        """Save tags index to JSON file."""
        index = self.build_index()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"💾 Tags index saved to {output_path}")
        print(f"   - {index['total_tags']} tags")
        print(f"   - {index['total_files']} files")

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main execution."""
    print("="*60)
    print("  Tag Extraction Script")
    print("="*60)

    extractor = TagExtractor(notes_dir="revision-notes")
    extractor.scan_files()
    extractor.save_index()

    print("\n✅ Tag extraction complete!")


if __name__ == "__main__":
    main()
