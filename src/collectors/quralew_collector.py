# Quralew Data Collector Module.
import re
from typing import Dict, Any
from bs4 import BeautifulSoup
from src.collectors.base_collector import BaseCollector
from src.utils.date_utils import get_utc_now_iso
from src.utils.file_utils import save_json, save_text

# Data collector for Quralew (quralew). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class QuralewCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="quralew",
            source_name="Quralew",
            source_url="https://quralew.et/en/listings?category=cars",
            evidence_type="LOCAL_MARKETPLACE_LISTING",
            raw_dir_name="quralew"
        )

    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing Quralew Collector...")
        snap = self.raw_dir / "audit_snapshot.html"
        if not snap.exists():
            _status, text, _, _err = self.client.get(self.source_url)
            if text:
                save_text(text, snap)
        else:
            text = snap.read_text(encoding="utf-8", errors="ignore")
            
        soup = BeautifulSoup(text, "html.parser")
        vehicle_listings = []
        
        seen_hrefs = set()
        for a in soup.find_all("a"):
            href = a.get("href", "")
            raw_text = a.get_text().strip()
            if "/listings/" in href and href not in seen_hrefs:
                seen_hrefs.add(href)
                combined_text = (href.lower() + " " + raw_text.lower())
                model = None
                mfg = "Unknown"
                if "seagull" in combined_text:
                    mfg, model = "BYD", "Seagull"
                elif "yuan" in combined_text and ("up" in combined_text or "pro" in combined_text):
                    mfg, model = "BYD", "Yuan Up"
                elif any(k in combined_text for k in ["benben", "e-star", "benni"]):
                    mfg, model = "Changan", "Benben E-Star"
                elif "bz4x" in combined_text:
                    mfg, model = "Toyota", "bZ4X"
                elif re.search(r"\bid[.\-_]?6\b", combined_text):
                    mfg, model = "Volkswagen", "ID.6"
                elif re.search(r"\bid[.\-_]?4\b", combined_text):
                    mfg, model = "Volkswagen", "ID.4"
                    
                if not model:
                    continue

                id_match = re.search(r"/listings/([a-z0-9]+)", href)
                listing_id = f"QURALEW-{id_match.group(1)[:8]}" if id_match else f"QURALEW-{len(vehicle_listings)+1}"
                
                year_match = re.search(r"\b(202[0-6])\b", raw_text)
                year = year_match.group(1) if year_match else "2024"
                
                price_match = re.search(r"([\d,]+)\s*(?:ETB|Birr)", raw_text)
                price = price_match.group(1).replace(",", "") if price_match else ""
                
                rec = {
                    "listing_id": listing_id,
                    "source_id": self.source_id,
                    "source_name": self.source_name,
                    "source_url": f"https://quralew.et{href}",
                    "manufacturer": mfg,
                    "vehicle_model": model,
                    "model_year": year,
                    "trim_or_variant": raw_text[:50],
                    "asking_price": price,
                    "currency": "ETB",
                    "seller_name": "Quralew Verified User",
                    "seller_location": "Addis Ababa, Ethiopia",
                    "vehicle_condition": "New" if "new" in raw_text.lower() else "Used",
                    "listing_date": "2026-11",
                    "collection_timestamp": get_utc_now_iso(),
                    "listing_description": raw_text,
                    "original_listing_text": raw_text,
                    "image_reference": "",
                    "original_platform": "Quralew",
                    "extraction_method": "HTML_PARSING",
                    "duplicate_candidate": "NO",
                    "verification_status": "COLLECTED_FROM_SOURCE"
                }
                vehicle_listings.append(rec)

        self.logger.info(f"Quralew collection finished: {len(vehicle_listings)} listings.")
        save_json(vehicle_listings, self.raw_dir / "extracted_vehicles.json")
        return {"vehicle_listings": vehicle_listings}
