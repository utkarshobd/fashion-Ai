import pandas as pd
import os
import json
from pathlib import Path

base_path = Path(r'c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed')
tshirt_folder = base_path / 'images_resized512' / 'western' / 't_shirt'
csv_path = base_path / 'labels_sorted2.csv'
output_csv = base_path / 'tshirt_processed.csv'

# Read existing CSV
df = pd.read_csv(csv_path)
existing_tshirt = df[df['file_path'].str.contains('western/t_shirt', na=False)].copy()

# Fit attribute mapping
fit_mapping = {
    'solid': 'SOLID & BASIC', 'basic': 'SOLID & BASIC', 'plain': 'SOLID & BASIC', 'fitted': 'SOLID & BASIC', 'regular': 'SOLID & BASIC',
    'crop': 'CROP TOPS',
    'floral': 'PRINTED', 'striped': 'PRINTED', 'animal': 'PRINTED', 'geometric': 'PRINTED', 'polka': 'PRINTED', 'printed': 'PRINTED',
    'ribbed': 'RIBBED',
    'shirt': 'SHIRT STYLE', 'collar': 'SHIRT STYLE', 'mandarin': 'SHIRT STYLE',
    'embroidered': 'EMBELLISHED', 'sequined': 'EMBELLISHED', 'lace': 'EMBELLISHED', 'crochet': 'EMBELLISHED', 'embellished': 'EMBELLISHED',
    'halter': 'SPECIAL NECKLINES', 'off-shoulder': 'SPECIAL NECKLINES', 'cowl': 'SPECIAL NECKLINES', 'sweetheart': 'SPECIAL NECKLINES',
    'peplum': 'SPECIAL STYLES', 'wrap': 'SPECIAL STYLES', 'blouson': 'SPECIAL STYLES', 'empire': 'SPECIAL STYLES', 'tube': 'SPECIAL STYLES',
    'puff': 'SLEEVE STYLES', 'bell': 'SLEEVE STYLES', 'flutter': 'SLEEVE STYLES', 'long': 'SLEEVE STYLES', 'sleeveless': 'SLEEVE STYLES',
    'cotton': 'FABRIC-BASED', 'georgette': 'FABRIC-BASED', 'satin': 'FABRIC-BASED', 'denim': 'FABRIC-BASED', 'velvet': 'FABRIC-BASED'
}

def extract_fit(filename, product_name, pattern, attrs_str):
    text = f"{filename} {product_name} {pattern} {attrs_str}".lower()
    for key, value in fit_mapping.items():
        if key in text:
            return value
    return 'SOLID & BASIC'

# Process existing t_shirt entries
new_rows = []
for idx, row in existing_tshirt.iterrows():
    new_row = row.copy()
    new_row['sub_class'] = 'top'
    new_row['category'] = 't_shirt'
    
    attrs = json.loads(row['attributes_json']) if pd.notna(row['attributes_json']) else {}
    fit_attr = extract_fit(
        row['file_path'], 
        row.get('product_name', ''), 
        attrs.get('pattern', ''),
        row['attributes_json']
    )
    attrs['fit'] = fit_attr
    new_row['attributes_json'] = json.dumps(attrs)
    new_rows.append(new_row)

new_df = pd.DataFrame(new_rows)
new_df.to_csv(output_csv, index=False)
print(f"Created {output_csv} with {len(new_df)} rows")
print(f"Sample entries:")
print(new_df[['file_path', 'category', 'sub_class', 'attributes_json']].head(10))
