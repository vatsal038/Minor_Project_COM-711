"""
Unit Tests for Week 2: Listings Ingestion, JDA Records, and Cleaning Pipeline.
"""

import pandas as pd
import pytest
from config.settings import (
    CLEANED_PROPERTY_DATASET_PATH, JDA_STRUCTURED_PATH,
    DOCS_DIR, RAW_DATA_DIR
)


def test_cleaned_dataset_exists_and_shape():
    assert CLEANED_PROPERTY_DATASET_PATH.exists()
    df = pd.read_csv(CLEANED_PROPERTY_DATASET_PATH)
    assert len(df) == 1200
    assert df["property_id"].is_unique


def test_jda_approvals_dataset():
    assert JDA_STRUCTURED_PATH.exists()
    df_jda = pd.read_csv(JDA_STRUCTURED_PATH)
    assert len(df_jda) == 36
    assert "locality" in df_jda.columns
    assert "approval_status" in df_jda.columns
    assert "master_plan_2032_zone" in df_jda.columns
    assert set(df_jda["approval_status"].unique()).issubset({"Approved", "Partially Approved", "Unapproved / Agrarian"})


def test_boolean_typing():
    df = pd.read_csv(CLEANED_PROPERTY_DATASET_PATH)
    for col in ["jda_approved", "bank_loan_approved", "corner_plot", "electricity_connection", "sewage_connection"]:
        assert df[col].dtype == bool or set(df[col].unique()).issubset({True, False})


def test_numeric_ranges_and_positivity():
    df = pd.read_csv(CLEANED_PROPERTY_DATASET_PATH)
    assert (df["area_sqft"] > 0).all()
    assert (df["price_per_sqft"] > 0).all()
    assert (df["total_price_lakh"] > 0).all()
    assert (df["property_age_years"] >= 0).all()


def test_cleaning_reports_exist():
    assert (DOCS_DIR / "week2_cleaning_report.json").exists()
    assert (DOCS_DIR / "week2_cleaning_report.md").exists()
    assert (DOCS_DIR / "jda_ingestion_metadata.json").exists()
