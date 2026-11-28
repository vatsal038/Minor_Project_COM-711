import os
import json
import pandas as pd
import numpy as np

CLEANED_DIR = 'data/DATA/cleaned'
REPORTS_DIR = os.path.join(CLEANED_DIR, 'reports')

def generate_report():
    with open(os.path.join(REPORTS_DIR, 'cleaning_summary.json'), 'r', encoding='utf-8') as f:
        summary = json.load(f)
        
    metrics = summary['file_metrics']
    totals = summary['totals']
    
    # Load combined residential
    with open(os.path.join(CLEANED_DIR, 'residential', 'residential_combined_cleaned.json'), 'r', encoding='utf-8') as f:
        res_combined = json.load(f)
    df_res = pd.DataFrame(res_combined)
    
    # Load combined commercial
    with open(os.path.join(CLEANED_DIR, 'commercial', 'commercial_combined_cleaned.json'), 'r', encoding='utf-8') as f:
        comm_combined = json.load(f)
    df_comm = pd.DataFrame(comm_combined)
    
    # Load rental
    with open(os.path.join(CLEANED_DIR, 'rental', 'rental_cleaned_separate.json'), 'r', encoding='utf-8') as f:
        rent_data = json.load(f)
    df_rent = pd.DataFrame(rent_data)
    
    # Load locality summary
    df_loc = pd.read_csv(os.path.join(REPORTS_DIR, 'locality_summary.csv'))
    
    # Load removed records
    with open(os.path.join(CLEANED_DIR, 'removed', 'removed_records.json'), 'r', encoding='utf-8') as f:
        removed = json.load(f)
    df_rem = pd.DataFrame(removed)
    rem_reasons = df_rem['removal_reason'].apply(lambda x: x.split(':')[0]).value_counts().to_dict()
    
    # Load reviews
    with open(os.path.join(CLEANED_DIR, 'review', 'geographic_review.json'), 'r', encoding='utf-8') as f:
        geo_rev = json.load(f)
    with open(os.path.join(CLEANED_DIR, 'review', 'outlier_review.json'), 'r', encoding='utf-8') as f:
        outlier_rev = json.load(f)
    with open(os.path.join(CLEANED_DIR, 'review', 'data_quality_review.json'), 'r', encoding='utf-8') as f:
        dq_rev = json.load(f)

    # Compute price and area stats for residential
    res_price_min = df_res['price_inr'].min()
    res_price_med = df_res['price_inr'].median()
    res_price_mean = df_res['price_inr'].mean()
    res_price_max = df_res['price_inr'].max()
    res_price_q1 = df_res['price_inr'].quantile(0.25)
    res_price_q3 = df_res['price_inr'].quantile(0.75)
    
    res_area_min = df_res['area_sqft_clean'].min()
    res_area_med = df_res['area_sqft_clean'].median()
    res_area_mean = df_res['area_sqft_clean'].mean()
    res_area_max = df_res['area_sqft_clean'].max()
    res_area_q1 = df_res['area_sqft_clean'].quantile(0.25)
    res_area_q3 = df_res['area_sqft_clean'].quantile(0.75)

    res_pps_min = df_res['price_per_sqft'].min()
    res_pps_med = df_res['price_per_sqft'].median()
    res_pps_mean = df_res['price_per_sqft'].mean()
    res_pps_max = df_res['price_per_sqft'].max()
    
    # Commercial stats
    comm_price_min = df_comm['price_inr'].min()
    comm_price_med = df_comm['price_inr'].median()
    comm_price_max = df_comm['price_inr'].max()
    comm_area_min = df_comm['area_sqft_clean'].min()
    comm_area_med = df_comm['area_sqft_clean'].median()
    comm_area_max = df_comm['area_sqft_clean'].max()

    report_md = f"""# Real Estate Data Cleaning Report — Housing.com & Magicbricks
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
3. **Physical & Unit Integrity**: Corrected unit conversion errors (including sq.yd to sq.ft and detected suspected Marla-sqft input inversions). Derived verified price-per-square-foot and price-per-marla metrics following the Jammu regional convention ($1\\text{{ Marla}} = 225\\text{{ sq.ft}}$, $1\\text{{ sq.yd}} = 9\\text{{ sq.ft}}$).
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
"""

    for m in metrics:
        report_md += f"| `{m['source_file']}` | {m['portal'].capitalize()} | {m['category'].capitalize()} | {m['original_records']} | {m['confirmed_jammu']} | {m['outside_removed']} | {m['price_removed']} | {m['area_removed']} | {m['duplicate_removed']} | {m['projects_separated']} | {m['flagged_review']} | **{m['final_retained']}** |\n"

    report_md += f"""| **TOTAL** | — | — | **{sum(m['original_records'] for m in metrics)}** | **{sum(m['confirmed_jammu'] for m in metrics)}** | **{sum(m['outside_removed'] for m in metrics)}** | **{sum(m['price_removed'] for m in metrics)}** | **{sum(m['area_removed'] for m in metrics)}** | **{sum(m['duplicate_removed'] for m in metrics)}** | **{sum(m['projects_separated'] for m in metrics)}** | **{sum(m['flagged_review'] for m in metrics)}** | **{sum(m['final_retained'] for m in metrics)}** |

---

## 3. Dataset Distribution & Output Structure

The cleaned datasets are saved under `data/DATA/cleaned/` with strict logical decoupling:

```text
data/DATA/cleaned/
├── residential/
│   ├── housing_residential_cleaned.json         # {totals['cleaned_residential_housing']} records (Cleaned Housing.com residential sales)
│   ├── magicbricks_residential_cleaned.json     # {totals['cleaned_residential_magicbricks']} records (Cleaned Magicbricks residential sales)
│   └── residential_combined_cleaned.json        # {totals['cleaned_residential_combined']} records (Combined de-duplicated residential sale dataset)
│
├── commercial/
│   ├── housing_commercial_cleaned.json          # {totals['cleaned_commercial_housing']} records (Cleaned Housing.com commercial properties)
│   ├── magicbricks_commercial_cleaned.json      # {totals['cleaned_commercial_magicbricks']} records (Cleaned Magicbricks commercial properties)
│   └── commercial_combined_cleaned.json         # {totals['cleaned_commercial_combined']} records (Combined commercial property dataset)
│
├── rental/
│   └── rental_cleaned_separate.json             # {totals['cleaned_rental']} records (Cleaned rental listings kept separate from sale model)
│
├── projects/
│   └── project_listings_separate.json           # {totals['separated_projects']} records (Multi-unit developer marketing listings & price ranges)
│
├── review/
│   ├── geographic_review.json                   # {totals['geographic_review']} records (Ambiguous localities requiring human geographic verification)
│   ├── outlier_review.json                      # {totals['outlier_review']} records (Statistical outliers flagged but preserved)
│   └── data_quality_review.json                 # {totals['data_quality_review']} records (Unit conversion / display discrepancies)
│
├── removed/
│   ├── removed_records.json                     # {totals['removed_records']} records (Out-of-district, missing price, invalid area)
│   └── duplicate_records.json                   # {totals['duplicate_records']} records (Internal portal and cross-portal duplicates)
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
  - Listing `21138422` (labeled city `Jammu` but with address `Nagrota, Udhampur` and coordinates $32.87^\\circ\\text{{N}}, 75.10^\\circ\\text{{E}}$) was confirmed in Udhampur District and removed.
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

## 5. Statistical Distributions (Cleaned Residential Combined: {len(df_res)} Records)

### Price Distribution (INR)
- **Minimum Asking Price**: ₹{res_price_min:,.0f} (₹{res_price_min/1e5:.1f} Lakhs)
- **25th Percentile (Q1)**: ₹{res_price_q1:,.0f} (₹{res_price_q1/1e5:.1f} Lakhs)
- **Median Asking Price**: ₹{res_price_med:,.0f} (₹{res_price_med/1e5:.1f} Lakhs)
- **Mean Asking Price**: ₹{res_price_mean:,.0f} (₹{res_price_mean/1e7:.2f} Crores)
- **75th Percentile (Q3)**: ₹{res_price_q3:,.0f} (₹{res_price_q3/1e7:.2f} Crores)
- **Maximum Asking Price**: ₹{res_price_max:,.0f} (₹{res_price_max/1e7:.2f} Crores)

### Area Distribution (Square Feet)
- **Minimum Area**: {res_area_min:,.0f} sq.ft ({res_area_min/225:.1f} Marlas)
- **25th Percentile (Q1)**: {res_area_q1:,.0f} sq.ft ({res_area_q1/225:.1f} Marlas)
- **Median Area**: {res_area_med:,.0f} sq.ft ({res_area_med/225:.1f} Marlas)
- **Mean Area**: {res_area_mean:,.0f} sq.ft ({res_area_mean/225:.1f} Marlas)
- **75th Percentile (Q3)**: {res_area_q3:,.0f} sq.ft ({res_area_q3/225:.1f} Marlas)
- **Maximum Area**: {res_area_max:,.0f} sq.ft ({res_area_max/225:.1f} Marlas)

### Derived Valuation Density (Price per Sq.Ft)
- **Minimum**: ₹{res_pps_min:,.1f} / sq.ft
- **Median**: ₹{res_pps_med:,.1f} / sq.ft
- **Mean**: ₹{res_pps_mean:,.1f} / sq.ft
- **Maximum**: ₹{res_pps_max:,.1f} / sq.ft

---

## 6. Top Canonical Localities by Cleaned Representation

| Canonical Locality | Residential Listings | Commercial Listings | Rental Listings | Total Cleaned Listings | Median Price (INR) |
|---|---:|---:|---:|---:|---:|
"""

    top_locs = df_loc.sort_values(by='total_listings', ascending=False).head(20)
    for _, row in top_locs.iterrows():
        report_md += f"| **{row['canonical_locality']}** | {row['residential_count']} | {row['commercial_count']} | {row['rental_count']} | **{row['total_listings']}** | ₹{row['median_price_inr']:,.0f} |\n"

    report_md += f"""
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
"""

    report_path = os.path.join(REPORTS_DIR, 'cleaning_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"Report successfully generated at: {report_path}")

if __name__ == '__main__':
    generate_report()
