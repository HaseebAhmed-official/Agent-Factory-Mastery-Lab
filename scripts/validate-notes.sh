#!/bin/bash
# Validate checkpoint notes against quality rubric
# Usage: ./validate-notes.sh [lesson|all]
#
# Examples:
#   ./validate-notes.sh 3.1       # Validate specific lesson
#   ./validate-notes.sh all       # Validate all lessons
#   ./validate-notes.sh           # Validate most recent
#
# Quality Dimensions:
#   1. Completeness (all concepts covered)
#   2. Clarity (definitions, examples, analogies present)
#   3. Professionalism (formatting, structure, language)
#   4. Actionability (exercises, next steps, practice items)

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REVISION_NOTES_DIR="$PROJECT_ROOT/revision-notes"

# Scoring thresholds
THRESHOLD_PASS=75
THRESHOLD_GOOD=85
THRESHOLD_EXCELLENT=95

# Global array for find results (avoids space-in-path issues with echo)
FOUND_FILES=()

# Issue separator (must not appear in issue text)
ISSUE_SEP=';;'

# Logging
log_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
  echo -e "${GREEN}✅${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
  echo -e "${RED}❌${NC} $1"
}

log_header() {
  echo -e "\n${CYAN}━━━ $1 ━━━${NC}\n"
}

# Find lesson files — populates global FOUND_FILES array
find_lesson_files() {
  local lesson="$1"

  FOUND_FILES=()
  while IFS= read -r -d '' file; do
    FOUND_FILES+=("$file")
  done < <(find "$REVISION_NOTES_DIR" -name "${lesson}-L*.md" -print0 2>/dev/null | sort -z)
}

# Join issues array with separator
join_issues() {
  local result=""
  local sep="$1"
  shift
  for item in "$@"; do
    if [ -n "$result" ]; then
      result="${result}${sep}${item}"
    else
      result="$item"
    fi
  done
  echo "$result"
}

# Check completeness
check_completeness() {
  local file="$1"
  local score=0
  local max=25
  local issues=()

  # Check for required sections (multiple patterns per category to match different naming conventions)
  local section_found

  # Terminology / Vocabulary
  section_found=false
  if grep -qi "Terminology\|Vocabulary\|Key Terms\|Glossary" "$file"; then section_found=true; fi
  if $section_found; then ((score += 5)); else issues+=("Missing section: Terminology/Vocabulary"); fi

  # Concepts / Core content
  section_found=false
  if grep -qi "## .*Concept\|### What It Is\|### Core Explanation\|## .*How It Works" "$file"; then section_found=true; fi
  if $section_found; then ((score += 5)); else issues+=("Missing section: Concepts"); fi

  # Examples / Visual aids
  section_found=false
  if grep -qi "Example\|Visual\|Diagram\|Analogy" "$file"; then section_found=true; fi
  if $section_found; then ((score += 5)); else issues+=("Missing section: Examples/Visuals"); fi

  # Exercises / Hands-on / Practice
  section_found=false
  if grep -qi "Exercise\|Hands-On\|Practice\|Try This\|Comprehension Check" "$file"; then section_found=true; fi
  if $section_found; then ((score += 5)); else issues+=("Missing section: Exercises/Practice"); fi

  # Check for vocabulary definitions
  if grep -q "^\*\*.*\*\*:" "$file"; then
    ((score += 5))
  else
    issues+=("No vocabulary definitions found (pattern: **Term**: definition)")
  fi

  # Calculate percentage
  local percent=$(( (score * 100) / max ))

  echo "$percent|$(join_issues "$ISSUE_SEP" "${issues[@]+"${issues[@]}"}")"
}

