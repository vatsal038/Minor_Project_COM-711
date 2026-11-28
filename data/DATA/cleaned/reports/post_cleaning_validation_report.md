# Post-Cleaning Data Validation & Reconciliation Report
**Project**: COM-711 — AI-Based Property Buy-Worthiness Assessment and Value Forecasting  
**Author**: Data Engineering & ML Preprocessing Team  
**Date**: November 28, 2026  
**Status**: Formal Validation Completed (Pre-Model Training Audit)

---

## 1. Executive Summary & Definitive Verdict

A rigorous, independent post-cleaning audit was performed on all datasets produced under `data/DATA/cleaned/`. Every source listing from Housing.com and Magicbricks across Buy, Commercial, and Rental categories has been traced, validated, and reconciled.

### Definitive Verdict

| Evaluation Dimension | Status | Summary Verdict |
|---|:---:|---|
| **Dataset Correctness** | **PASS** | Schema compatibility, field naming, and derived metrics (`price_inr`, `area_sqft_clean`, `price_per_sqft`, `area_marla`, `price_per_marla`) are 100% verified. Zero formula errors. |
| **Record Accounting** | **100% RECONCILED** | All 965 original source records map to exactly one mutually exclusive disposition: 687 CLEANED, 204 REMOVED, 63 REVIEW, 11 SEPARATED. The previous 114 vs 115 and 965 vs 966 discrepancies are completely resolved. |
| **Geographic Filtering** | **ZERO LEAKS** | Confirmed Samba District (Bari Brahmana, Vijaypur, Purmandal, Saror, Meen Sarkar), Udhampur District, and Reasi District listings have been fully eliminated from Jammu training data. All 63 ambiguous locality records remain in review. |
| **Numerical Integrity** | **PASS** | 0 null prices, 0 negative or zero prices, 0 null areas. Unit conversions ($1\text{ Marla} = 225\text{ sq.ft}$, $1\text{ sq.yd} = 9\text{ sq.ft}$) verified. |
| **Combined Datasets** | **EXACT MATCH** | `residential_combined_cleaned.json` (194 rows) and `commercial_combined_cleaned.json` (201 rows) represent exact, verified unions without omission or duplicate contamination. |
| **ML Baseline Readiness** | **CONDITIONALLY READY** | The 194-record residential dataset is clean and non-leaking, ready for a **preliminary proof-of-concept / baseline model**. However, **it is NOT sufficient for a generalizable production engine without incorporating 99acres (393 records)** due to high locality sparsity. |

---

## 2. Root-Cause Investigation & Resolution of Discrepancies

### The Identified Discrepancy
The previous cleaning summary reported:
- **Housing Buy**: Input = 114 records, but the column categories summed to $94 + 5 + 1 + 0 + 1 + 11 + 3 = 115$.
- **Grand Total**: Input = 965 records, but the column categories summed to $687 + 35 + 11 + 132 + 26 + 11 + 64 = 966$.

### Root Cause Analysis
During source code inspection of [`scripts/clean_housing_magicbricks.py`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/scripts/clean_housing_magicbricks.py) (lines 425–430):
```python
if area_flag_or_reason:
    flagged_review += 1
    dq = dict(item)
    dq['quality_flag'] = area_flag_or_reason
    review_data_quality.append(dq)
# ... script continued and appended item to file_candidates -> final_retained!
```
**Listing ID `15671868`** (*Residential Plot in Channi Himmat*, display `"600 sq.yd"`, stored `"600.0"` sq.ft):
1. Was correctly converted to physical ground truth (**5,400 sq.ft / 24 Marlas**).
2. Was flagged in `data_quality_review.json` as an advisory verification artifact.
3. **Double-Counting Mechanism**: The script incremented `flagged_review (+1)` AND ALSO retained the record in `housing_residential_cleaned.json`, incrementing `final_retained (+1)`.
4. Therefore, when summing across the report table columns, Listing `15671868` was counted twice (once in `flagged_review` and once in `final_retained`).

### Resolution & Mutually Exclusive Disposition
To enforce the principle that *every source record must have exactly one final disposition*:
- Listing `15671868` has primary disposition **CLEANED** (retained in training set with verified 5,400 sq.ft; audited in data quality review).
- The 2 records in `review/geographic_review.json` (*Sedhar* and *Rohi*) have primary disposition **REVIEW**.
- Under this mutually exclusive partition, the math reconciles with 100% precision:
  $$\text{Housing Buy: } 94\text{ Cleaned} + 7\text{ Removed} + 2\text{ Review} + 11\text{ Separated} = 114$$
  $$\text{Grand Total: } 687\text{ Cleaned} + 204\text{ Removed} + 63\text{ Review} + 11\text{ Separated} = 965$$

---

## 3. Official Record Reconciliation Matrix

All 965 records across the 6 processed source files map into the master [`record_reconciliation.csv`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/record_reconciliation.csv):

