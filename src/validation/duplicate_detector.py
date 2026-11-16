# Cross-Portal Vehicle Classified Advertisement Deduplication Module.
from typing import List, Dict, Any
import re

# Normalize whitespace and case fold input text.
def normalize_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower().strip())

# Detect duplicate candidate listings across and within sources based on model, year, price, and seller/description.
def detect_vehicle_listing_duplicates(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    duplicates = []
    seen = {}
    
    for item in listings:
        model = normalize_text(item.get("vehicle_model", ""))
        price = str(item.get("asking_price", "")).strip()
        year = str(item.get("model_year", "")).strip()
        seller = normalize_text(item.get("seller_name", ""))
        
        if model and price and price != "0" and price != "":
            key = (model, year, price, seller)
            if key in seen:
                primary = seen[key]
                item["duplicate_candidate"] = "YES"
                duplicates.append({
                    "candidate_id": f"DUP-{len(duplicates)+1:04d}",
                    "source_id": item.get("source_id", ""),
                    "primary_record_id": primary.get("listing_id", ""),
                    "matching_record_id": item.get("listing_id", ""),
                    "vehicle_model": item.get("vehicle_model", ""),
                    "match_criteria": "EXACT_MODEL_YEAR_PRICE_SELLER",
                    "similarity_score": 1.0,
                    "resolution": "FLAGGED_AS_DUPLICATE_CROSS_POST"
                })
            else:
                seen[key] = item
                item["duplicate_candidate"] = "NO"
        else:
            item["duplicate_candidate"] = "NO"
            
    return duplicates