# Check clarity
check_clarity() {
  local file="$1"
  local score=0
  local max=25
  local issues=()

  # Check for analogies
  if grep -qi "analogy\|like\|similar to\|imagine" "$file"; then
    ((score += 5))
  else
    issues+=("No analogies found")
  fi

  # Check for examples
  local example_count
  example_count=$(grep -ci "example\|for instance\|e\.g\." "$file" || echo "0")
  if [ "$example_count" -ge 3 ]; then
    ((score += 5))
  elif [ "$example_count" -ge 1 ]; then
    ((score += 3))
    issues+=("Limited examples (found $example_count, recommended 3+)")
  else
    issues+=("No examples found")
  fi

  # Check for diagrams/tables
  if grep -q "^|.*|.*|$" "$file"; then
    ((score += 5))
  else
    issues+=("No tables found")
  fi

  if grep -q '^\`\`\`' "$file"; then
    ((score += 5))
  else
    issues+=("No code blocks/diagrams found")
  fi

  # Check for key takeaways
  if grep -qi "key takeaway\|summary\|remember\|connection map\|where it fits" "$file"; then
    ((score += 5))
  else
    issues+=("No key takeaways/summary")
  fi

  # Calculate percentage
  local percent=$(( (score * 100) / max ))

  echo "$percent|$(join_issues "$ISSUE_SEP" "${issues[@]+"${issues[@]}"}")"
}

# Check professionalism
check_professionalism() {
  local file="$1"
  local score=25  # Start at max, deduct for issues
  local max=25
  local issues=()

  # Check for typos (common words)
  local typo_patterns=("teh " "taht " "recieve" "occured" "seperate")
  for pattern in "${typo_patterns[@]}"; do
    if grep -q "$pattern" "$file"; then
      ((score -= 2))
      issues+=("Possible typo: $pattern")
    fi
  done

  # Check for broken links
  if grep -q "\[.*\]()" "$file"; then
    ((score -= 3))
    issues+=("Broken links found")
  fi

  # Check for incomplete sentences
  if grep -q "\.\.\.$" "$file"; then
    ((score -= 2))
    issues+=("Incomplete sentences (trailing ...)")
  fi

  # Check for YAML frontmatter
  if ! grep -q "^---$" "$file"; then
    ((score -= 5))
    issues+=("Missing YAML frontmatter")
  fi

  # Check formatting consistency
  local heading_count
  heading_count=$(grep -c "^#" "$file" || echo "0")
  if [ "$heading_count" -lt 3 ]; then
    ((score -= 3))
    issues+=("Limited structure (< 3 headings)")
  fi

  # Ensure score doesn't go below 0
  if [ "$score" -lt 0 ]; then
    score=0
  fi

  # Calculate percentage
  local percent=$(( (score * 100) / max ))

  echo "$percent|$(join_issues "$ISSUE_SEP" "${issues[@]+"${issues[@]}"}")"
}

# Check actionability
check_actionability() {
  local file="$1"
  local score=0
  local max=25
  local issues=()

  # Check for exercises
  if grep -qi "exercise\|practice\|try this\|hands-on" "$file"; then
    ((score += 8))
  else
    issues+=("No exercises found")
  fi

  # Check for what goes wrong sections
  if grep -qi "what goes wrong\|common mistakes\|anti-pattern\|common pitfalls\|failure mode" "$file"; then
    ((score += 7))
  else
    issues+=("No failure modes/anti-patterns")
  fi

  # Check for next steps
  if grep -qi "next steps\|further reading\|related concepts\|connection map\|cross-reference\|enables\|leads to" "$file"; then
    ((score += 5))
  else
    issues+=("No next steps/further reading")
  fi

  # Check for comprehension questions
  if grep -qi "question\|quiz\|check understanding\|comprehension\|asked:" "$file"; then
    ((score += 5))
  else
    issues+=("No comprehension questions")
  fi

  # Calculate percentage
  local percent=$(( (score * 100) / max ))

  echo "$percent|$(join_issues "$ISSUE_SEP" "${issues[@]+"${issues[@]}"}")"
}

