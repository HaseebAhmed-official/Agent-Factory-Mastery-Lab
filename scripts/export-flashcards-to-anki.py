#!/usr/bin/env python3
"""
Export flashcards from JSON format to Anki (.apkg) package

Usage:
    python3 export-flashcards-to-anki.py flashcards/lesson-3.1-deck.json
    python3 export-flashcards-to-anki.py flashcards/*.json  # Merge multiple decks

Requirements:
    pip install genanki

Output:
    Creates .apkg file in exports/flashcards/
"""

import json
import sys
import os
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any

try:
    import genanki
except ImportError:
    print("Error: genanki not installed")
    print("Install with: pip install genanki")
    sys.exit(1)


class FlashcardExporter:
    """Convert JSON flashcard decks to Anki packages"""

    def __init__(self):
        """Initialize exporter with default models"""
        # Generate stable IDs from hash
        self.basic_model_id = self._generate_id("agent-factory-basic-model")
        self.cloze_model_id = self._generate_id("agent-factory-cloze-model")

        # Define Basic card model
        self.basic_model = genanki.Model(
            self.basic_model_id,
            'Agent Factory - Basic',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'},
                {'name': 'Hints'},
                {'name': 'Tags'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '''
                        <div class="front">
                            <div class="card-header">Agent Factory</div>
                            <div class="question">{{Front}}</div>
                            {{#Hints}}
                            <div class="hint">💡 Hint: {{Hints}}</div>
                            {{/Hints}}
                        </div>
                    ''',
                    'afmt': '''
                        <div class="back">
                            <div class="question">{{Front}}</div>
                            <hr>
                            <div class="answer">{{Back}}</div>
                            <div class="tags">{{Tags}}</div>
                        </div>
                    ''',
                },
            ],
            css=self._get_card_styles()
        )

        # Define Cloze card model
        self.cloze_model = genanki.Model(
            self.cloze_model_id,
            'Agent Factory - Cloze',
            fields=[
                {'name': 'Text'},
                {'name': 'Hints'},
                {'name': 'Tags'},
            ],
            templates=[
                {
                    'name': 'Cloze',
                    'qfmt': '''
                        <div class="front">
                            <div class="card-header">Agent Factory</div>
                            <div class="question">{{cloze:Text}}</div>
                            {{#Hints}}
                            <div class="hint">💡 Hint: {{Hints}}</div>
                            {{/Hints}}
                        </div>
                    ''',
                    'afmt': '''
                        <div class="back">
                            <div class="answer">{{cloze:Text}}</div>
                            <div class="tags">{{Tags}}</div>
                        </div>
                    ''',
                },
            ],
            model_type=genanki.Model.CLOZE,
            css=self._get_card_styles()
        )

    @staticmethod
    def _generate_id(seed: str) -> int:
        """Generate stable numeric ID from string seed"""
        hash_value = hashlib.md5(seed.encode('utf-8')).hexdigest()
        # Use first 8 hex chars as integer
        return int(hash_value[:8], 16)

    @staticmethod
    def _get_card_styles() -> str:
        """Get CSS styles for cards"""
        return '''
        .card {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 20px;
            text-align: center;
            color: #333;
            background: #f9f9f9;
            padding: 20px;
        }

        .card-header {
            font-size: 14px;
            color: #4A90E2;
            font-weight: 600;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .front, .back {
            max-width: 600px;
            margin: 0 auto;
        }

        .question {
            font-size: 24px;
            font-weight: 500;
            margin: 20px 0;
            line-height: 1.5;
            color: #2c3e50;
        }

        .answer {
            font-size: 20px;
            line-height: 1.6;
            text-align: left;
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4A90E2;
            margin: 20px 0;
        }

        .hint {
            font-size: 16px;
            color: #f39c12;
            margin-top: 15px;
            padding: 10px;
            background: #fff3cd;
            border-radius: 5px;
            text-align: left;
        }

        .tags {
            font-size: 12px;
            color: #999;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #e0e0e0;
        }

        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, #4A90E2, transparent);
            margin: 20px 0;
        }

        code {
            font-family: "SF Mono", Monaco, Menlo, Consolas, monospace;
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
            color: #e74c3c;
        }

        pre {
            text-align: left;
            background: #282c34;
            color: #abb2bf;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }

        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }

        strong {
            color: #2c3e50;
            font-weight: 600;
        }

        .cloze {
            font-weight: bold;
            color: #4A90E2;
        }
        '''

    def load_deck(self, filepath: Path) -> Dict[str, Any]:
        """Load flashcard deck from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ Loaded: {filepath.name}")
            return data
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing {filepath.name}: {e}")
            return None
        except Exception as e:
            print(f"✗ Error loading {filepath.name}: {e}")
            return None

    def convert_card(self, card_data: Dict[str, Any]) -> genanki.Note:
        """Convert JSON card to Anki note"""
        card_type = card_data.get('card_type', 'basic')
        tags = card_data.get('tags', [])
        hints = ' | '.join(card_data.get('hints', []))

        # Format tags
        tag_str = ' '.join(f"#{tag}" for tag in tags) if tags else ''

        if card_type == 'cloze':
            # Convert {{c1::text}} to Anki cloze format
            text = card_data.get('text', '')
            note = genanki.Note(
                model=self.cloze_model,
                fields=[text, hints, tag_str],
                tags=tags
            )
        else:  # basic, reverse, type-in all use basic model
            front = card_data.get('front', '')
            back = card_data.get('back', '')
            note = genanki.Note(
                model=self.basic_model,
                fields=[front, back, hints, tag_str],
                tags=tags
            )

        return note

    def create_deck(self, deck_data: Dict[str, Any]) -> genanki.Deck:
        """Create Anki deck from JSON data"""
        metadata = deck_data.get('deck_metadata', {})
        deck_name = metadata.get('deck_name', 'Agent Factory Deck')

        # Generate stable deck ID
        deck_id = self._generate_id(deck_name)

        deck = genanki.Deck(deck_id, deck_name)

        # Add description
        description = f"""
        <h3>{deck_name}</h3>
        <ul>
            <li><strong>Lesson:</strong> {metadata.get('lesson', 'N/A')}</li>
            <li><strong>Chapter:</strong> {metadata.get('chapter', 'N/A')}</li>
            <li><strong>Generated:</strong> {metadata.get('generated_date', 'N/A')}</li>
            <li><strong>Total Cards:</strong> {len(deck_data.get('cards', []))}</li>
            <li><strong>Difficulty:</strong> {metadata.get('difficulty', 'N/A')}</li>
        </ul>
        """
        deck.description = description

        # Convert and add cards
        cards = deck_data.get('cards', [])
        for card_data in cards:
            try:
                note = self.convert_card(card_data)
                deck.add_note(note)
            except Exception as e:
                print(f"  ⚠ Warning: Skipped card {card_data.get('card_id', '?')}: {e}")

        return deck

    def export(self, input_files: List[Path], output_file: Path, merge: bool = False):
        """Export flashcards to Anki package"""
        if merge and len(input_files) > 1:
            # Merge multiple decks
            print(f"\n📦 Merging {len(input_files)} decks...\n")
            merged_deck = None
            total_cards = 0

            for filepath in input_files:
                deck_data = self.load_deck(filepath)
                if not deck_data:
                    continue

                deck = self.create_deck(deck_data)

                if merged_deck is None:
                    # First deck becomes base
                    merged_deck = deck
                else:
                    # Add notes from subsequent decks
                    for note in deck.notes:
                        merged_deck.add_note(note)

                total_cards += len(deck.notes)

            if merged_deck:
                print(f"\n✓ Total cards: {total_cards}")
                package = genanki.Package(merged_deck)
                package.write_to_file(str(output_file))
                print(f"✅ Exported to: {output_file}")
            else:
                print("✗ No valid decks found")

        else:
            # Export each deck separately
            for filepath in input_files:
                deck_data = self.load_deck(filepath)
                if not deck_data:
                    continue

                deck = self.create_deck(deck_data)

                # Generate output filename
                if len(input_files) == 1 and output_file:
                    out_file = output_file
                else:
                    out_file = output_file.parent / f"{filepath.stem}.apkg"

                package = genanki.Package(deck)
                package.write_to_file(str(out_file))

                print(f"  ✓ {len(deck.notes)} cards")
                print(f"  ✅ Exported to: {out_file}\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Export Agent Factory flashcards to Anki format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Export single deck
  %(prog)s flashcards/lesson-3.1-deck.json

  # Export multiple decks
  %(prog)s flashcards/lesson-3.1-deck.json flashcards/lesson-3.15-deck.json

  # Merge multiple decks into one
  %(prog)s --merge flashcards/*.json -o exports/flashcards/chapter-3-complete.apkg

  # Specify output location
  %(prog)s flashcards/lesson-3.1-deck.json -o exports/flashcards/lesson-3.1.apkg
        '''
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input JSON flashcard file(s)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output .apkg file (default: exports/flashcards/[deck-name].apkg)'
    )

    parser.add_argument(
        '--merge',
        action='store_true',
        help='Merge multiple input decks into single .apkg file'
    )

    args = parser.parse_args()

    # Validate inputs
    input_files = []
    for pattern in args.input_files:
        path = Path(pattern)
        if path.exists():
            input_files.append(path)
        else:
            print(f"✗ Warning: {pattern} not found")

    if not input_files:
        print("✗ Error: No valid input files")
        sys.exit(1)

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_dir = Path('exports/flashcards')
        output_dir.mkdir(parents=True, exist_ok=True)

        if args.merge:
            output_file = output_dir / 'merged-deck.apkg'
        else:
            output_file = output_dir / f'{input_files[0].stem}.apkg'

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Export
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Export Flashcards to Anki")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    exporter = FlashcardExporter()
    exporter.export(input_files, output_file, merge=args.merge)

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  Import Instructions")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print("1. Open Anki Desktop")
    print("2. File → Import")
    print(f"3. Select: {output_file}")
    print("4. Click 'Import'")
    print("\n✨ Happy studying!\n")


if __name__ == '__main__':
    main()
