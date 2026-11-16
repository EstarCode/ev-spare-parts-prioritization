# Comprehensive Technical Data Dictionary & Schema Specification

**Project:** EV Spare-Parts Import Prioritization in Ethiopia  
**Author:** Abraham Amogne | Master Internship Project  
**Specification Version:** 1.0.0 (Production)  
**Encoding:** UTF-8 (No BOM) | **Standard:** RFC 4180  

---

## Table of Contents
1. [Gold Tier: Analytical & Decision Datasets](#1-gold-tier-analytical--decision-datasets)
2. [Silver Tier: Standardized Datasets](#2-silver-tier-standardized-datasets)
3. [Fitment Evidence Taxonomy Specification](#3-fitment-evidence-taxonomy-specification)
4. [Ethiopian Customs Commission (ECC) Tariff Schedule Reference](#4-ethiopian-customs-commission-ecc-tariff-schedule-reference)

---

## 1. Gold Tier: Analytical & Decision Datasets

### 1.1 `cleaned/top_5_recommended_parts.csv`
* **Role:** Final commercial import stocking prioritization recommendations for enterprise procurement.
* **Row Count:** Exactly 5 rows | **Primary Key:** `priority_rank` (1 to 5)

| Column Name | Data Type | Nullable | Description & Business Rules |
| :--- | :---: | :---: | :--- |
| `vehicle_model` | `VARCHAR(64)` | No | Selected fleet model (`BYD Seagull` or `Volkswagen ID.4 / ID.6`). |
| `part_category` | `VARCHAR(64)` | No | Functional component category from the 10 target categories. |
| `oem_reference` | `VARCHAR(64)` | No | Verified manufacturer OEM part number (`14758996-00`, `1EA-698-151`, etc.). |
| `demand_score` | `FLOAT` | No | Empirical demand rating (0–100) based on fleet visibility and mechanical wear rate. |
| `scarcity_score` | `FLOAT` | No | Market scarcity rating (0–100) reflecting Addis Ababa wholesale availability. |
| `compatibility_score` | `FLOAT` | No | Fitment certainty rating (0–100) based on verified OEM catalog documentation. |
| `practicality_score` | `FLOAT` | No | Import logistics rating (0–100) reflecting ECC duty burden and volumetric freight. |
| `confidence_score` | `FLOAT` | No | Data lineage reliability rating (0–100) based on verified provenance. |
| `composite_priority_score` | `FLOAT` | No | Weighted multi-criteria score: $0.30D + 0.25S + 0.20C + 0.15P + 0.10Conf$. |
| `wear_profile` | `VARCHAR(32)` | No | Failure mechanism (`HIGH_WEAR`, `URBAN_THEFT_HAZARD`, `MODERATE_WEAR`, etc.). |
| `priority_rank` | `INT` | No | Ordinal rank from 1 (highest priority) to 5. |
| `strategic_recommendation` | `TEXT` | No | Commercial stocking justification, freight mode, and supply-chain rationale. |

---

### 1.2 `cleaned/prioritized_parts_ranking.csv`
* **Role:** Complete MCDA ranking across all 30 candidate vehicle-part combinations.
* **Row Count:** Exactly 30 rows | **Primary Key:** `priority_rank` (1 to 30)

| Column Name | Data Type | Nullable | Description & Business Rules |
| :--- | :---: | :---: | :--- |
| `vehicle_model` | `VARCHAR(64)` | No | Vehicle model (`BYD Seagull`, `Toyota bZ4X`, `Volkswagen ID.4 / ID.6`). |
| `part_category` | `VARCHAR(64)` | No | One of the 10 functional component categories. |
| `oem_reference` | `VARCHAR(64)` | No | Verified OEM part number or catalog cross-reference. |
| `demand_score` | `FLOAT` | No | Calculated Demand criterion score (0–100). |
| `scarcity_score` | `FLOAT` | No | Calculated Scarcity criterion score (0–100). |
| `compatibility_score` | `FLOAT` | No | Calculated Compatibility criterion score (0–100). |
| `practicality_score` | `FLOAT` | No | Calculated Sourcing Practicality score (0–100). |
| `confidence_score` | `FLOAT` | No | Calculated Lineage Confidence score (0–100). |
| `composite_priority_score` | `FLOAT` | No | Final MCDA composite priority score. |
| `wear_profile` | `VARCHAR(32)` | No | Component degradation category. |
| `priority_rank` | `INT` | No | Ranked order position (1 through 30). |

---

### 1.3 `cleaned/sensitivity_analysis.csv`
* **Role:** Evaluates rank robustness across 4 distinct operational weighting scenarios.
* **Row Count:** 4 rows | **Primary Key:** `scenario`

| Column Name | Data Type | Nullable | Description & Business Rules |
| :--- | :---: | :---: | :--- |
| `scenario` | `VARCHAR(64)` | No | Scenario name (`Baseline`, `Demand-Heavy`, `Scarcity-Heavy`, `Practicality-Heavy`). |
| `rank_1` | `VARCHAR(64)` | No | Top-ranked component combination under this scenario. |
| `rank_2` | `VARCHAR(64)` | No | Second-ranked component combination. |
| `rank_3` | `VARCHAR(64)` | No | Third-ranked component combination. |
| `rank_4` | `VARCHAR(64)` | No | Fourth-ranked component combination. |
| `rank_5` | `VARCHAR(64)` | No | Fifth-ranked component combination. |

---

### 1.4 `cleaned/cleaned_vehicle_listings.csv`
* **Role:** Standardized vehicle classified advertisements with duplicate detection flags.
* **Row Count:** 2,062 rows | **Primary Key:** `listing_id`

| Column Name | Data Type | Nullable | Description & Business Rules |
| :--- | :---: | :---: | :--- |
| `listing_id` | `VARCHAR(64)` | No | Unique listing identifier (e.g., `ADEY-CAR-1707668`). |
| `source_id` | `VARCHAR(32)` | No | Identifier of the source portal (`adey_market`, `gezat`, `cargebeya`, etc.). |
| `source_name` | `VARCHAR(64)` | No | Display name of the source marketplace. |
| `source_url` | `VARCHAR(255)` | No | Canonical web URL of the original advertisement. |
| `manufacturer` | `VARCHAR(32)` | No | Normalized vehicle make (`BYD`, `Toyota`, `Volkswagen`, `Changan`). |
| `vehicle_model` | `VARCHAR(32)` | No | Normalized model (`Seagull`, `bZ4X`, `ID.4`, `ID.4 Crozz`, `ID.6`, `Yuan Up`, etc.). |
| `model_year` | `INT` | Yes | Model year (parsed 4-digit year; null if omitted in classified title). |
| `trim_or_variant` | `VARCHAR(128)` | No | Extracted trim or package description. |
| `asking_price` | `FLOAT` | Yes | Asking price in ETB (bounded between 500,000 and 40,000,000; null if unlisted). |
| `currency` | `VARCHAR(3)` | No | Standard currency code (`ETB`). |
| `seller_name` | `VARCHAR(128)` | No | Extracted dealership or seller name. |
| `seller_location` | `VARCHAR(128)` | No | Dealership city/sub-city (`Addis Ababa, Ethiopia`). |
| `vehicle_condition` | `VARCHAR(16)` | No | Standardized condition: `New` (0km/አዲስ) or `Used`. |
| `listing_date` | `VARCHAR(10)` | No | Publication date normalized to `YYYY-MM-DD` or `YYYY-MM`. |
| `collection_timestamp` | `VARCHAR(32)` | No | ISO 8601 UTC timestamp of web extraction. |
| `listing_description` | `TEXT` | No | Cleaned listing title/summary text. |
| `original_listing_text` | `TEXT` | No | Raw unparsed listing description. |
| `image_reference` | `VARCHAR(255)` | Yes | Representative vehicle image URL if present. |
| `original_platform` | `VARCHAR(32)` | No | Originating platform (`Website`, `Telegram`, etc.). |
| `extraction_method` | `VARCHAR(32)` | No | Scraper method (`DOM_PARSER_PCARD_DEEP`, `HTML_TABLE`, etc.). |
| `duplicate_candidate` | `VARCHAR(3)` | No | Flag (`YES` / `NO`) indicating duplicate classified cross-post. |
| `verification_status` | `VARCHAR(32)` | No | Audit status (`PUBLIC_MARKETPLACE_LISTING`). |

---

### 1.5 `cleaned/cleaned_parts_records.csv`
* **Role:** Normalized parts catalogue records across all 3 target manufacturers.
* **Row Count:** 420 rows | **Primary Key:** `record_id`

| Column Name | Data Type | Nullable | Description & Business Rules |
| :--- | :---: | :---: | :--- |
| `record_id` | `VARCHAR(64)` | No | Unique record identifier (e.g., `TOYOTA-BZ4X-04465-42210`). |
| `source_id` | `VARCHAR(32)` | No | Source identifier (`toyota_catalogue`, `vw_catalogue`, `cqs`). |
| `vehicle_make` | `VARCHAR(32)` | No | Vehicle make (`BYD`, `Toyota`, `Volkswagen`). |
| `vehicle_model` | `VARCHAR(32)` | No | Vehicle model applicability (`Seagull`, `bZ4X`, `ID.4 / ID.6`). |
| `model_year` | `VARCHAR(32)` | No | Applicable model year range (`2022-2025`). |
| `trim_or_variant` | `VARCHAR(64)` | No | Drivetrain / trim applicability (`FWD`, `AWD`, `Standard Range`). |
| `part_category` | `VARCHAR(64)` | No | Standardized category from the 10 target categories. |
| `part_description` | `VARCHAR(255)` | No | Detailed component technical description. |
| `OEM_part_number` | `VARCHAR(64)` | No | Canonical manufacturer OEM part number string. |
| `supplier_part_number` | `VARCHAR(64)` | No | Secondary supplier SKU or assembly code if available. |
| `manufacturer` | `VARCHAR(64)` | No | Normalized manufacturer entity. |
| `catalogue_price` | `VARCHAR(32)` | Yes | List price in source catalog (if published). |
| `currency` | `VARCHAR(3)` | No | Source currency code (`USD`, `EUR`, `ETB`). |
| `stock_status` | `VARCHAR(32)` | No | Catalog stock status (`AVAILABLE_INTERNATIONAL`, etc.). |
| `supplier_name` | `VARCHAR(64)` | No | Publishing catalog or distributor entity name. |
| `fitment_description` | `TEXT` | No | Technical mounting, side, and position description. |
| `compatibility_reference` | `VARCHAR(128)`| No | Engineering platform reference (`e-Platform 3.0`, `MEB`, `e-TNGA`). |
| `source_url` | `VARCHAR(255)` | No | Source catalog web endpoint. |
| `collection_timestamp` | `VARCHAR(32)` | No | ISO 8601 UTC collection timestamp. |
| `original_text` | `TEXT` | No | Raw unparsed catalog table text. |
| `extraction_method` | `VARCHAR(32)` | No | Extraction method (`HTML_TABLE_EXTRACTION`, `EPC_MICRODATA`). |
| `verification_status` | `VARCHAR(32)` | No | Verification status (`CATALOGUE_VERIFIED`). |

---

## 2. Silver Tier: Standardized Datasets

### 2.1 `processed/vehicle_part_coverage.csv`
* **Role:** The foundational 30-combination coverage matrix ($3 \text{ vehicles} \times 10 \text{ part categories}$).
* **Row Count:** Exactly 30 rows | **Primary Key:** Composite (`vehicle_model`, `part_category`)

| Column Name | Data Type | Nullable | Description & Business Rules |
| :--- | :---: | :---: | :--- |
| `vehicle_model` | `VARCHAR(32)` | No | Selected vehicle model. |
| `part_category` | `VARCHAR(32)` | No | Component category. |
| `source_found` | `VARCHAR(3)` | No | `YES` if at least one data source references this pair. |
| `catalogue_record_found` | `VARCHAR(3)` | No | `YES` if an authentic catalog entry exists. |
| `OEM_number_found` | `VARCHAR(64)` | No | Verified OEM part number (`14758996-00`, etc.). |
| `compatibility_evidence_found` | `VARCHAR(3)` | No | `YES` if technical fitment evidence is verified. |
| `Ethiopian_supplier_found` | `VARCHAR(16)`| No | `YES` if local supplier stocks/services; `INQUIRY_REQUIRED` otherwise. |
| `local_price_found` | `VARCHAR(16)`| No | Quoted price in ETB if available; `INQUIRY_REQUIRED` otherwise. |
| `local_stock_found` | `VARCHAR(32)`| No | `CONFIRMED_IN_STOCK`, `AVAILABLE_ON_ORDER`, or `UNKNOWN`. |
| `quotation_found` | `VARCHAR(3)` | No | `YES` if a fixed commercial quotation is on file; `NO` otherwise. |
| `evidence_confidence` | `VARCHAR(16)`| No | Lineage confidence level: `HIGH`, `MEDIUM_HIGH`, `MEDIUM`, or `LOW`. |
| `missing_information` | `TEXT` | No | Explicit gap documentation (e.g. unlisted wholesale price). |
| `next_research_action` | `TEXT` | No | Operational mitigation step for procurement desk. |

---

### 2.2 `processed/vehicle_selection_evidence.csv`
* **Row Count:** 5 rows | **Primary Key:** `vehicle_model`
* Documents empirical market visibility and distributor presence for all 5 candidate models, providing formal evidence for Decision 1 (selecting BYD Seagull, VW ID.4/ID.6, Toyota bZ4X, and omitting BYD Yuan Up and Changan Benben E-Star).

### 2.3 `processed/import_logistics_tariffs.csv`
* **Row Count:** 10 rows | **Primary Key:** `part_category`
* Encodes the Ethiopian Customs Commission (ECC) HS 2022/2024 tariff schedule for all 10 component categories, including base Customs Duty, VAT (15%), Sur-tax (10%), Withholding Tax (3%), Excise Duty, and calculated Total Effective Fiscal Burden.

### 2.4 `processed/supplier_directory.csv`
* **Row Count:** 9 rows | **Primary Key:** `supplier_id`
* Profiles verified automotive dealerships and spare parts retailers in Addis Ababa (Inchcape BYD, MOENCO Toyota, Sunny Spare Parts, Armana Motors, Ethio EV Spare, Gezat Electric, etc.).

### 2.5 `processed/supplier_quotations.csv`
* **Row Count:** 4 rows | **Primary Key:** `quotation_id`
* Records verified public commercial price quotations in Ethiopian Birr (ETB) extracted from live retailer production bundles.

### 2.6 `processed/nhtsa_complaints.csv` & `nhtsa_recalls.csv`
* **Row Count:** 642 complaints & 28 recalls | **Primary Keys:** `complaint_id`, `recall_number`
* Records live safety defect investigations, crashes, fires, and recall notices from the US Department of Transportation / NHTSA for target vehicle platforms.

### 2.7 `processed/duplicate_candidates.csv`
* **Row Count:** 179 rows | **Primary Key:** `candidate_id`
* Logs duplicate vehicle listings detected across multiple classified portals, recording primary record IDs, matching record IDs, similarity scores (1.0), and resolution flags.

### 2.8 `processed/missing_evidence.csv`
* **Row Count:** 8 rows | **Primary Key:** `item_id`
* Formally documents real-world market data gaps (such as unlisted local retailer prices, lack of a national EV registry, and anti-bot verification challenges) along with recommended commercial mitigations.

### 2.9 `processed/source_accessibility.csv` & `source_log.csv`
* **Row Count:** 19 rows each | **Primary Key:** `source_id`
* Tracks HTTP status codes, latency benchmarks, provenance metadata, and extraction parameters for all 19 surveyed domestic and international data sources.

---

## 3. Fitment Evidence Taxonomy Specification

All compatibility claims across `fitment_evidence.csv` and `cleaned_parts_records.csv` are strictly evaluated against the 6-tier fitment hierarchy enforced by `src/validation/fitment_validator.py`:

```
                 [Direct Technical Documentation]
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
     VERIFIED_BY_OEM                       VIN_CONFIRMED
 (Direct OEM catalog part               (Matched against chassis
  number verified in EPC)                or VIN prefix, e.g. XEAM10)
            │
            ▼
 CATALOGUE_ASSOCIATION
 (Verified cross-reference
  in 3rd-party catalog)
            │
            ▼
    POSSIBLE_FITMENT
 (Supplier claim supported
  by matching dimensions)
            │
            ▼
       UNVERIFIED
 (Supplier claim without
  OEM part number)
            │
            ▼
       NOT_FOUND
 (No catalogue or supplier
  fitment evidence exists)
```

---

## 4. Ethiopian Customs Commission (ECC) Tariff Schedule Reference

The following fiscal schedules from the Ethiopian Customs Commission Tariff Book (HS 2022/2024 Version) are incorporated into the prioritization scoring engine:

$$\text{Effective Fiscal Burden} = (1 + \text{Duty}) \times (1 + \text{Excise}) \times (1 + \text{Sur-tax}) \times (1 + \text{VAT}) - 1$$

| Component Category | HS Code (ECC) | Base Duty | Excise | Sur-Tax | VAT | Withholding | Effective Fiscal Burden | Recommended Freight Mode |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Brake pads** | `8708.30.00` | 20% | 0% | 10% | 15% | 3% | **54.3%** | Air Freight Consolidation |
| **Brake discs** | `8708.30.00` | 20% | 0% | 10% | 15% | 3% | **54.3%** | LCL Sea Freight (Djibouti Corridor) |
| **Shock absorbers** | `8708.80.00` | 20% | 0% | 10% | 15% | 3% | **54.3%** | LCL Sea Freight (Djibouti Corridor) |
| **Cabin-air filters** | `8421.39.00` | 10% | 0% | 10% | 15% | 3% | **41.5%** | Air Freight Consolidation |
| **Wiper blades** | `8512.90.00` | 20% | 0% | 10% | 15% | 3% | **54.3%** | Air Freight Consolidation |
| **Side mirrors** | `7009.10.00` | 25% | 0% | 10% | 15% | 3% | **60.7%** | Air Freight Consolidation |
| **Headlights** | `8512.20.00` | 30% | 10% | 10% | 15% | 3% | **82.4%** | Air Freight (Fragile) |
| **Tail lights** | `8512.20.00` | 30% | 10% | 10% | 15% | 3% | **82.4%** | Air Freight (Fragile) |
| **Bumpers** | `8708.10.00` | 35% | 0% | 10% | 15% | 3% | **73.5%** | 40ft High-Cube Container Sea |
| **Fenders/panels** | `8708.29.00` | 35% | 0% | 10% | 15% | 3% | **73.5%** | 40ft High-Cube Container Sea |

