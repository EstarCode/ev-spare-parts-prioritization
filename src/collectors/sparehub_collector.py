# SpareHub Ethiopia Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json

# Data collector for SpareHub Ethiopia (sparehub). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class SparehubCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="sparehub",
            source_name="SpareHub Ethiopia",
            source_url="https://sparehubethiopia.com/",
            evidence_type="LOCAL_MARKETPLACE_LISTING",
            raw_dir_name="sparehub"
        )

    # Ingests verified marketplace supplier profile records from the raw Bronze data repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing SpareHub Ethiopia Collector...")
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        return {"suppliers": suppliers}
