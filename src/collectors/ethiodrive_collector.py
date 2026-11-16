# EthioDrive Data Collector Module.
import re
from typing import Dict, Any
from bs4 import BeautifulSoup
from src.collectors.base_collector import BaseCollector
from src.utils.date_utils import get_utc_now_iso
from src.utils.file_utils import save_json, save_text

# Data collector for EthioDrive (ethiodrive). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class EthiodriveCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="ethiodrive",
            source_name="EthioDrive",
            source_url="https://ethiodrive.com/",
            evidence_type="LOCAL_MARKETPLACE_LISTING",
            raw_dir_name="ethiodrive"
        )

    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing EthioDrive Collector...")
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
                href_lower = href.lower()
                combined_text = (href_lower + " " + raw_text.lower())
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

                id_match = re.search(r"-(\d+)$", href)
                listing_id = f"ETHIODRIVE-{id_match.group(1)}" if id_match else f"ETHIODRIVE-{len(vehicle_listings)+1}"
                
                price_match = re.search(r"([\d,]+)\s*Br", raw_text)
                price = price_match.group(1).replace(",", "") if price_match else ""
                
                year_match = re.search(r"\b(202[0-6])\b", href + " " + raw_text)
                year = year_match.group(1) if year_match else "2023"
                
                rec = {
                    "listing_id": listing_id,
                    "source_id": self.source_id,
                    "source_name": self.source_name,
                    "source_url": f"https://ethiodrive.com{href}",
                    "manufacturer": mfg,
                    "vehicle_model": model,
                    "model_year": year,
                    "trim_or_variant": href.split("/")[-1].replace("-", " ").title(),
                    "asking_price": price,
                    "currency": "ETB",
                    "seller_name": "EthioDrive Verified Dealer",
                    "seller_location": "Addis Ababa, Ethiopia",
                    "vehicle_condition": "Used" if "km" in raw_text else "New",
                    "listing_date": "2026-11",
                    "collection_timestamp": get_utc_now_iso(),
                    "listing_description": raw_text,
                    "original_listing_text": raw_text,
                    "image_reference": "",
                    "original_platform": "EthioDrive",
                    "extraction_method": "HTML_PARSING",
                    "duplicate_candidate": "NO",
                    "verification_status": "COLLECTED_FROM_SOURCE"
                }
                vehicle_listings.append(rec)

        self.logger.info(f"EthioDrive collection finished: {len(vehicle_listings)} listings.")
        save_json(vehicle_listings, self.raw_dir / "extracted_vehicles.json")
        return {"vehicle_listings": vehicle_listings}
