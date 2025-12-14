# Forgesteel to Foundry VTT Converter

# Forgesteel to Foundry VTT Converter

Convert Draw Steel characters from Forgesteel (.ds-hero files) into Foundry Virtual Tabletop format for the Draw Steel system module.

## QUICK START - HOW TO CONVERT

**IMPORTANT: Use ONLY this command:**
```bash
python forgesteel_converter.py your_character.ds-hero converted_character.json
```

**Example:**
```bash
python forgesteel_converter.py Swami.ds-hero Swami_converted.json
```

**DO NOT USE:**
- `python converter/mapper.py` - This is an internal module!
- Any other converter/*.py files directly - These are internal modules!

**The only script you should run is `forgesteel_converter.py` in the root directory!**

## Features

- **Complete Character Conversion**: Converts all character attributes, abilities, features, and items
- **Smart Compendium Lookup**: Type-based matching to find correct items in Draw Steel compendium
- **Character Encoding Normalization**: Handles smart quotes, international characters (VÀLM), and encoding issues
- **Multi-Source Level Detection**: Priority-based level extraction from character, class, and features data
- **Complete Ability Conversion**: All class abilities converted with proper level filtering
- **Enhanced Description Transfer**: Full-text preservation with markdown/HTML enhancement for Foundry
- **Quality Validation**: Comprehensive validation and reporting for conversion integrity
- **Advancement Support**: Properly maps skills and languages to Foundry advancement selections
- **Movement Calculation**: Extracts Speed from ancestry features with kit bonuses
- **Resource Tracking**: Converts recoveries, stability, and heroic resources
- **Robust Error Handling**: Comprehensive logging and validation with helpful error messages
- **Flexible Modes**: Normal, verbose (debug), and strict conversion modes

## Requirements

- Python 3.6+
- Forgesteel character files (.ds-hero)
- Draw Steel compendium data (see Installation below)

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/forgesteel-foundry-converter.git
   cd forgesteel-foundry-converter
   ```

2. Install Python 3.6+ (if not already installed)

3. That's it! The converter uses a **hybrid approach** to get the Draw Steel compendium:
   - **Tries local first** (if you have `draw_steel_repo/src/packs` or specify `--compendium`)
   - **Uses cache** (faster on subsequent runs)
   - **Falls back to GitHub** (automatic, no setup required)

   **Optional:** For faster/offline use, clone Draw Steel locally:
   ```bash
   git clone https://github.com/MetaMorphic-Digital/draw-steel.git
   python forgesteel_converter.py character.ds-hero character.json --compendium ./draw-steel/src/packs
   ```

## Quick Start

```bash
# Basic usage - just works! (uses GitHub if needed)
python forgesteel_converter.py character.ds-hero character.json

# With local compendium path (faster, no network needed)
python forgesteel_converter.py character.ds-hero character.json --compendium /path/to/draw-steel/src/packs

# With verbose logging for debugging
python forgesteel_converter.py character.ds-hero character.json --verbose

# With strict mode (fail if any items can't be found in compendium)
python forgesteel_converter.py character.ds-hero character.json --strict
```

## Usage

### Basic Conversion

```bash
python forgesteel_converter.py "My Character.ds-hero" "My Character.json"
```

This will:
1. Load your Forgesteel character file
2. Load the Draw Steel compendium (from local → cache → GitHub, in order)
3. Convert all character data to Foundry format
4. Save to the specified JSON file

**First run may be slower** as it fetches compendium from GitHub and caches it locally. Subsequent runs will be faster.

### Debugging Issues

Use `--verbose` to see detailed conversion information:

```bash
python forgesteel_converter.py "My Character.ds-hero" "My Character.json" --verbose
```

This shows:
- Character loading progress
- Compendium statistics
- Item lookup results
- Conversion process details
- Any warnings or issues encountered

### Strict Mode

Use `--strict` to fail if any compendium items can't be found:

```bash
python forgesteel_converter.py "My Character.ds-hero" "My Character.json" --strict
```

Useful for catching data issues early in your workflow.

## Importing into Foundry VTT

After conversion, import the JSON file into Foundry VTT:

1. Open your Foundry world
2. Go to the **Actors** sidebar tab
3. Right-click and select **Import Data**
4. Choose your converted JSON file
5. The character will be imported with all items, skills, and advancements

## What Gets Converted

### Character Data
- ✓ Attributes (Might, Agility, Reason, Intuition, Presence)
- ✓ Stamina and Health
- ✓ Recovery & Stability values
- ✓ Movement speed (with ancestry and kit bonuses)
- ✓ Biography and notes

### Items & Features
- ✓ Ancestry (with traits)
- ✓ Culture/Background
- ✓ Career
- ✓ Class (with kit bonuses)
- ✓ Subclass (selected only)
- ✓ Abilities (including defaults)
- ✓ Features and perks
- ✓ Projects
- ✓ Complications
- ✓ Treasure/Equipment

### Knowledge & Skills
- ✓ Skill selections with advancement tracking
- ✓ Language selections
- ✓ Perk selections
- ✓ Domain selections

## Recent Improvements

### Character Encoding Fixes (v1.1)
- **Smart Quote Normalization**: Automatically converts smart quotes (" ") to regular quotes
- **International Character Support**: Handles problematic Unicode characters (e.g., VÀLM with Cyrillic А + combining accents)
- **JSON Compatibility**: Ensures all text survives JSON serialization cycles
- **Comprehensive Character Mapping**: Supports common encoding issues (em dashes, ellipsis, replacement characters)

### Level Detection Improvements (v1.1)
- **Multi-Source Detection**: Priority order: character.level → class.level → featuresByLevel calculation
- **Level Consistency Validation**: Detects and reports conflicting level sources
- **Proper Level Filtering**: High-level abilities correctly filtered for low-level characters
- **Edge Case Handling**: Robust error handling for missing or invalid level data

### Ability Conversion Fixes (v1.1)
- **Complete Ability Processing**: All 20-24 class abilities now properly converted
- **Level-Appropriate Filtering**: Only abilities ≤ character level are included
- **Ability Data Mapping**: Proper field conversion to Foundry VTT format
- **Conversion Validation**: Comprehensive reporting of ability conversion completeness

### Description Transfer Enhancements (v1.1)
- **Full-Text Preservation**: Source descriptions preserved verbatim when possible
- **Markdown Enhancement**: Automatic conversion of markdown to HTML for Foundry
- **Format Validation**: Safe HTML tag validation and dangerous content detection
- **Transfer Auditing**: Comprehensive reporting of description transfer success rates

### Quality Instrumentation (v1.1)
- **Comprehensive Validation**: 18+ validation checks across all conversion aspects
- **Quality Reporting**: Detailed metrics and actionable improvement suggestions
- **Error Tracking**: Categorized issues (errors/warnings/info) with specific guidance
- **Performance Monitoring**: Processing time tracking and optimization opportunities

## Troubleshooting

### "File not found" error
Ensure the path to your .ds-hero file is correct and the file exists.

### Compendium fetch fails
The converter tries three approaches: local → cache → GitHub. If all fail:
- **Check internet connection** - GitHub fetch needs network access
- **Use local path** - Clone draw-steel and specify it: `python forgesteel_converter.py input.ds-hero output.json --compendium ./draw-steel/src/packs`
- **Check cache** - Cache is stored in: `~/.cache/forgesteel-converter/compendium/`
- **GitHub API rate limit** - If converting many characters rapidly, you may hit GitHub's 60 req/hour limit. Use local compendium or wait an hour.

### Missing items in converted character
Use `--verbose` mode to see which items are being looked up and why some might be missing. This usually indicates:
- Items that don't exist in the compendium
- Items that are intentionally filtered (placeholders, containers)
- Version mismatches between Forgesteel and Draw Steel

### Character looks incomplete
- Check verbose output for warnings
- Compare with a native Foundry export to verify expected items
- Report issues on GitHub with verbose log output

## Project Structure

```
.
├── forgesteel_converter.py     # Main entry point
├── converter/
│   ├── loader.py              # File loading and compendium parsing
│   ├── mapper.py              # Core conversion logic with enhanced features
│   ├── writer.py              # JSON output
│   ├── text_normalizer.py     # Character encoding and text normalization
│   ├── level_detector.py      # Multi-source level detection and validation
│   ├── ability_converter.py   # Complete class ability conversion pipeline
│   ├── description_transfer.py # Enhanced description transfer and validation
│   └── quality_validator.py   # Comprehensive quality validation and reporting
├── tests/                      # Unit tests (83+ tests covering all modules)
├── README.md                   # This file
├── CONVERTER_IMPROVEMENTS.md   # Future enhancement plans
└── .gitignore                  # Git configuration
```

## Technical Details

### Compendium Lookup Strategy

The converter uses a three-tier lookup approach to find items in the Draw Steel compendium:

1. **Type + Name Match**: Looks for exact name match with correct item type (fastest, most reliable)
2. **Partial Name + Type Match**: Looks for name contains with correct type (handles name variants)
3. **Name Only Match**: Falls back to name-only lookup any type (handles edge cases)

This prevents confusion between items with identical names but different types (e.g., "Memonek" ancestry vs "Memonek Culture").

### Duplicate Resolution

When the same _dsid exists in multiple compendium packs:
- Non-heroic items are preferred over heroic variants (e.g., "Charge" vs "Charge!")
- This ensures characters get the base ability, with heroic alternatives available in Foundry

## Dependencies

**This converter is completely standalone** and only depends on Python standard library (no external packages needed).

**Draw Steel compendium data** is automatically obtained using a hybrid approach:
- **Local path** (if `--compendium` specified or `draw_steel_repo/src/packs` exists) - fastest
- **Cache** (`~/.cache/forgesteel-converter/compendium/`) - used on subsequent runs
- **GitHub** (automatic fallback) - fetches from https://github.com/MetaMorphic-Digital/draw-steel

**NOT required:** Forgesteel application or repository
- You only need `.ds-hero` character files exported from Forgesteel

## Known Limitations

- Only converts one selected subclass (Forgesteel limitation)
- Items not in the compendium are created as placeholders
- PDF exports are not supported (use .ds-hero format)
- GitHub API has a 60 requests/hour rate limit for unauthenticated users

## Contributing

Found a bug or have suggestions? Please report issues with:
- Your Forgesteel character (.ds-hero file)
- Verbose output from the converter
- Expected vs actual results

## License

This converter is designed to work with the Draw Steel system by MCDM for Foundry Virtual Tabletop. Ensure you have appropriate licenses for both Forgesteel and Foundry VTT.

## Support

For issues with:
- **The converter**: Check CONVERTER_IMPROVEMENTS.md for known issues and future plans
- **Forgesteel**: See [Forgesteel documentation](https://github.com/andyaiken/forgesteel)
- **Draw Steel in Foundry**: See [Draw Steel module](https://github.com/MetaMorphic-Digital/draw-steel)
- **Foundry VTT**: See [Foundry documentation](https://foundryvtt.com/document/)

## Changelog

### Version 1.1 (Latest)
- **Character Encoding Normalization**: Fixed smart quotes, international characters (VÀLM), and JSON compatibility
- **Multi-Source Level Detection**: Priority-based level extraction with validation and consistency checks
- **Complete Ability Conversion**: All class abilities (20-24) now converted with proper level filtering
- **Enhanced Description Transfer**: Full-text preservation with markdown-to-HTML conversion and validation
- **Quality Instrumentation**: Comprehensive validation with 18+ checks and detailed reporting
- **83+ Unit Tests**: Complete test coverage for all new modules and functionality
- **Robust Error Handling**: Improved error detection, logging, and user guidance

### Version 1.0
- Initial release
- Complete character conversion from Forgesteel to Foundry
- Type-based compendium lookup
- Comprehensive logging and error handling
- Support for --verbose and --strict modes
