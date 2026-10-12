# AI-Based Property Buy-Worthiness Assessment and Property Value Forecasting (COM-711)

**A practical, privacy-preserving AI/ML decision-support system evaluating property buy-worthiness and future valuation in Jammu.**

---

## 1. Project Overview & Scope (Weeks 1–4)

This repository hosts the implementation of **Minor Project COM-711** (Academic Session 2026–2027), focusing on evaluating user-specified residential, commercial, and plotted properties across 36 canonical localities in the Jammu Urban Agglomeration.

During the first four weeks, the engineering team executed the data engineering and source integration foundation across seven distinct public data streams:
1. **99acres Jammu Property Listings** (Curated public snapshot of 1,200 records across 36 localities).
2. **Jammu Development Authority (JDA)** (Official layout approvals, scheme notifications, and Master Plan 2032 land-use zones).
3. **J&K Real Estate Regulatory Authority (J&K RERA)** (Statutory builder registrations, delivery track records, and consumer complaints).
4. **Jammu Municipal Corporation (JMC) & Smart City Jammu** (Ward-level water supply hours, sewerage coverage %, drainage complaints, and road conditions).
5. **J&K Revenue & Registration Department** (Official statutory circle rates per kanal and per sq ft).
6. **J&K State Disaster Management Authority (SDMA)** (Tawi river basin flood inundation maps and drainage hazard classifications).
7. **OpenStreetMap (OSM)** (WGS-84 centroid geocoding, educational institutions, healthcare nodes, and transit corridors).

---

## 2. Repository Structure

```
Minor_Project_COM-711/
├── .gitignore                          # Python, OS, and virtual environment ignore rules
├── requirements.txt                    # Project dependencies
├── config/
│   ├── __init__.py
│   └── settings.py                     # Central project paths, constants, and canonical localities
├── data/
│   ├── raw/
│   │   ├── property_dataset_raw.csv    # Preserved original 1,200 raw property records
│   │   └── listings_99acres_raw.csv    # Verified raw listings snapshot with provenance tracking
│   ├── interim/                        # Intermediate processing staging
│   └── processed/
│       ├── listings_cleaned.csv        # Cleaned and standardized property listings
│       ├── jda_approvals_structured.csv# JDA scheme layout approvals and Master Plan 2032 zones
│       ├── rera_projects_structured.csv# J&K RERA promoter profiles and compliance scores
│       ├── jmc_civic_structured.csv    # Municipal ward civic infrastructure indicators
│       ├── revenue_circle_rates_structured.csv # Statutory circle rates per kanal and sq ft
│       ├── locality_standardized_mapping.csv   # 36 canonical localities with pin codes and aliases
│       ├── osm_amenities_jammu.csv     # Geocoded centroids, schools, hospitals, and transit stops
│       ├── sdma_flood_zones_jammu.csv  # Flood vulnerability and Tawi catchment hazard levels
│       ├── integrated_listings_week3.csv       # Multi-source integrated dataset (Week 3)
│       └── unified_property_dataset_jammu.csv  # Final Unified Dataset (1,200 rows x 71 features)
├── src/
│   ├── __init__.py
│   ├── audit/
│   │   ├── dataset_audit.py            # Reproducible audit of raw CSV integrity and distributions
│   │   ├── generate_data_dictionary.py # Canonical 35-variable data dictionary generator
│   │   └── source_investigator.py      # Network probes and robots.txt audit across 7 public sources
│   ├── ingestion/
│   │   ├── listings_ingestion.py       # Listings ingestion and live scraping probe
│   │   ├── jda_ingestion.py            # JDA layout approval gazette extraction
│   │   ├── rera_ingestion.py           # J&K RERA builder compliance and credibility scoring
│   │   ├── jmc_ingestion.py            # Municipal ward civic infrastructure extraction
│   │   ├── revenue_ingestion.py        # Statutory circle rate table structuring
│   │   ├── osm_ingestion.py            # OpenStreetMap amenities and spatial coordinates
│   │   └── sdma_ingestion.py           # J&K SDMA flood risk zoning ingestion
│   ├── cleaning/
│   │   └── standardize_clean.py        # Type coercion, boolean normalization, and IQR outlier audit
│   ├── geospatial/
│   │   └── spatial_features.py         # Haversine distance calculations and geocoding validation
│   ├── integration/
│   │   ├── week3_integration.py        # Multi-source joining and circle rate ratio calculation
│   │   └── dataset_integrator.py       # Master synthesis and 7 synopsis engineered variables
│   └── reports/
│       └── generate_word_reports.py    # Python-docx generator for editable Word reports
├── tests/
│   ├── test_raw_audit.py               # Tests for raw dataset audit and schema consistency
│   ├── test_cleaning.py                # Tests for cleaning, typing, and JDA approval dataset
│   ├── test_integration.py             # Tests for RERA, JMC, Revenue, and Week 3 integration
│   └── test_geospatial.py              # Tests for OSM, SDMA, and Week 4 unified dataset
├── docs/
│   ├── data_dictionary.md              # Formal markdown data dictionary
│   ├── data_dictionary.json            # Machine-readable schema definitions
│   ├── data_source_register.md         # Public data source access and governance inventory
│   ├── data_source_register.json       # Machine-readable network probe logs
│   ├── raw_dataset_audit.md            # Raw dataset statistical and leakage audit
│   ├── week2_cleaning_report.md        # Data cleaning and outlier audit report
│   ├── week3_integration_report.md     # Multi-source integration coverage report
│   └── week4_geospatial_unified_report.md # Geospatial processing and unified dataset report
└── weekly_reports/
    ├── WEEK_1.docx                     # Editable Word report for Week 1 (Task ID: COM71115-3)
    ├── WEEK_2.docx                     # Editable Word report for Week 2 (Task ID: COM71115-4)
    ├── WEEK_3.docx                     # Editable Word report for Week 3 (Task ID: COM71115-5)
    └── WEEK_4.docx                     # Editable Word report for Week 4 (Task ID: COM71115-6)
```

