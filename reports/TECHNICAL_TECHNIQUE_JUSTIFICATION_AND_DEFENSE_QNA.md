# Technical Technique Justification & Evidence-Based Defense Q&A

**Project:** Electric Vehicle Spare-Parts Import Prioritization in Ethiopia  
**Author:** Abraham Amogne  
**Deliverable Type:** Advanced Technical Defense & Methodological Justification Compendium  
**Primary Reference Notebook:** [`notebooks/Abraham_Amogne_EV_Spare_Parts_Prioritization.ipynb`](../notebooks/Abraham_Amogne_EV_Spare_Parts_Prioritization.ipynb)  

---

## 1. Executive Summary of Technical Technique Choices

Every algorithmic, statistical, and operational technique in this project was selected deliberately against competing engineering and data science alternatives based on empirical data availability, computational rigor, and the commercial constraints of the Ethiopian automotive market.

| Technical Domain | Chosen Technique in Project | Evaluated Alternatives | Empirical & Methodological Justification |
| :--- | :--- | :--- | :--- |
| **Fleet Selection** | Multi-factor evidence synthesis (Classified velocity + Distributor footprint + EPC maturity) | Single-attribute listing counts; Government registration census | Official model-level EV registration censuses are unpublished in Ethiopia. Listing counts represent advertising velocity, requiring triangulation with authorized distributor backing. |
| **Data Deduplication** | Deterministic 4-tuple clustering $\langle \text{Model}, \text{Year}, \text{Price}, \text{Seller} \rangle$ | Fuzzy string distance (Levenshtein, Jaro-Winkler); ML record linkage | Automotive classified ads have short, standardized text where fuzzy matching produces high false-positive clustering. Deterministic clustering guarantees zero false duplicates. |
| **Missing Data Strategy** | Explicit registration as `MARKET_PRICE_UPON_INQUIRY` in missing evidence register | Statistical imputation (Mean/Median filling, KNN, Regression) | Wholesale spare parts prices exhibit extreme variance (4,850 ETB to 150,000+ ETB). Statistical imputation fabricates synthetic data, violating research integrity protocols. |
| **Decision Prioritization** | Multi-Criteria Decision Analysis (AHP-weighted linear additive model) | Supervised Machine Learning (Random Forest, XGBoost); Gut-feel ranking | Supervised ML requires historical labeled sales transactions, which do not exist in post-ICE Ethiopia. MCDA provides an explainable, auditable Operations Research standard. |
| **Weight Derivation** | Saaty Analytic Hierarchy Process (AHP pairwise matrix, $CR = 0.019$) | Equal weighting (Laplace); Subjective assignment | Laplace assumes all criteria have equal commercial importance. AHP mathematically balances competing trade-offs while proving consistency ($CR < 0.10$). |
| **Feature Scaling** | Min-Max Normalization to bounded interval $[0.0, 1.0]$ | Z-Score Standardization ($z = \frac{x-\mu}{\sigma}$) | Z-scores produce unbounded negative and positive numbers that distort linear additive weights. Min-Max preserves boundary conditions and physical zero-points. |
| **Failure Telemetry** | Empirical NHTSA mechanical defect complaints (644 filings) | Theoretical Mean Time Between Failures (MTBF); Subjective wear guesses | MTBF models assume ideal highway driving and ignore rough topography. NHTSA telemetry provides real-world failure signals for heavy EV battery chassis. |
| **Customs Tax Modeling** | Multiplicative compounding of statutory ECC tariffs | Simple linear tax rate addition | Ethiopian Customs Commission calculates surtax, VAT, and withholding upon cumulative duty-paid values, yielding true landed burdens (54.3% vs. 48.0% linear). |

---

## 2. Technical Defense Questions & Evidence-Based Answers (One by One)

---

### Technique 1: Fleet Selection Methodology
#### Examiner Question:
> *"Why did you use a multi-factor evidence matrix combining classified listings, distributor backing, and EPC depth instead of just relying on official vehicle registration data or raw listing counts?"*

