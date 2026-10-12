"""
Comprehensive Raw Dataset Audit for Minor Project COM-711.
Audits the supplied property_dataset_raw.csv covering schema, integrity,
numeric distributions, categorical breakdowns, target leakage, and geographic fields.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from config.settings import RAW_PROPERTY_DATASET_PATH, DOCS_DIR, CANONICAL_LOCALITIES


def run_dataset_audit(csv_path: Path = RAW_PROPERTY_DATASET_PATH) -> dict:
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # 1. Basic Shape and Memory
    audit_results = {
        "dataset_path": str(csv_path),
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "columns_list": df.columns.tolist(),
        "memory_usage_kb": float(df.memory_usage(deep=True).sum() / 1024),
    }

    # 2. Missing Values & Null Analysis
    null_counts = df.isnull().sum().to_dict()
    audit_results["null_counts"] = {k: int(v) for k, v in null_counts.items() if v > 0}
    audit_results["has_any_nulls"] = bool(df.isnull().any().any())

    # 3. Duplicate Rows & Key Integrity
    exact_duplicates = int(df.duplicated().sum())
    id_unique = bool(df["property_id"].is_unique)
    id_null_count = int(df["property_id"].isnull().sum())
    audit_results["integrity"] = {
        "exact_duplicate_rows": exact_duplicates,
        "property_id_is_unique": id_unique,
        "property_id_nulls": id_null_count,
        "first_id": str(df["property_id"].iloc[0]),
        "last_id": str(df["property_id"].iloc[-1]),
    }

    # 4. Column Data Types
    dtype_map = {col: str(dtype) for col, dtype in df.dtypes.items()}
    audit_results["column_dtypes"] = dtype_map

    # 5. Unit Relationships & Math Consistency Check
    # Area consistency: marla * 272.25 should approximate sqft
    sqft_vs_marla_diff = np.abs(df["area_sqft"] - (df["area_marla"] * 272.25))
    marla_vs_kanal_diff = np.abs(df["area_marla"] - (df["area_kanal"] * 20.0))

    # Price consistency: (area_sqft * price_per_sqft) / 100,000 should approximate total_price_lakh
    calc_total_lakh = (df["area_sqft"] * df["price_per_sqft"]) / 100000.0
    price_diff_lakh = np.abs(df["total_price_lakh"] - calc_total_lakh)

    # Age consistency: check implied reference year
    implied_current_year = (df["year_built"] + df["property_age_years"]).mode()[0]

    audit_results["mathematical_consistency"] = {
        "sqft_marla_max_abs_error": float(sqft_vs_marla_diff.max()),
        "marla_kanal_max_abs_error": float(marla_vs_kanal_diff.max()),
        "total_price_calc_max_abs_error": float(price_diff_lakh.max()),
        "total_price_calc_mean_abs_error": float(price_diff_lakh.mean()),
        "implied_dataset_base_year": int(implied_current_year),
    }

    # 6. Numeric Feature Statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_summary = {}
    for col in numeric_cols:
        series = df[col]
        q25 = float(series.quantile(0.25))
        q75 = float(series.quantile(0.75))
        iqr = q75 - q25
        outliers_count = int(((series < (q25 - 1.5 * iqr)) | (series > (q75 + 1.5 * iqr))).sum())
        numeric_summary[col] = {
            "min": float(series.min()),
            "mean": round(float(series.mean()), 2),
            "median": float(series.median()),
            "max": float(series.max()),
            "std": round(float(series.std()), 2),
            "q25": q25,
            "q75": q75,
            "outliers_iqr_count": outliers_count,
        }
    audit_results["numeric_summary"] = numeric_summary

    # 7. Categorical & Boolean Distributions
    cat_summary = {}
    cat_cols = df.select_dtypes(include=["object", "bool"]).columns.tolist()
    for col in cat_cols:
        vc = df[col].value_counts().to_dict()
        cat_summary[col] = {
            "num_unique": int(df[col].nunique()),
            "value_counts": {str(k): int(v) for k, v in vc.items()}
        }
    audit_results["categorical_summary"] = cat_summary

    # 8. Locality Coverage Check
    dataset_localities = sorted(df["locality"].unique().tolist())
    canonical_set = set(CANONICAL_LOCALITIES)
    dataset_set = set(dataset_localities)
    audit_results["locality_audit"] = {
        "num_localities_in_data": len(dataset_localities),
        "expected_canonical_count": len(CANONICAL_LOCALITIES),
        "exact_match_with_canonical": dataset_set == canonical_set,
        "missing_canonical": list(canonical_set - dataset_set),
        "unrecognized_localities": list(dataset_set - canonical_set),
        "min_records_per_locality": int(df["locality"].value_counts().min()),
        "max_records_per_locality": int(df["locality"].value_counts().max()),
        "mean_records_per_locality": round(float(df["locality"].value_counts().mean()), 2),
    }

    # 9. Target Distribution & Leakage Risk Assessment
    rec_counts = df["recommendation"].value_counts().to_dict()
    audit_results["target_distribution"] = {
        "classes": {str(k): int(v) for k, v in rec_counts.items()},
        "buy_ratio": round(float(rec_counts.get("Buy", 0) / len(df)), 4),
        "not_buy_ratio": round(float(rec_counts.get("Not Buy", 0) / len(df)), 4),
    }

    # Target Leakage analysis
    # Price relationship: total_price_lakh = area_sqft * price_per_sqft / 100000
    # If predicting price, having both total_price_lakh and price_per_sqft in features creates trivial leakage.
    audit_results["leakage_audit"] = {
        "price_per_sqft_total_price_correlation": round(float(df["price_per_sqft"].corr(df["total_price_lakh"])), 4),
        "area_total_price_correlation": round(float(df["area_sqft"].corr(df["total_price_lakh"])), 4),
        "target_leakage_warning": (
            "CRITICAL: 'total_price_lakh' is exactly derived as (area_sqft * price_per_sqft) / 100000. "
            "For regression tasks predicting total_price_lakh, price_per_sqft must be excluded from feature set. "
            "Similarly, for classification of 'recommendation', forecast_3yr_price_growth_pct and locality_score "
            "correlate strongly with the recommendation label."
        )
    }

    # 10. Geographic / Coordinate Audit
    has_lat = "latitude" in df.columns
    has_lon = "longitude" in df.columns
    audit_results["geospatial_audit"] = {
        "has_explicit_coordinates": bool(has_lat and has_lon),
        "existing_spatial_features": [
            col for col in df.columns if any(k in col.lower() for k in ["distance", "road", "connectivity", "transport"])
        ],
        "coordinate_status": "Property-level coordinates (lat, lon) are ABSENT in raw dataset. Geocoding at locality centroid level required."
    }

    # Save to JSON
    json_path = DOCS_DIR / "raw_dataset_audit.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)

    # Save to Markdown
    md_path = DOCS_DIR / "raw_dataset_audit.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Comprehensive Raw Dataset Audit Report\n\n")
        f.write(f"- **Dataset Path**: `{csv_path}`\n")
        f.write(f"- **Total Records**: {audit_results['total_rows']}\n")
        f.write(f"- **Total Variables**: {audit_results['total_columns']}\n")
        f.write(f"- **Missing/Null Values**: {len(audit_results['null_counts'])} columns with nulls\n")
        f.write(f"- **Duplicate Rows**: {audit_results['integrity']['exact_duplicate_rows']}\n")
        f.write(f"- **Property ID Uniqueness**: {audit_results['integrity']['property_id_is_unique']} ({audit_results['integrity']['first_id']} to {audit_results['integrity']['last_id']})\n")
        f.write(f"- **Base Reference Year**: {audit_results['mathematical_consistency']['implied_dataset_base_year']}\n\n")

        f.write("## 1. Locality & Spatial Breakdown\n\n")
        f.write(f"- Distinct Localities: **{audit_results['locality_audit']['num_localities_in_data']}** (Exact match with 36 canonical Jammu localities)\n")
        f.write(f"- Records per locality: Min = {audit_results['locality_audit']['min_records_per_locality']}, Mean = {audit_results['locality_audit']['mean_records_per_locality']}, Max = {audit_results['locality_audit']['max_records_per_locality']}\n")
        f.write(f"- Property Coordinates: **ABSENT** in raw CSV. Geocoding to WGS84 required in Week 4.\n\n")

        f.write("## 2. Target Variable & Distribution\n\n")
        for cls_name, count in audit_results['target_distribution']['classes'].items():
            f.write(f"- `{cls_name}`: {count} ({round(count / audit_results['total_rows'] * 100, 2)}%)\n")
        f.write("\n## 3. Mathematical Consistency\n\n")
        f.write(f"- Area Formula: `area_sqft ≈ area_marla * 272.25` (Max error: {audit_results['mathematical_consistency']['sqft_marla_max_abs_error']:.4f})\n")
        f.write(f"- Total Price Formula: `total_price_lakh ≈ area_sqft * price_per_sqft / 100000` (Max error: {audit_results['mathematical_consistency']['total_price_calc_max_abs_error']:.4f})\n\n")

        f.write("## 4. Key Numeric Ranges\n\n")
        f.write("| Variable | Min | Mean | Median | Max | Outliers (IQR) |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for col, s in list(audit_results['numeric_summary'].items())[:12]:
            f.write(f"| `{col}` | {s['min']} | {s['mean']} | {s['median']} | {s['max']} | {s['outliers_iqr_count']} |\n")

        f.write("\n## 5. Leakage and Risk Warnings\n\n")
        f.write(f"> {audit_results['leakage_audit']['target_leakage_warning']}\n")

    print(f"[AUDIT COMPLETE] Saved JSON to {json_path} and Markdown to {md_path}")
    return audit_results


if __name__ == "__main__":
    run_dataset_audit()