# Display issues for a dimension
display_issues() {
  local dimension="$1"
  local issues_str="$2"

  if [ -n "$issues_str" ]; then
    echo "  $dimension:"
    while IFS= read -r issue; do
      if [ -n "$issue" ]; then
        echo "    - $issue"
      fi
    done <<< "${issues_str//$ISSUE_SEP/$'\n'}"
  fi
}

# Validate single file — display goes to stderr, score to stdout
validate_file() {
  local file="$1"
  local filename
  filename=$(basename "$file")

  log_header "$filename" >&2

  # Run all checks
  local completeness_result clarity_result professionalism_result actionability_result
  completeness_result=$(check_completeness "$file")
  clarity_result=$(check_clarity "$file")
  professionalism_result=$(check_professionalism "$file")
  actionability_result=$(check_actionability "$file")

  # Parse results
  local completeness_score completeness_issues
  completeness_score=$(echo "$completeness_result" | cut -d'|' -f1)
  completeness_issues=$(echo "$completeness_result" | cut -d'|' -f2)

  local clarity_score clarity_issues
  clarity_score=$(echo "$clarity_result" | cut -d'|' -f1)
  clarity_issues=$(echo "$clarity_result" | cut -d'|' -f2)

  local professionalism_score professionalism_issues
  professionalism_score=$(echo "$professionalism_result" | cut -d'|' -f1)
  professionalism_issues=$(echo "$professionalism_result" | cut -d'|' -f2)

  local actionability_score actionability_issues
  actionability_score=$(echo "$actionability_result" | cut -d'|' -f1)
  actionability_issues=$(echo "$actionability_result" | cut -d'|' -f2)

  # Calculate overall score (weighted average)
  local overall=$(( (completeness_score + clarity_score + professionalism_score + actionability_score) / 4 ))

  # Display results (all to stderr so stdout has only the score)
  {
    echo "┌─────────────────────────┬───────┐"
    echo "│ Dimension               │ Score │"
    echo "├─────────────────────────┼───────┤"
    printf "│ Completeness            │ %5d%% │\n" "$completeness_score"
    printf "│ Clarity                 │ %5d%% │\n" "$clarity_score"
    printf "│ Professionalism         │ %5d%% │\n" "$professionalism_score"
    printf "│ Actionability           │ %5d%% │\n" "$actionability_score"
    echo "├─────────────────────────┼───────┤"
    printf "│ ${MAGENTA}OVERALL${NC}                 │ ${MAGENTA}%5d%%${NC} │\n" "$overall"
    echo "└─────────────────────────┴───────┘"
    echo ""

    # Rating
    if [ "$overall" -ge "$THRESHOLD_EXCELLENT" ]; then
      log_success "Rating: EXCELLENT"
    elif [ "$overall" -ge "$THRESHOLD_GOOD" ]; then
      log_success "Rating: GOOD"
    elif [ "$overall" -ge "$THRESHOLD_PASS" ]; then
      log_warning "Rating: PASS (needs improvement)"
    else
      log_error "Rating: FAIL (below threshold)"
    fi
    echo ""

    # Show issues
    if [ -n "$completeness_issues" ] || [ -n "$clarity_issues" ] || \
       [ -n "$professionalism_issues" ] || [ -n "$actionability_issues" ]; then
      echo "Issues Found:"
      echo ""
      display_issues "Completeness" "$completeness_issues"
      display_issues "Clarity" "$clarity_issues"
      display_issues "Professionalism" "$professionalism_issues"
      display_issues "Actionability" "$actionability_issues"
      echo ""
    fi
  } >&2

  # Return only the score on stdout
  echo "$overall"
}

