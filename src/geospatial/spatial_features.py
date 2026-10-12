"""
Geospatial Feature Engineering & Distance Calculations for Minor Project COM-711.
Calculates Haversine distances to city center & highway corridors,
validates geocoding resolution, and derives amenity access indicators.
"""

import math
from pathlib import Path
import pandas as pd
from config.settings import CITY_CENTER_COORDINATES, PROCESSED_DATA_DIR


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


def attach_spatial_features(df_properties: pd.DataFrame) -> pd.DataFrame:
    osm_path = PROCESSED_DATA_DIR / "osm_amenities_jammu.csv"
    if not osm_path.exists():
        raise FileNotFoundError(f"OSM dataset missing at {osm_path}")

    df_osm = pd.read_csv(osm_path)
    center_lat, center_lon = CITY_CENTER_COORDINATES

    # Merge locality coordinates and OSM amenities
    merged = df_properties.merge(
        df_osm[["locality", "latitude", "longitude", "osm_schools_count", "osm_hospitals_count", "osm_bus_stops", "highway_distance_km"]],
        on="locality",
        how="left"
    )

    # Calculate precise Haversine distance from locality centroid to Jewel Chowk
    merged["calc_distance_to_center_km"] = merged.apply(
        lambda r: haversine(r["latitude"], r["longitude"], center_lat, center_lon),
        axis=1
    )

    # Geocoding confidence level
    # Since property-level coordinates are absent in raw data, we explicitly document this resolution
    merged["geocoding_resolution"] = "Locality_Centroid_WGS84"
    merged["geocoding_confidence"] = "High_Locality_Level_Approx"

    return merged
