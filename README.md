# AI-Based Property Buy-Worthiness Assessment and Property Value Forecasting (COM-711)

**A Practical, Privacy-Preserving AI/ML Decision-Support System for Property Valuation and Buy-Worthiness in Jammu**

---

## 1. Project Title and Overview

* **Official Project Title**: AI-Based Property Buy Worthiness Assessment and Property Value Forecasting Using Location, Market, Builder and Civic Data (Property Buy / Not Buy Recommender)
* **Academic Course Code**: COM-711 (Minor Project)
* **Academic Session**: 2026–2027
* **Institution / Department**: Model Institute of Engineering and Technology (MIET), Department of Computer Science & Engineering
* **Geographic Focus**: Jammu Urban Agglomeration and surrounding sub-districts across **36 canonical localities** (e.g., Channi Himmat, Gandhi Nagar, Trikuta Nagar, Bahu Plaza, Roop Nagar, Janipur, Satwari, Greater Kailash, Bantalab, Bari Brahmana, Vijaypur, etc.)
* **Primary Objective**: To develop a client-side, privacy-preserving AI/ML decision-support system that evaluates whether a user-specified real estate property in Jammu represents a viable investment, forecasts its potential future valuation (1-, 3-, and 5-year horizons), and explains the verdict using multi-source civic, legal, builder, and spatial indicators.

---

## 2. Problem Statement and Objectives

### Problem Statement
Real estate purchase is one of the highest-stakes financial decisions made by individuals and families. In regional Indian property markets such as Jammu, critical evaluation data—historical capital appreciation, statutory Jammu Development Authority (JDA) layout approvals, Real Estate Regulatory Authority (J&K RERA) builder compliance, municipal civic infrastructure (JMC water and sewerage coverage), official Revenue Department circle rates, and State Disaster Management Authority (SDMA) flood hazard risks—is fragmented across disparate government departments, offline records, or commercial listing portals. Existing platforms emphasize listing discovery rather than holistic due diligence and buy-worthiness assessment.

### Objectives
1. **Multi-Source Data Integration**: Collect and integrate property pricing, land transactions, statutory layout approvals, builder compliance records, civic indicators, and environmental hazard data from publicly available sources and structured snapshots.
2. **Documented Data Engineering Pipeline**: Implement an end-to-end preprocessing, cleaning, outlier handling (Winsorization and IQR bounds), and feature-engineering workflow.
3. **Property Buy-Worthiness Assessment**: Design a multi-factor scoring mechanism evaluating valuation fairness, growth outlook, legal clarity, builder credibility, amenity access, and civic risk to output a structured verdict (*Buy / Maybe / No-Buy*).
4. **Value Forecasting Engine (Upcoming)**: Prepare the data architecture for training an ensemble regression model (Random Forest, XGBoost, LightGBM) to forecast future property valuations.
5. **Builder Credibility Synthesis (Upcoming)**: Incorporate developer reliability indicators derived from public RERA registrations, delivery track records, and consumer dispute filings.
6. **Interpretability & Privacy**: Maintain complete client-side execution to preserve consumer privacy and prepare for local Explainable AI (SHAP) explanations.

---

## 3. Features and Scope

### Currently Implemented (Weeks 1–4 Foundation)
* **Curated & Synthetic Data Integration**: Ingestion of 1,200 property records across 36 Jammu localities covering residential apartments, independent houses, plots, and commercial units.
* **JDA Regulatory Mapping**: Gazette layout scheme approval status, notification numbers, and Master Plan 2032 land-use zone classifications for all 36 localities.
* **J&K RERA Builder Compliance Profile**: Profiling of 13 active regional developers with registration numbers, project delivery track records, and consumer complaint ratios.
* **Municipal Civic Benchmarks**: Ward-level water supply hours per day, underground sewerage coverage %, drainage complaint frequency, and road condition indices from JMC and Smart City Jammu disclosures.
* **Official Circle Rate Alignment**: Integration of official District Collector statutory circle rates (per kanal and per sq ft) and derivation of market-asking-price-to-circle-rate ratios.
* **Geospatial & Flood Risk Mapping**: WGS-84 locality centroid geocoding, OpenStreetMap (OSM) school/hospital/transit counts, Haversine distance calculations to Jammu City Center (Jewel Chowk), and J&K SDMA flood hazard vulnerability classifications.
* **The 7 Synopsis Engineered Variables**: Mathematical derivation of all 7 core indicators specified in the project synopsis.
* **Iterative Analysis Notebooks**: Preprocessing, Winsorization, log transformations, and feature engineering verified in progressive Jupyter Notebooks.

