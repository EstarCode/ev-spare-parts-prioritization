# Schema Definitions and Data Contract Validation Module.
from typing import Dict, List, Any

SCHEMAS: Dict[str, List[str]] = {
    "vehicle_market_listings": [
        "listing_id", "source_id", "source_name", "source_url", "manufacturer",
        "vehicle_model", "model_year", "trim_or_variant", "asking_price", "currency",
        "seller_name", "seller_location", "vehicle_condition", "listing_date",
        "collection_timestamp", "listing_description", "original_listing_text",
        "image_reference", "original_platform", "extraction_method", "duplicate_candidate",
        "verification_status"
    ],
    "vehicle_selection_evidence": [
        "vehicle_model", "manufacturer", "market_listings_count", "unique_listings_count",
        "distinct_sellers_count", "ethiopian_distributor_found", "local_supplier_coverage",
        "parts_availability_evidence", "evidence_quality", "selection_status", "justification"
    ],
    "parts_catalogue_records": [
        "record_id", "source_id", "vehicle_make", "vehicle_model", "model_year",
        "trim_or_variant", "part_category", "part_description", "OEM_part_number",
        "supplier_part_number", "manufacturer", "catalogue_price", "currency",
        "stock_status", "supplier_name", "fitment_description", "compatibility_reference",
        "source_url", "collection_timestamp", "original_text", "extraction_method",
        "verification_status"
    ],
    "fitment_evidence": [
        "evidence_id", "vehicle_model", "model_year", "trim_or_modification",
        "part_category", "OEM_part_number", "catalogue_reference", "fitment_statement",
        "vin_applicability", "supplier_compatibility_claim", "fitment_classification",
        "evidence_url", "collection_date", "notes"
    ],
    "local_availability_evidence": [
        "availability_id", "supplier_name", "vehicle_model", "part_category",
        "part_description", "OEM_part_number", "supplier_SKU", "stock_status",
        "quantity_in_stock", "listed_price", "currency", "location", "delivery_information",
        "lead_time", "availability_date", "source_url", "collection_timestamp",
        "original_text", "evidence_type", "verification_status"
    ],
    "supplier_directory": [
        "supplier_id", "supplier_name", "website", "supplier_type", "country", "city",
        "public_business_address", "public_business_phone", "public_business_email",
        "supported_vehicle_brands", "supported_models", "parts_categories",
        "original_parts_claim", "inventory_information_available", "pricing_information_available",
        "inquiry_method", "source_url", "collection_date", "verification_status"
    ],
    "supplier_quotations": [
        "quotation_id", "supplier_name", "vehicle_model", "model_year", "part_category",
        "OEM_part_number", "supplier_SKU", "quotation_price", "currency", "stock_status",
        "delivery_location", "lead_time", "quotation_date", "quotation_reference",
        "source_url", "evidence_file", "verification_status"
    ],
    "nhtsa_complaints": [
        "complaint_id", "manufacturer", "model", "model_year", "complaint_date",
        "component", "summary", "crash", "fire", "injuries", "deaths",
        "source_url", "collection_date"
    ],
    "nhtsa_recalls": [
        "recall_number", "manufacturer", "model", "model_year", "component",
        "recall_description", "consequence", "remedy", "source_url", "collection_date"
    ],
    "social_media_advertisements": [
        "ad_id", "seller_name", "platform", "post_url", "post_date", "vehicle_model",
        "part_category", "part_description", "advertised_price", "currency", "location",
        "contact_method", "original_post_text", "collection_timestamp", "verification_status"
    ],
    "source_log": [
        "source_id", "source_name", "source_url", "source_type", "country",
        "source_owner_or_publisher", "vehicle_model", "part_category", "collection_timestamp",
        "extraction_method", "original_file_path", "record_count", "extraction_status",
        "evidence_type", "verification_status", "reliability_notes", "limitations"
    ],
    "source_accessibility": [
        "source_id", "source_name", "source_url", "is_accessible", "http_status",
        "response_time_sec", "has_relevant_data", "data_types", "extraction_method",
        "access_restrictions", "reliability_score", "limitations", "next_action"
    ],
    "extraction_errors": [
        "error_id", "source_id", "source_url", "timestamp", "error_type",
        "error_details", "recovery_action_taken"
    ],
    "duplicate_candidates": [
        "candidate_id", "source_id", "primary_record_id", "matching_record_id",
        "vehicle_model", "match_criteria", "similarity_score", "resolution"
    ],
    "missing_evidence": [
        "item_id", "vehicle_model", "part_category", "data_dimension",
        "expected_source", "reason_missing", "impact_on_analysis", "recommended_mitigation"
    ],
    "vehicle_part_coverage": [
        "vehicle_model", "part_category", "source_found", "catalogue_record_found",
        "OEM_number_found", "compatibility_evidence_found", "Ethiopian_supplier_found",
        "local_price_found", "local_stock_found", "quotation_found", "evidence_confidence",
        "missing_information", "next_research_action"
    ]
}

# Check that all required fields exist in record.
def validate_record_schema(record: Dict[str, Any], schema_name: str) -> List[str]:
    if schema_name not in SCHEMAS:
        raise ValueError(f"Unknown schema: {schema_name}")
    required_fields = SCHEMAS[schema_name]
    missing = [f for f in required_fields if f not in record]
    return missing

# Alias for backward and external compatibility
validate_schema = validate_record_schema

