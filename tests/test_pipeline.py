import pandas as pd
from pathlib import Path
from src.validation.schema_validator import SCHEMAS
from src.validation.fitment_validator import classify_fitment
from src.validation.duplicate_detector import detect_vehicle_listing_duplicates
from src.scoring import calculate_prioritization_scores, run_sensitivity_analysis

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"

# Validates existence and non-empty status of all 18 Silver-tier processed CSV files.
def test_all_processed_csv_files_exist():
    expected_files = [
        "vehicle_market_listings.csv",
        "vehicle_selection_evidence.csv",
        "parts_catalogue_records.csv",
        "fitment_evidence.csv",
        "local_availability_evidence.csv",
        "supplier_directory.csv",
        "supplier_quotations.csv",
        "nhtsa_complaints.csv",
        "nhtsa_recalls.csv",
        "social_media_advertisements.csv",
        "source_log.csv",
        "source_accessibility.csv",
        "extraction_errors.csv",
        "duplicate_candidates.csv",
        "missing_evidence.csv",
        "vehicle_part_coverage.csv",
        "import_logistics_tariffs.csv",
        "vehicle_statistical_summary.csv"
    ]
    for filename in expected_files:
        file_path = PROCESSED_DIR / filename
        assert file_path.exists(), f"Missing required file: {filename}"
        assert file_path.stat().st_size > 0, f"File is empty: {filename}"

# Validates schemas and column presence across all registered datasets.
def test_csv_schemas_and_columns():
    for schema_name, required_cols in SCHEMAS.items():
        csv_path = PROCESSED_DIR / f"{schema_name}.csv"
        assert csv_path.exists(), f"Schema file not found: {schema_name}.csv"
        df = pd.read_csv(csv_path)
        for col in required_cols:
            assert col in df.columns, f"Column '{col}' missing from {schema_name}.csv"

# Validates dimensions and complete grid coverage of the 30-combination matrix.
def test_vehicle_part_coverage_matrix_dimensions():
    coverage_path = PROCESSED_DIR / "vehicle_part_coverage.csv"
    df = pd.read_csv(coverage_path)
    assert len(df) == 30, f"Coverage matrix must contain exactly 30 vehicle-part combinations, found {len(df)}"
    
    unique_vehicles = df["vehicle_model"].unique()
    assert len(unique_vehicles) == 3, f"Expected 3 selected vehicles, found {len(unique_vehicles)}: {unique_vehicles}"
    
    unique_parts = df["part_category"].unique()
    assert len(unique_parts) == 10, f"Expected 10 required part categories, found {len(unique_parts)}"

# Validates candidate vehicle evaluation counts and 3-selected 2-omitted selection statuses.
def test_vehicle_selection_evidence():
    sel_path = PROCESSED_DIR / "vehicle_selection_evidence.csv"
    df = pd.read_csv(sel_path)
    assert len(df) == 5, f"All 5 candidate vehicles must be investigated, found {len(df)}"
    selected = df[df["selection_status"] == "SELECTED"]
    not_selected = df[df["selection_status"] == "NOT_SELECTED"]
    assert len(selected) == 3, f"Expected exactly 3 selected vehicles, found {len(selected)}"
    assert len(not_selected) == 2, f"Expected exactly 2 omitted vehicles, found {len(not_selected)}"

# Validates standard 6-tier fitment classification taxonomy logic.
def test_fitment_taxonomy():
    assert classify_fitment(True, "OFFICIAL_MANUFACTURER", oem_verified=True) == "VERIFIED_BY_OEM"
    assert classify_fitment(True, "INTERNATIONAL_PARTS_CATALOGUE", catalogue_listed=True) == "CATALOGUE_ASSOCIATION"
    assert classify_fitment(False, "LOCAL_MARKETPLACE_LISTING") == "UNVERIFIED"
    assert classify_fitment(False, "UNKNOWN_SOURCE") == "NOT_FOUND"

# Validates deterministic vehicle advertisement duplicate detection logic.
def test_duplicate_detector():
    sample = [
        {"listing_id": "L1", "vehicle_model": "BYD Seagull", "model_year": "2024", "asking_price": "3500000", "seller_name": "AfroMekina"},
        {"listing_id": "L2", "vehicle_model": "BYD Seagull", "model_year": "2024", "asking_price": "3500000", "seller_name": "AfroMekina"},
        {"listing_id": "L3", "vehicle_model": "Toyota bZ4X", "model_year": "2023", "asking_price": "6500000", "seller_name": "EthioDrive"}
    ]
    dups = detect_vehicle_listing_duplicates(sample)
    assert len(dups) == 1
    assert dups[0]["primary_record_id"] == "L1"
    assert dups[0]["matching_record_id"] == "L2"

# Validates MCDA scoring engine rank generation, composite bounds, and top 5 selection.
def test_scoring_engine_prioritization():
    df_scored, df_top_5 = calculate_prioritization_scores(PROJECT_ROOT)
    assert len(df_scored) == 30, f"Expected 30 ranked combinations, got {len(df_scored)}"
    assert len(df_top_5) == 5, f"Expected exactly 5 recommended parts, got {len(df_top_5)}"
    
    assert "composite_priority_score" in df_scored.columns
    assert "priority_rank" in df_scored.columns
    assert "strategic_recommendation" in df_top_5.columns
    
    assert (df_scored["composite_priority_score"] >= 0.0).all()
    assert (df_scored["composite_priority_score"] <= 100.0).all()
    assert list(df_scored["priority_rank"]) == list(range(1, 31))

# Validates sensitivity analysis execution across all four strategic weighting scenarios.
def test_sensitivity_analysis():
    df_scored, _ = calculate_prioritization_scores(PROJECT_ROOT)
    df_sens = run_sensitivity_analysis(df_scored)
    assert len(df_sens) == 4, f"Expected 4 sensitivity scenarios, got {len(df_sens)}"
    for col in ["rank_1", "rank_2", "rank_3", "rank_4", "rank_5"]:
        assert col in df_sens.columns
        assert not df_sens[col].isnull().any()

# Validates existence, schema conformity, and data presence in Gold-tier analytical files.
def test_cleaned_gold_tier_files():
    expected_gold_files = [
        "cleaned_vehicle_listings.csv",
        "cleaned_parts_records.csv",
        "prioritized_parts_ranking.csv",
        "top_5_recommended_parts.csv",
        "sensitivity_analysis.csv"
    ]
    for filename in expected_gold_files:
        file_path = CLEANED_DIR / filename
        assert file_path.exists(), f"Missing gold tier file: {filename}"
        assert file_path.stat().st_size > 0, f"File is empty: {filename}"
        df = pd.read_csv(file_path)
        assert len(df) > 0, f"File has no data: {filename}"