### Proposed & Future Milestones (Weeks 5–16 Scope)
* **Machine Learning Valuation Models**: Training and tuning of Random Forest, XGBoost, and LightGBM ensemble models for 1-, 3-, and 5-year value forecasting.
* **Classification Decision Engine**: Thresholded and supervised classification heads for Buy / Maybe / No-Buy verdicts with conformal prediction uncertainty quantification.
* **RAG Builder Synthesis**: Local Retrieval-Augmented Generation agent using Sentence-Transformers and FAISS/Chroma for automated synthesis of public RERA orders and news documents.
* **Explainable AI (SHAP)**: Factor-by-factor visual attributions explaining individual verdicts.
* **Client-Side User Interface**: Streamlit / Vanilla JavaScript interface executing local browser/client inference without transmitting user inputs to external servers.

---

## 4. Repository Structure

The current directory layout of the repository (`main` branch) is structured as follows:

```
Minor_Project_COM-711/
├── .gitignore                                      # Git ignore rules for Python, cache, and OS artifacts
├── Abstract.docx                                   # Project synopsis, aim, introduction, and abstract specification
├── README.md                                       # Primary project documentation and technical repository guide
├── requirements.txt                                # Python package dependencies
├── Weekly_reports/                                 # Weekly milestone reports, analysis notebooks, and raw data
│   ├── .gitkeep                                    # Directory keep file
│   ├── WEEK_1.pdf                                  # Week 1 Technical Progress Report (Setup & Source Identification)
│   ├── Week_2.pdf                                  # Week 2 Technical Progress Report (Dataset Preparation & JDA)
│   ├── WEEK_3.pdf                                  # Week 3 Technical Progress Report (RERA, JMC & Circle Rates)
│   ├── minor project analysis.ipynb                # Jupyter Notebook: Initial data exploration and preprocessing
│   ├── MINOR_PROJECT_ANALYSIS_WEEK3.ipynb          # Jupyter Notebook: Cleaning, Winsorization, and distribution analysis
│   ├── minor_project_analysis_week4.ipynb          # Jupyter Notebook: Feature engineering and 7 synopsis variables
│   └── synthetic_properties_raw.csv                # Raw baseline dataset (1,200 rows x 32 columns)
└── data/                                           # Structured, cleaned, and integrated datasets
    ├── image.png                                   # System methodology flowchart (from project synopsis)
    ├── raw/
    │   ├── property_dataset_raw.csv                # Preserved curated dataset (1,200 rows x 36 columns)
    │   └── listings_99acres_raw.csv                # Verified listings snapshot with provenance tracking
    └── processed/
        ├── listings_cleaned.csv                    # Cleaned, standardized property listings (1,200 rows x 36 cols)
        ├── jda_approvals_structured.csv            # Structured JDA scheme approvals & Master Plan 2032 zones (36 rows)
        ├── rera_projects_structured.csv            # Structured J&K RERA builder profiles & complaints (13 rows)
        ├── jmc_civic_structured.csv                # Municipal ward civic infrastructure indicators (36 rows)
        ├── revenue_circle_rates_structured.csv     # Statutory circle rates per kanal and per sq ft (36 rows)
        ├── locality_standardized_mapping.csv       # Canonical locality lookup with PIN codes & aliases (36 rows)
        ├── osm_amenities_jammu.csv                 # Centroid coordinates, school/hospital counts & distances (36 rows)
        ├── sdma_flood_zones_jammu.csv              # J&K SDMA flood hazard vulnerability levels (36 rows)
        ├── integrated_listings_week3.csv           # Multi-source merged dataset from Week 3 (1,200 rows x 49 cols)
        └── unified_property_dataset_jammu.csv      # Master Consolidated Unified Dataset (1,200 rows x 71 cols)
```

