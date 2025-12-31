import json
import uuid
import time

def write_foundry_character(character_data, file_path):
    """Writes a Foundry VTT character to a .json file with proper document structure."""

    # Ensure the character has required top-level fields
    if "type" not in character_data:
        character_data["type"] = "hero"

    if "_id" not in character_data:
        character_data["_id"] = str(uuid.uuid4())

    # Set critical metadata for Foundry v13 compatibility
    if "_stats" not in character_data:
        character_data["_stats"] = {}

    character_data["_stats"].update({
        "compendiumSource": None,
        "duplicateSource": None,
        "exportSource": None,
        "coreVersion": "13.351",
        "systemId": "draw-steel",
        "systemVersion": "0.9.2",
        "createdTime": int(time.time() * 1000),
        "modifiedTime": None,
        "lastModifiedBy": None
    })

    # Ensure items array exists
    if "items" not in character_data:
        character_data["items"] = []

    # Ensure each item has required consistent metadata
    for item in character_data.get("items", []):
        if "_id" not in item:
            item["_id"] = str(uuid.uuid4())

        if "_stats" not in item:
            item["_stats"] = {}

        # Force consistent metadata to avoid version conflicts
        item["_stats"].update({
            "compendiumSource": None,
            "duplicateSource": None,
            "exportSource": None,
            "coreVersion": "13.351",
            "systemId": "draw-steel",
            "systemVersion": "0.9.2",
            "createdTime": int(time.time() * 1000),
            "modifiedTime": None,
            "lastModifiedBy": None
        })

    # Write with proper formatting
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(character_data, f, indent=2, ensure_ascii=False)