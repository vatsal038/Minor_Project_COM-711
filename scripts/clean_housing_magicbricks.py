import os
import json
import re
import numpy as np
import pandas as pd
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'DATA')
CLEANED_DIR = os.path.join(DATA_DIR, 'cleaned')

DIRS = [
    os.path.join(CLEANED_DIR, 'residential'),
    os.path.join(CLEANED_DIR, 'commercial'),
    os.path.join(CLEANED_DIR, 'rental'),
    os.path.join(CLEANED_DIR, 'projects'),
    os.path.join(CLEANED_DIR, 'review'),
    os.path.join(CLEANED_DIR, 'removed'),
    os.path.join(CLEANED_DIR, 'reports')
]

for d in DIRS:
    os.makedirs(d, exist_ok=True)

# Administrative District Rules: Confirmed outside Jammu District
OUTSIDE_DISTRICT_RULES = [
    ('bari brahmana', 'SAMBA', "Locality 'Bari Brahmana' confirmed in Samba District"),
    ('bari brahamana', 'SAMBA', "Locality 'Bari Brahmana' confirmed in Samba District"),
    ('vijaypur', 'SAMBA', "Locality 'Vijaypur' confirmed in Samba District"),
    ('aiims vijaypur', 'SAMBA', "Locality 'AIIMS Vijaypur' confirmed in Samba District"),
    ('jakh', 'SAMBA', "Locality 'Jakh' confirmed in Samba District"),
    ('sarore', 'SAMBA', "Locality 'Sarore' confirmed in Samba District"),
    ('saror', 'SAMBA', "Locality 'Saror' confirmed in Samba District"),
    ('purmandal', 'SAMBA', "Locality 'Purmandal' confirmed in Samba District"),
    ('meen sarkar', 'SAMBA', "Locality 'Meen Sarkar' confirmed in Samba District"),
    ('samba', 'SAMBA', "Locality 'Samba' confirmed in Samba District"),
    ('ramgarh', 'SAMBA', "Locality 'Ramgarh' confirmed in Samba District"),
    ('swankha', 'SAMBA', "Locality 'Swankha' confirmed in Samba District"),
    ('lupin factories', 'SAMBA', "Locality 'Lupin Factories' confirmed in Samba District"),
    ('sidco factories', 'SAMBA', "Locality 'SIDCO Factories' confirmed in Samba District"),
    ('tarore', 'SAMBA', "Locality 'Tarore' confirmed in Samba District"),
    
    ('udhampur town', 'UDHAMPUR', "Locality 'Udhampur Town' confirmed in Udhampur District"),
    ('udhampur', 'UDHAMPUR', "Locality 'Udhampur' confirmed in Udhampur District"),
    ('omala', 'UDHAMPUR', "Locality 'Omala' confirmed in Udhampur District"),
    ('kaller himmat', 'UDHAMPUR', "Locality 'Kaller Himmat' confirmed in Udhampur District"),
    ('ramnagar', 'UDHAMPUR', "Locality 'Ramnagar' confirmed in Udhampur District"),
    
    ('katra', 'REASI', "Locality 'Katra' confirmed in Reasi District"),
    ('vaishno devi', 'REASI', "Locality 'Mata Vaishno Devi Katra' confirmed in Reasi District"),
    
    ('kathua', 'KATHUA', "Locality 'Kathua' confirmed in Kathua District"),
    ('hiranagar', 'KATHUA', "Locality 'Hiranagar' confirmed in Kathua District"),
    
    ('rajouri', 'RAJOURI', "Locality 'Rajouri' confirmed in Rajouri District"),
    ('nowshera', 'RAJOURI', "Locality 'Nowshera' confirmed in Rajouri District"),
    ('sunderbani', 'RAJOURI', "Locality 'Sunderbani' confirmed in Rajouri District"),
    
    ('bhaderwah', 'DODA', "Locality 'Bhaderwah' confirmed in Doda District")
]