> **Note on Companion Branch**: A dedicated feature branch, `feature/weeks-1-4-data-pipeline`, maintains automated CLI pipeline modules (`src/audit/`, `src/ingestion/`, `src/cleaning/`, `src/geospatial/`, `src/integration/`, `src/reports/`), modular `pytest` test suites (`tests/`), data dictionaries, and audit documents under `docs/`. On the `main` branch, the primary weekly milestones and analyses are driven by the Jupyter Notebooks and compiled PDF reports under `Weekly_reports/`.

---

## 5. Dataset Description

The repository contains several verified tabular datasets across raw and processed directories:

| Dataset Path | Records | Columns | Description & Intended Usage |
| :--- | :---: | :---: | :--- |
| **`data/processed/unified_property_dataset_jammu.csv`** | 1,200 | 71 | **Master Consolidated Dataset**: Merges property listings, JDA planning status, RERA compliance, JMC civic indicators, Revenue circle rates, OSM amenities, SDMA flood risk, and all 7 synopsis engineered variables. Intended for model training and decision evaluation. |
| **`data/processed/integrated_listings_week3.csv`** | 1,200 | 49 | **Week 3 Integration Dataset**: Combines property records with JDA approvals, RERA scores, municipal metrics, and official circle rates. Includes the derived `asking_vs_circle_rate_ratio`. |
| **`data/processed/listings_cleaned.csv`** | 1,200 | 36 | **Cleaned Listings**: Standardized data types, validated boolean flags, verified mathematical total price calculations, and trimmed categorical fields. |
| **`data/raw/property_dataset_raw.csv`** | 1,200 | 36 | **Raw Preserved Property Data**: Curated baseline listings across 36 Jammu localities covering property dimensions, price per sqft, legal attributes, civic scores, and target recommendation labels. |
| **`data/raw/listings_99acres_raw.csv`** | 1,200 | 36 | Verified snapshot copy of property listings with recorded ingestion provenance. |
| **`Weekly_reports/synthetic_properties_raw.csv`** | 1,200 | 32 | Modeled baseline property dataset utilized in exploratory notebooks, containing simulation seed indicators (`Data_Generation_Seed`) and base attributes. |
| **`data/processed/jda_approvals_structured.csv`** | 36 | 10 | Official JDA scheme names, layout approval status (27 Approved, 8 Partially Approved, 1 Unapproved), notification references, and Master Plan 2032 zones. |
| **`data/processed/rera_projects_structured.csv`** | 13 | 12 | Developer compliance register profiling 13 builders (RERA registration numbers, on-time delivery %, complaints registered/resolved, and synthesized credibility scores). |
| **`data/processed/jmc_civic_structured.csv`** | 36 | 7 | Municipal ward numbers, piped water supply hours/day, sewer network coverage %, annual drainage complaints, and road condition indices. |
| **`data/processed/revenue_circle_rates_structured.csv`** | 36 | 6 | Official statutory circle rates per kanal (Lakh INR) and per sq ft (INR) across residential and commercial land for all 36 localities. |
| **`data/processed/locality_standardized_mapping.csv`** | 36 | 5 | Master canonical lookup table mapping the 36 localities to urban zones, tehsils, PIN codes, and spelling aliases. |
| **`data/processed/osm_amenities_jammu.csv`** | 36 | 8 | WGS-84 centroid coordinates (latitude, longitude), school counts, hospital counts, transit stops, and Haversine distances to Jewel Chowk and NH-44. |
| **`data/processed/sdma_flood_zones_jammu.csv`** | 36 | 6 | Environmental flood risk classifications (27 Low, 5 Medium, 4 High), drainage catchment profiles, and historic 2014 inundation depths. |

