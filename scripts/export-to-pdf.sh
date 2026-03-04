#!/bin/bash
# Export lesson notes to PDF using Pandoc
# Usage: ./export-to-pdf.sh <lesson> [template]
#
# Examples:
#   ./export-to-pdf.sh 3.1
#   ./export-to-pdf.sh 3.1 custom-template.tex
#
# Requirements:
#   - Pandoc (with xelatex support)
#   - LaTeX distribution (TeXLive or MiKTeX)

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REVISION_NOTES_DIR="$PROJECT_ROOT/revision-notes"
EXPORTS_DIR="$PROJECT_ROOT/exports"
TEMPLATES_DIR="$PROJECT_ROOT/templates"
TMP_DIR="/tmp/lesson-export-$$"

# Cleanup on exit
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

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
  echo -e "${RED}❌${NC} $1" >&2
}

# Check dependencies
check_dependencies() {
  local missing_deps=()

  if ! command -v pandoc &> /dev/null; then
    missing_deps+=("pandoc")
  fi

  if ! command -v xelatex &> /dev/null; then
    missing_deps+=("xelatex (TeXLive or MiKTeX)")
  fi

  if [ ${#missing_deps[@]} -ne 0 ]; then
    log_error "Missing required dependencies:"
    for dep in "${missing_deps[@]}"; do
      echo "  - $dep"
    done
    echo ""
    echo "Installation instructions:"
    echo "  macOS:   brew install pandoc && brew install --cask mactex-no-gui"
    echo "  Linux:   sudo apt install pandoc texlive-xetex texlive-fonts-recommended"
    echo "  Windows: Download from https://pandoc.org and https://miktex.org"
    exit 1
  fi
}

# Parse arguments
parse_args() {
  if [ $# -lt 1 ]; then
    echo "Usage: $(basename "$0") <lesson> [template]"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") 3.1"
    echo "  $(basename "$0") 3.17 custom-template.tex"
    exit 1
  fi

  LESSON="$1"
  TEMPLATE="${2:-$TEMPLATES_DIR/note-template.tex}"
}

# Find checkpoint files
find_checkpoint_files() {
  log_info "Searching for checkpoint files for lesson $LESSON..."

  # Find all matching checkpoint files
  local files=()
  while IFS= read -r -d '' file; do
    files+=("$file")
  done < <(find "$REVISION_NOTES_DIR" -name "${LESSON}-L*.md" -print0 2>/dev/null | sort -z)

  if [ ${#files[@]} -eq 0 ]; then
    log_error "No checkpoint files found for lesson $LESSON"
    log_info "Expected pattern: ${LESSON}-L*.md in revision-notes/"
    exit 1
  fi

  log_success "Found ${#files[@]} checkpoint file(s)"
  for file in "${files[@]}"; do
    echo "  - $(basename "$file")"
  done

  echo "${files[@]}"
}

# Merge checkpoint files
merge_files() {
  local files=("$@")
  local merged_file="$TMP_DIR/merged-${LESSON}.md"

  mkdir -p "$TMP_DIR"

  log_info "Merging checkpoint files..."

  # Add title page
  cat > "$merged_file" << EOF
---
title: "Lesson $LESSON - Complete Notes"
author: "Agent Factory Part 1: General Agents Foundations"
date: "$(date '+%B %d, %Y')"
geometry: margin=1in
fontsize: 11pt
toc: true
toc-depth: 3
numbersections: true
---

EOF

  # Merge all checkpoint files
  for file in "${files[@]}"; do
    # Extract frontmatter and content
    log_info "  + $(basename "$file")"

    # Add page break between checkpoints
    if [ -f "$merged_file" ] && [ -s "$merged_file" ]; then
      echo -e "\n\\newpage\n" >> "$merged_file"
    fi

    # Strip YAML frontmatter but preserve content
    awk '/^---$/{if(f){f=0;next}else{f=1;next}}!f' "$file" >> "$merged_file"
  done

  log_success "Merged into temporary file"
  echo "$merged_file"
}

# Convert to PDF
convert_to_pdf() {
  local input_file="$1"
  local output_file="$2"

  log_info "Converting to PDF..."

  local pandoc_args=(
    "$input_file"
    --output "$output_file"
    --from markdown
    --to pdf
    --pdf-engine=xelatex
    --toc
    --toc-depth=3
    --number-sections
    --highlight-style tango
    -V geometry:margin=1in
    -V fontsize=11pt
    -V documentclass=article
    -V papersize=letter
  )

  # Add custom template if exists
  if [ -f "$TEMPLATE" ]; then
    log_info "Using custom template: $(basename "$TEMPLATE")"
    pandoc_args+=(--template="$TEMPLATE")
  fi

  # Run Pandoc
  if pandoc "${pandoc_args[@]}" 2>&1 | tee "$TMP_DIR/pandoc.log"; then
    log_success "PDF conversion complete"
  else
    log_error "PDF conversion failed"
    log_info "See log: $TMP_DIR/pandoc.log"
    exit 1
  fi
}

# Handle file collision
handle_collision() {
  local output_file="$1"

  if [ -f "$output_file" ]; then
    log_warning "File already exists: $(basename "$output_file")"
    echo ""
    echo "Options:"
    echo "  1. Overwrite (replace existing)"
    echo "  2. Keep both (add timestamp)"
    echo "  3. Cancel export"
    echo ""
    read -p "Choose [1/2/3]: " choice

    case "$choice" in
      1)
        log_info "Overwriting existing file..."
        ;;
      2)
        local timestamp=$(date '+%Y%m%d-%H%M%S')
        local dir=$(dirname "$output_file")
        local base=$(basename "$output_file" .pdf)
        output_file="$dir/${base}-${timestamp}.pdf"
        log_info "New filename: $(basename "$output_file")"
        ;;
      3)
        log_info "Export cancelled"
        exit 0
        ;;
      *)
        log_error "Invalid choice"
        exit 1
        ;;
    esac
  fi

  echo "$output_file"
}

# Main execution
main() {
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Export Lesson to PDF"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  parse_args "$@"
  check_dependencies

  # Create exports directory
  mkdir -p "$EXPORTS_DIR"

  # Find and merge files
  local files=($(find_checkpoint_files))
  local merged_file=$(merge_files "${files[@]}")

  # Determine output file
  local output_file="$EXPORTS_DIR/lesson-${LESSON}-complete.pdf"
  output_file=$(handle_collision "$output_file")

  # Convert to PDF
  convert_to_pdf "$merged_file" "$output_file"

  echo ""
  log_success "PDF exported successfully"
  echo ""
  echo "  Location: $output_file"
  echo "  Size: $(du -h "$output_file" | cut -f1)"
  echo ""

  # Offer to open
  if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open PDF now? [y/N]: " open_choice
    if [[ "$open_choice" =~ ^[Yy]$ ]]; then
      open "$output_file"
    fi
  fi
}

main "$@"
