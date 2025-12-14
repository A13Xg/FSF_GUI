import json

def write_foundry_character(character_data, file_path):
    """Writes a Foundry VTT character to a .json file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, indent=2)