# Validate lesson
validate_lesson() {
  local lesson="$1"

  log_info "Searching for checkpoint files for lesson $lesson..."

  find_lesson_files "$lesson"

  if [ ${#FOUND_FILES[@]} -eq 0 ]; then
    log_error "No checkpoint files found for lesson $lesson"
    return 1
  fi

  log_success "Found ${#FOUND_FILES[@]} checkpoint file(s)"
  echo ""

  local total_score=0
  local file_count=0

  for file in "${FOUND_FILES[@]}"; do
    local score
    score=$(validate_file "$file")
    total_score=$((total_score + score))
    file_count=$((file_count + 1))
  done

  # Lesson average
  if [ "$file_count" -gt 1 ]; then
    local lesson_avg=$((total_score / file_count))
    log_header "Lesson $lesson Average"
    printf "${MAGENTA}Overall Score: %d%%${NC}\n" "$lesson_avg"
    echo ""

    if [ "$lesson_avg" -ge "$THRESHOLD_EXCELLENT" ]; then
      log_success "Lesson quality: EXCELLENT"
    elif [ "$lesson_avg" -ge "$THRESHOLD_GOOD" ]; then
      log_success "Lesson quality: GOOD"
    elif [ "$lesson_avg" -ge "$THRESHOLD_PASS" ]; then
      log_warning "Lesson quality: PASS (consider revision)"
    else
      log_error "Lesson quality: FAIL (revision recommended)"
    fi
  else
    # Single file — show the score as lesson score too
    local lesson_score=$total_score
    log_header "Lesson $lesson Score"
    printf "${MAGENTA}Overall Score: %d/100${NC}\n" "$lesson_score"
    echo ""

    if [ "$lesson_score" -ge "$THRESHOLD_EXCELLENT" ]; then
      log_success "Lesson quality: EXCELLENT"
    elif [ "$lesson_score" -ge "$THRESHOLD_GOOD" ]; then
      log_success "Lesson quality: GOOD"
    elif [ "$lesson_score" -ge "$THRESHOLD_PASS" ]; then
      log_warning "Lesson quality: PASS (consider revision)"
    else
      log_error "Lesson quality: FAIL (revision recommended)"
    fi
  fi
}

# Main execution
main() {
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Checkpoint Notes Quality Validator"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Quality Rubric:"
  echo "  • Completeness (25%): All required sections present"
  echo "  • Clarity (25%): Analogies, examples, visualizations"
  echo "  • Professionalism (25%): Formatting, structure, language"
  echo "  • Actionability (25%): Exercises, next steps, practice"
  echo ""
  echo "Thresholds:"
  echo "  • Excellent: $THRESHOLD_EXCELLENT%+"
  echo "  • Good: $THRESHOLD_GOOD-$((THRESHOLD_EXCELLENT-1))%"
  echo "  • Pass: $THRESHOLD_PASS-$((THRESHOLD_GOOD-1))%"
  echo "  • Fail: < $THRESHOLD_PASS%"
  echo ""

  local target="${1:-}"

  if [ -z "$target" ]; then
    # Find most recent lesson
    log_info "No lesson specified, validating most recent..."
    local recent_file
    recent_file=$(find "$REVISION_NOTES_DIR" -name "*-L*.md" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)

    if [ -z "$recent_file" ]; then
      log_error "No checkpoint files found"
      exit 1
    fi

    validate_file "$recent_file"

  elif [ "$target" == "all" ]; then
    # Validate all lessons
    log_info "Validating all lessons..."

    local all_files=()
    while IFS= read -r -d '' file; do
      all_files+=("$file")
    done < <(find "$REVISION_NOTES_DIR" -name "*-L*.md" -type f -print0 | sort -z)

    if [ ${#all_files[@]} -eq 0 ]; then
      log_error "No checkpoint files found"
      exit 1
    fi

    local total=0
    local count=0

    for file in "${all_files[@]}"; do
      local score
      score=$(validate_file "$file")
      total=$((total + score))
      count=$((count + 1))
    done

    # Overall average
    local overall_avg=$((total / count))
    log_header "Overall Statistics"
    printf "Files validated: %d\n" "$count"
    printf "Average score: ${MAGENTA}%d%%${NC}\n" "$overall_avg"
    echo ""

  else
    # Validate specific lesson
    validate_lesson "$target"
  fi
}

main "$@"
