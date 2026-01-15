import pandas as pd
import shutil
import os
import json
from pathlib import Path

# Paths
base_path = Path(r'c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed')
temp_folder = base_path / 'images_resized512' / 'western' / 'temp'
tshirt_folder = base_path / 'images_resized512' / 'western' / 't_shirt'
csv_path = base_path / 'labels_sorted2.csv'
output_csv = base_path / 'tshirt_processed.csv'

# Create t_shirt folder if not exists
tshirt_folder.mkdir(exist_ok=True)

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

def extract_fit(title, pattern, attributes):
    text = f"{title} {pattern} {json.dumps(attributes)}".lower()
    for key, value in fit_mapping.items():
        if key in text:
            return value
    return 'SOLID & BASIC'

# Process CSV first to check if temp entries exist
print("Processing CSV...")
df = pd.read_csv(csv_path)

# Filter rows with western/temp
temp_rows = df[df['file_path'].str.contains('western/temp', na=False)].copy()
print(f"Found {len(temp_rows)} rows with western/temp")

if len(temp_rows) == 0:
    print("No temp entries in CSV. Checking if images need to be moved...")
    # Move images anyway
    print("Moving images from temp to t_shirt folder...")
    moved_count = 0
    for img in temp_folder.glob('*.jpg'):
        dest = tshirt_folder / img.name
        if not dest.exists():
            shutil.move(str(img), str(dest))
            moved_count += 1
    print(f"Moved {moved_count} images")
    print("No CSV entries to process. Exiting.")
    exit(0)

# Move images
print("Moving images from temp to t_shirt folder...")
moved_count = 0
for img in temp_folder.glob('*.jpg'):
    dest = tshirt_folder / img.name
    if not dest.exists():
        shutil.move(str(img), str(dest))
        moved_count += 1
print(f"Moved {moved_count} images")

# Update paths and attributes
new_rows = []
for idx, row in temp_rows.iterrows():
    new_row = row.copy()
    new_row['file_path'] = row['file_path'].replace('western/temp/', 'western/t_shirt/')
    new_row['sub_class'] = 'top'
    new_row['category'] = 't_shirt'
    
    # Parse attributes
    attrs = json.loads(row['attributes_json']) if pd.notna(row['attributes_json']) else {}
    
    # Extract fit
    fit_attr = extract_fit(row.get('product_name', ''), attrs.get('pattern', ''), attrs)
    attrs['fit'] = fit_attr
    
    new_row['attributes_json'] = json.dumps(attrs)
    new_rows.append(new_row)

# Create new dataframe
new_df = pd.DataFrame(new_rows)
new_df.to_csv(output_csv, index=False)
print(f"Created {output_csv} with {len(new_df)} rows")