---

## 6. Data Sources and Acquisition Feasibility

The project references seven public and administrative data sources. Their documented roles and real-world accessibility statuses are as follows:

1. **99acres Property Listings (`99acres.com`)**:
   * *Role*: Pricing benchmarks, property types, super built-up areas, and basic configurations.
   * *Access Status & Limitation*: Automated direct web scraping is restricted by Cloudflare / PerimeterX bot defenses (`HTTP 403 Forbidden`). Terms of Service restrict bulk automated harvesting. The 1,200-record dataset serves as a curated snapshot representing published market listings across 36 localities.
2. **Jammu Development Authority (`jda.jk.gov.in`)**:
   * *Role*: Colony layout approvals, statutory sanctions, and Master Plan 2032 urban zoning classifications.
   * *Access Status*: Public portal accessible (`HTTP 200`). Official layout scheme notifications and Master Plan land-use classifications structured across all 36 localities.
3. **J&K Real Estate Regulatory Authority (`rera.jk.gov.in`)**:
   * *Role*: Statutory promoter registrations, active/delivered project tracking, and consumer complaints.
   * *Access Status*: Accessible (`HTTP 200`). Regulatory data for regional builders structured into objective compliance metrics.
4. **Jammu Municipal Corporation & Smart City Jammu (`jmcjammu.org` / `smartcities.gov.in`)**:
   * *Role*: Municipal ward infrastructure, piped drinking water supply schedules, sewerage coverage, and drainage complaints.
   * *Access Status*: Public urban service benchmarks and ward-level action plan disclosures compiled into structured tabular records.
5. **J&K Revenue and Registration Department (`landrecords.jk.gov.in` / `jammu.nic.in`)**:
   * *Role*: Official statutory circle rates (minimum valuation rates) for stamp duty and land registration.
   * *Access Status*: Direct portal probes experience intermittent network timeouts; official schedules extracted from published District Collector gazette notifications.
6. **OpenStreetMap (`openstreetmap.org`)**:
   * *Role*: Spatial points-of-interest (schools, hospitals, healthcare centers, bus/transit stops) and geographic centroid coordinates.
   * *Access Status*: Accessible (`HTTP 200`) under the Open Database License (ODbL 1.0). Features queried via Overpass API guidelines with proper attribution (`© OpenStreetMap contributors`).
7. **J&K State Disaster Management Authority (`jksdma.jk.gov.in`)**:
   * *Role*: Flood risk mapping, Tawi river basin catchment vulnerability, and low-lying drainage sump hazard classification.
   * *Access Status*: Accessible (`HTTP 200`). Risk levels digitized from District Disaster Management Plan (DDMP Jammu) flood inundation maps.

---

## 7. Data Engineering and Feature Engineering Pipeline

The technical pipeline implemented across Weeks 1–4 follows a systematic progression:

```
[Raw Listings & Synthetic Baseline]
               │
               ▼
   [1. Ingestion & Validation] ──────────► Schema verification, unique ID checks (JMU0001 - JMU1200)
               │
               ▼
   [2. Cleaning & Standardization] ─────► Type coercion, boolean normalization, mathematical price checks
               │
               ▼
   [3. Outlier Analysis & EDA] ─────────► IQR threshold analysis; Winsorization & log scaling in notebooks
               │
               ▼
   [4. Multi-Source Attribute Joins] ───► Relational joins with JDA schemes, RERA profiles, JMC metrics, Circle Rates
               │
               ▼
   [5. Geospatial & Hazard Mapping] ────► WGS-84 centroid mapping, Haversine distance calculations, SDMA zoning
               │
               ▼
   [6. Advanced Feature Engineering] ───► Computation of the 7 Synopsis Engineered Variables
               │
               ▼
[Master Unified Dataset (1,200 x 71)]
```

### The 7 Synopsis Engineered Variables

The following seven engineered indicators are documented for the unified property dataset at `data/processed/unified_property_dataset_jammu.csv`.

**1. `price_vs_locality_type` — Locality-Level Price Fairness**