---

## 3. The 7 Synopsis Engineered Variables

As specified in the project synopsis, seven advanced engineered indicators have been computed:

| Variable | Description | Mathematical Formulation | Range in Dataset |
| :--- | :--- | :--- | :--- |
| **`price_vs_locality_type`** | Relative price fairness within neighborhood and asset type | `asking_price ÷ median(asking_price for same locality & type)` | 0.551 to 1.742 |
| **`price_vs_type`** | Relative price fairness across Jammu citywide market | `asking_price ÷ citywide_median(asking_price for same type)` | 0.384 to 2.164 |
| **`growth_momentum`** | Appreciation acceleration | `forecast_3yr_price_growth_pct − past_5yr_price_growth_pct` | -10.8% to +14.6% |
| **`legal_clarity_index`** | Normalized title and statutory planning safety index | `0.35*RegDeed + 0.25*JDA + 0.25*BankLoan + 0.15*Freehold` | 0.020 to 1.000 |
| **`amenity_access_index`** | Composite access to education, healthcare, transit, and core | `0.25*Schools + 0.25*Hospitals + 0.25*Transit + 0.25*(1-NormDist)`| 0.184 to 0.892 |
| **`civic_risk_index`** | Municipal and environmental risk liability | `0.30*Complaints + 0.30*FloodRisk + 0.40*(UtilityDeficiencies)` | 0.114 to 0.884 |
| **`locality_price_rank`** | Market price percentile ranking across all 36 localities | `percentile_rank(locality_median_price_per_sqft)` | 0.028 to 1.000 |

---

## 4. Setup and Execution Instructions

### Prerequisites
- Python 3.10+
- Virtual environment or conda

### Installation
```bash
# Clone the repository (or navigate to workspace)
cd Minor_Project_COM-711

# Install required dependencies
pip install -r requirements.txt
```

### Reproducing the Complete Pipeline
```bash
# Step 1: Execute Week 1 Audits & Data Dictionary
python -m src.audit.dataset_audit
python -m src.audit.source_investigator
python -m src.audit.generate_data_dictionary

# Step 2: Execute Week 2 Ingestion & Cleaning
python -m src.ingestion.listings_ingestion
python -m src.ingestion.jda_ingestion
python -m src.cleaning.standardize_clean

# Step 3: Execute Week 3 Multi-Source Ingestion & Integration
python -m src.ingestion.rera_ingestion
python -m src.ingestion.jmc_ingestion
python -m src.ingestion.revenue_ingestion
python -m src.integration.week3_integration

# Step 4: Execute Week 4 Geospatial Processing & Master Synthesis
python -m src.ingestion.osm_ingestion
python -m src.ingestion.sdma_ingestion
python -m src.integration.dataset_integrator

# Step 5: Generate all four Word Reports
python -m src.reports.generate_word_reports
```

### Running the Test Suite
```bash
pytest tests/ -v
```
All **21 automated unit and integration tests** will execute and pass in under 1 second.

---

## 5. Weekly Reports Summary

The four requested editable Microsoft Word documents are maintained under `weekly_reports/`:
- **`weekly_reports/WEEK_1.docx`**: Project Setup, Environment Configuration, Raw Dataset Audit, Source Register, and Data Dictionary (Task ID: `COM71115-3`).
- **`weekly_reports/WEEK_2.docx`**: Listings Acquisition, JDA Layout Approvals, Master Plan 2032 Zoning, Cleaning, and Outlier Analysis (Task ID: `COM71115-4`).
- **`weekly_reports/WEEK_3.docx`**: J&K RERA Builder Compliance, JMC Civic Infrastructure, Revenue Circle Rates, and Multi-Source Integration (Task ID: `COM71115-5`).
- **`weekly_reports/WEEK_4.docx`**: OpenStreetMap Amenities, SDMA Flood Hazards, Centroid Geocoding, 7 Engineered Variables, and Unified Property Dataset (Task ID: `COM71115-6`).
