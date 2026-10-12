# Canonical Data Dictionary & Schema Specification

- **Project**: AI-Based Property Buy Worthiness Assessment (COM-711)
- **Total Schema Variables**: 42 (28 Base + 7 Engineered + 7 Supporting/Derived)

| Canonical Field Name | Type | Unit | Status | Source Dataset | Missing Policy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`property_id`** | `string` | ID (JMUxxxx) | `Observed` | Supplied Curated Dataset (99acres derived) | Mandatory primary key; reject recor... |
| **`property_type`** | `categorical (string)` | None (Apartment/Flat, Independent House, Plot, Commercial) | `Observed` | 99acres Listings | Impute with mode of locality or fla... |
| **`area_sqft`** | `float` | sq ft | `Observed` | 99acres Listings | Compute from area_marla if availabl... |
| **`area_marla`** | `float` | Marla | `Derived` | Revenue Records / Listings | Compute from area_sqft... |
| **`area_kanal`** | `float` | Kanal | `Derived` | Revenue Records / Listings | Compute from area_marla... |
| **`price_per_sqft`** | `float` | INR / sq ft | `Observed` | 99acres Listings | Derive from total_price_lakh and ar... |
| **`price_per_marla_lakh`** | `float` | Lakh INR / Marla | `Derived` | Derived from Listings | Compute from price_per_sqft... |
| **`total_price_lakh`** | `float` | Lakh INR | `Observed` | 99acres Listings | Derive from price_per_sqft * area_s... |
| **`property_age_years`** | `integer` | Years | `Observed` | Listings / Municipal Tax Records | Compute from year_built; if plot se... |
| **`corner_plot`** | `boolean` | True / False | `Observed` | 99acres Listings / Layout Map | Default to False... |
| **`facing_direction`** | `categorical (string)` | Compass (East, West, North, South, North-East, South-West) | `Observed` | 99acres Listings | Impute with mode (East/North-East) ... |
| **`road_width_ft`** | `integer` | Feet | `Observed` | JDA Layouts / Listings / OSM | Median road width by locality and p... |
| **`locality`** | `categorical (string)` | Name (36 Jammu Localities) | `Observed` | Listings / JDA / Revenue Records | Mandatory geographic anchor; drop o... |
| **`distance_to_city_center_km`** | `float` | Kilometers (km) | `Derived / Observed` | OpenStreetMap / Geocoded Centroid | Recalculate from locality centroid ... |
| **`distance_to_highway_km`** | `float` | Kilometers (km) | `Derived / Observed` | OpenStreetMap Road Network | Compute from OSM highway vector lin... |
| **`locality_score`** | `float` | Score (1.0 - 10.0) | `Observed` | Market Survey / 99acres Locality Insights | Locality mean score... |
| **`infrastructure_score`** | `float` | Score (1.0 - 10.0) | `Observed` | JMC & Smart City Jammu records | Locality mean... |
| **`road_connectivity_score`** | `float` | Score (1.0 - 10.0) | `Observed` | JDA / PWD / OSM Road Network | Locality median... |
| **`public_transport_score`** | `float` | Score (1.0 - 10.0) | `Observed` | JMC Transport / OSM Bus Stops | Locality median... |
| **`nearby_schools_count`** | `integer` | Count | `Observed` | OpenStreetMap (amenity=school) | Locality median count from OSM... |
| **`nearby_hospitals_count`** | `integer` | Count | `Observed` | OpenStreetMap (amenity=hospital/clinic) | Locality median count from OSM... |
| **`ownership_type`** | `categorical (string)` | Freehold, Leasehold, State Land (Lease) | `Observed` | Revenue Department / Registry | Mode by locality; high risk if Stat... |
| **`registry_type`** | `categorical (string)` | Registered Sale Deed, Power of Attorney (GPA), Mutation Pending | `Observed` | Revenue & Sub-Registrar Records | Default to 'Mutation Pending' if un... |
| **`jda_approved`** | `boolean` | True / False | `Observed` | JDA Approved Colony Registers | False if unverified in JDA approved... |
| **`bank_loan_approved`** | `boolean` | True / False | `Observed` | Bank Approved Project List (SBI/JK Bank) | Derived as False if registry is GPA... |
| **`builder_name`** | `categorical (string)` | Entity Name | `Observed` | 99acres / RERA Registrations | Categorize as 'Local Individual Sel... |
| **`builder_credibility_score`** | `float` | Score (1.0 - 10.0) | `Observed / Synthesized` | J&K RERA / RAG Synthesis | Default to 5.0 (neutral baseline) f... |
| **`civic_complaints_count`** | `integer` | Count | `Observed` | JMC Citizen Grievance Portal | Locality median count... |
| **`flood_risk`** | `categorical (string)` | Low, Medium, High | `Observed` | J&K SDMA Flood Hazard Atlas | Classify by locality baseline; Low ... |
| **`electricity_connection`** | `boolean` | True / False | `Observed` | JPDCL Municipal Records | Default to True for urban Jammu loc... |
| **`sewage_connection`** | `boolean` | True / False | `Observed` | JMC / UEED Sewerage Project Maps | Locality ward infrastructure mappin... |
| **`water_supply_score`** | `float` | Score (1.0 - 10.0) | `Observed` | Jal Shakti Dept / JMC | Locality mean score... |
| **`past_5yr_price_growth_pct`** | `float` | Percentage (%) | `Observed` | Market Index / Circle Rate Delta | Locality mean growth rate... |
| **`forecast_3yr_price_growth_pct`** | `float` | Percentage (%) | `Observed in raw / Target in modeling` | Market Forecast / Regression Ensemble Output | Target field; do not impute arbitra... |
| **`recommendation`** | `categorical (string)` | Buy / Not Buy | `Observed (Target label)` | Decision Engine Output | Target label; reject record if miss... |
| **`price_vs_locality_type`** | `float` | Ratio (>1 = premium, <1 = bargain) | `Engineered` | Engineered from Listings | Default to 1.0 if locality-type med... |
| **`price_vs_type`** | `float` | Ratio | `Engineered` | Engineered from Listings | Default to 1.0... |
| **`growth_momentum`** | `float` | Percentage point difference (%) | `Engineered` | Engineered from Market History | Default to 0.0... |
| **`legal_clarity_index`** | `float` | Index [0.0, 1.0] | `Engineered` | Engineered from Legal Attributes | Default to 0.0 (conservative legal ... |
| **`amenity_access_index`** | `float` | Index [0.0, 1.0] | `Engineered` | Engineered from Amenities & OSM | Locality mean index... |
| **`civic_risk_index`** | `float` | Index [0.0, 1.0] (Higher = higher risk) | `Engineered` | Engineered from Civic & SDMA attributes | Locality mean index... |
| **`locality_price_rank`** | `float` | Percentile [0.0, 1.0] | `Engineered` | Engineered from Locality Medians | Median percentile (0.50)... |


## Variable-by-Variable Specifications

### `property_id`
- **Description**: Unique alphanumeric identifier for property record in Jammu dataset
- **Data Type**: `string` | **Unit**: ID (JMUxxxx)
- **Status**: `Observed` | **Source Field**: `property_id`
- **Source Dataset**: Supplied Curated Dataset (99acres derived)
- **Derivation Method**: Sequential prefix formatting (JMU0001 - JMU1200)
- **Missing Value Policy**: Mandatory primary key; reject record if null or duplicate
- **Join Key / Level**: Primary Key (property level)

### `property_type`
- **Description**: Classification of property asset
- **Data Type**: `categorical (string)` | **Unit**: None (Apartment/Flat, Independent House, Plot, Commercial)
- **Status**: `Observed` | **Source Field**: `property_type`
- **Source Dataset**: 99acres Listings
- **Derivation Method**: Direct listing extraction; standard category mapping
- **Missing Value Policy**: Impute with mode of locality or flag as Unknown
- **Join Key / Level**: Composite key with locality

### `area_sqft`
- **Description**: Super built-up / plot area in square feet
- **Data Type**: `float` | **Unit**: sq ft
- **Status**: `Observed` | **Source Field**: `area_sqft`
- **Source Dataset**: 99acres Listings
- **Derivation Method**: Observed or converted from area_marla * 272.25
- **Missing Value Policy**: Compute from area_marla if available; else median by property_type
- **Join Key / Level**: N/A

### `area_marla`
- **Description**: Area in local land measurement unit Marla (1 Marla = 272.25 sq ft in Jammu)
- **Data Type**: `float` | **Unit**: Marla
- **Status**: `Derived` | **Source Field**: `area_marla`
- **Source Dataset**: Revenue Records / Listings
- **Derivation Method**: area_sqft / 272.25
- **Missing Value Policy**: Compute from area_sqft
- **Join Key / Level**: N/A

### `area_kanal`
- **Description**: Area in regional land measurement unit Kanal (1 Kanal = 20 Marlas = 5,445 sq ft)
- **Data Type**: `float` | **Unit**: Kanal
- **Status**: `Derived` | **Source Field**: `area_kanal`
- **Source Dataset**: Revenue Records / Listings
- **Derivation Method**: area_marla / 20.0
- **Missing Value Policy**: Compute from area_marla
- **Join Key / Level**: N/A

### `price_per_sqft`
- **Description**: Property unit asking price per square foot
- **Data Type**: `float` | **Unit**: INR / sq ft
- **Status**: `Observed` | **Source Field**: `price_per_sqft`
- **Source Dataset**: 99acres Listings
- **Derivation Method**: Listed unit price or (total_price_lakh * 100000) / area_sqft
- **Missing Value Policy**: Derive from total_price_lakh and area_sqft
- **Join Key / Level**: N/A

### `price_per_marla_lakh`
- **Description**: Unit asking price per Marla in Lakhs INR
- **Data Type**: `float` | **Unit**: Lakh INR / Marla
- **Status**: `Derived` | **Source Field**: `price_per_marla_lakh`
- **Source Dataset**: Derived from Listings
- **Derivation Method**: (price_per_sqft * 272.25) / 100000.0
- **Missing Value Policy**: Compute from price_per_sqft
- **Join Key / Level**: N/A

### `total_price_lakh`
- **Description**: Total asking price in Lakhs INR
- **Data Type**: `float` | **Unit**: Lakh INR
- **Status**: `Observed` | **Source Field**: `total_price_lakh`
- **Source Dataset**: 99acres Listings
- **Derivation Method**: (area_sqft * price_per_sqft) / 100000.0
- **Missing Value Policy**: Derive from price_per_sqft * area_sqft
- **Join Key / Level**: N/A

### `property_age_years`
- **Description**: Age of the property structure in years relative to base year 2026
- **Data Type**: `integer` | **Unit**: Years
- **Status**: `Observed` | **Source Field**: `property_age_years`
- **Source Dataset**: Listings / Municipal Tax Records
- **Derivation Method**: 2026 - year_built
- **Missing Value Policy**: Compute from year_built; if plot set to 0
- **Join Key / Level**: N/A

### `corner_plot`
- **Description**: Binary flag indicating whether property is situated on a corner plot
- **Data Type**: `boolean` | **Unit**: True / False
- **Status**: `Observed` | **Source Field**: `corner_plot`
- **Source Dataset**: 99acres Listings / Layout Map
- **Derivation Method**: Listing feature flag parsing
- **Missing Value Policy**: Default to False
- **Join Key / Level**: N/A

### `facing_direction`
- **Description**: Cardinal or intercardinal facing direction of main entrance
- **Data Type**: `categorical (string)` | **Unit**: Compass (East, West, North, South, North-East, South-West)
- **Status**: `Observed` | **Source Field**: `facing_direction`
- **Source Dataset**: 99acres Listings
- **Derivation Method**: Listing attribute extraction
- **Missing Value Policy**: Impute with mode (East/North-East) or Unknown
- **Join Key / Level**: N/A

### `road_width_ft`
- **Description**: Width of access road fronting the property in feet
- **Data Type**: `integer` | **Unit**: Feet
- **Status**: `Observed` | **Source Field**: `road_width_ft`
- **Source Dataset**: JDA Layouts / Listings / OSM
- **Derivation Method**: Listing specs or JDA layout sector plan
- **Missing Value Policy**: Median road width by locality and property type (typically 12-20 ft)
- **Join Key / Level**: N/A

### `locality`
- **Description**: Standardized geographic neighborhood in Jammu (36 canonical levels)
- **Data Type**: `categorical (string)` | **Unit**: Name (36 Jammu Localities)
- **Status**: `Observed` | **Source Field**: `locality`
- **Source Dataset**: Listings / JDA / Revenue Records
- **Derivation Method**: Canonical alias harmonization via lookup table
- **Missing Value Policy**: Mandatory geographic anchor; drop or geocode if missing
- **Join Key / Level**: Locality join key across JDA, JMC, SDMA, OSM, Revenue

### `distance_to_city_center_km`
- **Description**: Straight-line / road distance from property/locality to Jammu City Center (Jewel Chowk)
- **Data Type**: `float` | **Unit**: Kilometers (km)
- **Status**: `Derived / Observed` | **Source Field**: `distance_to_city_center_km`
- **Source Dataset**: OpenStreetMap / Geocoded Centroid
- **Derivation Method**: Haversine distance from centroid (lat, lon) to (32.7266, 74.8570)
- **Missing Value Policy**: Recalculate from locality centroid coordinates
- **Join Key / Level**: N/A

### `distance_to_highway_km`
- **Description**: Distance from property/locality to nearest National/State Highway (NH-44)
- **Data Type**: `float` | **Unit**: Kilometers (km)
- **Status**: `Derived / Observed` | **Source Field**: `distance_to_highway_km`
- **Source Dataset**: OpenStreetMap Road Network
- **Derivation Method**: Spatial distance calculation to NH-44 corridor segment
- **Missing Value Policy**: Compute from OSM highway vector line
- **Join Key / Level**: N/A

### `locality_score`
- **Description**: Aggregated locality desirability score based on demand and commercial infrastructure
- **Data Type**: `float` | **Unit**: Score (1.0 - 10.0)
- **Status**: `Observed` | **Source Field**: `locality_score`
- **Source Dataset**: Market Survey / 99acres Locality Insights
- **Derivation Method**: Composite index based on price trends and amenities
- **Missing Value Policy**: Locality mean score
- **Join Key / Level**: Locality level

### `infrastructure_score`
- **Description**: Composite score reflecting municipal roads, drainage, lighting, and power infrastructure
- **Data Type**: `float` | **Unit**: Score (1.0 - 10.0)
- **Status**: `Observed` | **Source Field**: `infrastructure_score`
- **Source Dataset**: JMC & Smart City Jammu records
- **Derivation Method**: Average of road, drainage, and utility readiness
- **Missing Value Policy**: Locality mean
- **Join Key / Level**: Locality level

### `road_connectivity_score`
- **Description**: Quality and lane capacity of road network connecting locality to arterial roads
- **Data Type**: `float` | **Unit**: Score (1.0 - 10.0)
- **Status**: `Observed` | **Source Field**: `road_connectivity_score`
- **Source Dataset**: JDA / PWD / OSM Road Network
- **Derivation Method**: Proximity to 4-lane corridors and internal access width
- **Missing Value Policy**: Locality median
- **Join Key / Level**: Locality level

### `public_transport_score`
- **Description**: Accessibility to Matador/bus routes, auto stands, and railway station
- **Data Type**: `float` | **Unit**: Score (1.0 - 10.0)
- **Status**: `Observed` | **Source Field**: `public_transport_score`
- **Source Dataset**: JMC Transport / OSM Bus Stops
- **Derivation Method**: Density of public transit stops within 1 km buffer
- **Missing Value Policy**: Locality median
- **Join Key / Level**: Locality level

### `nearby_schools_count`
- **Description**: Number of recognized primary and secondary schools within 2 km radius
- **Data Type**: `integer` | **Unit**: Count
- **Status**: `Observed` | **Source Field**: `nearby_schools_count`
- **Source Dataset**: OpenStreetMap (amenity=school)
- **Derivation Method**: Point-in-buffer spatial aggregation from OSM nodes
- **Missing Value Policy**: Locality median count from OSM
- **Join Key / Level**: Locality level

### `nearby_hospitals_count`
- **Description**: Number of hospitals, nursing homes, and primary health centres within 3 km radius
- **Data Type**: `integer` | **Unit**: Count
- **Status**: `Observed` | **Source Field**: `nearby_hospitals_count`
- **Source Dataset**: OpenStreetMap (amenity=hospital/clinic)
- **Derivation Method**: Point-in-buffer spatial aggregation from OSM healthcare nodes
- **Missing Value Policy**: Locality median count from OSM
- **Join Key / Level**: Locality level

### `ownership_type`
- **Description**: Tenure and title type of land ownership
- **Data Type**: `categorical (string)` | **Unit**: Freehold, Leasehold, State Land (Lease)
- **Status**: `Observed` | **Source Field**: `ownership_type`
- **Source Dataset**: Revenue Department / Registry
- **Derivation Method**: Revenue title classification
- **Missing Value Policy**: Mode by locality; high risk if State Land without lease deed
- **Join Key / Level**: N/A

### `registry_type`
- **Description**: Legal instrument of transfer / registration
- **Data Type**: `categorical (string)` | **Unit**: Registered Sale Deed, Power of Attorney (GPA), Mutation Pending
- **Status**: `Observed` | **Source Field**: `registry_type`
- **Source Dataset**: Revenue & Sub-Registrar Records
- **Derivation Method**: Document category at registration
- **Missing Value Policy**: Default to 'Mutation Pending' if unverified
- **Join Key / Level**: N/A

### `jda_approved`
- **Description**: Whether property/layout has statutory planning permission from Jammu Development Authority
- **Data Type**: `boolean` | **Unit**: True / False
- **Status**: `Observed` | **Source Field**: `jda_approved`
- **Source Dataset**: JDA Approved Colony Registers
- **Derivation Method**: Cross-match with JDA layout approval master gazette
- **Missing Value Policy**: False if unverified in JDA approved colony list
- **Join Key / Level**: Locality / Colony name join

### `bank_loan_approved`
- **Description**: Eligibility for retail home loans / mortgage financing from scheduled commercial banks
- **Data Type**: `boolean` | **Unit**: True / False
- **Status**: `Observed` | **Source Field**: `bank_loan_approved`
- **Source Dataset**: Bank Approved Project List (SBI/JK Bank)
- **Derivation Method**: Verification of title search clarity and building bye-law sanction
- **Missing Value Policy**: Derived as False if registry is GPA or State Land without JDA approval
- **Join Key / Level**: N/A

### `builder_name`
- **Description**: Name of developer, housing firm, or individual seller
- **Data Type**: `categorical (string)` | **Unit**: Entity Name
- **Status**: `Observed` | **Source Field**: `builder_name`
- **Source Dataset**: 99acres / RERA Registrations
- **Derivation Method**: Extracted from listing or project registration
- **Missing Value Policy**: Categorize as 'Local Individual Seller' if unnamed
- **Join Key / Level**: Builder join key with RERA registers

### `builder_credibility_score`
- **Description**: Reputational credibility rating derived from track record and RERA compliance
- **Data Type**: `float` | **Unit**: Score (1.0 - 10.0)
- **Status**: `Observed / Synthesized` | **Source Field**: `builder_credibility_score`
- **Source Dataset**: J&K RERA / RAG Synthesis
- **Derivation Method**: RAG synthesis based on past delivery timeliness, complaint count, and litigation
- **Missing Value Policy**: Default to 5.0 (neutral baseline) for unlisted individual sellers
- **Join Key / Level**: Builder name join

### `civic_complaints_count`
- **Description**: Reported municipal complaints regarding drainage, sanitation, or encroachment in locality
- **Data Type**: `integer` | **Unit**: Count
- **Status**: `Observed` | **Source Field**: `civic_complaints_count`
- **Source Dataset**: JMC Citizen Grievance Portal
- **Derivation Method**: Locality ward-level complaint frequency
- **Missing Value Policy**: Locality median count
- **Join Key / Level**: Locality level

### `flood_risk`
- **Description**: Environmental flood susceptibility zone classification
- **Data Type**: `categorical (string)` | **Unit**: Low, Medium, High
- **Status**: `Observed` | **Source Field**: `flood_risk`
- **Source Dataset**: J&K SDMA Flood Hazard Atlas
- **Derivation Method**: Spatial intersection of property locality with Tawi river flood maps
- **Missing Value Policy**: Classify by locality baseline; Low for elevated Jammu plateaus
- **Join Key / Level**: Locality / Spatial polygon

### `electricity_connection`
- **Description**: Availability of dedicated JPDCL grid electricity feeder line
- **Data Type**: `boolean` | **Unit**: True / False
- **Status**: `Observed` | **Source Field**: `electricity_connection`
- **Source Dataset**: JPDCL Municipal Records
- **Derivation Method**: Utility verification flag
- **Missing Value Policy**: Default to True for urban Jammu localities
- **Join Key / Level**: N/A

### `sewage_connection`
- **Description**: Availability of underground municipal sewerage network
- **Data Type**: `boolean` | **Unit**: True / False
- **Status**: `Observed` | **Source Field**: `sewage_connection`
- **Source Dataset**: JMC / UEED Sewerage Project Maps
- **Derivation Method**: Ward-level sewer master plan mapping
- **Missing Value Policy**: Locality ward infrastructure mapping
- **Join Key / Level**: Locality level

### `water_supply_score`
- **Description**: Piped tap water reliability score (Jal Shakti Department supply)
- **Data Type**: `float` | **Unit**: Score (1.0 - 10.0)
- **Status**: `Observed` | **Source Field**: `water_supply_score`
- **Source Dataset**: Jal Shakti Dept / JMC
- **Derivation Method**: Supply hours and pressure consistency rating
- **Missing Value Policy**: Locality mean score
- **Join Key / Level**: Locality level

### `past_5yr_price_growth_pct`
- **Description**: Historical compound annual capital appreciation rate over preceding 5 years
- **Data Type**: `float` | **Unit**: Percentage (%)
- **Status**: `Observed` | **Source Field**: `past_5yr_price_growth_pct`
- **Source Dataset**: Market Index / Circle Rate Delta
- **Derivation Method**: ((Price_2026 - Price_2021) / Price_2021) * 100
- **Missing Value Policy**: Locality mean growth rate
- **Join Key / Level**: Locality level

### `forecast_3yr_price_growth_pct`
- **Description**: Model / expert forecasted appreciation over subsequent 3 years
- **Data Type**: `float` | **Unit**: Percentage (%)
- **Status**: `Observed in raw / Target in modeling` | **Source Field**: `forecast_3yr_price_growth_pct`
- **Source Dataset**: Market Forecast / Regression Ensemble Output
- **Derivation Method**: Trend projection from past growth and infrastructure momentum
- **Missing Value Policy**: Target field; do not impute arbitrarily
- **Join Key / Level**: N/A

### `recommendation`
- **Description**: Ground truth investment suitability label
- **Data Type**: `categorical (string)` | **Unit**: Buy / Not Buy
- **Status**: `Observed (Target label)` | **Source Field**: `recommendation`
- **Source Dataset**: Decision Engine Output
- **Derivation Method**: Composite rule threshold based on buy-worthiness index
- **Missing Value Policy**: Target label; reject record if missing in training
- **Join Key / Level**: N/A

### `price_vs_locality_type`
- **Description**: Ratio of property asking price to median asking price of same property type in same locality
- **Data Type**: `float` | **Unit**: Ratio (>1 = premium, <1 = bargain)
- **Status**: `Engineered` | **Source Field**: `price_per_sqft`
- **Source Dataset**: Engineered from Listings
- **Derivation Method**: price_per_sqft / median(price_per_sqft for same locality & property_type)
- **Missing Value Policy**: Default to 1.0 if locality-type median unavailable
- **Join Key / Level**: N/A

### `price_vs_type`
- **Description**: Ratio of property asking price to citywide median asking price for same property type
- **Data Type**: `float` | **Unit**: Ratio
- **Status**: `Engineered` | **Source Field**: `price_per_sqft`
- **Source Dataset**: Engineered from Listings
- **Derivation Method**: price_per_sqft / citywide_median(price_per_sqft for same property_type)
- **Missing Value Policy**: Default to 1.0
- **Join Key / Level**: N/A

### `growth_momentum`
- **Description**: Differential between forecasted 3-year growth and historical 5-year growth
- **Data Type**: `float` | **Unit**: Percentage point difference (%)
- **Status**: `Engineered` | **Source Field**: `forecast_3yr_price_growth_pct, past_5yr_price_growth_pct`
- **Source Dataset**: Engineered from Market History
- **Derivation Method**: forecast_3yr_price_growth_pct - past_5yr_price_growth_pct
- **Missing Value Policy**: Default to 0.0
- **Join Key / Level**: N/A

### `legal_clarity_index`
- **Description**: Normalized composite index of title safety (JDA approval, registered deed, loan approval, freehold)
- **Data Type**: `float` | **Unit**: Index [0.0, 1.0]
- **Status**: `Engineered` | **Source Field**: `jda_approved, registry_type, ownership_type, bank_loan_approved`
- **Source Dataset**: Engineered from Legal Attributes
- **Derivation Method**: Weighted sum: 0.35*(registry=='Registered Sale Deed') + 0.25*jda_approved + 0.25*bank_loan_approved + 0.15*(ownership=='Freehold')
- **Missing Value Policy**: Default to 0.0 (conservative legal stance)
- **Join Key / Level**: N/A

### `amenity_access_index`
- **Description**: Normalized composite index of access to education, healthcare, transit, and city center
- **Data Type**: `float` | **Unit**: Index [0.0, 1.0]
- **Status**: `Engineered` | **Source Field**: `nearby_schools_count, nearby_hospitals_count, public_transport_score, distance_to_city_center_km`
- **Source Dataset**: Engineered from Amenities & OSM
- **Derivation Method**: Min-max normalized weighted combination of schools, hospitals, transit, and inverse distance
- **Missing Value Policy**: Locality mean index
- **Join Key / Level**: N/A

### `civic_risk_index`
- **Description**: Normalized composite index of civic liability (complaints, flood hazard, lack of water/sewer/power)
- **Data Type**: `float` | **Unit**: Index [0.0, 1.0] (Higher = higher risk)
- **Status**: `Engineered` | **Source Field**: `civic_complaints_count, flood_risk, water_supply_score, sewage_connection, electricity_connection`
- **Source Dataset**: Engineered from Civic & SDMA attributes
- **Derivation Method**: Weighted sum of normalized complaints, flood risk scale, and inverted utility scores
- **Missing Value Policy**: Locality mean index
- **Join Key / Level**: N/A

### `locality_price_rank`
- **Description**: Percentile rank of locality median price per sqft relative to all 36 Jammu localities
- **Data Type**: `float` | **Unit**: Percentile [0.0, 1.0]
- **Status**: `Engineered` | **Source Field**: `price_per_sqft, locality`
- **Source Dataset**: Engineered from Locality Medians
- **Derivation Method**: Locality median price percentile ranking across Jammu market
- **Missing Value Policy**: Median percentile (0.50)
- **Join Key / Level**: Locality level

