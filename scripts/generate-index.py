#!/usr/bin/env python3
"""
Generate Master INDEX.md
=========================

Auto-generates revision-notes/INDEX.md from YAML frontmatter in all markdown files.

Features:
- Hierarchical structure (Chapter → Module → Lesson)
- Concept extraction from frontmatter
- Framework listings
- Anti-pattern mappings
- Auto-sorted by lesson number

Usage:
    python scripts/generate-index.py

Output:
    revision-notes/INDEX.md (overwrites existing)
"""

import os
import json
import yaml
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List


class IndexGenerator:
    """Generates master INDEX.md from markdown files."""

    def __init__(self, notes_dir: str = "revision-notes"):
        self.notes_dir = Path(notes_dir)
        self.chapters = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.all_concepts = defaultdict(list)  # concept → [files]
        self.all_frameworks = defaultdict(list)  # framework → [files]
        self.all_anti_patterns = defaultdict(list)  # anti-pattern → [files]

    def extract_frontmatter(self, file_path: Path) -> dict:
        """Extract YAML frontmatter from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for YAML frontmatter
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter if isinstance(frontmatter, dict) else {}

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return {}

    def parse_lesson_number(self, lesson_str: str) -> tuple:
        """Parse lesson string into (chapter, lesson) for sorting."""
        # Examples: "3.1", "3.15", "3.17"
        match = re.match(r'(\d+)\.(\d+)', str(lesson_str))
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (999, 999)  # Unknown lessons sort last

    def scan_files(self):
        """Scan all markdown files and extract metadata."""
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

            # Extract metadata
            chapter = frontmatter.get('chapter', 'Unknown')
            module = frontmatter.get('module', 'Unknown')
            lesson = frontmatter.get('lesson', 'Unknown')
            title = frontmatter.get('title', file_path.stem)
            depth = frontmatter.get('depth', 'L1')
            concepts = frontmatter.get('concepts', [])
            frameworks = frontmatter.get('frameworks', [])
            anti_patterns = frontmatter.get('anti_patterns', [])

            relative_path = str(file_path.relative_to(self.notes_dir))

            # Store in hierarchy
            self.chapters[chapter][module][lesson].append({
                'file': relative_path,
                'title': title,
                'depth': depth,
                'concepts': concepts,
                'frameworks': frameworks,
                'anti_patterns': anti_patterns
            })

            # Build concept → files mapping
            for concept in concepts:
                self.all_concepts[concept].append(relative_path)

            for framework in frameworks:
                self.all_frameworks[framework].append(relative_path)

            for anti_pattern in anti_patterns:
                self.all_anti_patterns[anti_pattern].append(relative_path)

        print(f"✅ Found {len(self.chapters)} chapters")

    def generate_toc(self) -> str:
        """Generate Table of Contents section."""
        toc = ["## Table of Contents\n"]

        for chapter in sorted(self.chapters.keys()):
            toc.append(f"- [Chapter {chapter}](#{self._slugify(f'chapter-{chapter}')})")

            for module in sorted(self.chapters[chapter].keys()):
                toc.append(f"  - [{module}](#{self._slugify(module)})")

        toc.append("- [Concept Index](#concept-index)")
        toc.append("- [Framework Index](#framework-index)")
        toc.append("- [Anti-Pattern Index](#anti-pattern-index)")

        return "\n".join(toc) + "\n"

    def generate_chapters(self) -> str:
        """Generate chapters section."""
        content = []

        for chapter in sorted(self.chapters.keys()):
            content.append(f"## Chapter {chapter}\n")

            for module in sorted(self.chapters[chapter].keys()):
                content.append(f"### {module}\n")

                # Sort lessons by lesson number
                lessons = self.chapters[chapter][module]
                sorted_lessons = sorted(
                    lessons.items(),
                    key=lambda x: self.parse_lesson_number(x[0])
                )

                for lesson, files in sorted_lessons:
                    content.append(f"#### Lesson {lesson}\n")

                    # Sort by depth (L1, L2, L3...)
                    sorted_files = sorted(files, key=lambda x: x['depth'])

                    for file_data in sorted_files:
                        depth_label = {
                            'L1': '🔷 Fundamentals',
                            'L2': '🔶 Intermediate',
                            'L3': '🔸 Advanced'
                        }.get(file_data['depth'], file_data['depth'])

                        content.append(f"**{depth_label}**: [{file_data['title']}]({file_data['file']})")

                        if file_data['concepts']:
                            concepts_str = ', '.join(f"`{c}`" for c in file_data['concepts'])
                            content.append(f"- Concepts: {concepts_str}")

                        if file_data['frameworks']:
                            frameworks_str = ', '.join(f"`{f}`" for f in file_data['frameworks'])
                            content.append(f"- Frameworks: {frameworks_str}")

                        content.append("")  # Blank line

                    content.append("")  # Blank line between lessons

        return "\n".join(content)

    def generate_concept_index(self) -> str:
        """Generate alphabetical concept index."""
        content = ["## Concept Index\n"]

        if not self.all_concepts:
            content.append("_No concepts indexed yet._\n")
            return "\n".join(content)

        for concept in sorted(self.all_concepts.keys(), key=str.lower):
            files = self.all_concepts[concept]
            content.append(f"### {concept}\n")
            for file_path in sorted(files):
                content.append(f"- [{file_path}]({file_path})")
            content.append("")  # Blank line

        return "\n".join(content)

    def generate_framework_index(self) -> str:
        """Generate alphabetical framework index."""
        content = ["## Framework Index\n"]

        if not self.all_frameworks:
            content.append("_No frameworks indexed yet._\n")
            return "\n".join(content)

        for framework in sorted(self.all_frameworks.keys(), key=str.lower):
            files = self.all_frameworks[framework]
            content.append(f"### {framework}\n")
            for file_path in sorted(files):
                content.append(f"- [{file_path}]({file_path})")
            content.append("")  # Blank line

        return "\n".join(content)

    def generate_anti_pattern_index(self) -> str:
        """Generate alphabetical anti-pattern index."""
        content = ["## Anti-Pattern Index\n"]

        if not self.all_anti_patterns:
            content.append("_No anti-patterns indexed yet._\n")
            return "\n".join(content)

        for anti_pattern in sorted(self.all_anti_patterns.keys(), key=str.lower):
            files = self.all_anti_patterns[anti_pattern]
            content.append(f"### {anti_pattern}\n")
            for file_path in sorted(files):
                content.append(f"- [{file_path}]({file_path})")
            content.append("")  # Blank line

        return "\n".join(content)

    def generate_index(self) -> str:
        """Generate complete INDEX.md content."""
        sections = [
            "# Agent Factory Part 1: Master Index\n",
            "> **Auto-Generated**: This file is automatically generated by `scripts/generate-index.py`.",
            "> **Do not edit manually** -- changes will be overwritten.\n",
            f"**Last Updated**: {self._get_timestamp()}\n",
            "---\n",
            self.generate_toc(),
            "\n---\n",
            self.generate_chapters(),
            "\n---\n",
            self.generate_concept_index(),
            "\n---\n",
            self.generate_framework_index(),
            "\n---\n",
            self.generate_anti_pattern_index(),
        ]

        return "\n".join(sections)

    def save_index(self, output_path: str = "revision-notes/INDEX.md"):
        """Save generated INDEX.md to file."""
        content = self.generate_index()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"💾 Master INDEX.md saved to {output_path}")
        print(f"   - {len(self.chapters)} chapters")
        print(f"   - {len(self.all_concepts)} concepts")
        print(f"   - {len(self.all_frameworks)} frameworks")
        print(f"   - {len(self.all_anti_patterns)} anti-patterns")

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        return re.sub(r'[^\w\-]', '', text.lower().replace(' ', '-'))

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main execution."""
    print("="*60)
    print("  Master INDEX.md Generator")
    print("="*60)

    generator = IndexGenerator(notes_dir="revision-notes")
    generator.scan_files()
    generator.save_index()

    print("\n✅ INDEX.md generation complete!")


if __name__ == "__main__":
    main()