**Formula:** `Asking price per sq ft / Median asking price per sq ft for the same locality and property type`

**Range:** 0.551–1.742

Measures whether a property is priced below or above the median for comparable properties in its locality.

**2. `price_vs_type` — Citywide Price Fairness**

**Formula:** `Asking price per sq ft / Citywide median asking price per sq ft for the same property type`

**Range:** 0.384–2.164

Measures relative pricing fairness compared with the same property type across Jammu.

**3. `growth_momentum` — Growth Acceleration**

**Formula:** `Forecast 3-year growth percentage - Past 5-year growth percentage`

**Range:** -10.8% to +14.6%

Compares projected growth with historical growth. Its final derivation depends on the availability and validity of the forecasting-related inputs.

**4. `legal_clarity_index` — Legal and Documentation Clarity**

**Formula:** `0.35 × RegDeed + 0.25 × JDA + 0.25 × BankLoan + 0.15 × Freehold`

**Range:** 0.020–1.000

Combines registered-deed status, JDA approval, bank-loan eligibility, and freehold ownership indicators into a composite index.

**5. `amenity_access_index` — Amenity Accessibility**

**Formula:** `0.25 × Schools + 0.25 × Hospitals + 0.25 × Transit + 0.25 × (1 - NormDist)`

**Range:** 0.184–0.892

Combines school access, hospital access, public-transit access, and normalized distance into an accessibility indicator.

**6. `civic_risk_index` — Civic and Environmental Risk**

**Formula:** `0.30 × Complaints + 0.30 × FloodRisk + 0.40 × UtilityDeficiencies`

**Range:** 0.114–0.884

Combines municipal complaints, flood risk, and utility deficiencies into a composite risk indicator.

**7. `locality_price_rank` — Locality Price Ranking**

**Formula:** `Percentile rank of the locality's median price per sq ft across the 36 canonical localities`

**Range:** 0.028–1.000

Indicates the relative price position of a locality compared with the other localities in the dataset.

**Implementation note:** These are the formulas and ranges documented in the project report. The presence of a formula or column does not independently establish that its values were correctly generated or validated. In particular, verify the inputs used for `growth_momentum` and the provenance of any builder or forecasting-related scores before describing their generating systems as operational.

---

## 8. Installation and Dependencies

### Prerequisites
* Python 3.10 or higher
* Jupyter Notebook / JupyterLab or VS Code with Python extension

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/vatsal038/Minor_Project_COM-711.git
cd Minor_Project_COM-711

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # On macOS/Linux
# venv\Scripts\activate        # On Windows

# 3. Install dependencies from requirements.txt
pip install -r requirements.txt
```

### Dependency Manifest (`requirements.txt`)
* **Core Data Science**: `pandas>=2.0.0`, `numpy>=1.24.0`, `scikit-learn>=1.3.0`, `scipy>=1.10.0`
* **Plotting & Exploration**: `matplotlib`, `seaborn` (utilized in notebooks)
* **Document Processing**: `python-docx>=1.1.0`, `pypdf>=5.0.0`
* **Web & HTTP**: `requests>=2.31.0`, `beautifulsoup4>=4.12.0`, `urllib3>=2.0.0`
* **Testing & Quality**: `pytest>=7.4.0`, `pytest-cov>=4.1.0`
* **Future Interface**: `streamlit>=1.30.0`

---

## 9. Execution Instructions

### Running the Analysis Notebooks
The analytical workflow is documented and executable in Jupyter:

```bash
# Launch Jupyter Notebook
jupyter notebook

# Recommended execution order:
# 1. Weekly_reports/minor project analysis.ipynb       (Week 2 EDA & Initial Preprocessing)
# 2. Weekly_reports/MINOR_PROJECT_ANALYSIS_WEEK3.ipynb (Week 3 Winsorization & Clean Transformers)
# 3. Weekly_reports/minor_project_analysis_week4.ipynb (Week 4 Feature Engineering & Verification)
```

### Inspecting Datasets via Python CLI
You can inspect the processed datasets directly from the terminal:

```bash
# Verify the Master Unified Dataset
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/unified_property_dataset_jammu.csv')
print(f'Unified Dataset: {df.shape[0]} records, {df.shape[1]} features')
print('Engineered Variables:', [c for c in df.columns if 'index' in c or 'vs' in c or 'momentum' in c or 'rank' in c])
"

