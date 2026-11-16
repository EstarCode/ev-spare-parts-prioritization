# BYD Ethiopia (Inchcape Motors) Authorized National Distributor Collector.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json, save_text

# Collector for BYD Ethiopia (Inchcape Motors), the authorized national distributor for BYD electric vehicles (Seagull, Yuan Up) and genuine spare parts in Addis Ababa.
class BydEthiopiaCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="byd_ethiopia",
            source_name="BYD Ethiopia (Inchcape)",
            source_url="https://www.byd.com.et/",
            evidence_type="AUTHORIZED_DISTRIBUTOR",
            raw_dir_name="byd_ethiopia"
        )

    # Ingests verified distributor profile and parts availability records from the raw Bronze repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing BYD Ethiopia Collector...")
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
