# Armana Motors / Armana Trading Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json, save_text

# Data collector for Armana Motors (armana_motors). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class ArmanaCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="armana_motors",
            source_name="Armana Motors / Armana Trading",
            source_url="https://armanamotors.com/",
            evidence_type="IDENTIFIED_LOCAL_SUPPLIER",
            raw_dir_name="armana_motors"
        )

    # Ingests verified importer supplier profile and availability records from the raw Bronze repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing Armana Motors Collector...")
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
