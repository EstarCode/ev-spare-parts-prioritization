# Gezat Electric Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json, save_text

# Data collector for Gezat Electric (gezat). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class GezatCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="gezat",
            source_name="Gezat Electric",
            source_url="https://ev.gezat.et/",
            evidence_type="IDENTIFIED_LOCAL_SUPPLIER",
            raw_dir_name="gezat"
        )

    # Ingests verified retailer supplier profile, vehicle listing, and availability records from the raw Bronze repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing Gezat Electric Collector...")
        snap = self.raw_dir / "audit_snapshot.html"
        if not snap.exists():
            _status, text, _, _err = self.client.get(self.source_url)
            if text:
                save_text(text, snap)
                
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        availability = load_json(self.raw_dir / "extracted_availability.json") or []
        vehicles = load_json(self.raw_dir / "extracted_vehicles.json") or []
        return {
            "suppliers": suppliers,
            "availability": availability,
            "vehicle_listings": vehicles
        }
