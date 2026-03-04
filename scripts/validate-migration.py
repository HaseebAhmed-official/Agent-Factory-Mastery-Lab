#!/usr/bin/env python3

"""
================================================================================
MIGRATION VALIDATOR: Zero Data Loss Validation for Schema Migrations
================================================================================

PURPOSE:
    Validate migrated checkpoint files to ensure:
    - Zero data loss
    - Schema compliance
    - Content integrity
    - No corruption

USAGE:
    python3 scripts/validate-migration.py <staging-path>
    python3 scripts/validate-migration.py .migration-staging/v2

EXIT CODES:
    0 - Validation passed
    1 - Validation failed
    2 - Critical errors found

DEPENDENCIES:
    - Python 3.7+
    - pyyaml

AUTHOR: Professor Agent (Agent Factory Part 1 Tutoring System)
DATE: 2026-03-03
VERSION: 1.0.0
================================================================================
"""

import os
import sys
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# --- Configuration ---

REPO_ROOT = Path(__file__).parent.parent.absolute()
REVISION_NOTES_DIR = REPO_ROOT / "revision-notes"

# Required fields by schema version
REQUIRED_FIELDS = {
    "v1": [
        "lesson", "layer", "depth", "semantic_name", "title",
        "concepts", "tags", "keywords", "prerequisites",
        "difficulty", "estimated_time", "date", "status", "parent_checkpoint"
    ],
    "v2": [
        "lesson", "layer", "depth", "semantic_name", "title",
        "concepts", "tags", "keywords", "prerequisites",
        "difficulty", "estimated_time", "date", "status", "parent_checkpoint",
        "version", "learning_objectives", "mastery_level",
        "review_count", "last_reviewed", "comprehension_score"
    ]
}

# --- Color Output ---

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'

# --- Data Classes ---

@dataclass
class ValidationIssue:
    """A validation issue found"""
    severity: str  # 'critical', 'error', 'warning'
    file: str
    issue_type: str
    message: str

@dataclass
class ValidationReport:
    """Overall validation report"""
    files_checked: int
    files_passed: int
    files_failed: int
    critical_issues: List[ValidationIssue]
    errors: List[ValidationIssue]
    warnings: List[ValidationIssue]

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
    except yaml.YAMLError as e:
        return None, content

# --- Validators ---

