#!/usr/bin/env python3

"""
================================================================================
GIT AUTO-PUSH: Smart Auto-Commit & Push for Checkpoint System
================================================================================

PURPOSE:
    Automatically commit and push checkpoint files to git repository.
    Detects remote, validates quality, creates semantic commits, and tags.

USAGE:
    python3 scripts/git-auto-push.py checkpoint 3.1 L1
    python3 scripts/git-auto-push.py finish 3.1
    python3 scripts/git-auto-push.py --dry-run checkpoint 3.1 L2

FEATURES:
    - Auto-detect git remote (origin, upstream, etc.)
    - Semantic commit messages (follows Conventional Commits)
    - Quality validation (via pre-commit hook)
    - Auto-tagging on Finish
    - Lesson-branch workflow support
    - Conflict detection and resolution guidance
    - Dry-run mode for safety

EXIT CODES:
    0 - Success
    1 - Git operation failed
    2 - Quality validation failed
    3 - No changes to commit
    4 - User cancelled

DEPENDENCIES:
    - git (system command)
    - Python 3.7+

AUTHOR: Professor Agent (Agent Factory Part 1 Tutoring System)
DATE: 2026-03-03
VERSION: 1.0.0
================================================================================
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from datetime import datetime

# --- Worktree Detection ---

def get_git_context() -> dict:
    """
    Detect git worktree vs main repo and return normalized context.

    In a git worktree, .git is a FILE (not a directory) containing a reference
    to the main repo's .git directory. This function handles both cases and
    ensures all git operations use the correct working directory.

    Returns:
        dict with keys: repo_root, worktree_root, current_branch, is_worktree
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        worktree_root = Path(result.stdout.strip())
        git_path = worktree_root / ".git"

        # In a worktree, .git is a FILE referencing the common git dir
        is_worktree = git_path.is_file()

        if is_worktree:
            # Parse "gitdir: /path/to/main/.git/worktrees/name"
            git_file_content = git_path.read_text().strip()
            worktrees_git_dir = Path(git_file_content.replace("gitdir: ", ""))
            # .git/worktrees/{name} -> .git -> main repo root
            main_git_dir = worktrees_git_dir.parent.parent
            repo_root = main_git_dir.parent
        else:
            repo_root = worktree_root

        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, check=True,
            cwd=str(worktree_root)
        )
        current_branch = branch_result.stdout.strip()

        return {
            "repo_root": repo_root,
            "worktree_root": worktree_root,
            "current_branch": current_branch,
            "is_worktree": is_worktree,
        }
    except (subprocess.CalledProcessError, OSError):
        # Fallback to original behavior if detection fails
        fallback = Path(__file__).parent.parent.absolute()
        return {
            "repo_root": fallback,
            "worktree_root": fallback,
            "current_branch": "main",
            "is_worktree": False,
        }


# --- Configuration ---

# Determine repo root dynamically (handles worktrees)
_GIT_CONTEXT = get_git_context()
REPO_ROOT = _GIT_CONTEXT["repo_root"]
# Git operations (add, commit, push) must run from the working tree where
# files actually live — for worktrees this differs from repo_root.
WORK_ROOT = _GIT_CONTEXT["worktree_root"]
DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "main"
TAG_PREFIX = "lesson-"
COMMIT_PREFIX_MAP = {
    "checkpoint": "docs(checkpoint)",
    "finish": "docs(lesson)",
    "rewind": "refactor(checkpoint)"
}

# --- Color Output ---

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

# --- Helper Functions ---

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.NC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.NC}\n")

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

