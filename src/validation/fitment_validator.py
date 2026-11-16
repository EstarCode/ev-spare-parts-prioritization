# Fitment Evidence Taxonomy and Classification Validation Module.
from typing import Set

VALID_FITMENT_CLASSIFICATIONS: Set[str] = {
    "VERIFIED_BY_OEM",
    "VIN_CONFIRMED",
    "CATALOGUE_ASSOCIATION",
    "POSSIBLE_FITMENT",
    "UNVERIFIED",
    "NOT_FOUND"
}

# Apply strict fitment evidence taxonomy based on OEM verification and catalog status.
def classify_fitment(
    has_oem_part_num: bool,
    source_type: str,
    oem_verified: bool = False,
    vin_matched: bool = False,
    catalogue_listed: bool = False,
    supplier_claim_only: bool = False
) -> str:
    if vin_matched:
        classification = "VIN_CONFIRMED"
    elif oem_verified or (source_type == "OFFICIAL_MANUFACTURER" and has_oem_part_num):
        classification = "VERIFIED_BY_OEM"
    elif catalogue_listed or (source_type == "INTERNATIONAL_PARTS_CATALOGUE" and has_oem_part_num):
        classification = "CATALOGUE_ASSOCIATION"
    elif supplier_claim_only or (source_type in ["IDENTIFIED_LOCAL_SUPPLIER", "LOCAL_MARKETPLACE_LISTING"]):
        classification = "POSSIBLE_FITMENT" if has_oem_part_num else "UNVERIFIED"
    elif not has_oem_part_num and not catalogue_listed:
        classification = "NOT_FOUND"
    else:
        classification = "UNVERIFIED"

    assert classification in VALID_FITMENT_CLASSIFICATIONS, f"Invalid classification: {classification}"
    return classification