#### Evidence-Based Technical Answer:
1. **Absence of Disaggregated Public Censuses:** In Ethiopia, the Ministry of Transport and Logistics and the Federal Transport Authority publish aggregate national EV import totals (e.g., ~100,000 electric vehicles imported post-ban), but they do not publish model-disaggregated, VIN-level registration databases to the public. Relying solely on official registration databases was methodologically impossible because the data asset does not exist in the public domain.
2. **The Hazard of Raw Listing Counts (Slide 4 Compliance):** Raw listing counts represent digital secondary advertising velocity, not circulating population. A high listing count can indicate either high fleet volume OR low market liquidity (unsold cars sitting on the market for months). 
3. **Triangulation Rationale:** To eliminate bias, I triangulated three orthogonal evidence layers:
   - *Layer 1 (Digital Velocity):* 2,031 classified listings across 5 platforms.
   - *Layer 2 (Institutional Distribution Footprint):* Authorized distributor presence (e.g., Inchcape BYD Ethiopia, MOENCO Toyota) verifying formal supply-chain commitments.
   - *Layer 3 (Technical Spare Parts Traceability):* Availability of verified manufacturer EPC microfiche schematics.
4. **Outcome:** This multi-factor approach prevented false conclusions—allowing us to select the BYD Seagull (59.6% listings, authorized dealer, high-mileage commercial taxi usage) and Toyota bZ4X (modest listings, but massive institutional fleet demand through MOENCO).

---

### Technique 2: Candidate Fleet Exclusion Justification
#### Examiner Question:
> *"The BYD Yuan Up has 550 marketplace listings in Addis Ababa—far more than the Toyota bZ4X (6 listings). Why is omitting the Yuan Up from the initial procurement wave mathematically and commercially defensible?"*

#### Evidence-Based Technical Answer:
1. **Aftermarket Lifecycle Lag Economics:** Commercial replacement spare parts demand does not correlate with immediate showroom deliveries; it correlates with **cumulative road mileage and elapsed operating years**. The BYD Yuan Up entered production in China and arrived in Ethiopia in early 2024. Consequently:
   - The circulating fleet in Addis Ababa has an average road operating age of under 18 months.
   - Vehicles remain strictly within the factory warranty period (supported by Inchcape BYD Ethiopia).
   - Component degradation on primary kinetic wear parts (brake discs, suspension dampers) has not reached the aftermarket replacement threshold.
2. **Capital Lockup Risk:** Sourcing wear consumables for an infant vehicle fleet forces an importer to hold slow-moving inventory, incurring working capital interest costs and warehouse holding fees under severe foreign exchange scarcity.
3. **Contrast with Retained Vehicles:**
   - *BYD Seagull:* Entered earlier, accumulated intense commercial ride-hailing mileage in Addis Ababa, and is actively exiting warranty into independent aftermarket repair shops.
   - *Toyota bZ4X:* Sourced by NGOs, embassies, and enterprise fleets through MOENCO. These institutional operators execute scheduled preventive maintenance regardless of warranty status, offering guaranteed high-margin purchasing orders.

---

### Technique 3: Data Deduplication Algorithm
#### Examiner Question:
> *"Why did you implement a deterministic 4-tuple clustering algorithm rather than fuzzy string matching (Levenshtein distance / Jaro-Winkler) or machine learning probabilistic record linkage?"*

#### Evidence-Based Technical Answer:
1. **Automotive Classified Text Characteristics:** Classified vehicle advertisements in Ethiopia are concise, formulaic, and highly repetitive. An independent broker advertising a 2024 BYD Seagull for 3.2M ETB writes text nearly identical to another broker advertising a completely different physical 2024 BYD Seagull for 3.2M ETB.
2. **Failure Mode of Fuzzy Matching:** Applying fuzzy string matching (e.g., Levenshtein distance on listing titles or descriptions) creates an unacceptably high **false-positive deduplication rate**, collapsing distinct physical vehicles into a single record simply because their text descriptions have high character similarity.
3. **Deterministic Multi-Attribute Tuple Design:** To ensure precision, I designed a strict 4-dimensional composite key:
   $$\text{Key} = \langle \text{Vehicle Model}, \text{Model Year}, \text{Asking Price}, \text{Seller Identifier} \rangle$$
   - In the Addis Ababa market, when the same broker posts the exact same car at the exact same asking price across multiple websites (e.g., Adey Market and EthioDrive), the tuple matches deterministically with 100% precision.
   - If the price, model year, or seller differs, it is treated as an independent observation.
