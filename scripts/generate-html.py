#!/usr/bin/env python3
"""
generate-html.py — Lesson HTML Presentation Generator
======================================================

Reads a JSON content file and renders it using the Jinja2 template
at templates/html/lesson-presentation.html.j2.

Usage:
    python3 scripts/generate-html.py --content path/to/content.json --output visual-presentations/
    python3 scripts/generate-html.py --demo

Output:
    visual-presentations/lesson-{lesson_id}-{title-kebab}.html
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── Base paths ──────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent.parent
TEMPLATE_FILE = BASE_DIR / "templates" / "html" / "lesson-presentation.html.j2"
OUTPUT_DIR    = BASE_DIR / "visual-presentations"

# ── Demo content (Hook Architecture lesson) ─────────────────────────────────
DEMO_CONTENT = {
    "lesson_id":        "3.17",
    "lesson_title":     "Hook Architecture",
    "lesson_subtitle":  "How Claude Code intercepts and controls agent lifecycle events",
    "chapter_title":    "Chapter 3: Claude Code & Cowork",
    "chapter_badge":    "Ch.3 · Module 3 · Lesson 17",
    "lesson_date":      "2026-03-29",
    "layer_label":      "L1 — Fundamentals",
    "lesson_tags":      ["hooks", "lifecycle", "stop-hooks", "pre-tool", "post-tool"],
    "checkpoint_count": 2,
    "concept_count":    5,
    "vocab_count":      6,

    "vocabulary": [
        {"term": "Hook",          "definition": "A callback function registered with Claude Code that fires automatically at a defined lifecycle event (e.g., before a tool call, after a response)."},
        {"term": "Stop Hook",     "definition": "A special hook that can return a signal causing Claude Code to halt the current agent loop iteration before execution continues."},
        {"term": "PreTool Hook",  "definition": "Fires immediately before any tool call is executed. Receives tool name + parameters. Can block the call."},
        {"term": "PostTool Hook", "definition": "Fires after a tool call completes. Receives the tool result. Useful for logging, validation, side-effects."},
        {"term": "Lifecycle",     "definition": "The ordered sequence of events in an agent loop: receive prompt → plan → tool call(s) → synthesize → respond."},
        {"term": "Hook Registry", "definition": "The internal store where hooks are registered. Hooks fire in registration order within the same event type."}
    ],

    "core_concepts": [
        {"label": "What",  "title": "Hooks as Event Listeners",       "summary": "Hooks are functions you register that Claude Code calls automatically when specific events occur in the agent lifecycle. They let you observe, modify, or halt agent behavior without changing core logic."},
        {"label": "Why",   "title": "Control Without Forking",         "summary": "Without hooks, you'd have to fork or monkey-patch Claude Code to add safety guards, logging, or custom validation. Hooks provide sanctioned extension points."},
        {"label": "How",   "title": "Registration & Firing Order",     "summary": "Hooks are registered in CLAUDE.md or via the Claude Code SDK. Multiple hooks of the same type fire in registration order. A stop-hook returning a truthy stop signal halts the loop immediately."},
        {"label": "Where", "title": "Fits in the Agent Loop",          "summary": "Hooks slot into the lifecycle: PreTool fires before each tool call, PostTool after. Stop hooks evaluate before the next iteration begins."},
        {"label": "Risk",  "title": "Silent Failure & Hook Stacking",  "summary": "If a hook throws an uncaught exception, Claude Code may silently suppress it. Multiple conflicting stop hooks can create unpredictable halt conditions."}
    ],

    "analogies": [
        {
            "concept": "Hooks",
            "analogy": "Think of hooks like airport security checkpoints. Before any passenger (tool call) boards the plane, they pass through PreTool screening. After landing, PostTool customs checks run. A stop hook is the no-fly list: if a name matches, the loop is grounded before takeoff.",
            "diagram": "  AGENT LOOP\n  ──────────\n  Receive Prompt\n       │\n  [PreTool Hook] ← fires here, can STOP\n       │\n  Execute Tool\n       │\n  [PostTool Hook] ← fires here, logs/validates\n       │\n  Synthesize Response\n       │\n  [Stop Hook Check] ← fires here, can HALT loop\n       │\n  Respond → next iteration"
        }
    ],

    "failure_modes": [
        {"type": "Omission",            "name": "Unregistered Hook",         "description": "Hook written but never registered in CLAUDE.md. Agent lifecycle runs without it — no error, just silently missing.", "fix": "Always verify registration with `claude hooks list` after writing a new hook."},
        {"type": "Interaction Failure", "name": "Conflicting Stop Hooks",    "description": "Two stop hooks with opposing conditions both return stop signals on alternate iterations, creating an oscillating halt pattern.", "fix": "Use a single authoritative stop hook. Others should be observers only."},
        {"type": "Misapplication",      "name": "PreTool Used for Logging",  "description": "Using PreTool hooks for heavy logging adds latency before every tool call. Use PostTool or an async side-channel instead.", "fix": "Logging belongs in PostTool hooks or a dedicated observability sink."},
        {"type": "Excess",              "name": "Hook Stack Explosion",      "description": "10+ hooks on the same event type make execution order unpredictable and debug traces unreadable.", "fix": "Cap hooks per event type at 3-5. Combine related logic into a single hook function."}
    ],

    "exercises": [
        {
            "title":           "Write Your First Stop Hook",
            "task":            "Create a stop hook that halts the agent if any tool call targets a file path containing '/etc/' or '/root/'. This prevents accidental system file access.",
            "steps":           [
                "Open your CLAUDE.md in the project root",
                "Add a PreTool hook section with the path pattern check",
                "Test by asking Claude to 'read /etc/passwd' — it should halt with a clear message",
                "Verify the hook fires: check hook logs for the stop signal"
            ],
            "expected_output": "Agent halts with: 'Stop hook triggered: system path access denied for /etc/passwd'"
        }
    ],

    "checkpoints": [
        {"layer": "L1", "layer_label": "Fundamentals",  "concepts": "Hook definition, lifecycle events, PreTool vs PostTool, stop-hook signal mechanism", "timestamp": "2026-03-29 10:15"},
        {"layer": "L2", "layer_label": "Intermediate",  "concepts": "Hook stacking order, failure modes, registration patterns, conflict resolution", "timestamp": "2026-03-29 11:40"}
    ],

    "summary_points": [
        "Hooks are registered callbacks that fire at lifecycle events — not optional decorators, but primary control points.",
        "PreTool fires before execution; PostTool fires after. Stop hooks evaluate before the next loop iteration.",
        "Stop hooks returning a truthy signal halt the loop immediately — powerful but dangerous if conflicting.",
        "Silent failure is the #1 hook risk: uncaught exceptions are swallowed. Always test registration explicitly.",
        "Hook stacking is additive — more hooks = more complexity. Cap at 3-5 per event type."
    ],

    "next_steps":    "Lesson 3.18 — Hook Composition Patterns: chaining hooks, shared state between hooks, and the observer/interceptor distinction.",
    "anti_patterns": ["Silent-hook failure", "Hook stack explosion", "Stop-hook oscillation", "PreTool logging overhead"]
}


# ── Rendering ────────────────────────────────────────────────────────────────

def to_kebab(s: str) -> str:
    """Convert a title string to kebab-case."""
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def render_with_jinja2(template_path: Path, context: dict) -> str:
    """Render template using Jinja2 if available."""
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        env = Environment(
            loader=FileSystemLoader(str(template_path.parent)),
            autoescape=select_autoescape(["html"]),
            keep_trailing_newline=True,
        )
        # Disable autoescaping for diagram/text fields that contain raw HTML
        env.autoescape = False
        tmpl = env.get_template(template_path.name)
        return tmpl.render(**context)
    except ImportError:
        return None


def render_fallback(context: dict) -> str:
    """Simple string-based fallback renderer (no Jinja2 required)."""
    c = context

    def badge(text, cls="badge-indigo"):
        return f'<span class="badge {cls}">{text}</span>'

    def vocab_cards():
        if not c.get("vocabulary"):
            return "<p style='color:var(--muted)'>No vocabulary recorded.</p>"
        cards = []
        for v in c["vocabulary"]:
            cards.append(f'<div class="vocab-card"><div class="term">{v["term"]}</div><div class="def">{v["definition"]}</div></div>')
        return "\n".join(cards)

    def concept_cards():
        if not c.get("core_concepts"):
            return "<p style='color:var(--muted)'>No concepts recorded.</p>"
        cards = []
        for cc in c["core_concepts"]:
            cards.append(
                f'<div class="concept-card">'
                f'<div class="concept-label">{cc["label"]}</div>'
                f'<div class="concept-title">{cc["title"]}</div>'
                f'<div class="concept-body">{cc["summary"]}</div>'
                f'</div>'
            )
        return "\n".join(cards)

    def analogy_cards():
        if not c.get("analogies"):
            return "<p style='color:var(--muted)'>No analogies recorded.</p>"
        cards = []
        for a in c["analogies"]:
            diagram_html = f'<div class="diagram-box">{a["diagram"]}</div>' if a.get("diagram") else ""
            cards.append(
                f'<div class="analogy-card">'
                f'<div class="analogy-concept">{a["concept"]}</div>'
                f'<div class="analogy-text">{a["analogy"]}</div>'
                f'{diagram_html}'
                f'</div>'
            )
        return "\n".join(cards)

    def failure_cards():
        if not c.get("failure_modes"):
            return "<p style='color:var(--muted)'>No failure modes recorded.</p>"
        cards = []
        for f in c["failure_modes"]:
            fix_html = f'<div class="failure-fix">Fix: {f["fix"]}</div>' if f.get("fix") else ""
            cards.append(
                f'<div class="failure-card">'
                f'<div class="failure-type">{f["type"]}</div>'
                f'<div class="failure-name">{f["name"]}</div>'
                f'<div class="failure-desc">{f["description"]}</div>'
                f'{fix_html}'
                f'</div>'
            )
        return "\n".join(cards)

    def exercise_cards():
        if not c.get("exercises"):
            return "<p style='color:var(--muted)'>No exercises recorded.</p>"
        cards = []
        for e in c["exercises"]:
            steps_html = ""
            if e.get("steps"):
                steps_html = "<ol>" + "".join(f"<li>{s}</li>" for s in e["steps"]) + "</ol>"
            expected_html = f'<div class="expected"><strong>Expected:</strong> {e["expected_output"]}</div>' if e.get("expected_output") else ""
            cards.append(
                f'<div class="exercise-card">'
                f'<h3>{e["title"]}</h3>'
                f'<div class="task-text">{e["task"]}</div>'
                f'{steps_html}{expected_html}'
                f'</div>'
            )
        return "\n".join(cards)

    def timeline_items():
        if not c.get("checkpoints"):
            return "<p style='color:var(--muted)'>No checkpoints recorded.</p>"
        items = []
        for cp in c["checkpoints"]:
            items.append(
                f'<div class="timeline-item">'
                f'<div class="timeline-dot">{cp["layer"]}</div>'
                f'<div class="timeline-content">'
                f'<div class="tl-layer">{cp["layer"]} — {cp["layer_label"]}</div>'
                f'<div class="tl-concepts">{cp["concepts"]}</div>'
                f'<div class="tl-ts">{cp["timestamp"]}</div>'
                f'</div>'
                f'</div>'
            )
        return "\n".join(items)

    def summary_items():
        if not c.get("summary_points"):
            return "<li>Summary not yet recorded.</li>"
        return "\n".join(f"<li>{pt}</li>" for pt in c["summary_points"])

    tags_html = " ".join(badge(t, "badge-green") for t in c.get("lesson_tags", []))
    next_steps_html = (
        f'<div class="next-steps-box"><h3>Next Steps</h3><p>{c["next_steps"]}</p></div>'
        if c.get("next_steps") else ""
    )

    dots_html = "\n".join(
        f'<div class="dot {"active" if i == 0 else ""}" onclick="goTo({i})" title="Slide {i+1}"></div>'
        for i in range(8)
    )

    subtitle_html = f'<p style="font-size:1.15rem;color:var(--muted);margin-bottom:1.2rem;">{c["lesson_subtitle"]}</p>' if c.get("lesson_subtitle") else ""

    # Read the CSS/JS from the template file directly (just inline everything)
    # since this is a fallback, we embed a minimal version
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{c["lesson_id"]} — {c["lesson_title"]}</title>
<style>
:root{{--bg:#f8f7f4;--surface:#fff;--border:#e2e0da;--indigo:#4f46e5;--cyan:#06b6d4;--text:#1e1b18;--muted:#6b6560;--success:#16a34a;--warn:#ca8a04;--danger:#dc2626;--radius:12px;--shadow:0 4px 24px rgba(0,0,0,.08);--transition:.4s cubic-bezier(.4,0,.2,1)}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text)}}
#navbar{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:52px;background:var(--surface);border-bottom:1px solid var(--border);box-shadow:0 2px 8px rgba(0,0,0,.06)}}
#navbar .brand{{font-weight:700;font-size:.95rem;color:var(--indigo)}}
#navbar .meta{{font-size:.8rem;color:var(--muted)}}
#navbar .nav-controls{{display:flex;gap:.5rem;align-items:center}}
#navbar button{{padding:.3rem .8rem;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:.8rem;cursor:pointer}}
#navbar button:hover{{background:var(--indigo);color:#fff}}
#progress-bar{{position:fixed;top:52px;left:0;right:0;z-index:99;height:4px;background:var(--border)}}
#progress-fill{{height:100%;background:linear-gradient(90deg,var(--indigo),var(--cyan));transition:width var(--transition)}}
#slides{{position:fixed;top:56px;left:0;right:0;bottom:60px;overflow:hidden}}
.slide{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2.5rem 3rem;opacity:0;transform:translateX(60px);transition:opacity var(--transition),transform var(--transition);pointer-events:none;overflow-y:auto}}
.slide.active{{opacity:1;transform:translateX(0);pointer-events:auto}}
.slide.prev{{opacity:0;transform:translateX(-60px)}}
.slide-inner{{width:100%;max-width:960px}}
.slide-label{{font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--cyan);margin-bottom:.5rem}}
.slide h1{{font-size:2.6rem;font-weight:800;line-height:1.15;margin-bottom:.5rem}}
.slide h2{{font-size:1.9rem;font-weight:700;margin-bottom:1rem}}
.badge{{display:inline-block;padding:.2rem .7rem;border-radius:20px;font-size:.75rem;font-weight:600}}
.badge-indigo{{background:#ede9fe;color:var(--indigo)}}
.badge-cyan{{background:#cffafe;color:#0e7490}}
.badge-green{{background:#dcfce7;color:var(--success)}}
.tags{{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1rem}}
.stats-row{{display:flex;gap:1.5rem;margin-top:1rem;flex-wrap:wrap}}
.stat-card{{flex:1;min-width:100px;padding:1rem 1.2rem;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);text-align:center;box-shadow:var(--shadow)}}
.stat-card .val{{font-size:2rem;font-weight:800;color:var(--indigo)}}
.stat-card .lbl{{font-size:.75rem;color:var(--muted);margin-top:.2rem}}
.vocab-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;margin-top:1rem}}
.vocab-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.1rem 1.3rem;box-shadow:var(--shadow)}}
.vocab-card .term{{font-weight:700;font-size:1rem;color:var(--indigo);margin-bottom:.4rem}}
.vocab-card .def{{font-size:.88rem;color:var(--muted);line-height:1.5}}
.concept-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.2rem;margin-top:1rem}}
.concept-card{{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--indigo);border-radius:var(--radius);padding:1.2rem 1.4rem;box-shadow:var(--shadow)}}
.concept-label{{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--cyan);margin-bottom:.3rem}}
.concept-title{{font-size:1.05rem;font-weight:700;margin-bottom:.5rem}}
.concept-body{{font-size:.9rem;color:var(--muted);line-height:1.6}}
.analogy-card{{background:linear-gradient(135deg,#ede9fe 0%,#cffafe 100%);border-radius:var(--radius);padding:1.6rem 2rem;margin-top:1rem;border:1px solid #c4b5fd}}
.analogy-concept{{font-size:.75rem;font-weight:700;color:var(--indigo);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.4rem}}
.analogy-text{{font-size:1.05rem;line-height:1.7;margin-bottom:.8rem}}
.diagram-box{{background:var(--surface);border-radius:8px;padding:1rem 1.4rem;font-family:'Courier New',monospace;font-size:.85rem;white-space:pre-wrap;border:1px solid var(--border)}}
.failure-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;margin-top:1rem}}
.failure-card{{background:#fff7f7;border:1px solid #fecaca;border-left:4px solid var(--danger);border-radius:var(--radius);padding:1.1rem 1.3rem}}
.failure-type{{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--danger);margin-bottom:.3rem}}
.failure-name{{font-weight:700;font-size:.95rem;margin-bottom:.4rem}}
.failure-desc{{font-size:.87rem;color:var(--muted);line-height:1.5}}
.failure-fix{{margin-top:.7rem;font-size:.83rem;color:var(--success);font-weight:600;padding-top:.5rem;border-top:1px solid #fecaca}}
.exercise-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.6rem 2rem;margin-top:1rem;box-shadow:var(--shadow)}}
.exercise-card h3{{color:var(--indigo);font-size:1.1rem;margin-bottom:.6rem}}
.exercise-card .task-text{{font-size:1rem;margin-bottom:1rem;line-height:1.7}}
.exercise-card ol{{padding-left:1.4rem}}
.exercise-card ol li{{margin-bottom:.5rem;font-size:.93rem}}
.expected{{margin-top:1rem;background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:.8rem 1.1rem;font-size:.88rem;color:var(--success)}}
.timeline{{position:relative;padding:1rem 0;margin-top:1rem}}
.timeline::before{{content:'';position:absolute;left:20px;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--indigo),var(--cyan));border-radius:3px}}
.timeline-item{{display:flex;align-items:flex-start;gap:1.2rem;margin-bottom:1.5rem;position:relative}}
.timeline-dot{{flex-shrink:0;width:40px;height:40px;border-radius:50%;background:var(--indigo);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.85rem;box-shadow:0 0 0 4px var(--bg);position:relative;z-index:1}}
.timeline-content{{flex:1;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.3rem;box-shadow:var(--shadow)}}
.tl-layer{{font-weight:700;color:var(--indigo);font-size:.95rem}}
.tl-concepts{{font-size:.87rem;color:var(--text);line-height:1.6}}
.tl-ts{{font-size:.75rem;color:var(--muted);margin-top:.4rem}}
.summary-list{{list-style:none;padding:0;margin-top:1rem}}
.summary-list li{{display:flex;align-items:flex-start;gap:.8rem;padding:.8rem 1rem;margin-bottom:.6rem;background:var(--surface);border:1px solid var(--border);border-radius:8px}}
.summary-list li::before{{content:'✓';flex-shrink:0;width:22px;height:22px;background:var(--indigo);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;margin-top:2px}}
.next-steps-box{{margin-top:1.5rem;background:linear-gradient(135deg,var(--indigo) 0%,var(--cyan) 100%);color:#fff;border-radius:var(--radius);padding:1.2rem 1.6rem}}
.next-steps-box h3{{font-size:.85rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem;opacity:.8}}
#dots{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:100}}
.dot{{width:8px;height:8px;border-radius:50%;background:var(--border);cursor:pointer;transition:background .2s,transform .2s}}
.dot.active{{background:var(--indigo);transform:scale(1.4)}}
#arrow-prev,#arrow-next{{position:fixed;top:50%;transform:translateY(-50%);z-index:100;background:var(--surface);border:1px solid var(--border);border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:1.2rem;box-shadow:var(--shadow)}}
#arrow-prev{{left:16px}}#arrow-next{{right:16px}}
#arrow-prev:hover,#arrow-next:hover{{background:var(--indigo);color:#fff}}
</style>
</head>
<body>
<nav id="navbar">
  <span class="brand">{c["lesson_id"]} — {c["lesson_title"]}</span>
  <span class="meta">{c["chapter_title"]} &nbsp;·&nbsp; {c["lesson_date"]}</span>
  <div class="nav-controls">
    <span id="slide-counter" style="font-size:.8rem;color:var(--muted);margin-right:.5rem">1 / 8</span>
    <button onclick="goTo(0)">Start</button>
    <button onclick="goTo(7)">End</button>
  </div>
</nav>
<div id="progress-bar"><div id="progress-fill" style="width:12.5%"></div></div>
<button id="arrow-prev" onclick="prevSlide()" aria-label="Previous">&#8592;</button>
<button id="arrow-next" onclick="nextSlide()" aria-label="Next">&#8594;</button>
<div id="slides">
  <div class="slide active" data-index="0">
    <div class="slide-inner">
      <div class="slide-label">{c.get("chapter_badge","")}</div>
      <h1>{c["lesson_title"]}</h1>
      {subtitle_html}
      <div class="tags">
        <span class="badge badge-indigo">{c.get("layer_label","")}</span>
        <span class="badge badge-cyan">{c["lesson_id"]}</span>
        {tags_html}
      </div>
      <div class="stats-row" style="margin-top:2rem">
        <div class="stat-card"><div class="val">{c.get("concept_count",0)}</div><div class="lbl">Concepts</div></div>
        <div class="stat-card"><div class="val">{c.get("vocab_count",0)}</div><div class="lbl">Terms</div></div>
        <div class="stat-card"><div class="val">{c.get("checkpoint_count",0)}</div><div class="lbl">Checkpoints</div></div>
      </div>
    </div>
  </div>
  <div class="slide" data-index="1">
    <div class="slide-inner">
      <div class="slide-label">Terminology First</div>
      <h2>Key Vocabulary</h2>
      <div class="vocab-grid">{vocab_cards()}</div>
    </div>
  </div>
  <div class="slide" data-index="2">
    <div class="slide-inner">
      <div class="slide-label">Explain with Depth</div>
      <h2>Core Concepts</h2>
      <div class="concept-grid">{concept_cards()}</div>
    </div>
  </div>
  <div class="slide" data-index="3">
    <div class="slide-inner">
      <div class="slide-label">Analogize &amp; Visualize</div>
      <h2>Analogies &amp; Mental Models</h2>
      {analogy_cards()}
    </div>
  </div>
  <div class="slide" data-index="4">
    <div class="slide-inner">
      <div class="slide-label">What Goes Wrong</div>
      <h2>Failure Modes &amp; Anti-Patterns</h2>
      <div class="failure-grid">{failure_cards()}</div>
    </div>
  </div>
  <div class="slide" data-index="5">
    <div class="slide-inner">
      <div class="slide-label">Hands-On Practice</div>
      <h2>Exercises</h2>
      {exercise_cards()}
    </div>
  </div>
  <div class="slide" data-index="6">
    <div class="slide-inner">
      <div class="slide-label">Progress</div>
      <h2>Checkpoint Timeline</h2>
      <div class="timeline">{timeline_items()}</div>
    </div>
  </div>
  <div class="slide" data-index="7">
    <div class="slide-inner">
      <div class="slide-label">Lesson Complete</div>
      <h2>Summary</h2>
      <ul class="summary-list">{summary_items()}</ul>
      {next_steps_html}
    </div>
  </div>
</div>
<div id="dots">{dots_html}</div>
<script>
const totalSlides=8;let current=0;
const slides=document.querySelectorAll('.slide');
const dots=document.querySelectorAll('.dot');
const fill=document.getElementById('progress-fill');
const counter=document.getElementById('slide-counter');
function updateUI(){{
  slides.forEach((s,i)=>{{s.classList.remove('active','prev');if(i===current)s.classList.add('active');else if(i<current)s.classList.add('prev');}});
  dots.forEach((d,i)=>d.classList.toggle('active',i===current));
  fill.style.width=((current+1)/totalSlides*100)+'%';
  counter.textContent=(current+1)+' / '+totalSlides;
}}
function goTo(n){{if(n<0||n>=totalSlides)return;current=n;updateUI();}}
function nextSlide(){{goTo(current+1);}}
function prevSlide(){{goTo(current-1);}}
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key==='ArrowDown')nextSlide();
  if(e.key==='ArrowLeft'||e.key==='ArrowUp')prevSlide();
  if(e.key==='Home')goTo(0);if(e.key==='End')goTo(7);
}});
let tx=null;
document.addEventListener('touchstart',e=>{{tx=e.touches[0].clientX;}});
document.addEventListener('touchend',e=>{{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)dx<0?nextSlide():prevSlide();tx=null;}});
updateUI();
</script>
</body>
</html>"""
    return html


