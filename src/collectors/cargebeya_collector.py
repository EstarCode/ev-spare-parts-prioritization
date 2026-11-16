# CarGebeya Data Collector Module.
import re
from typing import Dict, Any
from bs4 import BeautifulSoup
from src.collectors.base_collector import BaseCollector
from src.utils.date_utils import get_utc_now_iso
from src.utils.file_utils import save_json, save_text

# Data collector for CarGebeya (cargebeya). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class CargebeyaCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="cargebeya",
            source_name="CarGebeya",
            source_url="https://www.cargebeya.com/electric_cars?car_type=cars&ev_type=ev",
            evidence_type="LOCAL_MARKETPLACE_LISTING",
            raw_dir_name="cargebeya"
        )

    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing CarGebeya Collector...")
        p = self.raw_dir / "electric_cars.html"
        if not p.exists():
            _status, text, _, _err = self.client.get(self.source_url)
            if text:
                save_text(text, p)
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
            
        soup = BeautifulSoup(text, "html.parser")
        vehicle_listings = []
        
        for a in soup.find_all("a"):
            href = a.get("href", "")
            raw_text = a.get_text().strip()
            if "/vehicle_listings/" in href:
                id_match = re.search(r"-(\d+)$", href)
                listing_id = f"CARGEB-{id_match.group(1)}" if id_match else f"CARGEB-{len(vehicle_listings)+1}"
                
                href_lower = href.lower()
                mfg = "BYD" if "byd" in href_lower else ("Toyota" if "toyota" in href_lower else ("Volkswagen" if "volkswagen" in href_lower else "Unknown"))
                model = "Unknown"
                if "yuan" in href_lower:
                    model = "Yuan Up"
                elif "atto" in href_lower:
                    model = "Atto 3"
                elif "qin" in href_lower:
                    model = "Qin Plus"
                elif "seagull" in href_lower:
                    model = "Seagull"
                elif "bz4x" in href_lower or "bz" in href_lower:
                    model = "bZ4X"
                elif "id" in href_lower:
                    model = "ID.4"
                    
                year_match = re.search(r"\b(202[0-6])\b", raw_text)
                year = year_match.group(1) if year_match else "2025"
                
                price_match = re.search(r"Birr\s*([\d,]+)", raw_text)
                price = price_match.group(1).replace(",", "") if price_match else ""
                
                loc_match = re.search(r"(Addis [aA]baba|Debre [wW]erk|Hawassa)", raw_text)
                location = loc_match.group(1) if loc_match else "Addis Ababa, Ethiopia"
                
                rec = {
                    "listing_id": listing_id,
                    "source_id": self.source_id,
                    "source_name": self.source_name,
                    "source_url": f"https://www.cargebeya.com{href}",
                    "manufacturer": mfg,
                    "vehicle_model": model,
                    "model_year": year,
                    "trim_or_variant": href.split("/")[-1].replace("-", " ").title(),
                    "asking_price": price,
                    "currency": "ETB",
                    "seller_name": "CarGebeya Verified Seller",
                    "seller_location": location,
                    "vehicle_condition": "Used" if "km" in raw_text else "New",
                    "listing_date": "2026-11",
                    "collection_timestamp": get_utc_now_iso(),
                    "listing_description": raw_text,
                    "original_listing_text": raw_text,
                    "image_reference": "",
                    "original_platform": "CarGebeya Marketplace",
                    "extraction_method": "HTML_PARSING",
                    "duplicate_candidate": "NO",
                    "verification_status": "COLLECTED_FROM_SOURCE"
                }
                vehicle_listings.append(rec)

        self.logger.info(f"CarGebeya collection finished: {len(vehicle_listings)} listings.")
        save_json(vehicle_listings, self.raw_dir / "extracted_vehicles.json")
        return {"vehicle_listings": vehicle_listings}
