#!/usr/bin/env python3
"""
generate-index.py — Visual Presentations Index Generator
=========================================================

Scans visual-presentations/ for lesson HTML files, reads status.json for
current lesson context, and generates visual-presentations/INDEX.html with:
  - Stats bar (total presentations, chapters covered, current lesson)
  - Chapter-grouped lesson cards linking to individual HTMLs
  - Current lesson highlighted with a border
  - Clean, professional CSS (no external dependencies)

Usage:
    python3 scripts/generate-index.py

Output:
    visual-presentations/INDEX.html
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR         = Path(__file__).resolve().parent.parent
PRESENTATIONS_DIR = BASE_DIR / "visual-presentations"
STATUS_FILE      = BASE_DIR / "context-bridge" / "status.json"
OUTPUT_FILE      = PRESENTATIONS_DIR / "INDEX.html"


def parse_lesson_filename(filename: str):
    """
    Extract lesson_id and title from filenames like:
      lesson-3.17-hook-architecture.html
      lesson-1.1-ai-paradigm-overview.html

    Returns (lesson_id, title_pretty, chapter_num) or None if no match.
    """
    m = re.match(r"^lesson-(\d+\.\d+)-(.+)\.html$", filename)
    if not m:
        return None
    lesson_id    = m.group(1)
    title_kebab  = m.group(2)
    title_pretty = title_kebab.replace("-", " ").title()
    chapter_num  = int(lesson_id.split(".")[0])
    return lesson_id, title_pretty, chapter_num


def lesson_sort_key(lesson_id: str):
    """Sort key: (chapter, lesson_number)"""
    try:
        parts = lesson_id.split(".")
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return (999, 999)


def load_status() -> dict:
    """Load context-bridge/status.json. Returns {} on missing/error."""
    if not STATUS_FILE.exists():
        return {}
    try:
        with open(STATUS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def scan_presentations():
    """
    Scan visual-presentations/ for lesson-*.html files.
    Returns list of dicts: {lesson_id, title, chapter_num, filename}
    """
    if not PRESENTATIONS_DIR.exists():
        return []

    results = []
    for path in sorted(PRESENTATIONS_DIR.glob("lesson-*.html")):
        parsed = parse_lesson_filename(path.name)
        if parsed is None:
            continue
        lesson_id, title, chapter_num = parsed
        results.append({
            "lesson_id":   lesson_id,
            "title":       title,
            "chapter_num": chapter_num,
            "filename":    path.name,
        })

    results.sort(key=lambda x: lesson_sort_key(x["lesson_id"]))
    return results


def group_by_chapter(lessons: list) -> dict:
    """Group lesson dicts by chapter number. Returns OrderedDict-like sorted dict."""
    chapters = {}
    for lesson in lessons:
        ch = lesson["chapter_num"]
        chapters.setdefault(ch, []).append(lesson)
    return dict(sorted(chapters.items()))


CHAPTER_TITLES = {
    1: "The AI Agent Paradigm",
    2: "Markdown & Writing Instructions",
    3: "Claude Code & Cowork",
    4: "Effective Context Engineering",
    5: "Spec-Driven Development",
    6: "Seven Principles of General Agent Problem Solving",
}


def generate_html(lessons: list, status: dict) -> str:
    current_lesson = status.get("lesson", "")
    current_layer  = status.get("layer", "")
    current_concept = status.get("concept", "")
    last_updated   = status.get("last_updated", "")

    chapters        = group_by_chapter(lessons)
    total_count     = len(lessons)
    chapter_count   = len(chapters)
    generated_at    = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build stats bar values
    current_label = f"Lesson {current_lesson}" if current_lesson else "None"
    if current_layer:
        current_label += f" · {current_layer}"

    # Build chapter sections HTML
    chapter_sections = ""
    for ch_num, ch_lessons in chapters.items():
        ch_title = CHAPTER_TITLES.get(ch_num, f"Chapter {ch_num}")
        cards_html = ""
        for lesson in ch_lessons:
            is_current = (lesson["lesson_id"] == current_lesson)
            current_cls   = " card-current" if is_current else ""
            current_badge = '<span class="badge badge-active">Current</span>' if is_current else ""
            layer_badge   = f'<span class="badge badge-layer">{current_layer}</span>' if is_current and current_layer else ""

            cards_html += f"""
            <a href="{lesson['filename']}" class="lesson-card{current_cls}">
              <div class="card-header">
                <span class="lesson-id">{lesson['lesson_id']}</span>
                <div class="card-badges">{current_badge}{layer_badge}</div>
              </div>
              <div class="card-title">{lesson['title']}</div>
              {f'<div class="card-concept">{current_concept}</div>' if is_current and current_concept else ''}
            </a>"""

        chapter_sections += f"""
        <section class="chapter-section">
          <div class="chapter-header">
            <span class="chapter-num">Ch.{ch_num}</span>
            <span class="chapter-title">{ch_title}</span>
            <span class="chapter-count">{len(ch_lessons)} lesson{'s' if len(ch_lessons) != 1 else ''}</span>
          </div>
          <div class="cards-grid">
            {cards_html}
          </div>
        </section>"""

    if not chapters:
        chapter_sections = """
        <div class="empty-state">
          <div class="empty-icon">📂</div>
          <p>No lesson presentations found yet.</p>
          <p style="color:var(--muted);font-size:.9rem;margin-top:.5rem">
            Run <code>python3 scripts/generate-html.py --demo</code> to create your first presentation.
          </p>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Agent Factory — Lesson Index</title>
  <style>
    :root {{
      --bg:      #f8f7f4;
      --surface: #ffffff;
      --border:  #e2e0da;
      --indigo:  #4f46e5;
      --cyan:    #06b6d4;
      --text:    #1e1b18;
      --muted:   #6b6560;
      --success: #16a34a;
      --radius:  12px;
      --shadow:  0 4px 24px rgba(0,0,0,.08);
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: var(--bg); color: var(--text);
      min-height: 100vh;
    }}

    /* ── Top Bar ── */
    #topbar {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 0 2rem; height: 52px;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,.06);
      position: sticky; top: 0; z-index: 50;
    }}
    #topbar .brand {{ font-weight: 800; font-size: 1rem; color: var(--indigo); }}
    #topbar .meta  {{ font-size: .8rem; color: var(--muted); }}

    /* ── Stats Bar ── */
    #stats-bar {{
      background: linear-gradient(135deg, var(--indigo) 0%, var(--cyan) 100%);
      color: #fff; padding: 1.5rem 2rem;
      display: flex; gap: 2.5rem; flex-wrap: wrap; align-items: center;
    }}
    .stat-item .val  {{ font-size: 2rem; font-weight: 800; line-height: 1; }}
    .stat-item .lbl  {{ font-size: .75rem; opacity: .8; margin-top: .2rem; text-transform: uppercase; letter-spacing: .08em; }}
    #stats-bar .divider {{ width: 1px; height: 40px; background: rgba(255,255,255,.3); }}

    /* ── Main Content ── */
    main {{ max-width: 1100px; margin: 0 auto; padding: 2rem; }}

    /* ── Chapter Section ── */
    .chapter-section {{ margin-bottom: 2.5rem; }}
    .chapter-header {{
      display: flex; align-items: center; gap: .8rem;
      margin-bottom: 1rem; padding-bottom: .6rem;
      border-bottom: 2px solid var(--border);
    }}
    .chapter-num   {{ font-weight: 800; font-size: .8rem; color: var(--indigo); background: #ede9fe; padding: .2rem .6rem; border-radius: 6px; }}
    .chapter-title {{ font-weight: 700; font-size: 1.05rem; }}
    .chapter-count {{ font-size: .78rem; color: var(--muted); margin-left: auto; }}

    /* ── Cards Grid ── */
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 1rem;
    }}

    /* ── Lesson Card ── */
    .lesson-card {{
      background: var(--surface); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 1.1rem 1.3rem;
      text-decoration: none; color: var(--text);
      box-shadow: var(--shadow);
      transition: transform .2s, box-shadow .2s, border-color .2s;
      display: block;
    }}
    .lesson-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(79,70,229,.12);
      border-color: var(--indigo);
    }}
    .lesson-card.card-current {{
      border: 2px solid var(--indigo);
      background: #fafaff;
      box-shadow: 0 0 0 3px rgba(79,70,229,.12), var(--shadow);
    }}
    .card-header {{
      display: flex; justify-content: space-between; align-items: flex-start;
      margin-bottom: .5rem;
    }}
    .lesson-id {{
      font-size: .75rem; font-weight: 700; color: var(--indigo);
      background: #ede9fe; padding: .15rem .5rem; border-radius: 5px;
    }}
    .card-badges {{ display: flex; gap: .3rem; flex-wrap: wrap; }}
    .card-title  {{ font-weight: 600; font-size: .93rem; line-height: 1.4; }}
    .card-concept {{ font-size: .78rem; color: var(--muted); margin-top: .4rem; font-style: italic; }}

    /* ── Badges ── */
    .badge {{ display: inline-block; padding: .15rem .5rem; border-radius: 5px; font-size: .7rem; font-weight: 700; }}
    .badge-active {{ background: #dcfce7; color: var(--success); }}
    .badge-layer  {{ background: #cffafe; color: #0e7490; }}

    /* ── Empty State ── */
    .empty-state {{
      text-align: center; padding: 4rem 2rem;
      color: var(--text);
    }}
    .empty-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
    .empty-state code {{
      background: #ede9fe; color: var(--indigo);
      padding: .2rem .5rem; border-radius: 4px; font-size: .88rem;
    }}

    /* ── Footer ── */
    footer {{
      text-align: center; padding: 1.5rem;
      font-size: .78rem; color: var(--muted);
      border-top: 1px solid var(--border);
      margin-top: 1rem;
    }}

    @media (max-width: 600px) {{
      #stats-bar {{ gap: 1.5rem; }}
      .cards-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<div id="topbar">
  <span class="brand">Agent Factory Part 1 — Lesson Index</span>
  <span class="meta">Generated: {generated_at}</span>
</div>

<div id="stats-bar">
  <div class="stat-item"><div class="val">{total_count}</div><div class="lbl">Presentations</div></div>
  <div class="divider"></div>
  <div class="stat-item"><div class="val">{chapter_count}</div><div class="lbl">Chapters Covered</div></div>
  <div class="divider"></div>
  <div class="stat-item"><div class="val">{current_label}</div><div class="lbl">Current Lesson</div></div>
</div>

<main>
  {chapter_sections}
</main>

<footer>
  Auto-generated by <code>scripts/generate-index.py</code> &nbsp;·&nbsp;
  Source: <code>visual-presentations/</code> &nbsp;·&nbsp;
  Status from: <code>context-bridge/status.json</code>
  {f'&nbsp;·&nbsp; Last bridge update: {last_updated}' if last_updated else ''}
</footer>

</body>
</html>"""


def main():
    print("=" * 60)
    print("  Visual Presentations Index Generator")
    print("=" * 60)

    lessons = scan_presentations()
    status  = load_status()

    print(f"Found {len(lessons)} lesson presentation(s) in visual-presentations/")
    if status.get("lesson"):
        print(f"Current lesson from status.json: {status['lesson']}")

    html = generate_html(lessons, status)

    PRESENTATIONS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    print(f"\n✅ INDEX.html written to: {OUTPUT_FILE}")
    return str(OUTPUT_FILE)


if __name__ == "__main__":
    main()