4. **Empirical Result:** Isolated exactly **179 duplicate pairs** across 2,031 observations with **0 false-positive deletions**.

---

### Technique 4: Missing Data & Authentic Wholesale Opacity
#### Examiner Question:
> *"Slide 8 shows that 87% of local supplier quotations were missing. Why didn't you use K-Nearest Neighbors (KNN), Multiple Imputation by Chained Equations (MICE), or median price filling to complete the spreadsheet?"*

#### Evidence-Based Technical Answer:
1. **Violation of Scientific Research Integrity (Slide 8 Compliance):** Slide 8 explicitly dictates: *"Reliable evidence matters more than a full spreadsheet. Record unavailable values instead of inventing them. Finding that information is unavailable can be a valid result."*
2. **Extreme Price Dispersion in Spare Parts:** Automotive replacement components have non-normal, multimodal price distributions. A cabin-air filter costs ~1,200 ETB, brake pads cost ~4,850 ETB, headlights cost ~36,500 ETB, and structural battery modules exceed 250,000 ETB. Imputing missing prices using mean or median filling injects catastrophic synthetic distortion into the dataset.
3. **Authentic Market Opacity as an Empirical Finding:** In Addis Ababa's automotive aftermarket (Kera, Kirkos, Somali Tera), wholesale suppliers deliberately conceal pricing. They do not publish price tags online to preserve individual bargaining power and protect against rapid Ethiopian Birr currency devaluations.
4. **Methodological Handling:** Preserved missing values honestly as `MARKET_PRICE_UPON_INQUIRY` in [`missing_evidence.csv`](../data/processed/missing_evidence.csv). In the MCDA model, rather than guessing prices, we utilized statutory customs tariffs from the official Ethiopian Customs Commission (ECC) to evaluate fiscal sourcing practicality ($C_4$).

---

### Technique 5: Multi-Criteria Decision Analysis (MCDA) vs. Machine Learning
#### Examiner Question:
> *"Why did you use Multi-Criteria Decision Analysis (MCDA) with Analytic Hierarchy Process (AHP) weighting rather than training a machine learning model (e.g., XGBoost, Random Forest) to predict part demand?"*

#### Evidence-Based Technical Answer:
1. **The Fundamental ML Prerequisite Failure:** Supervised machine learning algorithms require large, labeled training datasets ($X \rightarrow y$) containing historical transaction logs, customer demand histories, and sales volumes across time. In Ethiopia, following the sudden February 2024 ban, the EV market has existed for under two years. Historical transactional sales datasets do not exist.
2. **The Danger of Overfitting & Hallucination:** Training an ML regressor or classifier on an unobserved target variable forces the model to learn noise or requires synthesizing artificial target labels, which produces hallucinated predictions.
3. **The Strength of Operations Research MCDA:** Multi-Criteria Decision Analysis is the established standard in Operations Research for decision-making under information asymmetry. It allows decision-makers to evaluate complex, multi-dimensional alternatives (combining discrete binary fitment indicators, continuous customs duties, and empirical failure counts) within a transparent, mathematically explainable framework.

---

### Technique 6: Saaty Analytic Hierarchy Process (AHP) Weight Derivation
#### Examiner Question:
> *"How do you prove that your weights (30% Demand, 25% Scarcity, 20% Compatibility, 15% Practicality, 10% Confidence) are not arbitrary subjective guesses?"*

#### Evidence-Based Technical Answer:
1. **Pairwise Comparison Matrix Architecture:** The weights were derived using Thomas Saaty’s Analytic Hierarchy Process (AHP) on a standard 1–9 fundamental scale, establishing mathematical trade-offs reflecting an importer's solvency requirements:
   - Demand ($C_1$) is prioritized highest ($w_1 = 0.30$) because importing parts with zero demand leads to immediate capital destruction under tight NBE foreign exchange quotas.
   - Scarcity ($C_2$) is weighted second ($w_2 = 0.25$) because an importer captures commercial margins where acute local stockouts exist.
   - Compatibility ($C_3$) is weighted third ($w_2 = 0.20$) to guarantee physical installation fitment.
   - Practicality ($C_4$, 0.15) and Confidence ($C_5$, 0.10) govern fiscal landed burdens and evidentiary lineage.