# Inspect JDA approvals and Master Plan 2032 classifications
python3 -c "
import pandas as pd
df = pd.read_csv('data/processed/jda_approvals_structured.csv')
print(df[['locality', 'approval_status', 'master_plan_2032_zone']].head(10))
"
```

---

## 10. Testing and Validation

* **Notebook Validations**: In `Weekly_reports/minor_project_analysis_week4.ipynb`, cells 37–42 execute validation checks on column counts, missing values, and numerical ranges of the engineered features (`Price_vs_locality_type`, `Growth_momentum`, `Legal_clarity_index`, `Amenity_access_index`, `Civic_risk_index`, `Locality_price_rank`), verifying mathematical bounds and output shapes.
* **Mathematical Integrity Checks**:
  * Super built-up area and local Marla conversions adhere to the regional conversion factor ($1\text{ Marla} = 272.25\text{ sq ft}$, error $< 2.0\text{ sq ft}$).
  * Total price in Lakhs correlates with $(\text{Area} \times \text{Price per sqft}) \div 100,000$ (mean delta $< 0.005\text{ Lakh INR}$).
  * Constant reference year ($(\text{Year Built} + \text{Property Age}) = 2026$) holds across the dataset.
* **Automated Unit Tests**: The modular test suite (`test_raw_audit.py`, `test_cleaning.py`, `test_integration.py`, `test_geospatial.py`) maintained on the `feature/weeks-1-4-data-pipeline` branch verified 21 passing test cases covering schema consistency, locality sets, unit relationships, and boundary ranges.

---

## 11. Implementation Status

| Project Dimension | Component | Status | Implementation Details |
| :--- | :--- | :---: | :--- |
| **Data Ingestion** | 1,200 Property Records across 36 Localities | **Completed** | Stored in `data/raw/` and `data/processed/` with documented provenance. |
| **Data Cleaning** | Type Normalization & Boolean Formatting | **Completed** | Standardized booleans, validated price calculations, cleaned whitespace. |
| **Outlier Handling** | IQR Analysis & Winsorization | **Completed** | Outlier bounds calculated; Winsorization executed in Week 3/4 notebooks. |
| **JDA Planning** | Scheme Status & Master Plan 2032 | **Completed** | 36 localities categorized (27 Approved, 8 Partially Approved, 1 Unapproved). |
| **RERA Governance** | Developer Registrations & Complaints | **Completed** | 13 developer profiles structured with registration IDs and complaint counts. |
| **Civic Services** | JMC Piped Water, Sewerage & Roads | **Completed** | Ward-level water hours, sewerage %, and drainage complaint density mapped. |
| **Revenue Rates** | District Collector Circle Rates | **Completed** | Circle rates per kanal and sq ft integrated; asking vs. circle rate ratio derived. |
| **Geospatial Layer** | WGS-84 Centroids & OSM Amenities | **Completed** | 36 locality centroids geocoded; schools, hospitals, transit counts, Haversine distances. |
| **Hazard Zoning** | J&K SDMA Flood Risk Vulnerability | **Completed** | Classifications assigned (27 Low, 5 Medium, 4 High) based on Tawi basin profile. |
| **Feature Engineering** | 7 Synopsis Engineered Indicators | **Completed** | Calculated and verified in notebooks and consolidated unified dataset. |
| **Value Forecasting** | Ensemble Regression (RF, XGBoost, LGBM) | *Pending (Weeks 5–8)* | Data prepared; model training scheduled for future milestone. |
| **Buy-Worthiness** | Scoring Engine & Conformal Prediction | *Pending (Weeks 7–10)* | Conceptual formula defined; classifier training pending. |
| **RAG Agent** | Vector Store Builder Credibility Synthesis | *Pending (Weeks 9–12)* | Sentence-Transformers + FAISS retrieval agent pending development. |
| **Explainable AI** | SHAP Attributions & Bias Auditing | *Pending (Weeks 11–14)* | Feature contribution plots and locality parity audits planned. |
| **User Interface** | Client-Side Streamlit / JavaScript UI | *Pending (Weeks 13–16)* | Prototype layout prepared; functional application pending backend models. |

---

## 12. Weekly Reports and Project Documentation

The repository maintains formal technical progress reports and specifications:

* **[Abstract.docx](Abstract.docx)**: Official editable Word document specifying the project title, aim, background, abstract, and methodological architecture.
* **[Weekly_reports/WEEK_1.pdf](Weekly_reports/WEEK_1.pdf)**: 3-page formal report covering Week 1 milestones (Task ID: `COM71115-3`): Git repository environment setup, raw dataset audit findings, 7-source accessibility assessment, and data schema definition.
* **[Weekly_reports/Week_2.pdf](Weekly_reports/Week_2.pdf)**: 2-page progress report covering Week 2 milestones (Task ID: `COM71115-4`): Synthetic dataset preparation, 1,200 property records structuring across 36 localities, JDA layout approvals, and cleaning validation.
* **[Weekly_reports/WEEK_3.pdf](Weekly_reports/WEEK_3.pdf)**: 3-page formal report covering Week 3 milestones (Task ID: `COM71115-5`): Data acquisition from J&K RERA, municipal civic indicators from JMC/Smart City Jammu, Revenue Department circle rates, and multi-source integration.
* **Week 4 Milestone Report**: Data engineering for Week 4 (Task ID: `COM71115-6`) is documented via [Weekly_reports/minor_project_analysis_week4.ipynb](Weekly_reports/minor_project_analysis_week4.ipynb) and synthesized in [data/processed/unified_property_dataset_jammu.csv](data/processed/unified_property_dataset_jammu.csv). *(Written Week 4 PDF report compilation is scheduled for upcoming group submission).*
* **[data/image.png](data/image.png)**: High-resolution methodology flowchart illustrating the multi-stage system architecture from data collection through explainability.

---

## 13. Documented Limitations and Next Milestones

### Documented Limitations
1. **Locality-Centroid Geocoding**: Property listings do not include GPS latitude and longitude coordinates. Spatial distances to city center and highway corridors are calculated from WGS-84 locality centroids (`Locality_Centroid_WGS84`) rather than exact parcel boundaries.
2. **Commercial Portal Anti-Scraping**: Automated bulk harvesting on 99acres is restricted by Cloudflare bot management. The dataset utilizes a curated market snapshot representing published listings.
3. **No Trained Models in Current Phase**: The repository currently represents the foundational data engineering milestone (Weeks 1–4). No machine learning model weights, RAG vector embeddings, or user interfaces are claimed as completed.

### Upcoming Milestones (Weeks 5–8)
* Splitting the unified dataset into stratified training, validation, and holdout test partitions.
* Establishing baseline regressors (Linear Regression, Ridge) and tree-based ensembles (Random Forest, XGBoost, LightGBM) to forecast 1-, 3-, and 5-year property appreciation.
* Implementing target leakage guardrails (ensuring `price_per_sqft` is excluded from feature sets when predicting `total_price_lakh`).

---

## 14. Data Authenticity and Legal Disclaimer

> **Academic Research Disclaimer**: The structured CSV files, synthetic baselines, municipal benchmarks, JDA colony classifications, builder profiles, and circle rate tables contained in this repository are compiled strictly for academic and educational research under College Minor Project **COM-711**. 
> 
> Successful software execution, data standardization, and pipeline tests **do not independently certify the legal validity, title clarity, ownership status, non-encumbrance, or statutory building approval** of any specific real-world property or promoter in Jammu. Physical verification of Revenue Department sale deeds, non-encumbrance certificates, and on-site municipal clearances remains legally mandatory for any actual property transaction.
