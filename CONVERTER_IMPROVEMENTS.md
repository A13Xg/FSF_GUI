# Forgesteel to Foundry Converter - Code Review & Improvements

## Repository Structure Analysis

### Draw Steel Repo (`draw_steel_repo`)
**Pack Organization:**
```
src/packs/
├── abilities/          # All ability definitions
├── character-options/  # Complications, Kits, Perks
├── classes/           # Class definitions
├── origins/           # Ancestries, Backgrounds (Cultures)
├── rewards/           # Downtime Projects, Titles, Treasures
├── monsters/          # Monster definitions
├── monster-features/  # Monster-specific features
├── journals/          # Rules/lore content
└── tables/           # Random tables
```

**Data Model Structure:**
- All items have `_dsid` (Draw Steel ID) - unique identifier for game rules elements
- `description` field with `value` (HTML) and `director` (GM-only HTML)
- `source` field with book, page, license, revision
- Item types are strictly typed (ability, feature, perk, project, etc.)

### Forgesteel Repo (`forgesteel_repo`)
**Enums & Data Models:**
- Comprehensive TypeScript enums for all item types
- Well-structured data files for each class, ancestry, culture, career
- Feature type enumerations and feature field definitions
- Skill and perk list enums with complete listings

## Current Converter Status ✓

### Fully Implemented Features
1. ✓ Type-based compendium lookup (prefers type+name match)
2. ✓ Culture name resolution ("Memonek" → "Memonek Culture")
3. ✓ Ability disambiguation (Charge vs Charge! via category field)
4. ✓ Perk and Project extraction from selected items
5. ✓ Skill and language advancement tracking
6. ✓ Movement calculation from ancestry Speed features
7. ✓ Recoveries from class definitions
8. ✓ Stability from ancestry traits
9. ✓ Comprehensive logging system with --verbose flag
10. ✓ Input/output validation with helpful error messages
11. ✓ Proper exit codes and exception handling
12. ✓ Compendium loading statistics and duplicate resolution logging

## Recommended Improvements

### 1. **Use Pack Structure for Better Organization**
**Issue:** Currently scans all compendium items indiscriminately
**Solution:** Create pack-aware lookups to reduce search space
```python
PACK_STRUCTURE = {
    "ability": "abilities",
    "ancestry": "origins/Ancestries",
    "career": "origins/Backgrounds", 
    "culture": "origins/Backgrounds",
    "class": "classes",
    "perk": "character-options/Perks",
    "project": "rewards/Downtime_Projects",
    "treasure": "rewards/Treasures",
    "subclass": "classes",
    "complication": "character-options/Complications",
    "kit": "character-options/Kits",
    "feature": "monster-features"
}
```
**Benefits:**
- Faster lookups (smaller search space per type)
- More reliable type disambiguation
- Better error reporting (item not found in expected pack)

### 2. **Cache Compendium Data by Pack Structure**
**Current:** Linear scan of all items
**Improved:**
```python
compendium = {
    "ability": {name: item, ...},
    "ancestry": {name: item, ...},
    "perk": {name: item, ...},
    # etc.
}
```
**Benefits:**
- O(1) lookups instead of O(n)
- Natural fallback chain (exact match → prefix match → fuzzy)
- Clear organization per item type

### 3. **Add Logging/Verbosity Control**
**Issue:** Silent failures when items not found
**Solution:** Add `--verbose` flag to converter
```python
parser.add_argument('--verbose', '-v', action='store_true',
                    help='Enable verbose logging')
```
Output missing items, lookup failures, type mismatches for debugging.

### 4. **Validate Item Counts Against Expected Baselines**
**Current:** No validation
**Improved:** Add item count validation
```python
EXPECTED_ABILITY_COUNT = {
    "hero": 19,  # 11 base + others
    "npc": "variable"
}
```
Warn if item counts are significantly different from expected.

### 5. **Better Error Handling for Edge Cases**
**Current:**
- Unicode character issues with career names
- Empty/malformed features silently skipped
- No validation of required fields

**Improved:**
- Validate all required fields exist before conversion
- Report which features were skipped and why
- Handle character encoding issues gracefully
- Validate Forgesteel structure before conversion

### 6. **Add Configuration File Support**
**Current:** Hardcoded compendium path
**Improved:**
```python
# .converter.json
{
  "compendium_path": "draw_steel_repo/src/packs",
  "defaults": {
    "base_stamina": 20,
    "default_abilities": [...],
    "kit_bonus_speed": 1
  }
}
```
**Benefits:**
- Easier deployment and configuration
- Project-specific defaults
- Version tracking

### 7. **Implement Unit Tests**
**Current:** Manual test files in repository root
**Improved:** Proper test structure
```python
tests/
├── test_compendium_loader.py
├── test_mapper.py
├── fixtures/
│   ├── sample_forgesteel.json
│   ├── expected_output.json
│   └── native_foundry.json
└── conftest.py
```

### 8. **Add Known Issues Registry**
**Current:** Known mappings hardcoded in code
**Better:** Centralized registry
```python
# KNOWN_ISSUES.md
## Name Mappings
- "Clarity" → "clarity-and-strain" (Heroic Resource vs Feature name mismatch)

## Duplicate IDs
- "charge" (page 274 basic vs page 343 heroic)
  - Resolution: Prefer non-heroic category

## Missing Items
- Items genuinely not in compendium (log with --verbose)
```

### 9. **Support Multiple Forgesteel Versions**
**Issue:** Assumes Forgesteel data structure won't change
**Solution:** Add version detection
```python
MIN_FORGESTEEL_VERSION = "1.0.0"
if character.get("version") < MIN_FORGESTEEL_VERSION:
    error("Forgesteel version too old")
```

### 10. **Performance Optimization for Large Compendiums**
**Current:** Full scan on every load
**Improved:** 
- Lazy load only needed packs
- Cache compendium data to disk
- Parallel pack loading for large repos

---

## Implementation Priority

### High Priority (Immediate)
1. Pack-aware compendium lookup (#1)
2. Better error handling (#5)
3. Add logging/verbose mode (#3)

### Medium Priority (Soon)
1. Item count validation (#4)
2. Known issues registry (#8)
3. Configuration file support (#6)

### Lower Priority (Nice to Have)
1. Performance optimization (#10)
2. Unit test structure (#7)
3. Version detection (#9)

---

## Testing Recommendations

### Test Cases to Add
1. **Multiple characters with different classes/ancestries**
   - Verify item counts per type
   - Check all advancements preserved

2. **Edge cases**
   - Characters with no kits/projects
   - Unicode names in Forgesteel
   - Missing compendium items (graceful degradation)

3. **Regression tests**
   - Maintain reference conversions (native Foundry vs converted)
   - Automated diff reporting

---

## Code Quality Improvements

### Documentation
- Add docstrings to all functions with type hints
- Document the three-tier lookup strategy
- Create architecture diagram of conversion pipeline

### Maintainability
- Extract magic strings to constants
- Create enum for item types (remove string literals)
- Separate concerns: loading, validation, mapping, writing

### Error Messages
- Include item name/ID in all error messages
- Suggest fixes ("Did you mean...?")
- Provide context ("Failed in class features: ...")

---

## Future Enhancements

### Potential Features
1. **Incremental updates** - Convert only changed characters
2. **Batch conversion** - Convert multiple characters at once
3. **Dry-run mode** - Preview conversion without writing files
4. **Export validation** - Verify output can be imported
5. **Statistics report** - Summary of what was converted

### Integration Points
1. Direct Foundry import API (skip JSON export)
2. Web UI for conversion settings
3. Discord bot integration for batch jobs
4. GitHub Actions for automated conversions
