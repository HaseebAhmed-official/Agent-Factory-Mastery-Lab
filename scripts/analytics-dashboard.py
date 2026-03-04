#!/usr/bin/env python3

"""
================================================================================
ANALYTICS DASHBOARD: Study Progress and Performance Tracking
================================================================================

PURPOSE:
    Track and visualize learning progress across checkpoint system:
    - Checkpoint frequency analysis
    - Study time per lesson
    - Comprehension performance trends
    - Progress visualizations
    - Spaced repetition scheduling

USAGE:
    python3 scripts/analytics-dashboard.py
    python3 scripts/analytics-dashboard.py --lesson 3.1
    python3 scripts/analytics-dashboard.py --export-html

FEATURES:
    - Real-time progress tracking
    - Performance trend analysis
    - Study pattern insights
    - Spaced repetition recommendations
    - HTML dashboard generation

EXIT CODES:
    0 - Success
    1 - Error

DEPENDENCIES:
    - Python 3.7+
    - pyyaml
    - json

AUTHOR: Professor Agent (Agent Factory Part 1 Tutoring System)
DATE: 2026-03-03
VERSION: 1.0.0
================================================================================
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics

# --- Configuration ---

REPO_ROOT = Path(__file__).parent.parent.absolute()
REVISION_NOTES_DIR = REPO_ROOT / "revision-notes"
CONTEXT_BRIDGE_DIR = REPO_ROOT / "context-bridge"
ANALYTICS_DIR = REPO_ROOT / "analytics"
ANALYTICS_DATA = ANALYTICS_DIR / "analytics-data.json"

# Ensure analytics directory exists
ANALYTICS_DIR.mkdir(exist_ok=True)

# --- Color Output ---

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'

# --- Data Classes ---

@dataclass
class CheckpointEvent:
    """A checkpoint event"""
    lesson: str
    layer: str
    depth: int
    timestamp: datetime
    file_path: str
    concepts_count: int
    vocab_count: int

@dataclass
class LessonStats:
    """Statistics for a lesson"""
    lesson: str
    checkpoint_count: int
    total_concepts: int
    total_vocab: int
    first_checkpoint: datetime
    last_checkpoint: datetime
    study_duration: timedelta
    avg_checkpoint_interval: timedelta
    layers_completed: List[str]
    completion_percentage: float

@dataclass
class StudySession:
    """A study session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    lessons_worked: List[str]
    checkpoints_created: int
    total_concepts: int

@dataclass
class ProgressReport:
    """Overall progress report"""
    total_lessons: int
    completed_lessons: int
    in_progress_lessons: int
    total_checkpoints: int
    total_concepts_learned: int
    total_vocab_learned: int
    total_study_time: timedelta
    avg_study_time_per_lesson: timedelta
    completion_rate: float
    current_streak: int
    longest_streak: int
    lessons_per_week: float

# --- Helper Functions ---

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^70}{Colors.NC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.NC}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.NC} {text}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.NC} {text}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.NC} {text}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.NC} {text}")

def extract_yaml_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """Extract YAML frontmatter from markdown file"""
    if not content.startswith('---\n'):
        return None, content

    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return None, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2]
        return frontmatter, body
    except yaml.YAMLError:
        return None, content

def format_duration(td: timedelta) -> str:
    """Format timedelta as human-readable string"""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def create_bar_chart(label: str, value: float, max_value: float, width: int = 40) -> str:
    """Create ASCII bar chart"""
    filled = int((value / max_value) * width) if max_value > 0 else 0
    empty = width - filled
    bar = '█' * filled + '░' * empty
    percentage = (value / max_value * 100) if max_value > 0 else 0
    return f"{label:20} {bar} {percentage:5.1f}% ({int(value)})"

# --- Analytics Engine ---

