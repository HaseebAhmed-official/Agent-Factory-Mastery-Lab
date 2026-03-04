#!/usr/bin/env python3
"""
Generate Concept Map Data
==========================

Builds interactive concept map data from markdown files with YAML frontmatter.

Features:
- Graph structure (nodes + edges)
- Concept relationships (prerequisites, related concepts)
- Hierarchical layout (chapter → lesson → concept)
- Metadata for filtering (tags, depth, lesson)

Usage:
    python scripts/generate-concept-map.py

Output:
    visual-presentations/concept-map-data.json
"""

import os
import json
import yaml
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set


class ConceptMapGenerator:
    """Generates concept map graph data."""

    def __init__(self, notes_dir: str = "revision-notes"):
        self.notes_dir = Path(notes_dir)
        self.nodes = []  # List of node objects
        self.edges = []  # List of edge objects
        self.concept_to_id = {}  # concept name → node id
        self.node_id_counter = 0

    def extract_frontmatter(self, file_path: Path) -> dict:
        """Extract YAML frontmatter from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter if isinstance(frontmatter, dict) else {}

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return {}

    def create_node(self, name: str, metadata: dict) -> int:
        """Create a new node and return its ID."""
        if name in self.concept_to_id:
            return self.concept_to_id[name]

        node_id = self.node_id_counter
        self.node_id_counter += 1

        self.nodes.append({
            'id': node_id,
            'label': name,
            'type': metadata.get('type', 'concept'),
            'lesson': metadata.get('lesson', ''),
            'depth': metadata.get('depth', 'L1'),
            'chapter': metadata.get('chapter', ''),
            'file': metadata.get('file', ''),
            'definition': metadata.get('definition', ''),
            'tags': metadata.get('tags', [])
        })

        self.concept_to_id[name] = node_id
        return node_id

    def create_edge(self, source_id: int, target_id: int, edge_type: str = 'related'):
        """Create an edge between two nodes."""
        # Avoid duplicate edges
        existing_edge = any(
            e['source'] == source_id and e['target'] == target_id
            for e in self.edges
        )
        if existing_edge:
            return

        self.edges.append({
            'source': source_id,
            'target': target_id,
            'type': edge_type
        })

    def scan_files(self):
        """Scan all markdown files and build graph."""
        if not self.notes_dir.exists():
            print(f"⚠️  Directory not found: {self.notes_dir}")
            return

        md_files = list(self.notes_dir.rglob("*.md"))

        if not md_files:
            print(f"⚠️  No markdown files found in {self.notes_dir}")
            return

        print(f"📂 Scanning {len(md_files)} markdown files...")

        file_metadata_list = []

        # First pass: Create nodes
        for file_path in md_files:
            if file_path.name in ['INDEX.md', 'README.md']:
                continue

            frontmatter = self.extract_frontmatter(file_path)
            if not frontmatter:
                continue

            relative_path = str(file_path.relative_to(Path.cwd()))

            # Extract metadata
            lesson = frontmatter.get('lesson', '')
            depth = frontmatter.get('depth', 'L1')
            chapter = frontmatter.get('chapter', '')
            tags = frontmatter.get('tags', [])
            concepts = frontmatter.get('concepts', [])
            frameworks = frontmatter.get('frameworks', [])

            # Create nodes for each concept
            for concept in concepts:
                self.create_node(concept, {
                    'type': 'concept',
                    'lesson': lesson,
                    'depth': depth,
                    'chapter': chapter,
                    'file': relative_path,
                    'tags': tags
                })

            # Create nodes for each framework
            for framework in frameworks:
                self.create_node(framework, {
                    'type': 'framework',
                    'lesson': lesson,
                    'depth': depth,
                    'chapter': chapter,
                    'file': relative_path,
                    'tags': tags
                })

            # Store for second pass
            file_metadata_list.append({
                'concepts': concepts,
                'frameworks': frameworks,
                'prerequisites': frontmatter.get('prerequisites', []),
                'related_concepts': frontmatter.get('related_concepts', [])
            })

        # Second pass: Create edges
        for metadata in file_metadata_list:
            concepts = metadata['concepts']
            frameworks = metadata['frameworks']
            prerequisites = metadata['prerequisites']
            related_concepts = metadata['related_concepts']

            # Link concepts within same file (related)
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    if concept1 in self.concept_to_id and concept2 in self.concept_to_id:
                        self.create_edge(
                            self.concept_to_id[concept1],
                            self.concept_to_id[concept2],
                            'related'
                        )

            # Link frameworks to concepts (applies_to)
            for framework in frameworks:
                for concept in concepts:
                    if framework in self.concept_to_id and concept in self.concept_to_id:
                        self.create_edge(
                            self.concept_to_id[framework],
                            self.concept_to_id[concept],
                            'applies_to'
                        )

            # Link prerequisites (requires)
            for concept in concepts:
                if concept not in self.concept_to_id:
                    continue
                for prereq in prerequisites:
                    if prereq in self.concept_to_id:
                        self.create_edge(
                            self.concept_to_id[concept],
                            self.concept_to_id[prereq],
                            'requires'
                        )

            # Link related concepts
            for concept in concepts:
                if concept not in self.concept_to_id:
                    continue
                for related in related_concepts:
                    if related in self.concept_to_id:
                        self.create_edge(
                            self.concept_to_id[concept],
                            self.concept_to_id[related],
                            'related'
                        )

        print(f"✅ Created {len(self.nodes)} nodes")
        print(f"✅ Created {len(self.edges)} edges")

    def build_graph_data(self) -> dict:
        """Build the complete graph data structure."""
        return {
            'generated': self._get_timestamp(),
            'metadata': {
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges),
                'node_types': self._count_node_types(),
                'edge_types': self._count_edge_types()
            },
            'nodes': self.nodes,
            'edges': self.edges
        }

    def _count_node_types(self) -> dict:
        """Count nodes by type."""
        counts = defaultdict(int)
        for node in self.nodes:
            counts[node['type']] += 1
        return dict(counts)

    def _count_edge_types(self) -> dict:
        """Count edges by type."""
        counts = defaultdict(int)
        for edge in self.edges:
            counts[edge['type']] += 1
        return dict(counts)

    def save_graph_data(self, output_path: str = "visual-presentations/concept-map-data.json"):
        """Save graph data to JSON file."""
        graph_data = self.build_graph_data()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Concept map data saved to {output_path}")
        print(f"   - {graph_data['metadata']['total_nodes']} nodes")
        print(f"   - {graph_data['metadata']['total_edges']} edges")

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main execution."""
    print("="*60)
    print("  Concept Map Data Generator")
    print("="*60)

    generator = ConceptMapGenerator(notes_dir="revision-notes")
    generator.scan_files()
    generator.save_graph_data()

    print("\n✅ Concept map data generation complete!")


if __name__ == "__main__":
    main()