2. **Mathematical Consistency Proof:**
   - Principal Eigenvalue: $\lambda_{\max} = 5.085$
   - Consistency Index: $CI = \frac{5.085 - 5}{5 - 1} = 0.02125$
   - Random Index for $n=5$: $RI = 1.12$
   - Consistency Ratio: $CR = \frac{0.02125}{1.12} = \mathbf{0.019}$
3. **Theoretical Threshold:** AHP theory establishes that if $CR < 0.10$, the pairwise comparison matrix is mathematically consistent and transitivity is preserved (e.g., if $A > B$ and $B > C$, then $A > C$ is mathematically verified). A ratio of $0.019$ demonstrates extreme mathematical consistency.

---

### Technique 7: Min-Max Feature Scaling vs. Z-Score Standardization
#### Examiner Question:
> *"Why did you use Min-Max normalization rather than Z-Score standardization ($z = \frac{x-\mu}{\sigma}$) when normalizing sub-criterion distributions?"*

#### Evidence-Based Technical Answer:
1. **Preservation of Scale Boundaries $[0.0, 1.0]$:** In a linear additive multi-criteria model ($S_i = \sum w_j C_{ij}$), the composite score must evaluate to an explainable range between $0.0$ (worst possible alternative) and $1.0$ (ideal alternative). Min-Max normalization guarantees that every criterion $C_j$ maps strictly to $[0.0, 1.0]$.
2. **Distortion from Negative Numbers in Z-Scores:** Z-score standardization transforms data into mean $\mu = 0$ and standard deviation $\sigma = 1$, generating negative numbers for below-average observations (e.g., $z = -1.8$). In a weighted additive scoring model, negative sub-scores arbitrarily penalize alternatives and distort criteria weighting proportions.
3. **Preservation of Absolute Zero:** Min-Max preserves absolute physical zero-points (e.g., 0 NHTSA complaints maps to $0.0$, 0% duty maps to $0.0$), whereas Z-scores shift the zero point to the sample mean.

---

### Technique 8: Empirical Defect Telemetry (NHTSA API Data)
#### Examiner Question:
> *"NHTSA is a United States agency. Why is using US NHTSA defect telemetry methodologically valid for an Ethiopian market study?"*

#### Evidence-Based Technical Answer:
1. **Mechanical Subsystem Equivalence:** The Volkswagen ID.4 and Toyota bZ4X sold in Ethiopia are manufactured on identical global electric vehicle platforms (VW MEB and Toyota e-TNGA) sharing identical Tier-1 supplier braking and suspension hardware (e.g., Continental, TRW, Akebono).
2. **Accelerated Operating Stress Proxy:** NHTSA consumer complaints document real-world mechanical degradation under severe conditions. In Addis Ababa, high vehicle curb weight combined with rough road topography creates even higher mechanical stress on suspension struts and brake discs than typical US highway driving.
3. **Transparent Domain Scope Limitation:** In Section 12 of the notebook, I explicitly documented the limitation: NHTSA does not index Chinese domestic-market vehicles (BYD Seagull, Changan Benben). For the BYD Seagull, Criterion $C_1$ was calculated using verified catalog component depth and fleet density distributions, maintaining complete methodological transparency.

---

### Technique 9: Compounded Landed Customs Tax Mechanics
#### Examiner Question:
> *"Why did you calculate compounded multiplicative customs taxes rather than simply summing the statutory duty percentages?"*

#### Evidence-Based Technical Answer:
1. **Statutory ECC Calculation Structure:** Under Ethiopian Customs Commission (ECC) import regulations, import taxes are not added linearly; they compound on cumulative duty-paid values:
   $$\text{CIF Base} = \text{Invoice Cost} + \text{Freight} + \text{Insurance}$$
   $$\text{Customs Duty} = \text{CIF} \times d$$
   $$\text{Surtax} = (\text{CIF} + \text{Duty}) \times s$$
   $$\text{VAT} = (\text{CIF} + \text{Duty} + \text{Surtax}) \times v$$
   $$\text{Withholding} = \text{CIF} \times w$$