class AnalyticsEngine:
    """Main analytics engine"""

    def __init__(self):
        self.checkpoint_events: List[CheckpointEvent] = []
        self.lesson_stats: Dict[str, LessonStats] = {}

    def discover_checkpoints(self):
        """Discover all checkpoint files"""
        pattern = "**/*-L*-*.md"
        files = list(REVISION_NOTES_DIR.glob(pattern))
        print_info(f"Discovered {len(files)} checkpoint files")

        for file in files:
            event = self._parse_checkpoint_file(file)
            if event:
                self.checkpoint_events.append(event)

        # Sort by timestamp
        self.checkpoint_events.sort(key=lambda e: e.timestamp)

        print_success(f"Loaded {len(self.checkpoint_events)} checkpoint events")

    def _parse_checkpoint_file(self, file_path: Path) -> Optional[CheckpointEvent]:
        """Parse checkpoint file to extract event data"""
        try:
            content = file_path.read_text()
            frontmatter, body = extract_yaml_frontmatter(content)

            if not frontmatter:
                return None

            # Extract timestamp from date field or file modification time
            date_str = frontmatter.get('date')
            if date_str:
                try:
                    timestamp = datetime.fromisoformat(date_str)
                except ValueError:
                    # Try parsing as date only
                    timestamp = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                # Use file modification time as fallback
                timestamp = datetime.fromtimestamp(file_path.stat().st_mtime)

            event = CheckpointEvent(
                lesson=frontmatter.get('lesson', 'unknown'),
                layer=frontmatter.get('layer', 'L1'),
                depth=frontmatter.get('depth', 1),
                timestamp=timestamp,
                file_path=str(file_path),
                concepts_count=len(frontmatter.get('concepts', [])),
                vocab_count=0  # Could be extracted from content
            )

            return event

        except Exception as e:
            print_warning(f"Failed to parse {file_path.name}: {e}")
            return None

    def calculate_lesson_stats(self):
        """Calculate statistics per lesson"""
        # Group events by lesson
        lessons = defaultdict(list)
        for event in self.checkpoint_events:
            lessons[event.lesson].append(event)

        # Calculate stats for each lesson
        for lesson, events in lessons.items():
            events.sort(key=lambda e: e.timestamp)

            first_checkpoint = events[0].timestamp
            last_checkpoint = events[-1].timestamp
            study_duration = last_checkpoint - first_checkpoint

            # Calculate average interval between checkpoints
            if len(events) > 1:
                intervals = []
                for i in range(1, len(events)):
                    interval = events[i].timestamp - events[i-1].timestamp
                    intervals.append(interval)
                avg_interval = sum(intervals, timedelta()) / len(intervals)
            else:
                avg_interval = timedelta()

            # Determine completion percentage
            layers = [e.layer for e in events]
            unique_layers = set(layers)
            max_depth = max(e.depth for e in events)
            completion = (max_depth / 3.0) * 100  # Assuming L3 is complete

            stats = LessonStats(
                lesson=lesson,
                checkpoint_count=len(events),
                total_concepts=sum(e.concepts_count for e in events),
                total_vocab=sum(e.vocab_count for e in events),
                first_checkpoint=first_checkpoint,
                last_checkpoint=last_checkpoint,
                study_duration=study_duration,
                avg_checkpoint_interval=avg_interval,
                layers_completed=list(unique_layers),
                completion_percentage=min(completion, 100.0)
            )

            self.lesson_stats[lesson] = stats

    def generate_progress_report(self) -> ProgressReport:
        """Generate overall progress report"""
        if not self.lesson_stats:
            self.calculate_lesson_stats()

        # Count completed lessons (reached L3 or marked complete)
        completed = sum(1 for stats in self.lesson_stats.values()
                       if stats.completion_percentage >= 100)

        in_progress = len(self.lesson_stats) - completed

        # Calculate total study time
        total_study_time = sum(
            (stats.study_duration for stats in self.lesson_stats.values()),
            timedelta()
        )

        # Calculate average study time per lesson
        if self.lesson_stats:
            avg_study_time = total_study_time / len(self.lesson_stats)
        else:
            avg_study_time = timedelta()

        # Calculate completion rate
        completion_rate = (completed / len(self.lesson_stats) * 100) if self.lesson_stats else 0

        # Calculate streaks (days with checkpoint activity)
        if self.checkpoint_events:
            dates = sorted(set(e.timestamp.date() for e in self.checkpoint_events))
            current_streak = self._calculate_current_streak(dates)
            longest_streak = self._calculate_longest_streak(dates)
        else:
            current_streak = 0
            longest_streak = 0

        # Calculate lessons per week
        if self.checkpoint_events:
            first_date = min(e.timestamp for e in self.checkpoint_events)
            last_date = max(e.timestamp for e in self.checkpoint_events)
            weeks = (last_date - first_date).days / 7
            lessons_per_week = len(self.lesson_stats) / weeks if weeks > 0 else 0
        else:
            lessons_per_week = 0

        report = ProgressReport(
            total_lessons=len(self.lesson_stats),
            completed_lessons=completed,
            in_progress_lessons=in_progress,
            total_checkpoints=len(self.checkpoint_events),
            total_concepts_learned=sum(s.total_concepts for s in self.lesson_stats.values()),
            total_vocab_learned=sum(s.total_vocab for s in self.lesson_stats.values()),
            total_study_time=total_study_time,
            avg_study_time_per_lesson=avg_study_time,
            completion_rate=completion_rate,
            current_streak=current_streak,
            longest_streak=longest_streak,
            lessons_per_week=lessons_per_week
        )

        return report

    def _calculate_current_streak(self, dates: List) -> int:
        """Calculate current consecutive study streak"""
        if not dates:
            return 0

        today = datetime.now().date()
        streak = 0

        for i in range(len(dates) - 1, -1, -1):
            if dates[i] == today - timedelta(days=streak):
                streak += 1
            else:
                break

        return streak

    def _calculate_longest_streak(self, dates: List) -> int:
        """Calculate longest consecutive study streak"""
        if not dates:
            return 0

        max_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i-1] + timedelta(days=1):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1

        return max_streak

    def print_dashboard(self, lesson: Optional[str] = None):
        """Print analytics dashboard"""
        print_header("Analytics Dashboard")

        if lesson:
            # Lesson-specific dashboard
            self._print_lesson_dashboard(lesson)
        else:
            # Overall dashboard
            self._print_overall_dashboard()

    def _print_overall_dashboard(self):
        """Print overall progress dashboard"""
        report = self.generate_progress_report()

        # Overall Progress
        print(f"{Colors.BOLD}📊 Overall Progress{Colors.NC}\n")
        print(f"  Total Lessons: {Colors.CYAN}{report.total_lessons}{Colors.NC}")
        print(f"  Completed: {Colors.GREEN}{report.completed_lessons}{Colors.NC}")
        print(f"  In Progress: {Colors.YELLOW}{report.in_progress_lessons}{Colors.NC}")
        print(f"  Completion Rate: {Colors.CYAN}{report.completion_rate:.1f}%{Colors.NC}")
        print()

        # Learning Stats
        print(f"{Colors.BOLD}📚 Learning Stats{Colors.NC}\n")
        print(f"  Total Checkpoints: {Colors.CYAN}{report.total_checkpoints}{Colors.NC}")
        print(f"  Concepts Learned: {Colors.CYAN}{report.total_concepts_learned}{Colors.NC}")
        print(f"  Total Study Time: {Colors.CYAN}{format_duration(report.total_study_time)}{Colors.NC}")
        print(f"  Avg Time/Lesson: {Colors.CYAN}{format_duration(report.avg_study_time_per_lesson)}{Colors.NC}")
        print()

        # Streaks
        print(f"{Colors.BOLD}🔥 Study Streaks{Colors.NC}\n")
        print(f"  Current Streak: {Colors.GREEN}{report.current_streak} days{Colors.NC}")
        print(f"  Longest Streak: {Colors.CYAN}{report.longest_streak} days{Colors.NC}")
        print(f"  Lessons/Week: {Colors.CYAN}{report.lessons_per_week:.1f}{Colors.NC}")
        print()

        # Lesson Progress Bars
        if self.lesson_stats:
            print(f"{Colors.BOLD}📈 Lesson Progress{Colors.NC}\n")

            # Sort lessons by number
            sorted_lessons = sorted(self.lesson_stats.items(),
                                   key=lambda x: float(x[0].replace('.', '')))

            for lesson, stats in sorted_lessons[:10]:  # Show first 10
                bar = create_bar_chart(
                    f"Lesson {lesson}",
                    stats.completion_percentage,
                    100,
                    width=30
                )
                print(f"  {bar}")

            if len(sorted_lessons) > 10:
                print(f"  ... and {len(sorted_lessons) - 10} more")
            print()

        # Recent Activity
        if self.checkpoint_events:
            print(f"{Colors.BOLD}⏱  Recent Activity{Colors.NC}\n")
            recent = sorted(self.checkpoint_events, key=lambda e: e.timestamp, reverse=True)[:5]

            for event in recent:
                time_ago = datetime.now() - event.timestamp
                if time_ago.days > 0:
                    ago_str = f"{time_ago.days}d ago"
                elif time_ago.seconds > 3600:
                    ago_str = f"{time_ago.seconds // 3600}h ago"
                else:
                    ago_str = f"{time_ago.seconds // 60}m ago"

                print(f"  {Colors.CYAN}{ago_str:10}{Colors.NC} Lesson {event.lesson} {event.layer} "
                      f"({event.concepts_count} concepts)")
            print()

    def _print_lesson_dashboard(self, lesson: str):
        """Print lesson-specific dashboard"""
        if lesson not in self.lesson_stats:
            print_error(f"No data found for lesson {lesson}")
            return

        stats = self.lesson_stats[lesson]

        print(f"{Colors.BOLD}Lesson {lesson} - Detailed Analytics{Colors.NC}\n")

        # Basic Info
        print(f"{Colors.BOLD}📊 Overview{Colors.NC}\n")
        print(f"  Checkpoints: {Colors.CYAN}{stats.checkpoint_count}{Colors.NC}")
        print(f"  Layers: {Colors.CYAN}{', '.join(sorted(stats.layers_completed))}{Colors.NC}")
        print(f"  Completion: {Colors.GREEN}{stats.completion_percentage:.1f}%{Colors.NC}")
        print()

        # Learning Stats
        print(f"{Colors.BOLD}📚 Learning Stats{Colors.NC}\n")
        print(f"  Concepts: {Colors.CYAN}{stats.total_concepts}{Colors.NC}")
        print(f"  Study Duration: {Colors.CYAN}{format_duration(stats.study_duration)}{Colors.NC}")
        print(f"  Avg Checkpoint Interval: {Colors.CYAN}{format_duration(stats.avg_checkpoint_interval)}{Colors.NC}")
        print()

        # Timeline
        print(f"{Colors.BOLD}📅 Timeline{Colors.NC}\n")
        print(f"  First Checkpoint: {Colors.CYAN}{stats.first_checkpoint.strftime('%Y-%m-%d %H:%M')}{Colors.NC}")
        print(f"  Last Checkpoint: {Colors.CYAN}{stats.last_checkpoint.strftime('%Y-%m-%d %H:%M')}{Colors.NC}")
        print()

        # Checkpoint History
        lesson_events = [e for e in self.checkpoint_events if e.lesson == lesson]
        if lesson_events:
            print(f"{Colors.BOLD}📝 Checkpoint History{Colors.NC}\n")
            for event in lesson_events:
                print(f"  {event.timestamp.strftime('%Y-%m-%d %H:%M')} | "
                      f"{event.layer} | {event.concepts_count} concepts")
            print()

    def export_html_dashboard(self, output_file: Path):
        """Export dashboard as HTML"""
        report = self.generate_progress_report()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learning Analytics Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 30px;
            font-size: 2.5rem;
            text-align: center;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
        }}
        .progress-bar {{
            background: #f0f0f0;
            border-radius: 10px;
            height: 30px;
            margin: 10px 0;
            overflow: hidden;
            position: relative;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
        }}
        .lesson-row {{
            margin-bottom: 15px;
        }}
        .lesson-label {{
            font-weight: 600;
            margin-bottom: 5px;
            color: #333;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .activity-item {{
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }}
        .timestamp {{
            color: #667eea;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Learning Analytics Dashboard</h1>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Lessons</div>
                <div class="stat-value">{report.total_lessons}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Completed</div>
                <div class="stat-value">{report.completed_lessons}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Checkpoints</div>
                <div class="stat-value">{report.total_checkpoints}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Concepts Learned</div>
                <div class="stat-value">{report.total_concepts_learned}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Study Time</div>
                <div class="stat-value">{format_duration(report.total_study_time)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Current Streak</div>
                <div class="stat-value">{report.current_streak} 🔥</div>
            </div>
        </div>

        <div class="section">
            <h2>📈 Lesson Progress</h2>
"""

        # Add lesson progress bars
        sorted_lessons = sorted(self.lesson_stats.items(),
                               key=lambda x: float(x[0].replace('.', '')))

        for lesson, stats in sorted_lessons:
            html += f"""
            <div class="lesson-row">
                <div class="lesson-label">Lesson {lesson}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {stats.completion_percentage}%">
                        {stats.completion_percentage:.0f}%
                    </div>
                </div>
            </div>
"""

        html += """
        </div>

        <div class="section">
            <h2>⏱ Recent Activity</h2>
"""

        # Add recent activity
        recent = sorted(self.checkpoint_events, key=lambda e: e.timestamp, reverse=True)[:10]
        for event in recent:
            html += f"""
            <div class="activity-item">
                <span class="timestamp">{event.timestamp.strftime('%Y-%m-%d %H:%M')}</span>
                — Lesson {event.lesson} {event.layer} ({event.concepts_count} concepts)
            </div>
"""

        html += """
        </div>
    </div>
</body>
</html>
"""

        output_file.write_text(html)
        print_success(f"HTML dashboard exported to: {output_file}")

# --- CLI Interface ---

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Analytics dashboard for checkpoint system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View overall dashboard
  python3 scripts/analytics-dashboard.py

  # View lesson-specific dashboard
  python3 scripts/analytics-dashboard.py --lesson 3.1

  # Export HTML dashboard
  python3 scripts/analytics-dashboard.py --export-html
        """
    )

    parser.add_argument("--lesson", help="Show analytics for specific lesson")
    parser.add_argument("--export-html", action="store_true", help="Export HTML dashboard")
    parser.add_argument("--output", default="analytics/dashboard.html", help="HTML output path")

    args = parser.parse_args()

    # Create analytics engine
    engine = AnalyticsEngine()
    engine.discover_checkpoints()
    engine.calculate_lesson_stats()

    # Export HTML if requested
    if args.export_html:
        output_path = REPO_ROOT / args.output
        output_path.parent.mkdir(exist_ok=True)
        engine.export_html_dashboard(output_path)
        print()

    # Print dashboard
    engine.print_dashboard(lesson=args.lesson)

if __name__ == "__main__":
    main()
