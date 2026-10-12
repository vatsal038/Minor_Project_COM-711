# Week 4 Geospatial Processing & Unified Dataset Report

- **Execution Timestamp**: 2026-10-12T18:10:46.357126+00:00
- **Total Unified Records**: 1200
- **Total Variables in Unified Schema**: 71
- **Unified File Path**: `/Users/satyendrasharma/Documents/MINOR PROJECT/Minor_Project_COM-711/data/processed/unified_property_dataset_jammu.csv`

## 1. Synopsis 7 Engineered Variables Summary

| Variable Name | Min | Mean | Median | Max | Std Dev |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `price_vs_locality_type` | 0.594 | 1.002 | 1.0 | 1.618 | 0.129 |
| `price_vs_type` | 0.438 | 1.012 | 1.0 | 1.885 | 0.275 |
| `growth_momentum` | -11.4 | 1.415 | 1.4 | 12.3 | 3.762 |
| `legal_clarity_index` | 0.07 | 0.621 | 0.7 | 1.0 | 0.271 |
| `amenity_access_index` | 0.07 | 0.461 | 0.4765 | 0.799 | 0.143 |
| `civic_risk_index` | 0.038 | 0.264 | 0.248 | 0.667 | 0.126 |
| `locality_price_rank` | 0.028 | 0.521 | 0.528 | 1.0 | 0.287 |
| `asking_vs_circle_rate_ratio` | 0.82 | 3.164 | 2.925 | 10.25 | 1.296 |

## 2. Geospatial & Hazard Coverage

- Resolution: `Locality_Centroid_WGS84`
- Distance to City Center (km): Min = 0.0, Max = 23.3
- Flood Risk Zones: Low: 892, Medium: 178, High: 130

## 3. Data Provenance Summary

- **listings_source**: 99acres Curated Jammu Listings (1,200 records)
- **jda_source**: Jammu Development Authority Master Plan 2032 (36 schemes)
- **rera_source**: J&K RERA Project Registration & Builder History (13 builders)
- **jmc_source**: Jammu Municipal Corporation Civic Ward Infrastructure (36 localities)
- **revenue_source**: J&K Revenue Dept & District Collector Circle Rates 2024
- **osm_source**: OpenStreetMap WGS84 Centroids & Amenity Counts
- **sdma_source**: J&K SDMA Flood Hazard Atlas & Catchment Zoning
