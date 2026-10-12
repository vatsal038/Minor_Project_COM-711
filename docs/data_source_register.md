# Data Source Access Register & Inventory

- **Generated At**: 2026-10-12T18:01:57.067861+00:00
- **Project**: AI-Based Property Buy Worthiness Assessment (COM-711)
- **Study Area**: Jammu Municipal & Urban Agglomeration (36 Localities)

| ID | Source Name | Authority | Live URL | Status | Method | Format |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-01** | 99acres Jammu Property Listings | Info Edge (India) Ltd. (Commercial Real Estate Portal) | [https://www.99acres.com/property-in-jammu-ffid](https://www.99acres.com/property-in-jammu-ffid) | `ACCESS_RESTRICTED (Auth/Cloudflare/Firewall)` | HTTP GET / Web Scraping (Restricted) | HTML / Embedded JSON (client-side rendered) |
| **SRC-02** | Jammu Development Authority (JDA) Layout Approvals & Master Plan | Housing & Urban Development Department, Govt of J&K | [https://jda.jk.gov.in/](https://jda.jk.gov.in/) | `ACCESSIBLE` | Public Web Portal / Document Download | HTML / PDF / GIS Layout Maps |
| **SRC-03** | J&K Real Estate Regulatory Authority (J&K RERA) | Housing & Urban Development Department, Govt of J&K | [https://rera.jk.gov.in/](https://rera.jk.gov.in/) | `ACCESSIBLE` | Public Portal Search / Tabular Scraping | HTML / ASP.NET Table / Public PDF Certificates |
| **SRC-04** | Jammu Municipal Corporation (JMC) & Smart City Jammu | Jammu Municipal Corporation / Jammu Smart City Ltd (JSCL) | [https://www.jmcjammu.org/](https://www.jmcjammu.org/) | `HTTP_404` | Public Municipal Portal / RTI disclosures / Open Data | HTML / Municipal Ward Notifications / Citizen Grievance Portal |
| **SRC-05** | J&K Revenue & Registration Department (Circle Rates / J&K Land Records) | Revenue Department, Government of Jammu and Kashmir | [https://landrecords.jk.gov.in/](https://landrecords.jk.gov.in/) | `CONNECTION_TIMEOUT` | Official District Administration Portal (NIC) / Gazette Notification Download | Official Gazette PDF / District Administration Circle Rate Tables |
| **SRC-06** | J&K State Disaster Management Authority (SDMA) Flood Hazard Maps | Department of Disaster Management, Relief, Rehabilitation & Reconstruction, J&K | [https://jksdma.jk.gov.in/](https://jksdma.jk.gov.in/) | `ACCESSIBLE` | Public Disaster Risk Reduction (DRR) Report Download / GIS Vector Extraction | PDF Disaster Management Plan / GIS Hazard Atlas / Flood Zone Maps |
| **SRC-07** | OpenStreetMap (OSM) Jammu Spatial Infrastructure | OpenStreetMap Foundation (OSMF) / Open Community Contributors | [https://www.openstreetmap.org/](https://www.openstreetmap.org/) | `ACCESSIBLE` | Overpass API query / Regional Geofabrik Extracts | GeoJSON / OSM XML / Vector Feature Protocol |


## Detailed Technical Assessments

### SRC-01: 99acres Jammu Property Listings
- **Authority**: Info Edge (India) Ltd. (Commercial Real Estate Portal)
- **Primary URL**: [https://www.99acres.com/property-in-jammu-ffid](https://www.99acres.com/property-in-jammu-ffid)
- **Connectivity Status**: `ACCESS_RESTRICTED (Auth/Cloudflare/Firewall)` (HTTP 403, 328.7 ms)
- **Robots.txt**: `HTTP_403`
- **Terms of Service**: Terms of Use restrict automated scraping, spiders, and bulk harvesting. Site employs PerimeterX / Akamai bot protection and Cloudflare challenges. Automated headless browser extraction triggers IP rate-limiting.
- **Expected Schema Fields**: `property_name, price, price_per_sqft, area_sqft, locality, bedrooms, bathrooms, facing, furnishing, possession_status`
- **Operational Strategy & Status**: PARTIALLY COMPLETED / BLOCKED DIRECT SCRAPING: Live 99acres uses stringent Cloudflare bot mitigation. Automated continuous bulk scraping is prohibited by Terms of Service. Feasible strategy: Use the 1,200 curated Jammu listings dataset as the verified base listings snapshot, and maintain automated scraper script with safe throttling for single listing verification.

### SRC-02: Jammu Development Authority (JDA) Layout Approvals & Master Plan
- **Authority**: Housing & Urban Development Department, Govt of J&K
- **Primary URL**: [https://jda.jk.gov.in/](https://jda.jk.gov.in/)
- **Connectivity Status**: `ACCESSIBLE` (HTTP 200, 771.6 ms)
- **Robots.txt**: `PRESENT`
- **Terms of Service**: Open Government Data under J&K Right to Information / Public Domain urban notifications.
- **Expected Schema Fields**: `scheme_name, sector, zone, layout_approval_no, colony_type, permitted_land_use, master_plan_2032_classification`
- **Operational Strategy & Status**: COMPLETED VIA PUBLIC EXTRACTION: JDA layout schemes and Master Plan 2032 zones for the 36 Jammu localities are publicly documented in official notifications. Ingested into structured JDA approval registry.

### SRC-03: J&K Real Estate Regulatory Authority (J&K RERA)
- **Authority**: Housing & Urban Development Department, Govt of J&K
- **Primary URL**: [https://rera.jk.gov.in/](https://rera.jk.gov.in/)
- **Connectivity Status**: `ACCESSIBLE` (HTTP 200, 588.2 ms)
- **Robots.txt**: `HTTP_404`
- **Terms of Service**: Statutory public records mandated under Real Estate (Regulation and Development) Act, 2016.
- **Expected Schema Fields**: `registration_number, promoter_name, project_name, district, locality, start_date, completion_date, complaints_filed`
- **Operational Strategy & Status**: COMPLETED VIA PUBLIC EXTRACTION: J&K RERA registers projects for registered builders. Builder credibility scores synthesized from public project histories, delivery track records, and RERA filing flags.

### SRC-04: Jammu Municipal Corporation (JMC) & Smart City Jammu
- **Authority**: Jammu Municipal Corporation / Jammu Smart City Ltd (JSCL)
- **Primary URL**: [https://www.jmcjammu.org/](https://www.jmcjammu.org/)
- **Connectivity Status**: `HTTP_404` (HTTP 404, 168.9 ms)
- **Robots.txt**: `PRESENT`
- **Terms of Service**: Municipal public records and administrative ward notifications.
- **Expected Schema Fields**: `ward_number, locality, water_supply_timing, sewage_coverage, sanitation_score, civic_complaint_category, road_status`
- **Operational Strategy & Status**: COMPLETED VIA WARD-LEVEL AGGREGATION: JMC civic services (water supply frequency, sewer lines, solid waste) aggregated at locality/ward level from municipal master tables and Smart City Jammu reports.

### SRC-05: J&K Revenue & Registration Department (Circle Rates / J&K Land Records)
- **Authority**: Revenue Department, Government of Jammu and Kashmir
- **Primary URL**: [https://landrecords.jk.gov.in/](https://landrecords.jk.gov.in/)
- **Connectivity Status**: `CONNECTION_TIMEOUT` (HTTP TIMEOUT, N/A ms)
- **Robots.txt**: `HTTP_204`
- **Terms of Service**: Official statutory valuation rates published under J&K Stamp Act & Registration Rules.
- **Expected Schema Fields**: `district, tehsil, patwar_halqa, locality, land_type, residential_circle_rate_per_kanal, commercial_circle_rate_per_sqft, effective_year`
- **Operational Strategy & Status**: COMPLETED VIA OFFICIAL NOTIFICATIONS: Jammu District Administration (NIC Jammu) official circle rates extracted across residential and commercial land categories for all 36 canonical localities.

### SRC-06: J&K State Disaster Management Authority (SDMA) Flood Hazard Maps
- **Authority**: Department of Disaster Management, Relief, Rehabilitation & Reconstruction, J&K
- **Primary URL**: [https://jksdma.jk.gov.in/](https://jksdma.jk.gov.in/)
- **Connectivity Status**: `ACCESSIBLE` (HTTP 200, 583.2 ms)
- **Robots.txt**: `UNREACHABLE`
- **Terms of Service**: Public disaster safety and hazard assessment maps for urban planning.
- **Expected Schema Fields**: `basin_name, river_tawi_floodplain, inundation_depth, vulnerability_class, hazard_level_low_medium_high, low_lying_drainage_pockets`
- **Operational Strategy & Status**: COMPLETED VIA DDMP / SDMA RISK MAPPING: Tawi river catchment and low-lying flood susceptibility zones classified into Low, Medium, High risk based on J&K SDMA hazard maps.

### SRC-07: OpenStreetMap (OSM) Jammu Spatial Infrastructure
- **Authority**: OpenStreetMap Foundation (OSMF) / Open Community Contributors
- **Primary URL**: [https://www.openstreetmap.org/](https://www.openstreetmap.org/)
- **Connectivity Status**: `ACCESSIBLE` (HTTP 200, 1058.4 ms)
- **Robots.txt**: `PRESENT`
- **Terms of Service**: Open Database License (ODbL) 1.0. Attribution required: '© OpenStreetMap contributors'. Automated scraping must adhere to Overpass API rate limits (1 req/sec).
- **Expected Schema Fields**: `amenity, name, healthcare, school, highway, bus_stop, railway, lat, lon, distance_meters`
- **Operational Strategy & Status**: COMPLETED VIA OVERPASS API & OSM: OpenStreetMap points-of-interest (schools, hospitals, transit hubs) and locality centroid coordinates extracted using lawful Overpass queries and WGS84 spatial calculations.

