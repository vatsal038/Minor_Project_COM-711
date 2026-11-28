# Real Estate Data Cleaning Report — Housing.com & Magicbricks
**Project: COM-711 — AI-Based Property Buy-Worthiness Assessment and Value Forecasting**  
**Geographic Scope: Jammu District, Jammu and Kashmir, India**  
**Execution Date: November 2026**  
**Author: Data Engineering & Machine Learning Preprocessing Pipeline**

---

## 1. Executive Summary

This report documents the rigorous, auditable data engineering and preprocessing pipeline executed across **Housing.com** and **Magicbricks** real-estate listing datasets stored under `data/DATA/`.

The cleaning pipeline satisfies all core requirements established for Project COM-711:
1. **Conservative Retention Policy**: Preserves all valid property records with missing optional attributes (furnishing, age, amenities, parking, balconies, etc.), while eliminating fundamentally unusable rows (missing price, invalid/zero area, outside-district properties).
2. **Strict Administrative Geography**: Enforces Jammu District boundaries by removing properties confirmed in Samba District (Bari Brahmana, Vijaypur, Purmandal, Saror, Meen Sarkar), Udhampur District (Omala, Udhampur Town, Kaller Himmat), and Reasi District (Katra). Records with ambiguous locality context are preserved in a separate review dataset without polluting model training.
3. **Physical & Unit Integrity**: Corrected unit conversion errors (including sq.yd to sq.ft and detected suspected Marla-sqft input inversions). Derived verified price-per-square-foot and price-per-marla metrics following the Jammu regional convention ($1\text{ Marla} = 225\text{ sq.ft}$, $1\text{ sq.yd} = 9\text{ sq.ft}$).
4. **Logical Dataset Separation**: Kept residential sales, commercial sales, rental properties, and project-level developments in distinct, purpose-specific datasets.
5. **Traceability**: All original scraped fields and structures are preserved alongside normalized attributes.

---

## 2. Before-and-After Processing Metrics Table

### 2.1 Mutually Exclusive Final Disposition Table
Every source record has exactly one final disposition, ensuring 100% mathematical reconciliation:

| Source File | Portal | Category | CLEANED | REMOVED | REVIEW | SEPARATED | TOTAL |
|---|---|---|---:|---:|---:|---:|---:|
| `buy_properties_filtered.json` | Housing | Buy | 94 | 7 | 2 | 11 | **114** |
| `commercial_properties_filtered.json` | Housing | Commercial | 160 | 34 | 12 | 0 | **206** |
| `rent_properties_filtered.json` | Housing | Rental | 167 | 118 | 8 | 0 | **293** |
| `buy_properties_filtered.json` | Magicbricks | Buy | 100 | 29 | 25 | 0 | **154** |
| `commercial_properties_filtered.json` | Magicbricks | Commercial | 41 | 2 | 3 | 0 | **46** |
| `rent_properties_filtered.json` | Magicbricks | Rental | 125 | 14 | 13 | 0 | **152** |
| **TOTAL** | — | — | **687** | **204** | **63** | **11** | **965** |

*Note on Listing ID `15671868`*: Plot ID `15671868` (Channi Himmat, display 600 sq.yd, stored 600 sq.ft) is standardized to 5,400 sq.ft and counted under **CLEANED** (94) with an advisory quality flag. An audit copy is also kept in `review/data_quality_review.json`. The 2 records in REVIEW for Housing Buy are geographic reviews (*Sedhar* and *Rohi*).

### 2.2 Step-by-Step Pipeline Filter Progression
The table below details the step-by-step filter progression:

| Source File | Portal | Category | Input Records | Confirmed Jammu | Outside Jammu Removed | Missing/Invalid Price Removed | Missing/Invalid Area Removed | Duplicate Removed | Projects Separated | Flagged for Review | Final Retained |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `buy_properties_filtered.json` | Housing | Buy | 114 | 96 | 5 | 1 | 0 | 1 | 11 | 3 | **94** |
| `commercial_properties_filtered.json` | Housing | Commercial | 206 | 184 | 10 | 0 | 0 | 24 | 0 | 12 | **160** |
| `rent_properties_filtered.json` | Housing | Rent | 293 | 272 | 13 | 0 | 105 | 0 | 0 | 8 | **167** |
| `buy_properties_filtered.json` | Magicbricks | Buy | 154 | 127 | 2 | 9 | 18 | 0 | 0 | 25 | **100** |
| `commercial_properties_filtered.json` | Magicbricks | Commercial | 46 | 43 | 0 | 0 | 2 | 0 | 0 | 3 | **41** |
| `rent_properties_filtered.json` | Magicbricks | Rent | 152 | 134 | 5 | 1 | 7 | 1 | 0 | 13 | **125** |
| **TOTAL** | — | — | **965** | **856** | **35** | **11** | **132** | **26** | **11** | **64** | **687** |

---

## 3. Dataset Distribution & Output Structure

