# Parts catalogue normalization and category mapping.
from typing import List, Dict, Any

# Standardize OEM part numbers, map descriptions to target categories, and normalize manufacturers.
def clean_and_normalize_parts_records(raw_parts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned = []
    category_mapping = {
        "brake pad": "Brake pads",
        "brake disc": "Brake discs",
        "rotor": "Brake discs",
        "cabin": "Cabin-air filters",
        "pollen": "Cabin-air filters",
        "wiper": "Wiper blades",
        "headlight": "Headlights",
        "headlamp": "Headlights",
        "tail light": "Tail lights",
        "taillamp": "Tail lights",
        "mirror": "Side mirrors",
        "bumper": "Bumpers",
        "fender": "Fenders/body panels",
        "panel": "Fenders/body panels",
        "shock": "Shock absorbers",
        "strut": "Shock absorbers",
        "absorber": "Shock absorbers"
    }
    
    for item in raw_parts:
        c = dict(item)
        c["OEM_part_number"] = str(c.get("OEM_part_number", "")).strip().upper()
        
        desc = str(c.get("part_description", "")).lower()
        assigned_cat = str(c.get("part_category", "")).strip()
        for key, std_cat in category_mapping.items():
            if key in desc:
                assigned_cat = std_cat
                break
        c["part_category"] = assigned_cat
        
        mfg = str(c.get("manufacturer", "")).strip().lower()
        if "byd" in mfg:
            c["manufacturer"] = "BYD Auto Co., Ltd."
        elif "toyota" in mfg:
            c["manufacturer"] = "Toyota Motor Corporation"
        elif "volkswagen" in mfg or "vw" in mfg:
            c["manufacturer"] = "Volkswagen AG"
            
        cleaned.append(c)
        
    return cleaned