| Portal | Category | Source File | CLEANED | REMOVED | REVIEW | SEPARATED | TOTAL |
|---|---|---|---:|---:|---:|---:|---:|
| Housing | Buy | `housing/buy_properties_filtered.json` | 94 | 7 | 2 | 11 | **114** |
| Housing | Commercial | `housing/commercial_properties_filtered.json` | 160 | 34 | 12 | 0 | **206** |
| Housing | Rental | `housing/rent_properties_filtered.json` | 167 | 118 | 8 | 0 | **293** |
| Magicbricks | Buy | `magicbricks/buy_properties_filtered.json` | 100 | 29 | 25 | 0 | **154** |
| Magicbricks | Commercial | `magicbricks/commercial_properties_filtered.json` | 41 | 2 | 3 | 0 | **46** |
| Magicbricks | Rental | `magicbricks/rent_properties_filtered.json` | 125 | 14 | 13 | 0 | **152** |
| **TOTAL** | — | — | **687** | **204** | **63** | **11** | **965** |

### Breakdown of the 204 REMOVED Records:
1. **Confirmed Outside Jammu District (35 records)**:
   - Samba District: Bari Brahmana, Lupin Factories, SIDCO, Vijaypur, Purmandal, Meen Sarkar, Saror, Swankha.
   - Udhampur District: Omala, Udhampur Town, Kaller Himmat, Nagrota (Udhampur).
2. **Missing / Zero Numerical Price (11 records)**:
   - Magicbricks "₹Call for Price" and Housing "Price on Request" without usable values.
3. **Missing / Unusable / Physically Implausible Area (132 records)**:
   - 105 Housing Rental records with null area.
   - 18 Magicbricks Buy records with null area or unresolved fundamental inconsistencies ($< 50\text{ sq.ft}$ for multi-room houses).
   - 7 Magicbricks Rental and 2 Magicbricks Commercial records with missing area.
4. **Duplicate Scrapes Removed (26 records)**:
   - 24 Housing Commercial duplicate listings (consecutive listing IDs with identical coordinates, price, area, and titles).
   - 1 Housing Buy duplicate and 1 Magicbricks Rental duplicate.

---

## 4. Geographic Filtering & Boundary Validation

An automated regex scan across all 194 residential and 201 commercial records confirmed:
- **Zero Outside Leaks**: No records from Samba District, Udhampur District, Reasi District, Kathua District, Rajouri District, or Doda District exist in the cleaned datasets.
- **Border Zone Review**: Localities near the Jammu–Samba border (e.g., Kaluchak, Kunjwani, Satwari) were verified.
- **Neighborhood Normalization Integrity**: Normalization mapped alternative spellings without erroneously merging distinct neighborhoods (*Bagh-e-Bahu*, *Bahu Plaza*, *Channi Himmat*, *Channi Rama*, *Gandhi Nagar*, *Nanak Nagar*, *Trikuta Nagar* remain strictly separate).
- **Ambiguous Records**: 63 records lacking specific colony identifiers remain quarantined in `review/geographic_review.json`.

---

## 5. Numerical Field & Physical Unit Validation

Every record in `residential_combined_cleaned.json` and `commercial_combined_cleaned.json` was verified:
1. `price_inr > 0`: 100% compliant (0 nulls, 0 zeros).
2. `area_sqft_clean > 0`: 100% compliant (0 nulls, 0 zeros).
3. `price_per_sqft == price_inr / area_sqft_clean`: 100% compliant (0 formula mismatches).
4. `area_in_marla == area_sqft_clean / 225.0`: 100% compliant.
5. `price_per_marla == price_inr / area_in_marla`: 100% compliant.

### Outlier Audit (4 Flagged Listings in Residential Combined)
Outliers are flagged with `data_quality_flag = "outlier_review"` in `review/outlier_review.json` but preserved in the training dataset per specification:
1. **ID `15671868` (Housing, Channi Himmat)**: ₹3,50,000 for 5,400 sq.ft (₹64.8/sq.ft) — plot with verified converted sq.ft; extreme low valuation per sqft.
2. **ID `85069003` (Magicbricks, Akhnoor Road)**: ₹26,00,00,000 for 3,350 sq.ft (₹77,611.9/sq.ft) — high-value luxury estate.
3. **ID `81161389` (Magicbricks, Roop Nagar)**: ₹1,50,00,000 for 300 sq.ft (₹50,000.0/sq.ft) — high density commercial-residential plot.
4. **ID `84619627` (Magicbricks, Gorkha Nagar)**: ₹1,70,00,000 for 111 sq.ft (₹1,53,153.2/sq.ft) — suspected unit error in raw listing (111 sq.yd or Marlas entered as sqft).

---

## 6. Combined Datasets Union & Schema Compatibility

- **Residential Union**:
  - `housing_residential_cleaned.json`: 94 records
  - `magicbricks_residential_cleaned.json`: 100 records
  - Cross-portal deduplication: 0 collisions
  - `residential_combined_cleaned.json`: Exactly **194 records** ($94 + 100$).