# Canonical Locality Normalization Dictionary (Jammu District)
JAMMU_LOCALITY_MAP = {
    'channi himat': 'Channi Himmat',
    'channi himmat': 'Channi Himmat',
    'channi himmat sec 1-7': 'Channi Himmat',
    'channi': 'Channi Himmat',
    'bhatindi': 'Bathindi',
    'bathindi': 'Bathindi',
    'bathindi morh': 'Bathindi',
    'bahu plaza': 'Bahu Plaza',
    'bahuplaza': 'Bahu Plaza',
    'bahu plaza complex': 'Bahu Plaza',
    'bantalab': 'Bantalab',
    'bantalab road': 'Bantalab',
    'ban talab': 'Bantalab',
    'bantalab akhnoor road': 'Bantalab',
    'gandhi nagar': 'Gandhi Nagar',
    'gandhinagar': 'Gandhi Nagar',
    'gandhi nagar extension': 'Gandhi Nagar',
    'gangyal': 'Gangyal',
    'gangayal': 'Gangyal',
    'gangyal industrial': 'Gangyal',
    'gangyal industrial area': 'Gangyal',
    'greater kailash': 'Greater Kailash',
    'greater kailash jammu': 'Greater Kailash',
    'gk jammu': 'Greater Kailash',
    'guru nanak nagar': 'Nanak Nagar',
    'nanak nagar': 'Nanak Nagar',
    'janipur': 'Janipur',
    'janipura': 'Janipur',
    'janipur colony': 'Janipur',
    'old janipur': 'Janipur',
    'trikuta nagar': 'Trikuta Nagar',
    'trikuta nagar extension': 'Trikuta Nagar',
    'sainik colony': 'Sainik Colony',
    'sainik colony extension': 'Sainik Colony',
    'talab tillo': 'Talab Tillo',
    'talab tilloo': 'Talab Tillo',
    'shastri nagar': 'Shastri Nagar',
    'bakshi nagar': 'Bakshi Nagar',
    'bakshinagar': 'Bakshi Nagar',
    'roop nagar': 'Roop Nagar',
    'sidhra': 'Sidhra',
    'sidra': 'Sidhra',
    'tawi vihar': 'Sidhra',
    'sunjwan': 'Sunjwan',
    'sanjwan': 'Sunjwan',
    'sanjwan road': 'Sunjwan',
    'kunjwani': 'Kunjwani',
    'paloura': 'Paloura',
    'paloura top': 'Paloura',
    'muthi': 'Muthi',
    'lower muthi': 'Muthi',
    'domana': 'Domana',
    'raipur domana': 'Domana',
    'dumana': 'Domana',
    'satwari': 'Satwari',
    'raipur satwari': 'Satwari',
    'rani bagh': 'Satwari',
    'digiana': 'Digiana',
    'digiana camp': 'Digiana',
    'digiana colony': 'Digiana',
    'nagrota': 'Nagrota',
    'iim jammu': 'Nagrota',
    'iit jammu': 'Nagrota',
    'chowadhi': 'Chowadhi',
    'chatha': 'Chatha',
    'channi rama': 'Channi Rama',
    'durga nagar': 'Durga Nagar',
    'rehari': 'Rehari',
    'rehari colony': 'Rehari',
    'sarwal': 'Sarwal',
    'bhagwati nagar': 'Bhagwati Nagar',
    'bhagwatinagar': 'Bhagwati Nagar',
    'marh': 'Marh',
    'miran sahib': 'Miran Sahib',
    'bishnah': 'Bishnah',
    'bishna': 'Bishnah',
    'bishnah road': 'Bishnah',
    'panjtirthi': 'Panjtirthi',
    'rajpura': 'Rajpura',
    'rajpura chungi': 'Rajpura',
    'barnai': 'Barnai',
    'lower barnai': 'Barnai',
    'chinore': 'Chinore',
    'majhin': 'Majhin',
    'kheri': 'Kheri',
    'narwal': 'Narwal',
    'narwal bala': 'Narwal',
    'canal road': 'Canal Road',
    'ambphalla': 'Ambphalla',
    'purkhoo': 'Purkhoo',
    'porkhu': 'Purkhoo',
    'toph sherkhanian': 'Toph Sherkhanian',
    'preet nagar': 'Preet Nagar',
    'lower shiv nagar': 'Lower Shiv Nagar',
    'mishriwala': 'Mishriwala',
    'shakti nagar': 'Shakti Nagar',
    'pakki dhaki': 'Pakki Dhaki',
    'colonels colony': 'Colonels Colony',
    'manorama vihar': 'Manorama Vihar',
    'anuradhapuram': 'Anuradhapuram',
    'gorkha nagar': 'Gorkha Nagar',
    'gadigarh': 'Gadigarh',
    'upper gadigarh': 'Gadigarh',
    'nardani bajwan': 'Nardani Bajwan',
    'bhalwal': 'Kot Bhalwal',
    'kot bhalwal': 'Kot Bhalwal',
    'patoli': 'Patoli',
    'kot': 'Kot Bhalwal',
    'lale-da-bagh': 'Lale-Da-Bagh',
    'raghunath pura': 'Raghunath Pura',
    'raghunath bazaar': 'Raghunath Bazaar',
    'raghunath bazar': 'Raghunath Bazaar',
    'nai basti': 'Nai Basti',
    'chohala': 'Chohala',
    'gujjar nagar': 'Gujjar Nagar',
    'guru tegh bahadur nagar': 'Guru Tegh Bahadur Nagar',
    'suraj nagar': 'Suraj Nagar',
    'kacchi chawni': 'Kacchi Chawni',
    'akhnoor road': 'Akhnoor Road',
    'akhnoor': 'Akhnoor',
    'anand nagar': 'Anand Nagar',
    'subash nagar': 'Subash Nagar',
    'bohri': 'Bohri',
    'jain bazaar': 'Jain Bazaar',
    'residency road': 'Residency Road',
    'prem nagar': 'Prem Nagar',
    'karan nagar': 'Karan Nagar',
    'ajit nagar': 'Ajit Nagar',
    'shanti nagar': 'Shanti Nagar',
    'manda': 'Manda',
    'old heritage city': 'Old Heritage City',
    'peer kho': 'Peer Kho',
    'bharat nagar': 'Bharat Nagar',
    'babliana': 'Babliana',
    'bhour camp': 'Bhour Camp',
    'bhawaninagar': 'Bhawaninagar',
    'rampura': 'Rampura',
    'karan bagh': 'Karan Bagh',
    'jewel chowk': 'Jewel Chowk',
    'bagh-e-bahu': 'Bagh-e-Bahu',
    'gole market': 'Gole Market',
    'resham ghar colony': 'Resham Ghar Colony',
    'sanjay nagar': 'Sanjay Nagar',
    'purani mandi': 'Purani Mandi',
    'shalamar road': 'Shalamar Road',
    'udheywala': 'Udheywala',
    'sehora': 'Sehora',
    'jeevan nagar': 'Jeevan Nagar',
    'gobind nagar': 'Gobind Nagar'
}

