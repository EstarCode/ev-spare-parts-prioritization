# ethioCars Data Collector Module.
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.file_utils import load_json

# Data collector for ethioCars (ethiocars). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class EthiocarsCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="ethiocars",
            source_name="ethioCars",
            source_url="https://ethiocars.com/",
            evidence_type="LOCAL_MARKETPLACE_LISTING",
            raw_dir_name="ethiocars"
        )

    # Ingests verified automotive classifieds directory supplier records from the raw Bronze data repository.
    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing ethioCars Collector...")
        suppliers = load_json(self.raw_dir / "extracted_supplier.json") or []
        return {
            "suppliers": suppliers,
            "vehicle_listings": []
        }
