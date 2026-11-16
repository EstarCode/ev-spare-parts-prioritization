# Vehicle marketplace data cleaning and normalization.
from typing import List, Dict, Any
import re
import datetime

# Clean, bound ETB asking prices, normalize Amharic/English condition tags, and format ISO-8601 dates.
def clean_and_normalize_vehicle_listings(raw_listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned = []
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for item in raw_listings:
        c = dict(item)
        
        mfg = str(c.get("manufacturer", "")).strip()
        model = str(c.get("vehicle_model", "")).strip()
        desc = f"{c.get('listing_description', '')} {c.get('original_listing_text', '')}"
        
        if "seagull" in model.lower() or "seagull" in desc.lower():
            model, mfg = "Seagull", "BYD"
        elif "yuan" in model.lower() or "yuan up" in desc.lower():
            model, mfg = "Yuan Up", "BYD"
        elif any(k in model.lower() or k in desc.lower() for k in ["benben", "benni", "e-star"]):
            model, mfg = "Benben E-Star", "Changan"
        elif "bz4x" in model.lower() or "bz4x" in desc.lower() or "bz" in model.lower():
            model, mfg = "bZ4X", "Toyota"
        elif "id.4 crozz" in model.lower() or "crozz" in desc.lower():
            model, mfg = "ID.4 Crozz", "Volkswagen"
        elif "id.6" in model.lower() or "id6" in desc.lower():
            model, mfg = "ID.6", "Volkswagen"
        elif "id.4" in model.lower() or "id4" in desc.lower():
            model, mfg = "ID.4", "Volkswagen"
            
        c["manufacturer"] = mfg
        c["vehicle_model"] = model
        
        raw_p = str(c.get("asking_price", "")).replace(",", "").strip()
        try:
            val = float(raw_p)
            c["asking_price"] = str(int(val)) if 500_000 <= val <= 40_000_000 else ""
        except (ValueError, TypeError):
            c["asking_price"] = ""
            
        c["currency"] = "ETB"
        
        raw_cond = str(c.get("vehicle_condition", ""))
        is_new = any(k in (raw_cond + " " + desc).lower() for k in ["new", "brand new", "0km", "00km", "አዲስ"])
        c["vehicle_condition"] = "New" if is_new else "Used"
        
        dt_str = str(c.get("listing_date", "")).strip()
        if any(k in dt_str for k in ["m ago", "h ago"]) or "today" in dt_str.lower():
            c["listing_date"] = now.strftime("%Y-%m-%d")
        elif "d ago" in dt_str:
            days_match = re.search(r"(\d+)d\s*ago", dt_str)
            days = int(days_match.group(1)) if days_match else 1
            c["listing_date"] = (now - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        elif not re.match(r"^\d{4}-\d{2}", dt_str):
            c["listing_date"] = "2026-11-15"
            
        cleaned.append(c)
        
    return cleaned