def classify_geography(item):
    addr = item.get('address') or {}
    loc = (addr.get('locality') or '').strip()
    full = (addr.get('full_address') or '').strip()
    title = (item.get('title') or '').strip()
    
    full_text = f"{loc} | {full} | {title}".lower()
    
    # Check outside district rules
    for keyword, dist, reason in OUTSIDE_DISTRICT_RULES:
        if keyword in ['saror', 'sarore'] and 'kunjwani' in full_text:
            return 'REVIEW', None, loc, "Address conflict: 'Saror' and 'Kunjwani' both present"
        if re.search(r'\b' + re.escape(keyword) + r'\b', full_text):
            return 'REMOVE', None, loc, reason
            
    # Check normalization map
    loc_lower = loc.lower()
    if loc_lower in JAMMU_LOCALITY_MAP:
        return 'KEEP', JAMMU_LOCALITY_MAP[loc_lower], loc, "Recognized Jammu District locality"
        
    for k, v in JAMMU_LOCALITY_MAP.items():
        if re.search(r'\b' + re.escape(k) + r'\b', full_text):
            return 'KEEP', v, loc, f"Recognized Jammu District locality from address context: '{v}'"
            
    if not loc or loc_lower in ['', 'jammu']:
        return 'REVIEW', None, loc, "Missing or generic locality without specific colony/neighbourhood"
        
    return 'REVIEW', None, loc, f"Unrecognized locality '{loc}' requiring administrative boundary review"

