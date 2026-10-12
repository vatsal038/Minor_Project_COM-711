"""
Unit Tests for Week 4: Geospatial Processing, SDMA Flood Hazards, and Unified Dataset.
"""

import pandas as pd
import pytest
from config.settings import (
    OSM_AMENITIES_PATH, SDMA_FLOOD_ZONES_PATH,
    UNIFIED_DATASET_PATH, DOCS_DIR
)


def test_osm_dataset_integrity():
    assert OSM_AMENITIES_PATH.exists()
    df = pd.read_csv(OSM_AMENITIES_PATH)
    assert len(df) == 36
    assert "latitude" in df.columns
    assert "longitude" in df.columns
    assert (df["latitude"] >= 32.50).all() and (df["latitude"] <= 32.85).all()
    assert (df["longitude"] >= 74.70).all() and (df["longitude"] <= 75.10).all()


def test_sdma_flood_hazard_dataset():
    assert SDMA_FLOOD_ZONES_PATH.exists()
    df = pd.read_csv(SDMA_FLOOD_ZONES_PATH)
    assert len(df) == 36
    assert "flood_risk_level" in df.columns
    assert set(df["flood_risk_level"].unique()).issubset({"Low", "Medium", "High"})


def test_unified_dataset_dimensions():
    assert UNIFIED_DATASET_PATH.exists()
    df = pd.read_csv(UNIFIED_DATASET_PATH)
    assert len(df) == 1200
    assert df["property_id"].is_unique


def test_seven_engineered_variables_presence_and_bounds():
    df = pd.read_csv(UNIFIED_DATASET_PATH)
    engineered_cols = [
        "price_vs_locality_type",
        "price_vs_type",
        "growth_momentum",
        "legal_clarity_index",
        "amenity_access_index",
        "civic_risk_index",
        "locality_price_rank"
    ]
    for col in engineered_cols:
        assert col in df.columns, f"Engineered column {col} missing in unified dataset"

    # Index bounds checks [0.0, 1.0]
    assert (df["legal_clarity_index"] >= 0.0).all() and (df["legal_clarity_index"] <= 1.0).all()
    assert (df["amenity_access_index"] >= 0.0).all() and (df["amenity_access_index"] <= 1.0).all()
    assert (df["civic_risk_index"] >= 0.0).all() and (df["civic_risk_index"] <= 1.0).all()
    assert (df["locality_price_rank"] >= 0.0).all() and (df["locality_price_rank"] <= 1.0).all()

    # Ratio positivity
    assert (df["price_vs_locality_type"] > 0).all()
    assert (df["price_vs_type"] > 0).all()


def test_week4_reports_exist():
    assert (DOCS_DIR / "week4_geospatial_unified_report.json").exists()
    assert (DOCS_DIR / "week4_geospatial_unified_report.md").exists()
    assert (DOCS_DIR / "osm_ingestion_metadata.json").exists()
    assert (DOCS_DIR / "sdma_ingestion_metadata.json").exists()
