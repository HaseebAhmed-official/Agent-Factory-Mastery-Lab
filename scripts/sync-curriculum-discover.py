#!/usr/bin/env python3
"""
Curriculum Discovery Script

Crawls the official Agent Factory curriculum website to discover all lessons,
extracts metadata, and builds a curriculum manifest for sync operations.

Usage:
    python scripts/sync-curriculum-discover.py

Outputs:
    - curriculum-manifest.json (full lesson inventory with URLs and metadata)
    - logs/discovery-{timestamp}.log (detailed crawl log)

Dependencies:
    - requests (for HTTP requests)
    - beautifulsoup4 (for HTML parsing)

Author: Professor Agent
Version: 1.0
Created: 2026-03-03
"""

import json
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required dependencies not installed.")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


class CurriculumDiscovery:
    """Discovers and catalogs lessons from official curriculum website."""

    def __init__(self, base_url: str = "https://agentfactory.panaversity.org/docs/General-Agents-Foundations/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (curriculum sync bot)'
        })
        self.lessons: Dict[str, Dict] = {}
        self.errors: List[str] = []
        self.log: List[str] = []

    def discover(self) -> Dict:
        """
        Main discovery workflow.

        Returns:
            Dict containing curriculum manifest data
        """
        self._log("INFO", "Starting curriculum discovery...")
        self._log("INFO", f"Base URL: {self.base_url}")

        # Step 1: Fetch table of contents
        try:
            toc_html = self._fetch_page(self.base_url)
            if not toc_html:
                self._log("ERROR", "Failed to fetch table of contents")
                return self._build_manifest()
        except Exception as e:
            self._log("ERROR", f"Exception while fetching TOC: {e}")
            return self._build_manifest()

        # Step 2: Parse TOC to extract lesson list
        try:
            self._parse_toc(toc_html)
        except Exception as e:
            self._log("ERROR", f"Exception while parsing TOC: {e}")

        # Step 3: Fetch content for each lesson (to compute hash)
        self._fetch_lesson_content()

        # Step 4: Build final manifest
        manifest = self._build_manifest()

        self._log("INFO", f"Discovery complete. Found {len(self.lessons)} lessons.")

        return manifest

    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from URL.

        Args:
            url: URL to fetch

        Returns:
            HTML content as string, or None if fetch fails
        """
        self._log("INFO", f"Fetching: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            self._log("SUCCESS", f"Fetched {len(response.text)} bytes")
            return response.text
        except requests.RequestException as e:
            self._log("ERROR", f"Failed to fetch {url}: {e}")
            self.errors.append(f"Fetch failed: {url} - {e}")
            return None

    def _parse_toc(self, html: str):
        """
        Parse table of contents HTML to extract lesson list.

        Args:
            html: HTML content of TOC page
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Strategy 1: Look for sidebar navigation (common in Docusaurus sites)
        sidebar = soup.find('nav', class_=re.compile(r'menu|sidebar|navigation', re.I))
        if sidebar:
            self._log("INFO", "Found sidebar navigation")
            self._parse_sidebar(sidebar)
            return

        # Strategy 2: Look for main content links
        main_content = soup.find('main') or soup.find('article')
        if main_content:
            self._log("INFO", "Parsing main content for lesson links")
            self._parse_content_links(main_content)
            return

        # Strategy 3: Fallback - search for all links matching lesson pattern
        self._log("WARN", "No structured navigation found. Falling back to pattern matching.")
        self._parse_all_links(soup)

    def _parse_sidebar(self, sidebar):
        """
        Parse sidebar navigation to extract lesson links.

        Args:
            sidebar: BeautifulSoup element containing sidebar
        """
        links = sidebar.find_all('a', href=True)

        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)

            # Extract lesson number from text (e.g., "3.1", "3.15", "3.22")
            lesson_match = re.search(r'(\d+)\.(\d+)', text)
            if lesson_match:
                chapter = int(lesson_match.group(1))
                lesson_num = f"{chapter}.{lesson_match.group(2)}"

                # Build absolute URL
                url = urljoin(self.base_url, href)

                # Extract title (remove lesson number from text)
                title = re.sub(r'^\d+\.\d+\s*[-–—:]*\s*', '', text).strip()

                self._add_lesson(lesson_num, title, url, chapter)

    def _parse_content_links(self, content):
        """
        Parse main content links to extract lessons.

        Args:
            content: BeautifulSoup element containing main content
        """
        links = content.find_all('a', href=True)

        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)

            # Only process links that look like lesson links
            if re.search(r'\d+\.\d+', text):
                lesson_match = re.search(r'(\d+)\.(\d+)', text)
                chapter = int(lesson_match.group(1))
                lesson_num = f"{chapter}.{lesson_match.group(2)}"

                url = urljoin(self.base_url, href)
                title = re.sub(r'^\d+\.\d+\s*[-–—:]*\s*', '', text).strip()

                self._add_lesson(lesson_num, title, url, chapter)

    def _parse_all_links(self, soup):
        """
        Fallback: parse all links looking for lesson patterns.

        Args:
            soup: BeautifulSoup object of entire page
        """
        links = soup.find_all('a', href=True)

        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)

            # Match patterns like "3.1 Origin Story", "Lesson 3.15", etc.
            if re.search(r'\d+\.\d+', text):
                lesson_match = re.search(r'(\d+)\.(\d+)', text)
                chapter = int(lesson_match.group(1))
                lesson_num = f"{chapter}.{lesson_match.group(2)}"

                url = urljoin(self.base_url, href)
                title = re.sub(r'^(Lesson\s+)?\d+\.\d+\s*[-–—:]*\s*', '', text, flags=re.I).strip()

                self._add_lesson(lesson_num, title, url, chapter)

    def _add_lesson(self, lesson_num: str, title: str, url: str, chapter: int):
        """
        Add lesson to internal catalog.

        Args:
            lesson_num: Lesson number (e.g., "3.1")
            title: Lesson title
            url: Lesson URL
            chapter: Chapter number
        """
        # Skip duplicates
        if lesson_num in self.lessons:
            return

        self._log("INFO", f"Found lesson {lesson_num}: {title}")

        self.lessons[lesson_num] = {
            "chapter": chapter,
            "title": title,
            "url": url,
            "hash": None,  # Will be computed when fetching content
            "discovered_at": datetime.now().isoformat(),
            "status": "discovered"
        }

    def _fetch_lesson_content(self):
        """
        Fetch content for each discovered lesson and compute hash.
        """
        self._log("INFO", f"Fetching content for {len(self.lessons)} lessons...")

        for lesson_num, lesson_data in self.lessons.items():
            url = lesson_data["url"]

            # Fetch content
            content = self._fetch_page(url)
            if not content:
                self._log("WARN", f"Skipping hash computation for {lesson_num} (fetch failed)")
                continue

            # Compute content hash
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            lesson_data["hash"] = content_hash

            self._log("INFO", f"Lesson {lesson_num} hash: {content_hash[:16]}...")

    def _build_manifest(self) -> Dict:
        """
        Build final curriculum manifest.

        Returns:
            Dict containing manifest data
        """
        # Group lessons by chapter
        chapters_stats = {}
        for lesson_num, lesson_data in self.lessons.items():
            chapter = lesson_data["chapter"]
            chapters_stats[chapter] = chapters_stats.get(chapter, 0) + 1

        manifest = {
            "version": "1.0",
            "last_sync": datetime.now().isoformat(),
            "source": {
                "base_url": self.base_url,
                "toc_url": self.base_url
            },
            "lessons": self.lessons,
            "stats": {
                "total_lessons": len(self.lessons),
                "synced": len(self.lessons),
                "deprecated": 0,
                "chapters": chapters_stats
            },
            "discovery": {
                "errors": self.errors,
                "log_entries": len(self.log)
            }
        }

        return manifest

    def _log(self, level: str, message: str):
        """
        Add entry to internal log.

        Args:
            level: Log level (INFO, WARN, ERROR, SUCCESS)
            message: Log message
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {level:8s} {message}"
        self.log.append(entry)
        print(entry)

    def save_manifest(self, manifest: Dict, output_path: Path):
        """
        Save manifest to JSON file.

        Args:
            manifest: Manifest data
            output_path: Path to output file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        self._log("SUCCESS", f"Manifest saved to {output_path}")

    def save_log(self, log_path: Path):
        """
        Save discovery log to file.

        Args:
            log_path: Path to log file
        """
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("CURRICULUM DISCOVERY LOG\n")
            f.write("=" * 80 + "\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Base URL: {self.base_url}\n")
            f.write("=" * 80 + "\n\n")

            for entry in self.log:
                f.write(entry + "\n")

            if self.errors:
                f.write("\n" + "=" * 80 + "\n")
                f.write("ERRORS\n")
                f.write("=" * 80 + "\n")
                for error in self.errors:
                    f.write(f"- {error}\n")

        self._log("SUCCESS", f"Log saved to {log_path}")


def main():
    """Main entry point."""
    # Paths
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / "curriculum-manifest.json"
    logs_dir = project_root / "logs"
    log_path = logs_dir / f"discovery-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    # Discovery
    print("=" * 80)
    print("CURRICULUM DISCOVERY")
    print("=" * 80)
    print()

    discovery = CurriculumDiscovery()
    manifest = discovery.discover()

    print()
    print("=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    print()

    # Save outputs
    discovery.save_manifest(manifest, manifest_path)
    discovery.save_log(log_path)

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Lessons discovered: {manifest['stats']['total_lessons']}")
    print(f"Chapters covered: {len(manifest['stats']['chapters'])}")
    print(f"Errors encountered: {len(discovery.errors)}")
    print()
    print(f"Manifest: {manifest_path}")
    print(f"Log: {log_path}")
    print()

    if discovery.errors:
        print("⚠️  Some errors occurred during discovery. Check log for details.")
        return 1
    else:
        print("✅ Discovery completed successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