def run_command(cmd: List[str], capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command safely from the active working tree root.

    Uses WORK_ROOT (worktree root) rather than REPO_ROOT so that git add/commit/push
    operate on the files in the current working tree. In a worktree these differ:
    REPO_ROOT is the main repo, WORK_ROOT is the worktree where files live.
    """
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, check=check, cwd=str(WORK_ROOT))
        else:
            result = subprocess.run(cmd, check=check, cwd=str(WORK_ROOT))
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        if e.stderr:
            print(f"{Colors.RED}{e.stderr}{Colors.NC}")
        raise

# --- Git Operations ---

class GitManager:
    """Manages all git operations"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        ctx = get_git_context()
        self.repo_root = ctx["repo_root"]
        self.worktree_root = ctx["worktree_root"]
        self.current_branch = ctx["current_branch"]
        self.is_worktree = ctx["is_worktree"]
        if self.is_worktree:
            print_info(f"Worktree detected: {self.worktree_root}")
            print_info(f"Main repo root: {self.repo_root}")

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            run_command(["git", "rev-parse", "--is-inside-work-tree"])
            return True
        except subprocess.CalledProcessError:
            return False

    def get_current_branch(self) -> str:
        """Get current git branch name"""
        result = run_command(["git", "branch", "--show-current"])
        return result.stdout.strip()

    def get_remote_name(self) -> Optional[str]:
        """Auto-detect git remote name"""
        result = run_command(["git", "remote"], check=False)
        remotes = result.stdout.strip().split('\n')

        if not remotes or remotes == ['']:
            return None

        # Prefer 'origin', otherwise use first available
        if 'origin' in remotes:
            return 'origin'
        return remotes[0]

    def get_remote_url(self, remote: str) -> Optional[str]:
        """Get URL for specified remote"""
        try:
            result = run_command(["git", "remote", "get-url", remote])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes"""
        result = run_command(["git", "status", "--porcelain"])
        return bool(result.stdout.strip())

    def get_staged_files(self) -> List[str]:
        """Get list of staged files"""
        result = run_command(["git", "diff", "--cached", "--name-only"])
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]

    def stage_files(self, patterns: List[str]):
        """Stage files matching patterns"""
        if self.dry_run:
            print_info(f"[DRY RUN] Would stage: {', '.join(patterns)}")
            return

        for pattern in patterns:
            try:
                run_command(["git", "add", pattern])
                print_success(f"Staged: {pattern}")
            except subprocess.CalledProcessError:
                print_warning(f"No files matched pattern: {pattern}")

    def commit(self, message: str, allow_empty: bool = False):
        """Create git commit"""
        if self.dry_run:
            print_info(f"[DRY RUN] Would commit with message:\n  {message}")
            return

        cmd = ["git", "commit", "-m", message]
        if allow_empty:
            cmd.append("--allow-empty")

        try:
            run_command(cmd, capture_output=False)
            print_success(f"Committed: {message}")
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e.stderr):
                print_info("No changes to commit")
            else:
                raise

    def tag(self, tag_name: str, message: str):
        """Create git tag"""
        if self.dry_run:
            print_info(f"[DRY RUN] Would create tag: {tag_name}")
            return

        # Check if tag already exists
        result = run_command(["git", "tag", "-l", tag_name])
        if result.stdout.strip():
            print_warning(f"Tag '{tag_name}' already exists, skipping")
            return

        run_command(["git", "tag", "-a", tag_name, "-m", message])
        print_success(f"Created tag: {tag_name}")

    def push(self, remote: str, branch: str, tags: bool = False):
        """Push to remote"""
        if self.dry_run:
            print_info(f"[DRY RUN] Would push to {remote}/{branch}" + (" (with tags)" if tags else ""))
            return

        cmd = ["git", "push", remote, branch]
        if tags:
            cmd.append("--tags")

        try:
            run_command(cmd, capture_output=False)
            print_success(f"Pushed to {remote}/{branch}" + (" (with tags)" if tags else ""))
        except subprocess.CalledProcessError as e:
            print_error(f"Push failed: {e}")
            print_info("Possible reasons:")
            print("  - No network connection")
            print("  - Remote branch is ahead (need to pull first)")
            print("  - Authentication failed")
            print("  - No write permission")
            raise

    def pull(self, remote: str, branch: str):
        """Pull from remote"""
        if self.dry_run:
            print_info(f"[DRY RUN] Would pull from {remote}/{branch}")
            return

        try:
            run_command(["git", "pull", remote, branch], capture_output=False)
            print_success(f"Pulled from {remote}/{branch}")
        except subprocess.CalledProcessError:
            print_error("Pull failed (merge conflicts?)")
            raise

# --- Checkpoint Auto-Push ---

class CheckpointAutoPush:
    """Handles auto-commit and auto-push for checkpoints"""

    def __init__(self, dry_run: bool = False, skip_quality: bool = False):
        self.git = GitManager(dry_run=dry_run)
        self.dry_run = dry_run
        self.skip_quality = skip_quality

    def checkpoint_workflow(self, lesson: str, layer: str):
        """Auto-push after checkpoint"""
        print_header(f"Checkpoint Auto-Push: Lesson {lesson} Layer {layer}")

        # 1. Verify git repo
        if not self.git.is_git_repo():
            print_error("Not a git repository. Skipping auto-push.")
            return

        # 2. Detect remote
        remote = self.git.get_remote_name()
        if not remote:
            print_warning("No git remote configured. Skipping push.")
            print_info("Hint: Add a remote with: git remote add origin <url>")
            remote = None

        # 3. Stage checkpoint files (worktree-aware paths)
        layer_lower = layer.lower()
        patterns = [
            f"revision-notes/**/module*/{lesson}-*/{lesson}-{layer_lower}-*.md",
            f"context-bridge/master-cumulative.md",
            f"context-bridge/snapshots/lesson-{lesson}-{layer_lower}-*.md",
            f"context-bridge/backup/master-cumulative-*.md",
            f"revision-notes/**/module*/{lesson}-*/.checkpoint-meta.json",
            f"revision-notes/**/module*/{lesson}-*/teaching-log-current.md",
            f"revision-notes/**/module*/{lesson}-*/pending-topics.md",
        ]

        print_info("Staging checkpoint files...")
        self.git.stage_files(patterns)

        # 4. Check if anything was staged
        staged = self.git.get_staged_files()
        if not staged:
            print_warning("No checkpoint files found to commit")
            return

        print_info(f"Staged {len(staged)} file(s):")
        for f in staged:
            print(f"  - {f}")

        # 5. Create commit message
        commit_msg = self._generate_checkpoint_commit_message(lesson, layer)

        # 6. Commit (pre-commit hook will validate quality)
        try:
            self.git.commit(commit_msg)
        except subprocess.CalledProcessError:
            print_error("Commit blocked by quality checks")
            print_info("Run: ./scripts/validate-notes.sh " + lesson)
            sys.exit(2)

        # 7. Push if remote exists
        if remote:
            branch = self.git.get_current_branch()
            try:
                self.git.push(remote, branch)
            except subprocess.CalledProcessError:
                print_warning("Push failed. You may need to pull first:")
                print(f"  git pull {remote} {branch}")
                sys.exit(1)

        print_success("Checkpoint auto-push complete!")

    def finish_workflow(self, lesson: str):
        """Auto-push after finish (includes tagging)"""
        print_header(f"Finish Auto-Push: Lesson {lesson}")

        # 1. Verify git repo
        if not self.git.is_git_repo():
            print_error("Not a git repository. Skipping auto-push.")
            return

        # 2. Detect remote
        remote = self.git.get_remote_name()
        if not remote:
            print_warning("No git remote configured. Skipping push.")
            remote = None

        # 3. Stage all lesson artifacts (worktree-aware paths)
        patterns = [
            f"revision-notes/**/module*/{lesson}-*/*.md",
            f"context-bridge/master-cumulative.md",
            f"context-bridge/snapshots/lesson-{lesson}-*.md",
            f"context-bridge/backup/master-cumulative-*.md",
            f"visual-presentations/session-*-lesson-{lesson}-*.html",
            f"quick-reference/lesson-{lesson}-*.md",
            f"flashcards/lesson-{lesson}-*.json",
            f"revision-notes/INDEX.md",
            f"visual-presentations/concept-map*.json",
            f"search-index/*.json"
        ]

        print_info("Staging lesson artifacts...")
        self.git.stage_files(patterns)

        # 4. Check if anything was staged
        staged = self.git.get_staged_files()
        if not staged:
            print_warning("No lesson files found to commit")
            return

        print_info(f"Staged {len(staged)} file(s)")

        # 5. Create commit message
        commit_msg = self._generate_finish_commit_message(lesson)

        # 6. Commit
        try:
            self.git.commit(commit_msg)
        except subprocess.CalledProcessError:
            print_error("Commit blocked by quality checks")
            sys.exit(2)

        # 7. Create tag
        tag_name = f"{TAG_PREFIX}{lesson}"
        tag_msg = f"Lesson {lesson} complete (6-tier synthesis)"
        self.git.tag(tag_name, tag_msg)

        # 8. Push with tags
        if remote:
            branch = self.git.get_current_branch()
            try:
                self.git.push(remote, branch, tags=True)
            except subprocess.CalledProcessError:
                print_warning("Push failed. You may need to pull first.")
                sys.exit(1)

        print_success("Finish auto-push complete (with tag)!")

    def _generate_checkpoint_commit_message(self, lesson: str, layer: str) -> str:
        """Generate semantic commit message for checkpoint"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Try to read checkpoint metadata for better message
        meta_file = REPO_ROOT / f"revision-notes" / "**" / f"{lesson}-*" / ".checkpoint-meta.json"
        # Simplified message (metadata parsing can be added later)

        return f"docs(checkpoint): lesson {lesson} layer {layer}\n\n" \
               f"Checkpoint saved at {timestamp}\n" \
               f"Layer: {layer}\n" \
               f"Lesson: {lesson}\n\n" \
               f"Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

    def _generate_finish_commit_message(self, lesson: str) -> str:
        """Generate semantic commit message for finish"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        return f"docs(lesson): complete lesson {lesson}\n\n" \
               f"6-tier synthesis completed at {timestamp}\n" \
               f"- Master lesson documentation\n" \
               f"- Cumulative context bridge\n" \
               f"- Interactive HTML presentations\n" \
               f"- Quick reference cheatsheet\n" \
               f"- Flashcards\n" \
               f"- Discovery updates\n\n" \
               f"Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# --- CLI Interface ---

def main():
    parser = argparse.ArgumentParser(
        description="Smart auto-commit and auto-push for checkpoint system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/git-auto-push.py checkpoint 3.1 L1
  python3 scripts/git-auto-push.py finish 3.1
  python3 scripts/git-auto-push.py --dry-run checkpoint 3.15 L2
  python3 scripts/git-auto-push.py --skip-quality finish 3.17
        """
    )

    parser.add_argument("action", choices=["checkpoint", "finish"],
                        help="Action type (checkpoint or finish)")
    parser.add_argument("lesson", help="Lesson number (e.g., 3.1)")
    parser.add_argument("layer", nargs="?", default=None,
                        help="Checkpoint layer (e.g., L1, L2) - required for checkpoint action")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    parser.add_argument("--skip-quality", action="store_true",
                        help="Skip quality validation (use with caution)")
    parser.add_argument("--worktree-aware", action="store_true",
                        help="Enable explicit worktree detection (auto-detected by default)")

    args = parser.parse_args()

    # Validate arguments
    if args.action == "checkpoint" and not args.layer:
        parser.error("checkpoint action requires a layer argument (e.g., L1, L2)")

    # Create auto-push manager
    auto_push = CheckpointAutoPush(dry_run=args.dry_run, skip_quality=args.skip_quality)

    # Execute workflow
    try:
        if args.action == "checkpoint":
            auto_push.checkpoint_workflow(args.lesson, args.layer)
        elif args.action == "finish":
            auto_push.finish_workflow(args.lesson)
    except KeyboardInterrupt:
        print("\n")
        print_warning("Operation cancelled by user")
        sys.exit(4)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
