# Real Estate Price Prediction AI – Jammu Property Buy-Worthiness Assessment

A privacy-preserving decision-support tool that evaluates **one property in Jammu that you are considering**: is it fairly priced, is it worth buying, what might it be worth in 1, 3 and 5 years, and what are the red flags. It assesses a property you supply; it does not recommend listings.

**Live demo:** https://miet-realestatepricepredictioai-19.streamlit.app/
**Repository:** https://github.com/Richavij19/MIET-realestatepricepredictio.ai

> 7th-semester minor project, MIET. Decision support only – not financial, legal or valuation advice.

## Contents
1. [Quick facts](#quick-facts) · 2. [What the system does](#what-the-system-does) · 3. [Dataset](#dataset) · 4. [The 35 variables](#the-35-variables) · 5. [Models](#models) · 6. [Buy-Worthiness Score](#buy-worthiness-score) · 7. [Evaluation](#evaluation) · 8. [Privacy and architecture](#privacy-and-architecture) · 9. [Using the app](#using-the-app) · 10. [Run locally](#run-locally) · 11. [Project structure](#project-structure) · 12. [Limitations](#limitations) · 13. [Future work](#future-work)

## Quick facts

| Item | Value |
|---|---|
| Location | Jammu, India (36 localities) |
| Records | 1,200 (development dataset – see [Dataset](#dataset)) |
| Property types | Apartment/Flat 347 · Independent House 386 · Plot 377 · Commercial 90 |
| Price range | ₹8.85 – 302.17 lakh (mean ₹77.24 L, median ₹68.76 L, SD ₹46.20 L) |
| Model variables | 35 (28 base + 7 engineered) |
| Verdicts | Buy / Maybe / Not Buy, with confidence |
| Valuation accuracy (offline 5-fold CV) | R² ≈ 0.92, MAE ≈ ₹9.4 lakh, MAPE ≈ 12.8% |
| Privacy | User inputs are processed in the browser and are not uploaded |

## What the system does

- **Fair-value estimate** for the property, and the gap between the asking price and fair value.
- **Buy-Worthiness Score (0–100)** with a Buy / Maybe / Not Buy verdict, confidence, the top contributing factors and any red flags (power-of-attorney sale, mutation pending, non-JDA colony, flood risk, missing utilities).
- **1-, 3- and 5-year value scenarios** with an uncertainty band. The data is a single snapshot, so these are scenario estimates, not time-series forecasts.
- **Builder-credibility report** from a local retrieval-augmented (RAG) agent over public documents, with a cited source for each claim.
- **Locality explorer, property comparison and model transparency** tabs (see [Using the app](#using-the-app)).

## Dataset

**File:** `property_dataset.csv` – 1,200 rows × 36 columns (ID, 34 attributes, 1 label). No missing values, no duplicate IDs. Internal checks pass: total price = area × price per sq ft (max error ₹0.02 lakh); marla = sq ft ÷ 272.25.

**Provenance:** [TEAM TO COMPLETE – state exactly how the records were produced (manually recorded sample / generated or simulated with a documented script / combination), the dates, and how the Buy / Not Buy label was assigned. Do not describe the data as "verified listings" unless that is exactly what it is. Portal content must not be copied or redistributed without the portal's written consent.]

| Property type | Count | Mean price | Price range |
|---|---|---|---|
| Apartment/Flat | 347 | ₹80.9 L | ₹13.7 – 238.1 L |
| Independent House | 386 | ₹83.2 L | ₹12.8 – 212.0 L |
| Plot | 377 | ₹54.8 L | ₹8.8 – 156.8 L |
| Commercial | 90 | ₹131.7 L | ₹34.6 – 302.2 L |

**Label:** Buy 297 (25%) / Not Buy 903 (75%). The Maybe class comes from the score bands below.

**36 localities:** Bagh-e-Bahu, Bahu Plaza, Bakshi Nagar, Bantalab, Bari Brahmana, Bathindi, Bhagwati Nagar, Channi Himmat, Digiana, Domana, Gandhi Nagar, Gangyal, Gole Market, Greater Kailash Jammu, Janipur, Jewel Chowk, Kunjwani, Marh, Miran Sahib, Muthi, Nagrota, Nanak Nagar, Paloura, Panjtirthi, Rajpura, Rehari, Roop Nagar, Sainik Colony, Sarwal, Satwari, Shastri Nagar, Sidhra, Sunjwan, Talab Tillo, Trikuta Nagar, Vijaypur.

**Public sources for enrichment and refresh**

| # | Source | Used for | Status |
|---|---|---|---|
| S1 | J&K RERA (rera.jk.gov.in) | builder credibility, legal risk | portal public; export method to test |
| S2 | Jammu Development Authority | `jda_approved`, infrastructure | availability to confirm |
| S3 | Jammu Municipal Corporation / Smart City data | civic complaints, water, sewerage | to confirm |
| S4 | J&K Revenue / Registration (circle rates) | price benchmark, past growth | to confirm |
| S5 | OpenStreetMap (ODbL) | schools, hospitals, transport, distances | open |
| S6 | Flood-hazard layers | `flood_risk` | to confirm |
| S7 | Census of India | locality inputs | published |
| S8 | Public news, consumer-forum and court text on builders | RAG evidence | open pages only |

## The 35 variables

The CSV has 34 attribute columns. Four are unit duplicates or restatements (`area_marla`, `area_kanal`, `price_per_marla_lakh`, `year_built`) and are dropped. Two are prediction targets (`total_price_lakh`, `forecast_3yr_price_growth_pct`). That leaves **28 base variables**; **7 engineered variables** bring the total to **35**. (After one-hot encoding of `locality` and `builder_name` the design matrix has more than 35 columns.)

| Group | Variables | No. |
|---|---|---|
| Property | `property_type`, `area_sqft`, `price_per_sqft`, `property_age_years`, `corner_plot`, `facing_direction`, `road_width_ft` | 7 |
| Location and access | `locality`, `distance_to_city_center_km`, `distance_to_highway_km`, `locality_score`, `infrastructure_score`, `road_connectivity_score`, `public_transport_score` | 7 |
| Amenities | `nearby_schools_count`, `nearby_hospitals_count` | 2 |
| Legal and builder | `ownership_type`, `registry_type`, `jda_approved`, `bank_loan_approved`, `builder_name`, `builder_credibility_score` | 6 |
| Civic and utilities | `civic_complaints_count`, `flood_risk`, `electricity_connection`, `sewage_connection`, `water_supply_score` | 5 |
| Market history | `past_5yr_price_growth_pct` | 1 |
| **Engineered** | `price_vs_locality_type`, `price_vs_type`, `growth_momentum`, `legal_clarity_index`, `amenity_access_index`, `civic_risk_index`, `locality_price_rank` | 7 |

Actual ranges in the data: area 451–3,199 sq ft; price per sq ft ₹1,312–11,158; distance to centre 0.5–24.8 km; builder score 3.0–10.0; civic complaints 0–15; schools 0–12; hospitals 0–8; past growth −6% to +16%; forecast growth −5.8% to +22.3%.

**Leakage control:** price and price per sq ft never predict each other; the score uses out-of-fold predicted growth, not the recorded forecast column; medians and scalers are fitted inside each training fold. Both growth columns are treated as annualised percentages (to be confirmed).

## Models

| Task | Models | Output |
|---|---|---|
| Fair value | Random Forest, XGBoost, LightGBM ensemble (weights fitted on out-of-fold predictions); Ridge and a locality-type median as baselines | price per sq ft → total price |
| Growth | Same ensemble; split-conformal intervals | annual growth with 80% band |
| Verdict check | Gradient-boosted classifier compared with the transparent score | probability; disagreement lowers confidence |
| Builder credibility | Sentence-Transformer embeddings + FAISS/Chroma over public documents, fixed rubric | 0–10 score with citations |
| Explanations | SHAP (tree models), pillar-contribution chart | top-5 reasons |

Forecast formulas: `V1 = V0(1+g)`, `V3 = V0(1+g)^3`, `V5 = V0(1+g5)^5`, with `g5 = 0.5·g + 0.5·past 5-yr growth`.

## Buy-Worthiness Score

`BWS = 100 × Σ weight × pillar` where each pillar is a 0–1 index.

| Pillar | Weight | Built from |
|---|---|---|
| Location and infrastructure | 0.30 | locality, infrastructure, roads, transport, distance to centre, schools, hospitals |
| Price value | 0.22 | asking price per sq ft vs the median of the same type (citywide and in the same locality) |
| Growth outlook | 0.22 | predicted 3-yr growth, past 5-yr growth, momentum |
| Civic and risk | 0.14 | complaints, flood risk, water, sewage, electricity |
| Legal and builder | 0.12 | registry type, ownership, JDA approval, loan eligibility, builder credibility |

**Knock-out rules:** power-of-attorney registry or State-Land lease without JDA approval → at best Maybe; high flood risk with no sewage, or no electricity with water score below 3 → Not Buy.
**Thresholds:** BWS ≥ 62 Buy · 55 – 62 Maybe · < 55 Not Buy. **Confidence** = 1 − exp(−d/4), where d is the distance in points to the nearest threshold.
Reference implementation: `bws_scoring.py`.

## Evaluation

Offline evaluation, 5-fold cross-validation, scikit-learn stand-ins for the boosted models. Final figures will use the full XGBoost/LightGBM ensemble.

| Valuation (total price) | R² | MAE (₹ lakh) | RMSE (₹ lakh) | MAPE |
|---|---|---|---|---|
| Naive locality-type median | 0.915 | 9.1 | – | – |
| Ridge | 0.919 | 9.4 | 13.1 | 13.1% |
| Random Forest | 0.918 | 9.3 | 13.2 | 12.6% |
| Gradient boosting (HistGB) | 0.910 | 9.8 | 13.8 | 13.3% |
| RF + gradient boosting ensemble | 0.917 | 9.4 | 13.3 | 12.8% |

Unseen-locality validation: R² 0.909, MAE ₹9.9 lakh. Growth model: R² ≈ 0.37, MAE ≈ 2.5 percentage points. Verdict vs dataset label: AUC ≈ 0.75. Weight sensitivity (±20%): verdict unchanged for 94% of properties on average.

Error by property type (MAPE): Apartment 11.6% · House 12.2% · Commercial 12.5% · Plot 14.5%.

| Price band (₹ lakh) | Count | MAPE |
|---|---|---|
| 0–30 | 165 | 13.8% |
| 30–50 | 235 | 13.5% |
| 50–80 | 321 | 12.8% |
| 80–120 | 270 | 12.4% |
| 120+ | 209 | 11.4% |

**Reading these results honestly:** on this dataset the ensemble matches, but does not clearly beat, a simple locality-type median, so its main value is explanations and generalisation checks. Growth is only moderately predictable, and the Buy / Not Buy label plateaus near AUC 0.75 whatever the method. R² is not "accuracy"; the earlier README's "92% accuracy" wording has been removed.

## Privacy and architecture

Training runs offline in Python. Coefficients and tree tables are exported to JavaScript and run in the browser, so property details entered by the user are not uploaded. The page still loads libraries (Chart.js, Leaflet, PapaParse) and map tiles over the network, and the Streamlit demo is a hosting wrapper; none of these receive user inputs.

```
Offline:  CSV + public sources -> preprocessing -> models, BWS weights, RAG index
Export:   coefficients / tree tables / pillar tables -> index.html
Browser:  user inputs -> features -> fair value, growth, BWS, reasons -> display
```

Stack: Python, Pandas, NumPy, scikit-learn, XGBoost, LightGBM, SHAP, Sentence-Transformers, FAISS/Chroma; Streamlit wrapper; vanilla JavaScript, Chart.js 4.4.1, Leaflet.js 1.9.4, PapaParse 5.4.1.

## Using the app

<!-- VERIFY each tab below against the deployed app before publishing -->
1. **BUY** – enter property details (type, locality, area, age, builder, infrastructure, utilities, legal status). Output: fair value, asking-price gap, BWS, verdict, confidence, reasons, red flags, scenarios.
2. **EXPLORE** – map and scorecards for the 36 localities: prices, growth, civic and amenity indicators.
3. **COMPARE** – side-by-side comparison of up to 5 properties.
4. **MODEL** – feature importance, model comparison, training-data statistics and the score definition.
5. **HOW IT WORKS** – guide, variable glossary, limitations.

## Run locally

```bash
git clone https://github.com/Richavij19/MIET-realestatepricepredictio.ai.git
cd MIET-realestatepricepredictio.ai
pip install -r requirements.txt
streamlit run streamlit_app.py
# open http://localhost:8501
python bws_scoring.py property_dataset.csv   # reproduce score evaluation
```

Deployment: Streamlit Community Cloud (current) or GitHub Pages for the static `index.html`.

## Project structure

```
README.md · streamlit_app.py · requirements.txt · index.html · property_dataset.csv
bws_scoring.py            # Buy-Worthiness Score reference implementation
docs/ABSTRACT.md          # project abstract
.streamlit/config.toml · .github/workflows/pages.yml
```

## Limitations

- Development dataset: the origin and label rule must be read from the Provenance note above; results on real, independently collected listings may differ.
- Single snapshot: growth and 1-, 3-, 5-year values are scenarios, not forecasts of a time series.
- Growth is moderately predictable (R² ≈ 0.37); the label is partly noisy.
- Commercial (n = 90) and plots (higher error) have less reliable estimates.
- Not a legal title check: always verify registry, mutation, JDA approval and builder records independently.

## Future work

1. Replace development values with real public-source values (S1–S8) and validate on at least 100 independently collected listings.
2. Builder RAG agent over J&K RERA and public documents, with human-rater validation.
3. Quality-of-Life Index per locality (air quality, noise, traffic, crime, water and electricity reliability, hospital proximity, registry activity).
4. Extension to other cities.

## License and acknowledgements

MIT License – see `LICENSE`. Libraries: Chart.js, Leaflet.js, PapaParse, Streamlit, scikit-learn, XGBoost, LightGBM, SHAP. Map data © OpenStreetMap contributors.

*Last updated: October 2026.*