The cleaned datasets are saved under `data/DATA/cleaned/` with strict logical decoupling:

```text
data/DATA/cleaned/
├── residential/
│   ├── housing_residential_cleaned.json         # 94 records (Cleaned Housing.com residential sales)
│   ├── magicbricks_residential_cleaned.json     # 100 records (Cleaned Magicbricks residential sales)
│   └── residential_combined_cleaned.json        # 194 records (Combined de-duplicated residential sale dataset)
│
├── commercial/
│   ├── housing_commercial_cleaned.json          # 160 records (Cleaned Housing.com commercial properties)
│   ├── magicbricks_commercial_cleaned.json      # 41 records (Cleaned Magicbricks commercial properties)
│   └── commercial_combined_cleaned.json         # 201 records (Combined commercial property dataset)
│
├── rental/
│   └── rental_cleaned_separate.json             # 292 records (Cleaned rental listings kept separate from sale model)
│
├── projects/
│   └── project_listings_separate.json           # 11 records (Multi-unit developer marketing listings & price ranges)
│
├── review/
│   ├── geographic_review.json                   # 63 records (Ambiguous localities requiring human geographic verification)
│   ├── outlier_review.json                      # 4 records (Statistical outliers flagged but preserved)
│   └── data_quality_review.json                 # 1 records (Unit conversion / display discrepancies)
│
├── removed/
│   ├── removed_records.json                     # 178 records (Out-of-district, missing price, invalid area)
│   └── duplicate_records.json                   # 26 records (Internal portal and cross-portal duplicates)
│
└── reports/
    ├── cleaning_report.md                       # Complete technical Markdown report
    ├── cleaning_summary.json                    # Machine-readable JSON summary
    └── locality_summary.csv                     # Canonical locality-wise property counts and price stats
```

---

## 4. Key Data Engineering Interventions

### 4.1 Geographic Boundary Enforcement
- **Confirmed Non-Jammu Removals**: 
  - Properties in **Bari Brahmana** (including SIDCO, Lupin Factories, and Anand Vihar in Bari Brahmana) were removed because Bari Brahmana is in **Samba District**.
  - Properties in **Vijaypur**, **Purmandal**, **Meen Sarkar**, **Saror**, and **Swankha** were confirmed in **Samba District** and removed.
  - Properties in **Omala**, **Udhampur Town**, and **Kaller Himmat** were confirmed in **Udhampur District** and removed.
  - Listing `21138422` (labeled city `Jammu` but with address `Nagrota, Udhampur` and coordinates $32.87^\circ\text{N}, 75.10^\circ\text{E}$) was confirmed in Udhampur District and removed.
- **Ambiguous Geographic Isolation**:
  - 54 listings in Magicbricks had empty locality strings (`""`) and generic text (`"Jammu, Jammu & Kashmir"`). Where sub-colony text (e.g. *Bathindi*, *Nagrota/IIT*, *Sidhra*, *Satwari/Airport*) could be reliably extracted from the address line, it was normalized into `locality_clean`. Where no sub-locality existed, the record was moved to `geographic_review.json` to prevent geographic noise.

### 4.2 Physical Area & Unit Standardization
- **Square Yard Conversion**: Listing ID `15671868` (*Residential Plot in Channi Himmat*) reported display area `600 sq.yd` while structured numeric area had stored `600.0` (sq.ft). The area was converted to its true physical dimension of **5,400 sq.ft (24 Marlas)**, and the record was flagged in `data_quality_review.json`.
- **Suspected Marla Input Detection**: In Magicbricks, multiple houses (e.g. 10BHK, 4BHK) reported areas such as `10 sq.ft`, `11 sq.ft`, `14 sq.ft`, `5 sq.ft`. These represent sellers typing Marla counts into square-foot fields. Where raw data contained `coveredArea` (e.g. ID `86249341` with `coveredArea=3500`), the true area was recovered; unresolved listings were removed from individual training into `removed_records.json` with reason `fundamental_area_inconsistency`.

### 4.3 Multi-Unit Project Separation
- 11 builder development listings in Housing.com (e.g., *Horizon Concept River Castle*, *Parsvnath Passion*, *Ansal Grace*, *Adarsh Royal Palms*) containing price ranges (e.g., `₹70.01 L - 1.27 Cr`) or unpriced marketing entries (`"Price on Request"`) were quarantined into `project_listings_separate.json`.

### 4.4 Duplicate Identification & Elimination
- **Internal Portal Duplicates**: In Housing.com Commercial, 24 duplicate listings with consecutive property IDs (e.g., `100631653` and `100631654` with identical coordinates, price, area, and URL slugs) were eliminated, preserving the canonical instance and routing the duplicates to `duplicate_records.json`.
- **Cross-Portal Duplicates**: Cross-portal deduplication evaluated matches across verified locality, property type, price, area, and configuration, ensuring that no property is double-counted in combined training.

---

## 5. Statistical Distributions (Cleaned Residential Combined: 194 Records)

