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

df = pd.read_csv("../labels_tested.csv")

fit_changes = 0

for idx in range(len(df)):
    # Only process western/skirt category
    if 'western/skirt' not in str(df.iloc[idx]['file_path']):
        continue
    
    try:
        attributes = json.loads(df.iloc[idx]['attributes_json'])
    except:
        continue
    
    product_name = str(df.iloc[idx]['product_name'])
    
    # Extract fit only
    detected_fit = extract_fit_from_name(product_name)
    if detected_fit:
        attributes['fit'] = detected_fit
        df.at[idx, 'attributes_json'] = json.dumps(attributes, ensure_ascii=False)
        fit_changes += 1

print(f"Fit changes: {fit_changes}")

df.to_csv("../labels_tested.csv", index=False)
print("Updated labels_tested.csv!")