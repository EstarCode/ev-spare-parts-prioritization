# Data Validation & Integrity Subpackage. Provides schema contract enforcement, fitment evidence classification, and listing duplicate detection.
from .schema_validator import SCHEMAS, validate_record_schema
from .fitment_validator import classify_fitment, VALID_FITMENT_CLASSIFICATIONS
from .duplicate_detector import detect_vehicle_listing_duplicates
from .source_validator import run_source_audit

__all__ = [
    "SCHEMAS",
    "validate_record_schema",
    "classify_fitment",
    "VALID_FITMENT_CLASSIFICATIONS",
    "detect_vehicle_listing_duplicates",
    "run_source_audit"
]
