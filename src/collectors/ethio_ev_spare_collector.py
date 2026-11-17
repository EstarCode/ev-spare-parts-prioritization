# Ethio EV Spare Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json, save_text

# Data collector for Ethio EV Spare (ethio_ev_spare). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class EthioEvSpareCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="ethio_ev_spare",
            source_name="Ethio EV Spare",
            source_url="https://ethioevspare.com/",
            evidence_type="IDENTIFIED_LOCAL_SUPPLIER",
            raw_dir_name="ethio_ev_spare"
        )

    # Ingests verified supplier profile, availability records, and spot quotations from the raw Bronze repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing Ethio EV Spare Collector...")
        snap = self.raw_dir / "audit_snapshot.html"
        if not snap.exists():
            _status, text, _, _err = self.client.get(self.source_url)
            if text:
                save_text(text, snap)
                
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        availability = load_json(self.raw_dir / "extracted_availability.json") or []
        quotations_file = self.raw_dir / "extracted_quotations.json"
        quotations = load_json(quotations_file) if quotations_file.exists() else []
        return {
            "suppliers": suppliers,
            "availability": availability,
            "quotations": quotations
        }
