"""
Unit and Validation Tests for Week 1: Project Setup and Raw Dataset Audit.
"""

from pathlib import Path
import pandas as pd
import pytest
from config.settings import RAW_PROPERTY_DATASET_PATH, CANONICAL_LOCALITIES, DOCS_DIR
from src.audit.dataset_audit import run_dataset_audit


def test_raw_dataset_exists():
    assert RAW_PROPERTY_DATASET_PATH.exists(), f"Raw dataset missing at {RAW_PROPERTY_DATASET_PATH}"


def test_raw_dataset_dimensions_and_keys():
    df = pd.read_csv(RAW_PROPERTY_DATASET_PATH)
    assert df.shape == (1200, 36), f"Expected (1200, 36), got {df.shape}"
    assert "property_id" in df.columns
    assert df["property_id"].is_unique, "property_id column must contain strictly unique values"
    assert df["property_id"].iloc[0] == "JMU0001"
    assert df["property_id"].iloc[-1] == "JMU1200"


def test_canonical_localities_coverage():
    df = pd.read_csv(RAW_PROPERTY_DATASET_PATH)
    localities_in_data = set(df["locality"].unique())
    canonical_set = set(CANONICAL_LOCALITIES)
    assert len(localities_in_data) == 36, f"Expected 36 localities, got {len(localities_in_data)}"
    assert localities_in_data == canonical_set, "Locality set must match canonical list exactly"


def test_area_unit_conversions():
    df = pd.read_csv(RAW_PROPERTY_DATASET_PATH)
    # Marla to sqft conversion in Jammu: 1 Marla = 272.25 sqft
    sqft_calc = df["area_marla"] * 272.25
    error = (df["area_sqft"] - sqft_calc).abs()
    # Allowing small rounding variance (< 2.0 sqft due to floating point rounding in source)
    assert (error < 2.0).all(), "area_sqft must mathematically correspond to area_marla * 272.25"


def test_price_calculation_consistency():
    df = pd.read_csv(RAW_PROPERTY_DATASET_PATH)
    # total_price_lakh = (area_sqft * price_per_sqft) / 100,000
    calc_total = (df["area_sqft"] * df["price_per_sqft"]) / 100000.0
    diff = (df["total_price_lakh"] - calc_total).abs()
    assert (diff < 0.1).all(), "total_price_lakh must be consistent with area_sqft * price_per_sqft / 100000"


def test_audit_execution_and_reports():
    audit = run_dataset_audit(RAW_PROPERTY_DATASET_PATH)
    assert audit["total_rows"] == 1200
    assert audit["total_columns"] == 36
    assert (DOCS_DIR / "raw_dataset_audit.json").exists()
    assert (DOCS_DIR / "raw_dataset_audit.md").exists()
    assert (DOCS_DIR / "data_source_register.json").exists()
    assert (DOCS_DIR / "data_dictionary.json").exists()