def generate(content: dict, output_dir: Path) -> Path:
    """Render content to HTML and write to output_dir. Returns output path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    lesson_id    = content.get("lesson_id", "unknown")
    lesson_title = content.get("lesson_title", "Lesson")
    filename     = f"lesson-{lesson_id}-{to_kebab(lesson_title)}.html"
    output_path  = output_dir / filename

    # Try Jinja2 first
    html = None
    if TEMPLATE_FILE.exists():
        html = render_with_jinja2(TEMPLATE_FILE, content)
        if html is None:
            print("ℹ️  Jinja2 not available — using fallback renderer.")

    if html is None:
        html = render_fallback(content)

    output_path.write_text(html, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate lesson HTML presentations.")
    parser.add_argument("--content", help="Path to content JSON file")
    parser.add_argument("--output",  help="Output directory (default: visual-presentations/)", default=None)
    parser.add_argument("--demo",    action="store_true", help="Generate a sample Hook Architecture presentation")
    args = parser.parse_args()

    if not args.demo and not args.content:
        parser.print_help()
        sys.exit(1)

    output_dir = Path(args.output) if args.output else OUTPUT_DIR

    if args.demo:
        content = DEMO_CONTENT
        print("ℹ️  Using built-in demo content (Lesson 3.17 — Hook Architecture)")
    else:
        content_path = Path(args.content)
        if not content_path.exists():
            print(f"ERROR: Content file not found: {content_path}")
            sys.exit(1)
        with open(content_path, encoding="utf-8") as f:
            content = json.load(f)

    output_path = generate(content, output_dir)
    print(f"✅ HTML presentation written to: {output_path}")


if __name__ == "__main__":
    main()
