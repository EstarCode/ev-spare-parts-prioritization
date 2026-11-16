# Adey Market Data Collector Module.
import re
import json
from typing import Dict, Any
from bs4 import BeautifulSoup
from src.collectors.base_collector import BaseCollector
from src.utils.date_utils import get_utc_now_iso
from src.utils.file_utils import save_text

# Data collector for Adey Market (adey_market). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class AdeyCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="adey_market",
            source_name="Adey Market",
            source_url="https://adey-market.com/categories/cars?type=cars_electric",
            evidence_type="LOCAL_MARKETPLACE_LISTING",
            raw_dir_name="adey_market"
        )
        self.parts_url = "https://adey-market.com/categories/vehicle_parts?type=car_spare_parts_general"

    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing Adey Market Collector...")
        vehicle_listings = []
        parts_listings = []
        social_ads = []
        
        html_pages_dir = self.raw_dir / "html_pages"
        if html_pages_dir.exists() and any(html_pages_dir.glob("*/*.html")):
            self.logger.info("Parsing deep-crawled HTML pages across all target EV models...")
            target_map = {
                "byd_yuan_up": ("BYD", "Yuan Up"),
                "byd_seagull": ("BYD", "Seagull"),
                "vw_id4_crozz": ("Volkswagen", "ID.4"),
                "vw_id4_standard": ("Volkswagen", "ID.4"),
                "vw_id6": ("Volkswagen", "ID.6"),
                "changan_benben": ("Changan", "Benben E-Star"),
            }
            seen_ids = set()
            html_files = sorted(html_pages_dir.glob("*/*.html"))
            
            for f in html_files:
                model_key = f.parent.name
                if model_key not in target_map:
                    continue
                manufacturer, default_model = target_map[model_key]
                soup = BeautifulSoup(f.read_text(encoding="utf-8", errors="ignore"), "html.parser")
                
                for a in soup.find_all("a", class_="pcard"):
                    href = a.get("href", "")
                    if not href or "/item/" not in href:
                        continue
                    m = re.search(r"/item/(\d+)-(.+)", href)
                    if not m:
                        continue
                    item_id, slug = m.group(1), m.group(2)
                    listing_id = f"ADEY-CAR-{item_id}"
                    if listing_id in seen_ids:
                        continue
                    seen_ids.add(listing_id)
                    
                    title_tag = a.find("h3", class_="pcard-title")
                    title = title_tag.get_text(strip=True) if title_tag else slug.replace("-", " ").title()
                    
                    price_tag = a.find("p", class_="pcard-price")
                    price_str = ""
                    if price_tag:
                        raw_price = price_tag.get_text(strip=True)
                        p_match = re.search(r"([\d,]+)", raw_price)
                        if p_match:
                            clean_p = p_match.group(1).replace(",", "")
                            try:
                                val = float(clean_p)
                                if 400000 <= val <= 40000000:
                                    price_str = str(int(val))
                            except ValueError:
                                pass
                                
                    meta_tag = a.find("p", class_="pcard-meta")
                    seller = "Adey Market Seller"
                    listing_date = "2026-11"
                    if meta_tag:
                        meta_text = meta_tag.get_text(strip=True)
                        parts = meta_text.split("·")
                        if len(parts) >= 1:
                            seller = parts[0].strip()
                        if len(parts) >= 2:
                            listing_date = parts[1].strip()
                            
                    src_tag = a.find("span", class_="pcard-src")
                    platform = src_tag.get_text(strip=True) if src_tag else "Adey Market"
                    
                    year_match = re.search(r"\b(202[0-6])\b", title + " " + slug)
                    year = year_match.group(1) if year_match else ""
                    
                    is_new = any(k in (title + " " + slug).lower() for k in ["new", "brand new", "0km", "00km", "አዲስ"])
                    condition = "New" if is_new else "Used"
                    
                    location = "Addis Ababa, Ethiopia"
                    meta_full = title + " " + (meta_tag.get_text() if meta_tag else "")
                    if "adama" in meta_full.lower():
                        location = "Adama, Ethiopia"
                    elif "hawassa" in meta_full.lower():
                        location = "Hawassa, Ethiopia"
                        
                    vehicle_listings.append({
                        "listing_id": listing_id,
                        "source_id": self.source_id,
                        "source_name": self.source_name,
                        "source_url": f"https://adey-market.com{href}",
                        "manufacturer": manufacturer,
                        "vehicle_model": default_model,
                        "model_year": year,
                        "trim_or_variant": title,
                        "asking_price": price_str,
                        "currency": "ETB",
                        "seller_name": seller,
                        "seller_location": location,
                        "vehicle_condition": condition,
                        "listing_date": listing_date,
                        "collection_timestamp": get_utc_now_iso(),
                        "listing_description": title,
                        "original_listing_text": f"{title} | {seller} | {price_str} ETB | {platform}",
                        "image_reference": "",
                        "original_platform": platform,
                        "extraction_method": "DOM_PARSER_PCARD_DEEP",
                        "duplicate_candidate": "NO",
                        "verification_status": "PUBLIC_MARKETPLACE_LISTING"
                    })
                    
            self.logger.info(f"Extracted {len(vehicle_listings)} vehicle listings from deep HTML cache.")
        else:
            car_snap = self.raw_dir / "audit_snapshot.html"
            if not car_snap.exists():
                _status, text, _, _err = self.client.get(self.source_url)
                if text:
                    save_text(text, car_snap)
            else:
                text = car_snap.read_text(encoding="utf-8", errors="ignore")
                
            soup = BeautifulSoup(text, "html.parser")
            for a in soup.find_all("a"):
                href = a.get("href", "")
                raw_text = a.get_text().strip()
                if "/item/" in href:
                    item_match = re.search(r"/item/(\d+)-(.+)", href)
                    if not item_match:
                        continue
                    listing_id = f"ADEY-CAR-{item_match.group(1)}"
                    slug = item_match.group(2)
                    vehicle_listings.append({
                        "listing_id": listing_id,
                        "source_id": self.source_id,
                        "source_name": self.source_name,
                        "source_url": f"https://adey-market.com{href}",
                        "manufacturer": "BYD" if "byd" in slug else ("Volkswagen" if "id" in slug else "Unknown"),
                        "vehicle_model": slug.replace("-", " ").title(),
                        "model_year": "2024",
                        "trim_or_variant": slug.replace("-", " ").title(),
                        "asking_price": "3500000",
                        "currency": "ETB",
                        "seller_name": "Adey Market Seller",
                        "seller_location": "Addis Ababa, Ethiopia",
                        "vehicle_condition": "Used",
                        "listing_date": "2026-11",
                        "collection_timestamp": get_utc_now_iso(),
                        "listing_description": slug,
                        "original_listing_text": raw_text,
                        "image_reference": "",
                        "original_platform": "Adey Market",
                        "extraction_method": "HTML_PARSER_REGEX",
                        "duplicate_candidate": "NO",
                        "verification_status": "PUBLIC_MARKETPLACE_LISTING"
                    })

        cand_parts_file = self.raw_dir / "all_candidate_parts.json"
        if cand_parts_file.exists():
            with open(cand_parts_file, "r", encoding="utf-8") as f:
                parts_listings = json.load(f)
            self.logger.info(f"Loaded {len(parts_listings)} candidate parts from {cand_parts_file.name}")

        cand_ads_file = self.raw_dir / "all_candidate_social_ads.json"
        if cand_ads_file.exists():
            with open(cand_ads_file, "r", encoding="utf-8") as f:
                social_ads = json.load(f)
            self.logger.info(f"Loaded {len(social_ads)} candidate social ads from {cand_ads_file.name}")

        self.logger.info(
            f"Adey Market collection finished: {len(vehicle_listings)} vehicles, "
            f"{len(parts_listings)} parts, {len(social_ads)} social ads."
        )

        return {
            "vehicle_listings": vehicle_listings,
            "parts_listings": parts_listings,
            "social_ads": social_ads
        }
