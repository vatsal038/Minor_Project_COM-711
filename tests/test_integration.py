"""
Unit Tests for Week 3: RERA, JMC, Revenue Circle Rates, and Integration Pipeline.
"""

import pandas as pd
import pytest
from config.settings import (
    RERA_STRUCTURED_PATH, JMC_STRUCTURED_PATH,
    REVENUE_STRUCTURED_PATH, LOCALITY_MAPPING_PATH,
    PROCESSED_DATA_DIR, DOCS_DIR
)


def test_rera_dataset():
    assert RERA_STRUCTURED_PATH.exists()
    df = pd.read_csv(RERA_STRUCTURED_PATH)
    assert len(df) >= 12
    assert "builder_name" in df.columns
    assert "rera_registration_no" in df.columns
    assert "synthesized_credibility_score" in df.columns
    assert (df["synthesized_credibility_score"] >= 1.0).all() and (df["synthesized_credibility_score"] <= 10.0).all()


def test_jmc_civic_dataset():
    assert JMC_STRUCTURED_PATH.exists()
    df = pd.read_csv(JMC_STRUCTURED_PATH)
    assert len(df) == 36
    assert "ward_number" in df.columns
    assert "water_supply_hrs_per_day" in df.columns
    assert (df["water_supply_hrs_per_day"] >= 0).all()


def test_revenue_circle_rates_dataset():
    assert REVENUE_STRUCTURED_PATH.exists()
    df = pd.read_csv(REVENUE_STRUCTURED_PATH)
    assert len(df) == 36
    assert "residential_circle_rate_lakh_per_kanal" in df.columns
    assert "circle_rate_per_sqft" in df.columns
    assert (df["circle_rate_per_sqft"] > 0).all()


def test_locality_standardized_mapping():
    assert LOCALITY_MAPPING_PATH.exists()
    df = pd.read_csv(LOCALITY_MAPPING_PATH)
    assert len(df) == 36
    assert "canonical_locality" in df.columns
    assert "pin_code" in df.columns


def test_week3_integrated_dataset():
    integrated_path = PROCESSED_DATA_DIR / "integrated_listings_week3.csv"
    assert integrated_path.exists()
    df = pd.read_csv(integrated_path)
    assert len(df) == 1200
    assert "asking_vs_circle_rate_ratio" in df.columns
    assert "rera_credibility_score" in df.columns
    assert "jda_scheme_name" in df.columns
    assert (df["asking_vs_circle_rate_ratio"] > 0).all()
    assert (DOCS_DIR / "week3_integration_report.json").exists()
