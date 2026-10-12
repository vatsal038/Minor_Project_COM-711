"""
Central configuration settings and project paths for Minor Project COM-711.
AI-Based Property Buy Worthiness Assessment and Property Value Forecasting System.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"
REPORTS_DIR = PROJECT_ROOT / "weekly_reports"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

# Ensure runtime directories exist
for path in [RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, DOCS_DIR, REPORTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# File Paths
RAW_PROPERTY_DATASET_PATH = RAW_DATA_DIR / "property_dataset_raw.csv"
CLEANED_PROPERTY_DATASET_PATH = PROCESSED_DATA_DIR / "listings_cleaned.csv"
JDA_STRUCTURED_PATH = PROCESSED_DATA_DIR / "jda_approvals_structured.csv"
RERA_STRUCTURED_PATH = PROCESSED_DATA_DIR / "rera_projects_structured.csv"
JMC_STRUCTURED_PATH = PROCESSED_DATA_DIR / "jmc_civic_structured.csv"
REVENUE_STRUCTURED_PATH = PROCESSED_DATA_DIR / "revenue_circle_rates_structured.csv"
LOCALITY_MAPPING_PATH = PROCESSED_DATA_DIR / "locality_standardized_mapping.csv"
OSM_AMENITIES_PATH = PROCESSED_DATA_DIR / "osm_amenities_jammu.csv"
SDMA_FLOOD_ZONES_PATH = PROCESSED_DATA_DIR / "sdma_flood_zones_jammu.csv"
UNIFIED_DATASET_PATH = PROCESSED_DATA_DIR / "unified_property_dataset_jammu.csv"

# Study Area Parameters
STUDY_CITY = "Jammu"
STUDY_STATE = "Jammu & Kashmir"
CITY_CENTER_COORDINATES = (32.7266, 74.8570)  # Jewel Chowk / Old City Jammu
STUDY_BBOX = {
    "min_lat": 32.55,
    "max_lat": 32.85,
    "min_lon": 74.70,
    "max_lon": 75.05,
}

# Unit Conversion Constants
SQFT_PER_MARLA = 272.25
MARLA_PER_KANAL = 20.0
SQFT_PER_KANAL = 5445.0

# Canonical Localities (36 levels in Jammu dataset)
CANONICAL_LOCALITIES = [
    "Bagh-e-Bahu", "Bahu Plaza", "Bakshi Nagar", "Bantalab", "Bari Brahmana",
    "Bathindi", "Bhagwati Nagar", "Channi Himmat", "Digiana", "Domana",
    "Gandhi Nagar", "Gangyal", "Gole Market", "Greater Kailash Jammu", "Janipur",
    "Jewel Chowk", "Kunjwani", "Marh", "Miran Sahib", "Muthi",
    "Nagrota", "Nanak Nagar", "Paloura", "Panjtirthi", "Rajpura",
    "Rehari", "Roop Nagar", "Sainik Colony", "Sarwal", "Satwari",
    "Shastri Nagar", "Sidhra", "Sunjwan", "Talab Tillo", "Trikuta Nagar", "Vijaypur"
]
