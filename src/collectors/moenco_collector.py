# MOENCO Ethiopia Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json

# Data collector for MOENCO Ethiopia (moenco). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class MoencoCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="moenco",
            source_name="MOENCO Ethiopia",
            source_url="https://www.moencoethiopia.com/parts/",
            evidence_type="AUTHORIZED_DISTRIBUTOR",
            raw_dir_name="moenco"
        )

    # Ingests verified dealer supplier profile and availability records from the raw Bronze data repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing MOENCO Ethiopia Collector...")
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        availability = load_json(self.raw_dir / "extracted_availability.json") or []
        return {
            "suppliers": suppliers,
            "availability": availability
        }
