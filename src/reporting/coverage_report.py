# Vehicle Selection and 30-Combination Coverage Matrix Reporting Module.
from typing import List, Dict, Any
from pathlib import Path
from src.utils.file_utils import load_json

ASSIGNED_PARTS = [
    "Brake pads",
    "Brake discs",
    "Cabin-air filters",
    "Wiper blades",
    "Headlights",
    "Tail lights",
    "Side mirrors",
    "Bumpers",
    "Fenders/body panels",
    "Shock absorbers"
]

# Evaluate all 5 candidate vehicles across market evidence dimensions and justify 3 selected vehicles.
def build_vehicle_selection_evidence(vehicle_listings: List[Dict[str, Any]] = None, project_root: Path = None) -> List[Dict[str, Any]]:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent
    evidence_file = project_root / "data" / "raw" / "vehicle_selection_evidence.json"
    candidates = load_json(evidence_file) or []
    return candidates

# Build the exact 30-combination matrix: 3 selected vehicles x 10 assigned part categories.
def generate_30_combination_coverage_matrix(
    catalogue_records: List[Dict[str, Any]],
    availability_records: List[Dict[str, Any]],
    quotation_records: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    selected_vehicles = [
        "BYD Seagull",
        "Toyota bZ4X",
        "Volkswagen ID.4 / ID.6"
    ]
    
    matrix = []
    
    for v_model in selected_vehicles:
        for part_cat in ASSIGNED_PARTS:
            cat_matches = [
                r for r in catalogue_records 
                if (v_model.split()[0].lower() in r.get("vehicle_make", "").lower() or v_model.split()[-1].lower() in r.get("vehicle_model", "").lower())
                and part_cat.lower() in r.get("part_category", "").lower()
            ]
            
            avail_matches = [
                r for r in availability_records
                if (v_model.split()[0].lower() in r.get("vehicle_model", "").lower() or v_model.split()[-1].lower() in r.get("vehicle_model", "").lower())
                and (part_cat.lower() in r.get("part_category", "").lower() or part_cat.lower() in r.get("part_description", "").lower())
            ]
            
            quote_matches = [
                r for r in quotation_records
                if (v_model.split()[0].lower() in r.get("vehicle_model", "").lower() or v_model.split()[-1].lower() in r.get("vehicle_model", "").lower())
                and (part_cat.lower() in r.get("part_category", "").lower() or part_cat.lower() in r.get("part_description", "").lower())
            ]
            
            catalogue_found = "YES" if cat_matches else "NO"
            oem_found = cat_matches[0].get("OEM_part_number", "") if cat_matches else "NOT_FOUND"
            compat_found = "YES" if cat_matches else "NO"
            eth_supp_found = "YES" if avail_matches else "INQUIRY_REQUIRED"
            local_price_found = quote_matches[0].get("quotation_price", "") if quote_matches else ("FOUND" if any(a.get("listed_price") for a in avail_matches) else "INQUIRY_REQUIRED")
            local_stock_found = avail_matches[0].get("stock_status", "UNKNOWN") if avail_matches else "UNKNOWN"
            quotation_found = "YES" if quote_matches else "NO"
            
            if catalogue_found == "YES" and eth_supp_found == "YES" and oem_found != "NOT_FOUND":
                confidence = "HIGH"
                missing = "None; verified OEM number and supplier evidence present"
                next_action = "Obtain formal commercial price quotation from supplier"
            elif catalogue_found == "YES" and oem_found != "NOT_FOUND":
                confidence = "MEDIUM_HIGH"
                missing = "Local wholesale stock quantity and ETB landing price"
                next_action = "Direct inquiry to MOENCO / Sunny / Armana with verified OEM number"
            elif eth_supp_found == "YES":
                confidence = "MEDIUM"
                missing = "Specific OEM part number verification in public catalogue"
                next_action = "Request technical specification and OEM cross-reference"
            else:
                confidence = "LOW"
                missing = "Local supplier listing and public catalogue schematic"
                next_action = "Expand international EPC lookup and manual supplier outreach"

            row = {
                "vehicle_model": v_model,
                "part_category": part_cat,
                "source_found": "YES" if (cat_matches or avail_matches) else "NO",
                "catalogue_record_found": catalogue_found,
                "OEM_number_found": oem_found,
                "compatibility_evidence_found": compat_found,
                "Ethiopian_supplier_found": eth_supp_found,
                "local_price_found": local_price_found,
                "local_stock_found": local_stock_found,
                "quotation_found": quotation_found,
                "evidence_confidence": confidence,
                "missing_information": missing,
                "next_research_action": next_action
            }
            matrix.append(row)
            
    return matrix
