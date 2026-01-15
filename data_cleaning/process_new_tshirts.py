import pandas as pd
import os
import json
from pathlib import Path

base_path = Path(r'c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed')
tshirt_folder = base_path / 'images_resized512' / 'western' / 't_shirt'
csv_path = base_path / 'labels_sorted2.csv'
output_csv = base_path / 'tshirt_processed.csv'

df = pd.read_csv(csv_path)
existing_files = set(df['file_path'].str.replace('\\', '/').tolist())
all_images = set(f"western/t_shirt/{f.name}" for f in tshirt_folder.glob('*.jpg'))
new_images = all_images - existing_files

print(f"Total images in folder: {len(all_images)}")
print(f"Existing in CSV: {len(all_images & existing_files)}")
print(f"New images: {len(new_images)}")

fit_mapping = {
    'solid': 'SOLID & BASIC', 'basic': 'SOLID & BASIC', 'plain': 'SOLID & BASIC', 'fitted': 'SOLID & BASIC', 'regular': 'SOLID & BASIC',
    'crop': 'CROP TOPS', 'floral': 'PRINTED', 'striped': 'PRINTED', 'animal': 'PRINTED', 'geometric': 'PRINTED', 'polka': 'PRINTED', 'printed': 'PRINTED',
    'ribbed': 'RIBBED', 'shirt': 'SHIRT STYLE', 'collar': 'SHIRT STYLE', 'mandarin': 'SHIRT STYLE',
    'embroidered': 'EMBELLISHED', 'sequined': 'EMBELLISHED', 'lace': 'EMBELLISHED', 'crochet': 'EMBELLISHED', 'embellished': 'EMBELLISHED',
    'halter': 'SPECIAL NECKLINES', 'off-shoulder': 'SPECIAL NECKLINES', 'cowl': 'SPECIAL NECKLINES', 'sweetheart': 'SPECIAL NECKLINES',
    'peplum': 'SPECIAL STYLES', 'wrap': 'SPECIAL STYLES', 'blouson': 'SPECIAL STYLES', 'empire': 'SPECIAL STYLES', 'tube': 'SPECIAL STYLES',
    'puff': 'SLEEVE STYLES', 'bell': 'SLEEVE STYLES', 'flutter': 'SLEEVE STYLES', 'long': 'SLEEVE STYLES', 'sleeveless': 'SLEEVE STYLES',
    'cotton': 'FABRIC-BASED', 'georgette': 'FABRIC-BASED', 'satin': 'FABRIC-BASED', 'denim': 'FABRIC-BASED', 'velvet': 'FABRIC-BASED'
}

def extract_fit(filename):
    text = filename.lower()
    for key, value in fit_mapping.items():
        if key in text:
            return value
    return 'SOLID & BASIC'

new_rows = []
for img_path in sorted(new_images):
    attrs = {"color_primary": "unknown", "gender": "unisex", "occasion_suitability": "casual", 
             "season": "all_season", "pattern": "solid", "fit": extract_fit(img_path), "year": "2024"}
    new_rows.append({
        'file_path': img_path, 'category': 't_shirt', 'sub_category': 'western',
        'attributes_json': json.dumps(attrs), 'gender': 'Unisex', 'source': 'myntra',
        'original_id': '', 'product_name': '', 'sub_class': 'top'
    })

new_df = pd.DataFrame(new_rows)
final_df = pd.concat([df, new_df], ignore_index=True)
final_df.to_csv(output_csv, index=False)
print(f"Created {output_csv} with {len(final_df)} total rows ({len(new_rows)} new)")