def parse_price(item):
    pr = item.get('price') or {}
    pv = pr.get('price_value')
    if pv is not None and isinstance(pv, (int, float)) and pv > 0:
        return float(pv), None
    disp = str(pr.get('display_price') or '')
    if 'call for price' in disp.lower() or 'price on request' in disp.lower():
        return None, f"Price is '{disp}'"
    return None, "Missing or zero numerical price"

def parse_area(item, raw_item=None):
    ar = item.get('area') or {}
    adisp = str(ar.get('area_display') or '').strip()
    asqft = ar.get('area_sqft')
    
    flag = None
    sqft_val = None
    if asqft is not None and isinstance(asqft, (int, float)) and asqft > 0:
        sqft_val = float(asqft)
        
    # Check if raw item has coveredArea that resolves carpetArea ambiguity
    if raw_item and sqft_val and sqft_val < 50:
        cov = raw_item.get('coveredArea')
        if cov and isinstance(cov, (int, float)) and cov >= 50:
            flag = f"recovered_area_from_raw: replaced ambiguous carpetArea={sqft_val} with coveredArea={cov}"
            sqft_val = float(cov)
            
    # Check sq.yd discrepancy
    if 'sq.yd' in adisp.lower() or 'sqyd' in adisp.lower() or 'sq yard' in adisp.lower():
        m = re.search(r'([\d\.,]+)', adisp)
        if m:
            num = float(m.group(1).replace(',', ''))
            calc_sqft = num * 9.0
            if sqft_val and abs(sqft_val - calc_sqft) > 1.0:
                flag = f"unit_conversion_discrepancy: display reports {num} sq.yd ({calc_sqft:.0f} sq.ft), but stored as {sqft_val} sq.ft"
                sqft_val = calc_sqft
            elif not sqft_val:
                sqft_val = calc_sqft
                
    if sqft_val is None or sqft_val <= 0:
        return None, "Missing or zero area in square feet"
        
    # Check for fundamental area inconsistency (e.g. area < 50 sq.ft for a residential / commercial building)
    ptype = str(item.get('type_of_property') or '').lower()
    if sqft_val < 50.0 and ('house' in ptype or 'villa' in ptype or 'apartment' in ptype or 'floor' in ptype or 'showroom' in ptype):
        return None, f"fundamental_area_inconsistency: reported area {sqft_val} sq.ft is physically implausible for {ptype} (suspected Marlas entered as sqft)"
        
    return sqft_val, flag

def is_project(item):
    ptype = str(item.get('type_of_property') or '').strip().lower()
    if ptype == 'project':
        return True, "Listing explicitly categorized as 'Project'"
        
    pr = item.get('price') or {}
    pdisp = str(pr.get('display_price') or '')
    ar = item.get('area') or {}
    adisp = str(ar.get('area_display') or '')
    
    if ' - ' in pdisp or ' - ' in adisp:
        return True, f"Multi-unit/aggregate range detected: Price='{pdisp}', Area='{adisp}'"
        
    title = str(item.get('title') or '').lower()
    if any(w in title for w in ['river castle', 'royal palms', 'parsvnath passion', 'ansal grace', 'nidesh enclave', 'paradise avenue']):
        return True, f"Known development/project listing: '{item.get('title')}'"
        
    return False, ""