### Price Distribution (INR)
- **Minimum Asking Price**: ₹350,000 (₹3.5 Lakhs)
- **25th Percentile (Q1)**: ₹6,000,000 (₹60.0 Lakhs)
- **Median Asking Price**: ₹9,965,000 (₹99.7 Lakhs)
- **Mean Asking Price**: ₹16,313,507 (₹1.63 Crores)
- **75th Percentile (Q3)**: ₹17,000,000 (₹1.70 Crores)
- **Maximum Asking Price**: ₹260,000,000 (₹26.00 Crores)

### Area Distribution (Square Feet)
- **Minimum Area**: 111 sq.ft (0.5 Marlas)
- **25th Percentile (Q1)**: 1,250 sq.ft (5.6 Marlas)
- **Median Area**: 1,905 sq.ft (8.5 Marlas)
- **Mean Area**: 2,448 sq.ft (10.9 Marlas)
- **75th Percentile (Q3)**: 2,788 sq.ft (12.4 Marlas)
- **Maximum Area**: 19,057 sq.ft (84.7 Marlas)

### Derived Valuation Density (Price per Sq.Ft)
- **Minimum**: ₹64.8 / sq.ft
- **Median**: ₹5,667.4 / sq.ft
- **Mean**: ₹8,215.6 / sq.ft
- **Maximum**: ₹153,153.1 / sq.ft

---

## 6. Top Canonical Localities by Cleaned Representation

| Canonical Locality | Residential Listings | Commercial Listings | Rental Listings | Total Cleaned Listings | Median Price (INR) |
|---|---:|---:|---:|---:|---:|
| **Trikuta Nagar** | 17 | 14 | 66 | **97** | ₹27,500 |
| **Channi Himmat** | 8 | 19 | 40 | **67** | ₹65,000 |
| **Greater Kailash** | 6 | 2 | 40 | **48** | ₹31,999 |
| **Sainik Colony** | 10 | 5 | 24 | **39** | ₹30,000 |
| **Gandhi Nagar** | 3 | 12 | 15 | **30** | ₹217,500 |
| **Talab Tillo** | 6 | 12 | 10 | **28** | ₹4,900,000 |
| **Nanak Nagar** | 6 | 12 | 6 | **24** | ₹6,500,000 |
| **Sidhra** | 8 | 1 | 11 | **20** | ₹36,000 |
| **Gangyal** | 4 | 13 | 2 | **19** | ₹12,000,000 |
| **Sunjwan** | 8 | 1 | 4 | **13** | ₹4,200,000 |
| **Roop Nagar** | 6 | 2 | 5 | **13** | ₹6,000,000 |
| **Bathindi** | 7 | 2 | 3 | **12** | ₹7,500,000 |
| **Bakshi Nagar** | 3 | 4 | 5 | **12** | ₹2,750,000 |
| **Digiana** | 4 | 4 | 3 | **11** | ₹5,000,000 |
| **Shastri Nagar** | 2 | 4 | 5 | **11** | ₹420,000 |
| **Bantalab** | 4 | 1 | 5 | **10** | ₹2,765,000 |
| **Channi Rama** | 1 | 5 | 4 | **10** | ₹1,475,000 |
| **Bishnah** | 2 | 7 | 0 | **9** | ₹85,000,000 |
| **Paloura** | 3 | 5 | 1 | **9** | ₹12,500,000 |
| **Pakki Dhaki** | 0 | 9 | 0 | **9** | ₹7,000,000 |

---

## 7. Model-Training Readiness Assessment

Per Section 14 of the specification, the cleaned dataset is evaluated for supervised property price prediction:

1. **Target Variable Validation**: All 194 records in `residential_combined_cleaned.json` contain non-null, strictly positive numerical asking prices (`price_inr`).
2. **Physical Area Completeness**: All records contain non-null, strictly positive, physically plausible area measurements (`area_sqft_clean`).
3. **Target Leakage Prevention**: Derived fields `price_per_sqft` and `price_per_marla` are explicitly calculated from the target variable (`price_inr`). **They MUST NOT be used as input features in regression models predicting `price_inr`**.
4. **Data Independence**: Verified deduplication ensures no duplicate listings exist that could contaminate cross-validation splits.
5. **Categorical Feature Preservation**: Useful categorical attributes (`type_of_property`, `furnished_status`, `status`, `property_ownership`, `configuration`) are preserved in their native structure alongside clean normalized columns.
6. **Asking Price Limitation Notice**: Portal asking prices reflect seller expectations rather than certified Revenue Department deed transaction prices. For property buy-worthiness scoring, this asking price serves as the numerator compared against circle-rate and model-forecasted valuation benchmarks.

---

## 8. Reproducibility

The entire data cleaning workflow is encapsulated in [`scripts/clean_housing_magicbricks.py`](file:///c:/Users/vatsa/.antigravity/Minor_Project_COM-711/scripts/clean_housing_magicbricks.py). It can be executed deterministically on new scraper drops without manual intervention.
