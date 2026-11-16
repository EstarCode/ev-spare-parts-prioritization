# Abstract Base Collector Architecture.
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path
from src.utils.http_client import HttpClient
from src.utils.logger import get_logger
from src.utils.file_utils import ensure_dir
from src.utils.date_utils import get_utc_now_iso

# Abstract base class providing standard logging, HTTP client, and error tracking for all automotive data collectors.
class BaseCollector(ABC):
    def __init__(self, source_id: str, source_name: str, source_url: str, evidence_type: str, raw_dir_name: str):
        self.source_id = source_id
        self.source_name = source_name
        self.source_url = source_url
        self.evidence_type = evidence_type
        self.raw_dir = Path(__file__).resolve().parent.parent.parent / "data" / "raw" / raw_dir_name
        ensure_dir(self.raw_dir)
        self.logger = get_logger(f"collector_{source_id}")
        self.client = HttpClient()
        self.errors: List[Dict[str, Any]] = []

    # Record a standardized error entry conforming to the extraction_errors schema.
    def log_error(self, url: str, error_type: str, details: str, recovery: str = "Logged and skipped") -> None:
        err = {
            "error_id": f"ERR-{len(self.errors)+1:04d}",
            "source_id": self.source_id,
            "source_url": url,
            "timestamp": get_utc_now_iso(),
            "error_type": error_type,
            "error_details": details,
            "recovery_action_taken": recovery
        }
        self.errors.append(err)
        self.logger.error(f"[{error_type}] {url}: {details}")

    @abstractmethod
    # Execute the collector and return structured data dictionary.
    def collect(self) -> Dict[str, Any]:
        pass