def run_cleaning():
    print("==================================================================")
    print("STARTING HOUSING.COM AND MAGICBRICKS CLEANING PIPELINE")
    print("==================================================================")
    
    portals = ['housing', 'magicbricks']
    categories = ['buy', 'commercial', 'rent']
    
    # Store results
    cleaned_residential = defaultdict(list)
    cleaned_commercial = defaultdict(list)
    cleaned_rental = []
    separated_projects = []
    
    review_geographic = []
    review_outlier = []
    review_data_quality = []
    
    removed_records = []
    duplicate_records = []
    
    file_metrics = []
    
    for portal in portals:
        for cat in categories:
            fname = f"{cat}_properties_filtered.json"
            fpath = os.path.join(DATA_DIR, portal, fname)
            
            if not os.path.exists(fpath):
                print(f"Skipping missing file: {fpath}")
                continue
                
            with open(fpath, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            raw_by_id = {}
            if portal == 'magicbricks':
                raw_path = os.path.join(DATA_DIR, portal, f"{cat}_properties.json")
                if os.path.exists(raw_path):
                    with open(raw_path, 'r', encoding='utf-8') as rf:
                        rdata = json.load(rf)
                        raw_by_id = {str(r.get('id')): r for r in rdata if 'id' in r}
                
            orig_count = len(raw_data)
            confirmed_jammu = 0
            outside_removed = 0
            price_removed = 0
            area_removed = 0
            dup_removed = 0
            proj_separated = 0
            flagged_review = 0
            
            # Temporary list of candidates for this file
            file_candidates = []
            
            for item in raw_data:
                pid = str(item.get('property_id'))
                title = item.get('title') or ''
                
                # Attach portal and category provenance
                item['source_portal'] = portal
                item['source_category'] = cat
                
                # Check 1: Project-level listings (only relevant for Buy/Residential)
                if cat == 'buy':
                    is_proj, proj_reason = is_project(item)
                    if is_proj:
                        proj_separated += 1
                        proj_record = dict(item)
                        proj_record['separation_reason'] = proj_reason
                        separated_projects.append(proj_record)
                        continue
                        
                # Check 2: Geographic Classification
                geo_dec, loc_clean, loc_orig, geo_reason = classify_geography(item)
                item['locality_original'] = loc_orig
                item['locality_clean'] = loc_clean
                item['geographic_status'] = geo_dec
                
                if geo_dec == 'REMOVE':
                    outside_removed += 1
                    rem = dict(item)
                    rem['removal_reason'] = f"outside_jammu_district: {geo_reason}"
                    removed_records.append(rem)
                    continue
                elif geo_dec == 'REVIEW':
                    flagged_review += 1
                    rev = dict(item)
                    rev['review_reason'] = geo_reason
                    review_geographic.append(rev)
                    continue
                else:
                    confirmed_jammu += 1
                    
                # Check 3: Price Validation
                price_val, price_reason = parse_price(item)
                if price_val is None:
                    price_removed += 1
                    rem = dict(item)
                    rem['removal_reason'] = f"missing_or_invalid_price: {price_reason}"
                    removed_records.append(rem)
                    continue
                    
                # Check 4: Area Validation
                raw_item = raw_by_id.get(pid)
                area_val, area_flag_or_reason = parse_area(item, raw_item)
                if area_val is None:
                    area_removed += 1
                    rem = dict(item)
                    rem['removal_reason'] = f"missing_or_invalid_area: {area_flag_or_reason}"
                    removed_records.append(rem)
                    continue
                    
                if area_flag_or_reason:
                    flagged_review += 1
                    dq = dict(item)
                    dq['quality_flag'] = area_flag_or_reason
                    review_data_quality.append(dq)
                    
                # Derived Fields
                price_inr = round(price_val, 2)
                area_sqft = round(area_val, 2)
                price_per_sqft = round(price_inr / area_sqft, 2)
                area_marla = round(area_sqft / 225.0, 2)
                price_per_marla = round(price_inr / area_marla, 2) if area_marla > 0 else 0.0
                
                item['price_inr'] = price_inr
                item['area_sqft_clean'] = area_sqft
                item['price_per_sqft'] = price_per_sqft
                item['area_in_marla'] = area_marla
                item['price_per_marla'] = price_per_marla
                item['property_category'] = cat
                item['data_quality_flag'] = 'clean'
                
                file_candidates.append(item)
                
            # Check 5: Duplicate Detection within this file
            seen_signatures = {}
            retained_candidates = []
            
            for item in file_candidates:
                # Signature: (locality_clean, property_type, price_inr, area_sqft_clean, bedrooms)
                cfg = item.get('configuration') or {}
                bed = cfg.get('bedrooms') if isinstance(cfg, dict) else None
                ptype = (item.get('type_of_property') or '').strip().lower()
                
                sig = (item['locality_clean'], ptype, item['price_inr'], item['area_sqft_clean'], str(bed))
                
                if sig in seen_signatures:
                    dup_removed += 1
                    dup = dict(item)
                    dup['removal_reason'] = 'duplicate_listing'
                    dup['duplicate_of_id'] = seen_signatures[sig]['property_id']
                    duplicate_records.append(dup)
                else:
                    seen_signatures[sig] = item
                    retained_candidates.append(item)
                    
            final_retained = len(retained_candidates)
            
            file_metrics.append({
                'source_file': fname,
                'portal': portal,
                'category': cat,
                'original_records': orig_count,
                'confirmed_jammu': confirmed_jammu,
                'outside_removed': outside_removed,
                'price_removed': price_removed,
                'area_removed': area_removed,
                'duplicate_removed': dup_removed,
                'projects_separated': proj_separated,
                'flagged_review': flagged_review,
                'final_retained': final_retained
            })
            
            # Route to respective category dataset
            if cat == 'buy':
                cleaned_residential[portal].extend(retained_candidates)
            elif cat == 'commercial':
                cleaned_commercial[portal].extend(retained_candidates)
            elif cat == 'rent':
                cleaned_rental.extend(retained_candidates)

    # Cross-portal deduplication for combined residential
    print("\nPerforming cross-portal deduplication on residential...")
    combined_res = []
    seen_cross = {}
    cross_dup_count = 0
    
    for p in ['housing', 'magicbricks']:
        for item in cleaned_residential[p]:
            cfg = item.get('configuration') or {}
            bed = cfg.get('bedrooms') if isinstance(cfg, dict) else None
            ptype = (item.get('type_of_property') or '').strip().lower()
            sig = (item['locality_clean'], ptype, item['price_inr'], item['area_sqft_clean'], str(bed))
            
            if sig in seen_cross:
                cross_dup_count += 1
                dup = dict(item)
                dup['removal_reason'] = 'cross_portal_duplicate'
                dup['duplicate_of_id'] = seen_cross[sig]['property_id']
                duplicate_records.append(dup)
            else:
                seen_cross[sig] = item
                combined_res.append(item)
                
    # Outlier Detection on Cleaned Residential
    if combined_res:
        df_res = pd.DataFrame(combined_res)
        q1_sqft = df_res['price_per_sqft'].quantile(0.25)
        q3_sqft = df_res['price_per_sqft'].quantile(0.75)
        iqr_sqft = q3_sqft - q1_sqft
        upper_bound = q3_sqft + 3.0 * iqr_sqft
        lower_bound = max(100.0, q1_sqft - 1.5 * iqr_sqft)
        
        for item in combined_res:
            pps = item['price_per_sqft']
            if pps > upper_bound or pps < lower_bound or item['price_inr'] > 200000000:
                item['data_quality_flag'] = 'outlier_review'
                review_outlier.append({
                    'property_id': item['property_id'],
                    'source_portal': item['source_portal'],
                    'title': item['title'],
                    'locality_clean': item['locality_clean'],
                    'price_inr': item['price_inr'],
                    'area_sqft': item['area_sqft_clean'],
                    'price_per_sqft': item['price_per_sqft'],
                    'outlier_reason': f"price_per_sqft {pps} outside normal bounds [{lower_bound:.1f}, {upper_bound:.1f}]"
                })

    # Combined Commercial
    combined_comm = []
    for p in ['housing', 'magicbricks']:
        combined_comm.extend(cleaned_commercial[p])

    # Save Outputs
    print("\nSaving output datasets...")
    # Residential
    with open(os.path.join(CLEANED_DIR, 'residential', 'housing_residential_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(cleaned_residential['housing'], f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'residential', 'magicbricks_residential_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(cleaned_residential['magicbricks'], f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'residential', 'residential_combined_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(combined_res, f, indent=2, ensure_ascii=False)

    # Commercial
    with open(os.path.join(CLEANED_DIR, 'commercial', 'housing_commercial_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(cleaned_commercial['housing'], f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'commercial', 'magicbricks_commercial_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(cleaned_commercial['magicbricks'], f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'commercial', 'commercial_combined_cleaned.json'), 'w', encoding='utf-8') as f:
        json.dump(combined_comm, f, indent=2, ensure_ascii=False)

    # Rental
    with open(os.path.join(CLEANED_DIR, 'rental', 'rental_cleaned_separate.json'), 'w', encoding='utf-8') as f:
        json.dump(cleaned_rental, f, indent=2, ensure_ascii=False)

    # Projects
    with open(os.path.join(CLEANED_DIR, 'projects', 'project_listings_separate.json'), 'w', encoding='utf-8') as f:
        json.dump(separated_projects, f, indent=2, ensure_ascii=False)

    # Review
    with open(os.path.join(CLEANED_DIR, 'review', 'geographic_review.json'), 'w', encoding='utf-8') as f:
        json.dump(review_geographic, f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'review', 'outlier_review.json'), 'w', encoding='utf-8') as f:
        json.dump(review_outlier, f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'review', 'data_quality_review.json'), 'w', encoding='utf-8') as f:
        json.dump(review_data_quality, f, indent=2, ensure_ascii=False)

    # Removed
    with open(os.path.join(CLEANED_DIR, 'removed', 'removed_records.json'), 'w', encoding='utf-8') as f:
        json.dump(removed_records, f, indent=2, ensure_ascii=False)
    with open(os.path.join(CLEANED_DIR, 'removed', 'duplicate_records.json'), 'w', encoding='utf-8') as f:
        json.dump(duplicate_records, f, indent=2, ensure_ascii=False)

    # Locality Summary CSV
    all_clean_listings = combined_res + combined_comm + cleaned_rental
    loc_summary_rows = []
    loc_group = defaultdict(lambda: {'residential': 0, 'commercial': 0, 'rental': 0, 'prices': []})
    for x in all_clean_listings:
        loc = x['locality_clean']
        cat = x['source_category']
        cat_key = 'residential' if cat == 'buy' else ('rental' if cat == 'rent' else 'commercial')
        loc_group[loc][cat_key] += 1
        loc_group[loc]['prices'].append(x['price_inr'])
        
    for loc, data in sorted(loc_group.items()):
        prices = data['prices']
        loc_summary_rows.append({
            'canonical_locality': loc,
            'residential_count': data['residential'],
            'commercial_count': data['commercial'],
            'rental_count': data['rental'],
            'total_listings': len(prices),
            'min_price_inr': min(prices) if prices else 0,
            'median_price_inr': float(np.median(prices)) if prices else 0,
            'max_price_inr': max(prices) if prices else 0
        })
    df_loc_summary = pd.DataFrame(loc_summary_rows)
    df_loc_summary.to_csv(os.path.join(CLEANED_DIR, 'reports', 'locality_summary.csv'), index=False)

    # Cleaning Summary JSON
    summary_data = {
        'file_metrics': file_metrics,
        'totals': {
            'cleaned_residential_housing': len(cleaned_residential['housing']),
            'cleaned_residential_magicbricks': len(cleaned_residential['magicbricks']),
            'cleaned_residential_combined': len(combined_res),
            'cleaned_commercial_housing': len(cleaned_commercial['housing']),
            'cleaned_commercial_magicbricks': len(cleaned_commercial['magicbricks']),
            'cleaned_commercial_combined': len(combined_comm),
            'cleaned_rental': len(cleaned_rental),
            'separated_projects': len(separated_projects),
            'geographic_review': len(review_geographic),
            'outlier_review': len(review_outlier),
            'data_quality_review': len(review_data_quality),
            'removed_records': len(removed_records),
            'duplicate_records': len(duplicate_records)
        }
    }
    with open(os.path.join(CLEANED_DIR, 'reports', 'cleaning_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2)

    print("\nCleaning Pipeline Complete!")
    print("Metrics Table:")
    metrics_df = pd.DataFrame(file_metrics)
    print(metrics_df.to_string(index=False))
    print("\nTotals:")
    for k, v in summary_data['totals'].items():
        print(f"  {k:35}: {v:5}")

if __name__ == '__main__':
    run_cleaning()
