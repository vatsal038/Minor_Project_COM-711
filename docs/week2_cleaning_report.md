# Week 2 Data Cleaning & Format Standardization Report

- **Execution Date**: 2026-10-12T18:05:37.223367+00:00
- **Total Input Records**: 1200
- **Cleaned Output Records**: 1200
- **Output Path**: `/Users/satyendrasharma/Documents/MINOR PROJECT/Minor_Project_COM-711/data/processed/listings_cleaned.csv`

## 1. Mathematical Consistency & Integrity

- Price Calculation Discrepancies (>1%): **0**
- Area Unit Discrepancies (>5 sqft): **0**
- Year Built vs Property Age Mismatches: **0**

## 2. Statistical Outlier Boundaries (IQR Method)

| Variable | Lower Bound | Upper Bound | Outliers Count | Sample IDs |
| :--- | :--- | :--- | :--- | :--- |
| `price_per_sqft` | -22.5 | 8273.5 | 31 | JMU0014, JMU0025, JMU0123... |
| `total_price_lakh` | -50.67 | 195.69 | 26 | JMU0107, JMU0110, JMU0118... |
| `area_sqft` | -925.0 | 4573.0 | 0 | ... |

## 3. JDA Regulatory Matching Validation

- **total_listings_claiming_jda_approved**: 594
- **total_listings_in_approved_jda_localities**: 881
- **anomalous_claims_in_unapproved_zones**: 15
- **anomalous_sample_ids**: ['JMU0039', 'JMU0047', 'JMU0232', 'JMU0313', 'JMU0366']
