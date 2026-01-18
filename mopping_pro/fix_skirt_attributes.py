import pandas as pd
import json
import re

def extract_fit_from_name(name):
    name = name.lower()
    if re.search(r'\b(maxi|long)\b', name):
        return 'maxi'
    elif re.search(r'\b(short|midi|mini)\b', name):
        return 'midi'
    return None

def extract_pattern_from_name(name):
    name = name.lower()
    if re.search(r'\b(embr|embellish|embroidered)\b', name):
        return 'embroidered'
    elif re.search(r'\b(floral|flower)\b', name):
        return 'floral'
    elif re.search(r'\b(print|printed)\b', name):
        return 'printed'
    elif re.search(r'\b(solid|plain)\b', name):
        return 'solid'
    return None

df = pd.read_csv("../labels_tested.csv")

fit_changes = 0
pattern_changes = 0

for idx in range(len(df)):
    # Only process western/skirt category
    if 'western/skirt' not in str(df.iloc[idx]['file_path']):
        continue
    
    try:
        attributes = json.loads(df.iloc[idx]['attributes_json'])
    except:
        continue
    
    product_name = str(df.iloc[idx]['product_name'])
    
    # Extract fit
    detected_fit = extract_fit_from_name(product_name)
    if detected_fit:
        attributes['fit'] = detected_fit
        fit_changes += 1
    
    # Extract pattern
    detected_pattern = extract_pattern_from_name(product_name)
    if detected_pattern:
        attributes['pattern'] = detected_pattern
        pattern_changes += 1
    
    # Update attributes_json if any changes were made
    if detected_fit or detected_pattern:
        df.at[idx, 'attributes_json'] = json.dumps(attributes, ensure_ascii=False)

print(f"Fit changes: {fit_changes}")
print(f"Pattern changes: {pattern_changes}")

df.to_csv("../labels_tested.csv", index=False)
print("Updated labels_tested.csv!")