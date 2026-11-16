# Sunny Spare Parts Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json, save_text

# Data collector for Sunny Spare Parts (sunny_spare_parts). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class SunnyCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="sunny_spare_parts",
            source_name="Sunny Spare Parts",
            source_url="https://sunnyspareparts.com/",
            evidence_type="IDENTIFIED_LOCAL_SUPPLIER",
            raw_dir_name="sunny_spare_parts"
        )

    # Ingests verified retailer supplier profile and availability records from the raw Bronze repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing Sunny Spare Parts Collector...")
        snap = self.raw_dir / "audit_snapshot.html"
        if not snap.exists():
            _status, text, _, _err = self.client.get(self.source_url)
            if text:
                save_text(text, snap)
                
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        availability = load_json(self.raw_dir / "extracted_availability.json") or []
        return {
            "suppliers": suppliers,
            "availability": availability
        }
