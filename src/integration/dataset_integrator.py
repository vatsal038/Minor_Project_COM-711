"""
Unified Property Dataset Integrator for Minor Project COM-711 (Week 4).
Synthesizes all acquired data layers (Listings, JDA, RERA, JMC, Revenue, OSM, SDMA),
computes the 7 synopsis engineered variables, and exports the unified dataset.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from config.settings import (
    CLEANED_PROPERTY_DATASET_PATH, JDA_STRUCTURED_PATH,
    RERA_STRUCTURED_PATH, JMC_STRUCTURED_PATH,
    REVENUE_STRUCTURED_PATH, OSM_AMENITIES_PATH,
    SDMA_FLOOD_ZONES_PATH, UNIFIED_DATASET_PATH,
    DOCS_DIR, CITY_CENTER_COORDINATES
)
from src.geospatial.spatial_features import attach_spatial_features


def build_unified_dataset() -> pd.DataFrame:
    print("Building unified property dataset for Jammu...")

    # 1. Load Cleaned Base Listings (1,200 records)
    df = pd.read_csv(CLEANED_PROPERTY_DATASET_PATH)

    # 2. Attach Spatial & Geocoding Features (OSM)
    df = attach_spatial_features(df)

    # 3. Attach JDA Layout Schemes
    df_jda = pd.read_csv(JDA_STRUCTURED_PATH)
    df = df.merge(
        df_jda[["locality", "jda_scheme_name", "approval_status", "master_plan_2032_zone"]],
        on="locality",
        how="left"
    ).rename(columns={"approval_status": "jda_scheme_approval"})

    # 4. Attach J&K RERA Builder Compliance Records
    df_rera = pd.read_csv(RERA_STRUCTURED_PATH)
    df = df.merge(
        df_rera[["builder_name", "rera_registration_no", "registration_status", "on_time_delivery_pct", "synthesized_credibility_score"]],
        on="builder_name",
        how="left"
    ).rename(columns={
        "registration_status": "rera_registration_status",
        "synthesized_credibility_score": "rera_credibility_score"
    })

    # 5. Attach JMC Civic & Infrastructure Records
    df_jmc = pd.read_csv(JMC_STRUCTURED_PATH)
    df = df.merge(
        df_jmc[["locality", "ward_number", "water_supply_hrs_per_day", "sewer_coverage_pct", "drainage_complaints_per_year", "road_condition_index"]],
        on="locality",
        how="left"
    )

    # 6. Attach Revenue Circle Rates
    df_rev = pd.read_csv(REVENUE_STRUCTURED_PATH)
    df = df.merge(
        df_rev[["locality", "residential_circle_rate_lakh_per_kanal", "circle_rate_per_sqft"]],
        on="locality",
        how="left"
    )

    # 7. Attach SDMA Flood Hazard Zones
    df_sdma = pd.read_csv(SDMA_FLOOD_ZONES_PATH)
    df = df.merge(
        df_sdma[["locality", "flood_risk_level", "basin_name", "elevation_profile", "historic_inundation_depth_m"]],
        on="locality",
        how="left"
    )

    # -------------------------------------------------------------
    # 8. Compute the 7 Synopsis Engineered Variables
    # -------------------------------------------------------------

    # Variable 29: Price_vs_locality_type
    # Asking price ÷ median of same type in same locality
    locality_type_medians = df.groupby(["locality", "property_type"])["price_per_sqft"].transform("median")
    df["price_vs_locality_type"] = (df["price_per_sqft"] / locality_type_medians).round(3)

    # Variable 30: Price_vs_type
    # Asking price ÷ citywide median of same type
    type_medians = df.groupby("property_type")["price_per_sqft"].transform("median")
    df["price_vs_type"] = (df["price_per_sqft"] / type_medians).round(3)

    # Variable 31: Growth_momentum
    # Forecast growth − past growth
    df["growth_momentum"] = (df["forecast_3yr_price_growth_pct"] - df["past_5yr_price_growth_pct"]).round(2)

    # Variable 32: Legal_clarity_index
    # Registry, ownership, JDA, loan eligibility (Range [0.0, 1.0])
    def calc_legal_clarity(row):
        score = 0.0
        # Registry weight = 0.35
        if row["registry_type"] == "Registered Sale Deed":
            score += 0.35
        elif row["registry_type"] == "Mutation Pending":
            score += 0.15
        elif "Power of Attorney" in row["registry_type"]:
            score += 0.05
        # JDA approval weight = 0.25
        if row["jda_approved"] == True:
            score += 0.25
        # Bank loan approved weight = 0.25
        if row["bank_loan_approved"] == True:
            score += 0.25
        # Ownership type weight = 0.15
        if row["ownership_type"] == "Freehold":
            score += 0.15
        elif row["ownership_type"] == "Leasehold":
            score += 0.10
        elif "State Land" in row["ownership_type"]:
            score += 0.02
        return round(score, 3)

    df["legal_clarity_index"] = df.apply(calc_legal_clarity, axis=1)

    # Variable 33: Amenity_access_index
    # Schools, hospitals, transport, distance to centre (Range [0.0, 1.0])
    s_min, s_max = df["nearby_schools_count"].min(), df["nearby_schools_count"].max()
    h_min, h_max = df["nearby_hospitals_count"].min(), df["nearby_hospitals_count"].max()
    t_min, t_max = df["public_transport_score"].min(), df["public_transport_score"].max()
    d_min, d_max = df["distance_to_city_center_km"].min(), df["distance_to_city_center_km"].max()

    norm_schools = (df["nearby_schools_count"] - s_min) / (s_max - s_min)
    norm_hospitals = (df["nearby_hospitals_count"] - h_min) / (h_max - h_min)
    norm_transport = (df["public_transport_score"] - t_min) / (t_max - t_min)
    norm_inv_dist = 1.0 - ((df["distance_to_city_center_km"] - d_min) / (d_max - d_min))

    df["amenity_access_index"] = (
        0.25 * norm_schools + 0.25 * norm_hospitals + 0.25 * norm_transport + 0.25 * norm_inv_dist
    ).round(3)

    # Variable 34: Civic_risk_index
    # Complaints, flood, water, sewage, electricity (Range [0.0, 1.0], Higher = higher risk)
    c_min, c_max = df["civic_complaints_count"].min(), df["civic_complaints_count"].max()
    norm_complaints = (df["civic_complaints_count"] - c_min) / (c_max - c_min)

    flood_risk_map = {"Low": 0.1, "Medium": 0.5, "High": 0.9}
    flood_scale = df["flood_risk"].map(flood_risk_map).fillna(0.3)

    w_min, w_max = df["water_supply_score"].min(), df["water_supply_score"].max()
    norm_water_deficiency = 1.0 - ((df["water_supply_score"] - w_min) / (w_max - w_min))

    sewage_deficiency = df["sewage_connection"].map({True: 0.0, False: 1.0})
    electricity_deficiency = df["electricity_connection"].map({True: 0.0, False: 1.0})

    df["civic_risk_index"] = (
        0.30 * norm_complaints +
        0.30 * flood_scale +
        0.15 * norm_water_deficiency +
        0.15 * sewage_deficiency +
        0.10 * electricity_deficiency
    ).round(3)

    # Variable 35: Locality_price_rank
    # Locality median price percentile rank across all 36 Jammu localities [0.0, 1.0]
    loc_medians = df.groupby("locality")["price_per_sqft"].median()
    loc_percentiles = loc_medians.rank(pct=True).to_dict()
    df["locality_price_rank"] = df["locality"].map(loc_percentiles).round(3)

    # Also compute asking vs circle rate ratio
    df["asking_vs_circle_rate_ratio"] = (df["price_per_sqft"] / df["circle_rate_per_sqft"]).round(2)

    # 9. Save Unified Dataset
    UNIFIED_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(UNIFIED_DATASET_PATH, index=False)
    print(f"[UNIFIED DATASET COMPLETE] Successfully generated {UNIFIED_DATASET_PATH} with {len(df)} rows and {len(df.columns)} columns.")

    # 10. Generate Integration Report
    eng_summary = {}
    for ev in ["price_vs_locality_type", "price_vs_type", "growth_momentum", "legal_clarity_index", "amenity_access_index", "civic_risk_index", "locality_price_rank", "asking_vs_circle_rate_ratio"]:
        eng_summary[ev] = {
            "min": float(df[ev].min()),
            "mean": round(float(df[ev].mean()), 3),
            "median": float(df[ev].median()),
            "max": float(df[ev].max()),
            "std": round(float(df[ev].std()), 3),
        }

    report = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_properties": len(df),
        "total_columns": len(df.columns),
        "columns_list": df.columns.tolist(),
        "localities_covered": int(df["locality"].nunique()),
        "seven_engineered_variables": eng_summary,
        "geocoding_audit": {
            "geocoded_resolution": "Locality_Centroid_WGS84",
            "coverage_pct": 100.0,
            "min_distance_to_center_km": float(df["calc_distance_to_center_km"].min()),
            "max_distance_to_center_km": float(df["calc_distance_to_center_km"].max()),
        },
        "flood_hazard_audit": df["flood_risk_level"].value_counts().to_dict(),
        "integration_provenance": {
            "listings_source": "99acres Curated Jammu Listings (1,200 records)",
            "jda_source": "Jammu Development Authority Master Plan 2032 (36 schemes)",
            "rera_source": "J&K RERA Project Registration & Builder History (13 builders)",
            "jmc_source": "Jammu Municipal Corporation Civic Ward Infrastructure (36 localities)",
            "revenue_source": "J&K Revenue Dept & District Collector Circle Rates 2024",
            "osm_source": "OpenStreetMap WGS84 Centroids & Amenity Counts",
            "sdma_source": "J&K SDMA Flood Hazard Atlas & Catchment Zoning",
        }
    }

    with open(DOCS_DIR / "week4_geospatial_unified_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open(DOCS_DIR / "week4_geospatial_unified_report.md", "w", encoding="utf-8") as f:
        f.write("# Week 4 Geospatial Processing & Unified Dataset Report\n\n")
        f.write(f"- **Execution Timestamp**: {report['execution_timestamp']}\n")
        f.write(f"- **Total Unified Records**: {report['total_properties']}\n")
        f.write(f"- **Total Variables in Unified Schema**: {report['total_columns']}\n")
        f.write(f"- **Unified File Path**: `{UNIFIED_DATASET_PATH}`\n\n")

        f.write("## 1. Synopsis 7 Engineered Variables Summary\n\n")
        f.write("| Variable Name | Min | Mean | Median | Max | Std Dev |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for ev, s in eng_summary.items():
            f.write(f"| `{ev}` | {s['min']} | {s['mean']} | {s['median']} | {s['max']} | {s['std']} |\n")

        f.write("\n## 2. Geospatial & Hazard Coverage\n\n")
        f.write(f"- Resolution: `{report['geocoding_audit']['geocoded_resolution']}`\n")
        f.write(f"- Distance to City Center (km): Min = {report['geocoding_audit']['min_distance_to_center_km']}, Max = {report['geocoding_audit']['max_distance_to_center_km']}\n")
        f.write("- Flood Risk Zones: " + ", ".join([f"{k}: {v}" for k, v in report['flood_hazard_audit'].items()]) + "\n\n")

        f.write("## 3. Data Provenance Summary\n\n")
        for k, v in report["integration_provenance"].items():
            f.write(f"- **{k}**: {v}\n")

    return df


if __name__ == "__main__":
    build_unified_dataset()