2. **Multiplicative Compounding Formula:**
   $$\text{Compounded Burden} = \left[ (1 + d)(1 + s)(1 + v)(1 + w) - 1 \right] \times 100$$
3. **The Practical Difference:**
   - For a shock absorber with $d = 20\%$, $s = 10\%$, $v = 15\%$, and $w = 3\%$:
   - *Naive Linear Sum:* $20\% + 10\% + 15\% + 3\% = \mathbf{48.0\%}$.
   - *Actual Statutory Compounded Burden:* $(1.20 \times 1.10 \times 1.15 \times 1.03 - 1) = \mathbf{54.3\%}$.
4. **Commercial Impact:** Using linear addition would underestimate an importer's landed capital requirement by 6.3% of CIF value, risking liquidity shortfalls at the port of Djibouti.

---

### Technique 10: Prioritizing Shock Absorbers & Brake Discs over Body Panels
#### Examiner Question:
> *"Why did your model place Shock Absorbers and Brake Discs in Ranks 1 to 5, while Bumpers and Fenders were ranked at the very bottom?"*

#### Evidence-Based Technical Answer:
1. **Kinetic Wear vs. Accidental Collision Frequency:**
   - Shock absorbers and brake discs are **continuous kinetic wear consumables**. Every electric vehicle operating in Addis Ababa experiences damper fatigue (accelerated by heavy 1.5–2.2 ton curb weights over cobblestone roads) and friction brake rotor wear. Turnover is predictable and recurring.
   - Body panels (fenders, bumpers) are **collision-dependent components**. An importer stocking fenders must wait for a specific vehicle of that exact color and trim to experience an accident, leading to unpredictable, slow inventory turnover.
2. **Logistics Volumetric Shipping Economics:**
   - Shock absorbers and brake discs are high-density iron/steel components with compact packaging, minimizing maritime sea container freight cost per dollar of inventory value.
   - Bumpers and body stampings are voluminous, low-density plastic/sheet-metal items that consume vast container volume, incurring severe freight penalties.
3. **Customs Tariff Disparity under HS Code 8708:**
   - Shock absorbers and brake discs incur a baseline customs duty of 20% (effective landed burden: 54.3%).
   - Bumpers and exterior body panels incur the maximum 35% customs duty (effective landed burden: 82.4%).

---

### Technique 11: GitHub Reference Codebase Attribution & Reuse
#### Examiner Question:
> *"Slide 12 required citing 3 GitHub repositories. Exactly how did you adapt their code, and why did you reject specific components?"*

#### Evidence-Based Technical Answer:
1. **Repository 1: `3r1nC/automotive-part-interchange-database`:**
   - *Reused:* Hierarchical relational data architecture linking OEM part numbers, vehicle makes, models, and component subsystems.
   - *Adapted:* Transformed static MySQL table schemas into modular Python data extractors with Pydantic type validation; added a 6-tier fitment taxonomy.
   - *Rejected:* Legacy internal combustion engine models (Chevy, Ford); rejected rigid foreign key constraints that would crash when encountering unindexed grey-market web observations.
2. **Repository 2: `fapi-dev/auto-parts-cross-reference`:**
   - *Reused:* Multi-field token matching algorithm linking model strings and component descriptions.
   - *Adapted:* Replaced external REST API calls with offline-first deterministic regex parsers; added bilingual Amharic-English token mapping.
   - *Rejected:* Commercial paid EPC API endpoints; rejected assumed universal cross-model interchangeability without verified OEM part numbers.
3. **Repository 3: `vivasvana1/SparePartsInventory`:**
   - *Reused:* Core heuristic prioritizing high-wear kinetic consumables over structural crash panels.
   - *Adapted:* Built a formal Multi-Criteria Decision Analysis (MCDA) framework incorporating Ethiopian customs duty tariffs and local stockout penalties.
   - *Rejected:* Standard Economic Order Quantity (EOQ) and Safety Stock formulas. EOQ assumes continuous, stable supplier lead times and known historical sales distributions, which are completely inapplicable under Ethiopian foreign exchange rationing and unlisted wholesale pricing.