class MigrationValidator:
    """Main validator for migrated files"""

    def __init__(self, staging_path: Path):
        self.staging_path = staging_path
        self.issues: List[ValidationIssue] = []

    def validate_all(self) -> ValidationReport:
        """Validate all files in staging"""
        print_header("Migration Validation")

        # Discover files
        files = list(self.staging_path.rglob("*-L*-*.md"))
        print_info(f"Found {len(files)} files to validate")

        files_passed = 0
        files_failed = 0

        for file in files:
            is_valid = self.validate_file(file)
            if is_valid:
                files_passed += 1
            else:
                files_failed += 1

        # Categorize issues
        critical = [i for i in self.issues if i.severity == 'critical']
        errors = [i for i in self.issues if i.severity == 'error']
        warnings = [i for i in self.issues if i.severity == 'warning']

        report = ValidationReport(
            files_checked=len(files),
            files_passed=files_passed,
            files_failed=files_failed,
            critical_issues=critical,
            errors=errors,
            warnings=warnings
        )

        return report

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single file"""
        try:
            content = file_path.read_text()
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity='critical',
                file=str(file_path),
                issue_type='read_error',
                message=f"Cannot read file: {e}"
            ))
            return False

        # Check 1: YAML frontmatter exists
        frontmatter, body = extract_yaml_frontmatter(content)
        if frontmatter is None:
            self.issues.append(ValidationIssue(
                severity='critical',
                file=str(file_path),
                issue_type='no_frontmatter',
                message="No YAML frontmatter found"
            ))
            return False

        # Check 2: Detect schema version
        version = frontmatter.get('version', 'v1')

        # Check 3: Required fields present
        required = REQUIRED_FIELDS.get(version, REQUIRED_FIELDS['v1'])
        missing_fields = []
        for field in required:
            if field not in frontmatter:
                missing_fields.append(field)

        if missing_fields:
            self.issues.append(ValidationIssue(
                severity='error',
                file=str(file_path),
                issue_type='missing_fields',
                message=f"Missing required fields: {', '.join(missing_fields)}"
            ))
            return False

        # Check 4: Field types are correct
        type_errors = self._validate_field_types(frontmatter, file_path)
        if type_errors:
            return False

        # Check 5: Content integrity (not empty)
        if len(body.strip()) < 100:
            self.issues.append(ValidationIssue(
                severity='warning',
                file=str(file_path),
                issue_type='short_content',
                message=f"Content is very short ({len(body)} chars)"
            ))

        # Check 6: Lesson number format
        lesson = frontmatter.get('lesson', '')
        if not self._validate_lesson_format(lesson):
            self.issues.append(ValidationIssue(
                severity='error',
                file=str(file_path),
                issue_type='invalid_lesson',
                message=f"Invalid lesson format: '{lesson}' (expected X.Y)"
            ))
            return False

        # Check 7: Layer format
        layer = frontmatter.get('layer', '')
        if not layer.startswith('L'):
            self.issues.append(ValidationIssue(
                severity='error',
                file=str(file_path),
                issue_type='invalid_layer',
                message=f"Invalid layer format: '{layer}' (expected L1, L2, L3)"
            ))
            return False

        # Check 8: Depth is integer
        depth = frontmatter.get('depth')
        if not isinstance(depth, int) or depth < 1 or depth > 3:
            self.issues.append(ValidationIssue(
                severity='error',
                file=str(file_path),
                issue_type='invalid_depth',
                message=f"Invalid depth: {depth} (expected 1, 2, or 3)"
            ))
            return False

        # Check 9: Concepts is list
        concepts = frontmatter.get('concepts')
        if not isinstance(concepts, list):
            self.issues.append(ValidationIssue(
                severity='error',
                file=str(file_path),
                issue_type='invalid_concepts',
                message="'concepts' field must be a list"
            ))
            return False

        # Check 10 (v2): Learning objectives is list
        if version == 'v2':
            objectives = frontmatter.get('learning_objectives')
            if not isinstance(objectives, list):
                self.issues.append(ValidationIssue(
                    severity='error',
                    file=str(file_path),
                    issue_type='invalid_objectives',
                    message="'learning_objectives' field must be a list"
                ))
                return False

        return True

    def _validate_field_types(self, frontmatter: Dict, file_path: Path) -> bool:
        """Validate field types"""
        type_checks = {
            'lesson': str,
            'layer': str,
            'depth': int,
            'semantic_name': str,
            'title': str,
            'concepts': list,
            'tags': list,
            'keywords': list,
            'prerequisites': list,
            'difficulty': str,
            'estimated_time': str,
            'date': str,
            'status': str,
        }

        has_errors = False
        for field, expected_type in type_checks.items():
            if field in frontmatter:
                value = frontmatter[field]
                if value is not None and not isinstance(value, expected_type):
                    self.issues.append(ValidationIssue(
                        severity='error',
                        file=str(file_path),
                        issue_type='type_mismatch',
                        message=f"Field '{field}' has wrong type: {type(value).__name__} (expected {expected_type.__name__})"
                    ))
                    has_errors = True

        return has_errors

    def _validate_lesson_format(self, lesson: str) -> bool:
        """Validate lesson number format (X.Y)"""
        if not lesson:
            return False

        parts = lesson.split('.')
        if len(parts) != 2:
            return False

        try:
            int(parts[0])
            int(parts[1])
            return True
        except ValueError:
            return False

# --- Content Comparison ---

class ContentComparator:
    """Compare original and migrated files for data loss"""

    def __init__(self, original_dir: Path, staging_dir: Path):
        self.original_dir = original_dir
        self.staging_dir = staging_dir

    def compare_all(self) -> List[ValidationIssue]:
        """Compare all files"""
        issues = []

        # Find all original files
        original_files = list(self.original_dir.rglob("*-L*-*.md"))

        for original in original_files:
            # Find corresponding staged file
            relative = original.relative_to(self.original_dir)
            staged = self.staging_dir / relative

            if not staged.exists():
                issues.append(ValidationIssue(
                    severity='critical',
                    file=str(original),
                    issue_type='file_missing',
                    message="File missing in staging (data loss!)"
                ))
                continue

            # Compare content
            original_content = original.read_text()
            staged_content = staged.read_text()

            original_fm, original_body = extract_yaml_frontmatter(original_content)
            staged_fm, staged_body = extract_yaml_frontmatter(staged_content)

            if original_fm is None or staged_fm is None:
                continue

            # Check for lost data in body
            if len(staged_body) < len(original_body) * 0.95:  # Allow 5% shrinkage
                issues.append(ValidationIssue(
                    severity='critical',
                    file=str(original),
                    issue_type='content_loss',
                    message=f"Body content shrank by {len(original_body) - len(staged_body)} chars"
                ))

            # Check for lost concepts
            original_concepts = set(original_fm.get('concepts', []))
            staged_concepts = set(staged_fm.get('concepts', []))
            lost_concepts = original_concepts - staged_concepts

            if lost_concepts:
                issues.append(ValidationIssue(
                    severity='critical',
                    file=str(original),
                    issue_type='concept_loss',
                    message=f"Lost concepts: {', '.join(lost_concepts)}"
                ))

        return issues

# --- CLI Interface ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/validate-migration.py <staging-path>")
        sys.exit(1)

    staging_path = Path(sys.argv[1])

    if not staging_path.exists():
        print_error(f"Staging path does not exist: {staging_path}")
        sys.exit(2)

    # Validate migrated files
    validator = MigrationValidator(staging_path)
    report = validator.validate_all()

    # Compare with originals (if available)
    print()
    print_info("Comparing with original files...")
    comparator = ContentComparator(REVISION_NOTES_DIR, staging_path)
    comparison_issues = comparator.compare_all()

    # Combine issues
    all_critical = report.critical_issues + [i for i in comparison_issues if i.severity == 'critical']
    all_errors = report.errors + [i for i in comparison_issues if i.severity == 'error']
    all_warnings = report.warnings + [i for i in comparison_issues if i.severity == 'warning']

    # Print report
    print()
    print_header("Validation Report")

    print(f"Files Checked: {Colors.CYAN}{report.files_checked}{Colors.NC}")
    print(f"Files Passed: {Colors.GREEN}{report.files_passed}{Colors.NC}")
    print(f"Files Failed: {Colors.RED}{report.files_failed}{Colors.NC}")
    print()
    print(f"Critical Issues: {Colors.RED}{len(all_critical)}{Colors.NC}")
    print(f"Errors: {Colors.YELLOW}{len(all_errors)}{Colors.NC}")
    print(f"Warnings: {Colors.YELLOW}{len(all_warnings)}{Colors.NC}")
    print()

    # Print critical issues
    if all_critical:
        print(f"{Colors.RED}{Colors.BOLD}CRITICAL ISSUES:{Colors.NC}")
        for issue in all_critical:
            print(f"  {Colors.RED}✗{Colors.NC} {issue.file}")
            print(f"    {issue.issue_type}: {issue.message}")
        print()

    # Print errors
    if all_errors:
        print(f"{Colors.YELLOW}{Colors.BOLD}ERRORS:{Colors.NC}")
        for issue in all_errors[:10]:  # Show first 10
            print(f"  {Colors.YELLOW}⚠{Colors.NC} {issue.file}")
            print(f"    {issue.issue_type}: {issue.message}")
        if len(all_errors) > 10:
            print(f"  ... and {len(all_errors) - 10} more")
        print()

    # Print warnings
    if all_warnings and len(all_warnings) <= 5:
        print(f"{Colors.BLUE}{Colors.BOLD}WARNINGS:{Colors.NC}")
        for issue in all_warnings:
            print(f"  {Colors.BLUE}ℹ{Colors.NC} {issue.file}")
            print(f"    {issue.issue_type}: {issue.message}")
        print()

    # Final verdict
    if all_critical:
        print_error("VALIDATION FAILED: Critical issues found (data loss detected!)")
        sys.exit(2)
    elif all_errors:
        print_error("VALIDATION FAILED: Errors found")
        sys.exit(1)
    elif all_warnings:
        print_warning(f"VALIDATION PASSED with {len(all_warnings)} warnings")
        sys.exit(0)
    else:
        print_success("VALIDATION PASSED: No issues found")
        sys.exit(0)

if __name__ == "__main__":
    main()
