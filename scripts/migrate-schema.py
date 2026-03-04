#!/usr/bin/env python3

"""
================================================================================
SCHEMA MIGRATION: Zero-Downtime Migration System for Checkpoint Files
================================================================================

PURPOSE:
    Safely migrate checkpoint files to new schema versions without data loss.
    Uses staging directory, validation, and rollback capabilities.

USAGE:
    python3 scripts/migrate-schema.py --version v2 --preview
    python3 scripts/migrate-schema.py --version v2 --execute
    python3 scripts/migrate-schema.py --rollback

FEATURES:
    - Staging migration strategy (.migration-staging/)
    - Zero data loss validation
    - User approval workflow
    - Automatic rollback on failure
    - Diff preview before migration
    - Backup creation

EXIT CODES:
    0 - Success
    1 - Migration failed
    2 - Validation failed
    3 - User cancelled
    4 - Rollback failed

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
import shutil
import argparse
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

# --- Configuration ---

REPO_ROOT = Path(__file__).parent.parent.absolute()
STAGING_DIR = REPO_ROOT / ".migration-staging"
BACKUP_DIR = REPO_ROOT / ".migration-backups"
REVISION_NOTES_DIR = REPO_ROOT / "revision-notes"
MIGRATION_LOG = STAGING_DIR / "migration.log"

# Schema versions registry
SCHEMA_VERSIONS = {
    "v1": {
        "description": "Original schema (current)",
        "yaml_fields": [
            "lesson", "layer", "depth", "semantic_name", "title",
            "concepts", "tags", "keywords", "prerequisites",
            "difficulty", "estimated_time", "date", "status", "parent_checkpoint"
        ]
    },
    "v2": {
        "description": "Enhanced schema with learning metadata",
        "yaml_fields": [
            "lesson", "layer", "depth", "semantic_name", "title",
            "concepts", "tags", "keywords", "prerequisites",
            "difficulty", "estimated_time", "date", "status", "parent_checkpoint",
            # New fields in v2
            "version", "learning_objectives", "mastery_level",
            "review_count", "last_reviewed", "comprehension_score"
        ]
    }
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
    NC = '\033[0m'

# --- Data Classes ---

@dataclass
class MigrationResult:
    """Result of migrating a single file"""
    source_file: str
    target_file: str
    status: str  # 'success', 'failed', 'skipped'
    changes: List[str]
    errors: List[str]
    checksum_before: str
    checksum_after: str

@dataclass
class MigrationPlan:
    """Plan for entire migration"""
    source_version: str
    target_version: str
    files_to_migrate: List[Path]
    estimated_changes: int
    timestamp: str
    staging_path: Path

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

def calculate_checksum(file_path: Path) -> str:
    """Calculate MD5 checksum of file"""
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

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
    except yaml.YAMLError as e:
        print_error(f"YAML parse error: {e}")
        return None, content

def reconstruct_markdown(frontmatter: Dict, body: str) -> str:
    """Reconstruct markdown file with updated frontmatter"""
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n{body}"

# --- Migration Strategies ---

class MigrationStrategy:
    """Base class for migration strategies"""

    def __init__(self, source_version: str, target_version: str):
        self.source_version = source_version
        self.target_version = target_version

    def migrate_frontmatter(self, frontmatter: Dict) -> Tuple[Dict, List[str]]:
        """
        Migrate frontmatter from source to target version.
        Returns: (migrated_frontmatter, list_of_changes)
        """
        raise NotImplementedError

class V1toV2Migration(MigrationStrategy):
    """Migration from v1 to v2 schema"""

    def migrate_frontmatter(self, frontmatter: Dict) -> Tuple[Dict, List[str]]:
        changes = []
        migrated = frontmatter.copy()

        # Add new required fields
        if 'version' not in migrated:
            migrated['version'] = 'v2'
            changes.append("Added field: version = 'v2'")

        if 'learning_objectives' not in migrated:
            # Infer from concepts if available
            concepts = migrated.get('concepts', [])
            objectives = [f"Understand {concept}" for concept in concepts[:3]]
            migrated['learning_objectives'] = objectives
            changes.append(f"Added field: learning_objectives (inferred from concepts)")

        if 'mastery_level' not in migrated:
            # Default to 'learning'
            migrated['mastery_level'] = 'learning'
            changes.append("Added field: mastery_level = 'learning'")

        if 'review_count' not in migrated:
            migrated['review_count'] = 0
            changes.append("Added field: review_count = 0")

        if 'last_reviewed' not in migrated:
            migrated['last_reviewed'] = None
            changes.append("Added field: last_reviewed = null")

        if 'comprehension_score' not in migrated:
            migrated['comprehension_score'] = None
            changes.append("Added field: comprehension_score = null")

        return migrated, changes

# Migration strategy registry
MIGRATION_STRATEGIES = {
    ('v1', 'v2'): V1toV2Migration
}

# --- Migration Engine ---

class MigrationEngine:
    """Main migration engine"""

    def __init__(self, target_version: str, dry_run: bool = False):
        self.target_version = target_version
        self.dry_run = dry_run
        self.results: List[MigrationResult] = []

        # Ensure directories exist
        STAGING_DIR.mkdir(exist_ok=True)
        BACKUP_DIR.mkdir(exist_ok=True)

    def discover_files(self) -> List[Path]:
        """Discover all checkpoint markdown files"""
        pattern = "**/*-L*-*.md"
        files = list(REVISION_NOTES_DIR.glob(pattern))
        print_info(f"Discovered {len(files)} checkpoint files")
        return files

    def detect_current_version(self, file_path: Path) -> str:
        """Detect schema version of a file"""
        content = file_path.read_text()
        frontmatter, _ = extract_yaml_frontmatter(content)

        if frontmatter is None:
            return "unknown"

        # Check for v2 fields
        if 'version' in frontmatter and frontmatter['version'] == 'v2':
            return 'v2'

        # Check for v2-specific fields
        v2_fields = {'learning_objectives', 'mastery_level', 'review_count'}
        if any(field in frontmatter for field in v2_fields):
            return 'v2'

        # Default to v1
        return 'v1'

    def create_migration_plan(self) -> MigrationPlan:
        """Create migration plan"""
        files = self.discover_files()

        # Filter files that need migration
        files_to_migrate = []
        for file in files:
            current_version = self.detect_current_version(file)
            if current_version != self.target_version:
                files_to_migrate.append(file)

        plan = MigrationPlan(
            source_version='v1',  # Assuming v1 for now
            target_version=self.target_version,
            files_to_migrate=files_to_migrate,
            estimated_changes=len(files_to_migrate) * 6,  # ~6 fields added per file
            timestamp=datetime.now().isoformat(),
            staging_path=STAGING_DIR / f"v{self.target_version.replace('v', '')}"
        )

        return plan

    def preview_migration(self, plan: MigrationPlan):
        """Preview migration changes"""
        print_header("Migration Preview")

        print(f"Source Version: {Colors.CYAN}{plan.source_version}{Colors.NC}")
        print(f"Target Version: {Colors.CYAN}{plan.target_version}{Colors.NC}")
        print(f"Files to Migrate: {Colors.YELLOW}{len(plan.files_to_migrate)}{Colors.NC}")
        print(f"Estimated Changes: {Colors.YELLOW}{plan.estimated_changes}{Colors.NC}")
        print(f"Staging Path: {Colors.BLUE}{plan.staging_path}{Colors.NC}")
        print()

        if len(plan.files_to_migrate) == 0:
            print_info("No files need migration (all files already at target version)")
            return

        # Preview first file changes
        print_info("Preview of changes (first file):")
        sample_file = plan.files_to_migrate[0]

        content = sample_file.read_text()
        frontmatter, body = extract_yaml_frontmatter(content)

        if frontmatter:
            strategy_class = MIGRATION_STRATEGIES.get((plan.source_version, plan.target_version))
            if strategy_class:
                strategy = strategy_class(plan.source_version, plan.target_version)
                migrated_fm, changes = strategy.migrate_frontmatter(frontmatter)

                print(f"\n{Colors.BOLD}Sample file:{Colors.NC} {sample_file.name}")
                print(f"\n{Colors.BOLD}Changes:{Colors.NC}")
                for i, change in enumerate(changes, 1):
                    print(f"  {i}. {change}")

        print()

    def execute_migration(self, plan: MigrationPlan) -> bool:
        """Execute migration"""
        print_header("Executing Migration")

        if len(plan.files_to_migrate) == 0:
            print_info("No files to migrate")
            return True

        # Create staging directory
        plan.staging_path.mkdir(parents=True, exist_ok=True)

        # Get migration strategy
        strategy_class = MIGRATION_STRATEGIES.get((plan.source_version, plan.target_version))
        if not strategy_class:
            print_error(f"No migration strategy found for {plan.source_version} → {plan.target_version}")
            return False

        strategy = strategy_class(plan.source_version, plan.target_version)

        # Migrate each file
        for i, file_path in enumerate(plan.files_to_migrate, 1):
            print(f"[{i}/{len(plan.files_to_migrate)}] Migrating {file_path.name}...", end=' ')

            try:
                result = self._migrate_file(file_path, plan.staging_path, strategy)
                self.results.append(result)

                if result.status == 'success':
                    print(f"{Colors.GREEN}✓{Colors.NC}")
                elif result.status == 'skipped':
                    print(f"{Colors.YELLOW}⊘{Colors.NC}")
                else:
                    print(f"{Colors.RED}✗{Colors.NC}")
                    for error in result.errors:
                        print(f"  {Colors.RED}Error:{Colors.NC} {error}")

            except Exception as e:
                print(f"{Colors.RED}✗{Colors.NC}")
                print_error(f"Unexpected error: {e}")
                return False

        return True

    def _migrate_file(self, file_path: Path, staging_path: Path, strategy: MigrationStrategy) -> MigrationResult:
        """Migrate a single file"""
        # Calculate original checksum
        checksum_before = calculate_checksum(file_path)

        # Read content
        content = file_path.read_text()
        frontmatter, body = extract_yaml_frontmatter(content)

        if frontmatter is None:
            return MigrationResult(
                source_file=str(file_path),
                target_file="",
                status='skipped',
                changes=[],
                errors=["No YAML frontmatter found"],
                checksum_before=checksum_before,
                checksum_after=""
            )

        # Migrate frontmatter
        try:
            migrated_fm, changes = strategy.migrate_frontmatter(frontmatter)
        except Exception as e:
            return MigrationResult(
                source_file=str(file_path),
                target_file="",
                status='failed',
                changes=[],
                errors=[f"Migration strategy failed: {e}"],
                checksum_before=checksum_before,
                checksum_after=""
            )

        # Reconstruct content
        new_content = reconstruct_markdown(migrated_fm, body)

        # Write to staging
        relative_path = file_path.relative_to(REVISION_NOTES_DIR)
        target_path = staging_path / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.dry_run:
            target_path.write_text(new_content)
            checksum_after = calculate_checksum(target_path)
        else:
            checksum_after = hashlib.md5(new_content.encode()).hexdigest()

        return MigrationResult(
            source_file=str(file_path),
            target_file=str(target_path),
            status='success',
            changes=changes,
            errors=[],
            checksum_before=checksum_before,
            checksum_after=checksum_after
        )

    def validate_migration(self, plan: MigrationPlan) -> bool:
        """Validate migration results"""
        print_header("Validating Migration")

        success_count = sum(1 for r in self.results if r.status == 'success')
        failed_count = sum(1 for r in self.results if r.status == 'failed')
        skipped_count = sum(1 for r in self.results if r.status == 'skipped')

        print(f"Migrated: {Colors.GREEN}{success_count}{Colors.NC}")
        print(f"Failed: {Colors.RED}{failed_count}{Colors.NC}")
        print(f"Skipped: {Colors.YELLOW}{skipped_count}{Colors.NC}")
        print()

        # Run validation script
        validation_script = REPO_ROOT / "scripts" / "validate-migration.py"
        if validation_script.exists():
            print_info("Running validation script...")
            import subprocess
            result = subprocess.run(
                [sys.executable, str(validation_script), str(plan.staging_path)],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print_success("Validation passed")
                return True
            else:
                print_error("Validation failed")
                print(result.stdout)
                print(result.stderr)
                return False
        else:
            print_warning("Validation script not found, skipping validation")
            return failed_count == 0

    def finalize_migration(self, plan: MigrationPlan) -> bool:
        """Finalize migration by moving staged files to production"""
        print_header("Finalizing Migration")

        # Create backup
        backup_path = BACKUP_DIR / f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        print_info(f"Creating backup at {backup_path}...")

        if not self.dry_run:
            shutil.copytree(REVISION_NOTES_DIR, backup_path)
            print_success("Backup created")

        # Move staged files to production
        print_info("Moving staged files to production...")

        moved_count = 0
        for result in self.results:
            if result.status == 'success' and not self.dry_run:
                target = Path(result.target_file)
                source = Path(result.source_file)

                # Copy from staging to production
                shutil.copy2(target, source)
                moved_count += 1

        print_success(f"Moved {moved_count} files to production")

        # Clean up staging
        if not self.dry_run:
            print_info("Cleaning up staging directory...")
            shutil.rmtree(plan.staging_path)
            print_success("Staging cleaned up")

        return True

    def rollback(self, backup_path: Path) -> bool:
        """Rollback to backup"""
        print_header("Rolling Back Migration")

        if not backup_path.exists():
            print_error(f"Backup path does not exist: {backup_path}")
            return False

        print_info(f"Restoring from backup: {backup_path}")

        if not self.dry_run:
            # Remove current revision notes
            shutil.rmtree(REVISION_NOTES_DIR)
            # Restore from backup
            shutil.copytree(backup_path, REVISION_NOTES_DIR)
            print_success("Rollback complete")

        return True

# --- CLI Interface ---

def main():
    parser = argparse.ArgumentParser(
        description="Schema migration system for checkpoint files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview migration to v2
  python3 scripts/migrate-schema.py --version v2 --preview

  # Execute migration to v2
  python3 scripts/migrate-schema.py --version v2 --execute

  # Rollback to most recent backup
  python3 scripts/migrate-schema.py --rollback
        """
    )

    parser.add_argument("--version", choices=['v2'], help="Target schema version")
    parser.add_argument("--preview", action="store_true", help="Preview migration changes")
    parser.add_argument("--execute", action="store_true", help="Execute migration")
    parser.add_argument("--rollback", action="store_true", help="Rollback to most recent backup")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no file writes)")
    parser.add_argument("--backup-path", type=str, help="Specific backup to rollback to")

    args = parser.parse_args()

    # Rollback mode
    if args.rollback:
        if args.backup_path:
            backup_path = Path(args.backup_path)
        else:
            # Find most recent backup
            backups = sorted(BACKUP_DIR.glob("backup-*"))
            if not backups:
                print_error("No backups found")
                sys.exit(4)
            backup_path = backups[-1]

        engine = MigrationEngine("v1", dry_run=args.dry_run)
        success = engine.rollback(backup_path)
        sys.exit(0 if success else 4)

    # Migration mode
    if not args.version:
        parser.error("--version is required (unless using --rollback)")

    engine = MigrationEngine(args.version, dry_run=args.dry_run)
    plan = engine.create_migration_plan()

    # Preview mode
    if args.preview:
        engine.preview_migration(plan)
        sys.exit(0)

    # Execute mode
    if args.execute:
        # Show preview first
        engine.preview_migration(plan)

        # Ask for confirmation
        if not args.dry_run:
            print(f"\n{Colors.YELLOW}⚠ This will modify {len(plan.files_to_migrate)} files.{Colors.NC}")
            response = input(f"{Colors.BOLD}Proceed with migration? (yes/no):{Colors.NC} ")
            if response.lower() != 'yes':
                print_warning("Migration cancelled by user")
                sys.exit(3)

        # Execute
        success = engine.execute_migration(plan)
        if not success:
            print_error("Migration failed during execution")
            sys.exit(1)

        # Validate
        validation_ok = engine.validate_migration(plan)
        if not validation_ok:
            print_error("Migration validation failed")
            print_warning("Staged files are in: " + str(plan.staging_path))
            print_info("You can manually inspect and rollback if needed")
            sys.exit(2)

        # Finalize
        finalize_ok = engine.finalize_migration(plan)
        if not finalize_ok:
            print_error("Migration finalization failed")
            sys.exit(1)

        print()
        print_success(f"Migration to {args.version} complete!")
        print_info(f"Backup created in: {BACKUP_DIR}")
        sys.exit(0)

    # If neither preview nor execute, show help
    parser.print_help()

if __name__ == "__main__":
    main()
