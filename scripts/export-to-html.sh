#!/bin/bash
# Export lesson notes to standalone HTML using Pandoc
# Usage: ./export-to-html.sh <lesson> [style]
#
# Examples:
#   ./export-to-html.sh 3.1
#   ./export-to-html.sh 3.1 custom-style.css
#
# Requirements:
#   - Pandoc

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
  if ! command -v pandoc &> /dev/null; then
    log_error "Pandoc not installed"
    echo ""
    echo "Installation instructions:"
    echo "  macOS:   brew install pandoc"
    echo "  Linux:   sudo apt install pandoc"
    echo "  Windows: Download from https://pandoc.org"
    exit 1
  fi
}

# Parse arguments
parse_args() {
  if [ $# -lt 1 ]; then
    echo "Usage: $(basename "$0") <lesson> [style]"
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") 3.1"
    echo "  $(basename "$0") 3.17 custom-style.css"
    exit 1
  fi

  LESSON="$1"
  STYLE="${2:-$TEMPLATES_DIR/note-style.css}"
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

  # Add title page metadata
  cat > "$merged_file" << EOF
---
title: "Lesson $LESSON - Complete Notes"
subtitle: "Agent Factory Part 1: General Agents Foundations"
date: "$(date '+%B %d, %Y')"
toc: true
toc-depth: 3
---

EOF

  # Merge all checkpoint files
  for file in "${files[@]}"; do
    log_info "  + $(basename "$file")"

    # Add separator between checkpoints
    if [ -s "$merged_file" ]; then
      echo -e "\n---\n" >> "$merged_file"
    fi

    # Strip YAML frontmatter but preserve content
    awk '/^---$/{if(f){f=0;next}else{f=1;next}}!f' "$file" >> "$merged_file"
  done

  log_success "Merged into temporary file"
  echo "$merged_file"
}

# Convert to HTML
convert_to_html() {
  local input_file="$1"
  local output_file="$2"

  log_info "Converting to HTML..."

  local pandoc_args=(
    "$input_file"
    --output "$output_file"
    --from markdown
    --to html5
    --standalone
    --self-contained
    --toc
    --toc-depth=3
    --highlight-style tango
  )

  # Add custom CSS if exists
  if [ -f "$STYLE" ]; then
    log_info "Using custom stylesheet: $(basename "$STYLE")"
    pandoc_args+=(--css="$STYLE")
  else
    # Use inline default styles
    local default_css='<style>
      body {
        max-width: 800px;
        margin: 2rem auto;
        padding: 0 2rem;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
      }
      h1, h2, h3, h4, h5, h6 {
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
        line-height: 1.25;
      }
      h1 { font-size: 2.5rem; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.5rem; }
      h2 { font-size: 2rem; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.3rem; }
      h3 { font-size: 1.5rem; }
      code {
        background: #f5f5f5;
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: "SF Mono", Monaco, Menlo, Consolas, monospace;
        font-size: 0.9em;
      }
      pre {
        background: #f8f8f8;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 1rem;
        overflow-x: auto;
      }
      pre code {
        background: transparent;
        padding: 0;
      }
      table {
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
      }
      th, td {
        border: 1px solid #e0e0e0;
        padding: 0.75rem;
        text-align: left;
      }
      th {
        background: #f5f5f5;
        font-weight: 600;
      }
      blockquote {
        border-left: 4px solid #4A90E2;
        padding-left: 1rem;
        margin-left: 0;
        color: #666;
        font-style: italic;
      }
      #TOC {
        background: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 1.5rem;
        margin: 2rem 0;
      }
      #TOC ul {
        list-style: none;
        padding-left: 0;
      }
      #TOC ul ul {
        padding-left: 1.5rem;
      }
      #TOC a {
        color: #4A90E2;
        text-decoration: none;
      }
      #TOC a:hover {
        text-decoration: underline;
      }
    </style>'
    pandoc_args+=(--variable="header-includes=${default_css}")
  fi

  # Run Pandoc
  if pandoc "${pandoc_args[@]}" 2>&1 | tee "$TMP_DIR/pandoc.log"; then
    log_success "HTML conversion complete"
  else
    log_error "HTML conversion failed"
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
        local base=$(basename "$output_file" .html)
        output_file="$dir/${base}-${timestamp}.html"
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
  echo "  Export Lesson to HTML"
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
  local output_file="$EXPORTS_DIR/lesson-${LESSON}-complete.html"
  output_file=$(handle_collision "$output_file")

  # Convert to HTML
  convert_to_html "$merged_file" "$output_file"

  echo ""
  log_success "HTML exported successfully"
  echo ""
  echo "  Location: $output_file"
  echo "  Size: $(du -h "$output_file" | cut -f1)"
  echo ""

  # Offer to open
  if command -v xdg-open &> /dev/null; then
    read -p "Open HTML now? [y/N]: " open_choice
    if [[ "$open_choice" =~ ^[Yy]$ ]]; then
      xdg-open "$output_file" &
    fi
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open HTML now? [y/N]: " open_choice
    if [[ "$open_choice" =~ ^[Yy]$ ]]; then
      open "$output_file"
    fi
  fi
}

main "$@"
