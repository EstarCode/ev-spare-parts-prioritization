# EV Spare Buyer Application Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json

# Data collector for EV Spare Buyer Application (ev_spare_app). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class EvSpareAppCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="ev_spare_app",
            source_name="EV Spare Buyer Application",
            source_url="https://play.google.com/store/apps/details?id=com.evspare.buyer",
            evidence_type="IDENTIFIED_LOCAL_SUPPLIER",
            raw_dir_name="ev_spare_app"
        )

    # Ingests verified mobile application supplier profile records from the raw Bronze data repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing EV Spare App Collector...")
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        return {"suppliers": suppliers}