- **Commercial Union**:
  - `housing_commercial_cleaned.json`: 160 records
  - `magicbricks_commercial_cleaned.json`: 41 records
  - `commercial_combined_cleaned.json`: Exactly **201 records** ($160 + 41$).
- **Dual-Schema Design**: Both portals retain original scraped nested structures (`price`, `area`, `address`, `configuration`, `amenities`) while supplying standardized flat attributes (`price_inr`, `area_sqft_clean`, `locality_clean`, `source_portal`, `property_category`, `data_quality_flag`).

---

## 7. Machine-Learning Readiness Assessment

### Residential Dataset Profile (194 Usable Listings)
* **Target Feature Integrity**: 100% complete (`price_inr`, `area_sqft_clean`).
* **Price Distribution**: Median = ₹99.65 Lakhs, Mean = ₹1.63 Crores, Max = ₹26 Crores (Skewness = 6.47).
* **Area Distribution**: Median = 1,905 sq.ft (8.5 Marlas), Mean = 2,448 sq.ft (10.9 Marlas), Max = 19,057 sq.ft (Skewness = 3.66).
* **Price per Sq.Ft**: Median = ₹5,667 / sq.ft, Mean = ₹8,216 / sq.ft (Skewness = 8.47).
* **Locality Sparsity Challenge**:
  - Total unique canonical localities represented: **58**.
  - Top 5 localities (*Trikuta Nagar, Sainik Colony, Sidhra, Sunjwan, Channi Himmat*) account for **26.3%** of data.
  - **18 localities have only 1 listing (31.0%)**.
  - **36 localities have $\le 3$ listings (62.1%)**.

### Critical Modeling Insights & Caveats
1. **Baseline Proof-of-Concept Suitability**: 
   The 194-record dataset is sufficient to construct an initial **cross-validated baseline pipeline** (e.g. Ridge Regression, shallow Decision Tree / Random Forest with `max_depth=3`, or regularized XGBoost with log-transformed price and area).
2. **Generalizability Limitation**: 
   194 records are **statistically insufficient** for training a complex, multi-feature production valuation model across 58 Jammu localities. With 5-fold cross-validation (~155 training rows, ~39 test rows per fold), high-cardinality locality target encoding will suffer from severe variance and out-of-fold overfitting.
3. **Mandatory Log Transformations**: 
   Due to significant skewness ($6.47$ for price, $3.66$ for area), models predicting raw price will be biased toward extreme luxury outliers (e.g., ₹26 Cr). Training on $\log(\text{price})$ and $\log(\text{area})$ is mandatory.
4. **Target Leakage Strict Rule**: 
   `price_per_sqft` and `price_per_marla` are derived directly from the target `price_inr`. They must never be included as input features in regression models predicting property value.

---

## 8. Required Additional Data & Roadmap to Model Training

To achieve an industrial-grade, generalizable valuation model for Project COM-711:

1. **Ingest 99acres Residential Listings**:
   - `data/DATA/99acres/buy_properties_filtered.json` contains **393 scraped residential records**.
   - Processing 99acres with this exact cleaning pipeline will add ~350+ clean records, increasing sample size to **~550+ residential listings** and eliminating locality sparsity across major Jammu neighborhoods.
2. **Fuse Static Civic & Administrative Benchmarks**:
   - Merge statutory Circle Rates from [`revenue_circle_rates_structured.csv`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/data/processed/revenue_circle_rates_structured.csv) to provide an authoritative per-locality price baseline.
   - Merge municipal indicators from [`jmc_civic_structured.csv`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/data/processed/jmc_civic_structured.csv) and flood risks from [`sdma_flood_zones_jammu.csv`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/data/processed/sdma_flood_zones_jammu.csv).
3. **Feature Preprocessing Pipeline**:
   - Impute missing bathroom counts on plot properties with 0.
   - Group rare localities ($< 3$ listings) into a categorical `"Other_Jammu"` bin or cluster them by geographic sub-tehsil.

---

## 9. Deliverables Inventory

The validation artifacts generated by this audit:
* [`record_reconciliation.csv`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/record_reconciliation.csv) (Root) & [`data/DATA/cleaned/reports/record_reconciliation.csv`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/data/DATA/cleaned/reports/record_reconciliation.csv): Row-by-row audit of all 965 source listings.
* [`post_cleaning_validation_summary.json`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/post_cleaning_validation_summary.json) (Root) & [`data/DATA/cleaned/reports/post_cleaning_validation_summary.json`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/data/DATA/cleaned/reports/post_cleaning_validation_summary.json): Machine-readable audit metrics.
* [`post_cleaning_validation_report.md`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/post_cleaning_validation_report.md) (Root) & [`data/DATA/cleaned/reports/post_cleaning_validation_report.md`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/data/DATA/cleaned/reports/post_cleaning_validation_report.md): Technical validation document.
