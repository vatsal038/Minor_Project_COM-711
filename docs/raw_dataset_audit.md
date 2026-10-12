# Comprehensive Raw Dataset Audit Report

- **Dataset Path**: `/Users/satyendrasharma/Documents/MINOR PROJECT/Minor_Project_COM-711/data/raw/property_dataset_raw.csv`
- **Total Records**: 1200
- **Total Variables**: 36
- **Missing/Null Values**: 0 columns with nulls
- **Duplicate Rows**: 0
- **Property ID Uniqueness**: True (JMU0001 to JMU1200)
- **Base Reference Year**: 2026

## 1. Locality & Spatial Breakdown

- Distinct Localities: **36** (Exact match with 36 canonical Jammu localities)
- Records per locality: Min = 23, Mean = 33.33, Max = 45
- Property Coordinates: **ABSENT** in raw CSV. Geocoding to WGS84 required in Week 4.

## 2. Target Variable & Distribution

- `Not Buy`: 903 (75.25%)
- `Buy`: 297 (24.75%)

## 3. Mathematical Consistency

- Area Formula: `area_sqft ≈ area_marla * 272.25` (Max error: 1.3575)
- Total Price Formula: `total_price_lakh ≈ area_sqft * price_per_sqft / 100000` (Max error: 0.0195)

## 4. Key Numeric Ranges

| Variable | Min | Mean | Median | Max | Outliers (IQR) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `area_sqft` | 451.0 | 1818.24 | 1823.0 | 3199.0 | 0 |
| `area_marla` | 1.66 | 6.68 | 6.695 | 11.75 | 0 |
| `area_kanal` | 0.083 | 0.33 | 0.335 | 0.588 | 0 |
| `price_per_sqft` | 1312.0 | 4258.11 | 4013.5 | 11158.0 | 31 |
| `price_per_marla_lakh` | 3.57 | 11.59 | 10.925 | 30.38 | 31 |
| `total_price_lakh` | 8.85 | 77.24 | 68.765 | 302.17 | 26 |
| `builder_credibility_score` | 3.0 | 6.84 | 6.9 | 10.0 | 0 |
| `year_built` | 1990.0 | 2007.06 | 2007.0 | 2024.0 | 0 |
| `property_age_years` | 2.0 | 18.94 | 19.0 | 36.0 | 0 |
| `road_width_ft` | 8.0 | 16.12 | 16.0 | 35.0 | 2 |
| `distance_to_city_center_km` | 0.5 | 7.91 | 6.1 | 24.8 | 1 |
| `distance_to_highway_km` | 0.3 | 7.95 | 7.1 | 22.2 | 6 |

## 5. Leakage and Risk Warnings

> CRITICAL: 'total_price_lakh' is exactly derived as (area_sqft * price_per_sqft) / 100000. For regression tasks predicting total_price_lakh, price_per_sqft must be excluded from feature set. Similarly, for classification of 'recommendation', forecast_3yr_price_growth_pct and locality_score correlate strongly with the recommendation label.
