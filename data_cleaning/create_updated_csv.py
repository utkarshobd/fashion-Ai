import pandas as pd
import os
import json
import re

# Read existing CSV
csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_sorted2.csv"
df_existing = pd.read_csv(csv_path)

# Get list of images from temp folder
temp_folder = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_resized512\western\temp"
temp_images = [f for f in os.listdir(temp_folder) if f.lower().endswith(('.jpg', '.png'))]

print(f"Found {len(temp_images)} images in temp folder")
print(f"Existing CSV has {len(df_existing)} rows")

# Extract attributes from filename
def extract_attributes(filename):
    # Remove extension
    name = os.path.splitext(filename)[0]
    
    # Split by underscore
    parts = name.split('_')
    
    # First part is ID
    item_id = parts[0] if len(parts) > 0 else ""
    
    # Last part is color
    color = parts[-1].lower() if len(parts) > 0 else "unknown"
    
    # Middle parts are the description
    description = ' '.join(parts[1:-1]) if len(parts) > 2 else parts[1] if len(parts) > 1 else ""
    
    # Extract fit attributes from description
    description_lower = description.lower()
    fit_attributes = []
    
    # Check for various fit types
    if 'crop' in description_lower or 'cropped' in description_lower:
        fit_attributes.append('crop_top')
    if 'ribbed' in description_lower:
        fit_attributes.append('ribbed')
    if 'basic' in description_lower:
        fit_attributes.append('basic')
    if 'halter' in description_lower:
        fit_attributes.append('halter')
    if 'off-shoulder' in description_lower or 'off shoulder' in description_lower:
        fit_attributes.append('off_shoulder')
    if 'cowl' in description_lower:
        fit_attributes.append('cowl_neck')
    if 'v-neck' in description_lower or 'v neck' in description_lower:
        fit_attributes.append('v_neck')
    if 'sleeveless' in description_lower:
        fit_attributes.append('sleeveless')
    if 'long sleeve' in description_lower:
        fit_attributes.append('long_sleeve')
    if 'short sleeve' in description_lower:
        fit_attributes.append('short_sleeve')
    if 'tank' in description_lower:
        fit_attributes.append('tank')
    if 'tube' in description_lower:
        fit_attributes.append('tube')
    if 'peplum' in description_lower:
        fit_attributes.append('peplum')
    if 'wrap' in description_lower:
        fit_attributes.append('wrap')
    if 'asymmetric' in description_lower:
        fit_attributes.append('asymmetric')
    
    # Determine pattern
    pattern = "solid"
    if 'print' in description_lower or 'printed' in description_lower:
        pattern = "printed"
    if 'stripe' in description_lower or 'striped' in description_lower:
        pattern = "striped"
    if 'floral' in description_lower:
        pattern = "floral"
    if 'animal print' in description_lower:
        pattern = "animal_print"
    if 'polka' in description_lower or 'dot' in description_lower:
        pattern = "polka_dot"
    
    # Default fit if none found
    if not fit_attributes:
        fit_attributes.append('regular')
    
    fit = ', '.join(fit_attributes)
    
    # Map color names
    color_map = {
        'brown': 'brown',
        'black': 'black',
        'white': 'white',
        'red': 'red',
        'blue': 'blue',
        'green': 'green',
        'yellow': 'yellow',
        'pink': 'pink',
        'purple': 'purple',
        'grey': 'grey',
        'gray': 'grey',
        'orange': 'orange',
        'beige': 'beige',
        'navy': 'navy_blue',
        'maroon': 'maroon',
        'olive': 'olive',
        'cream': 'cream',
        'gold': 'gold',
        'silver': 'silver',
        'multicolor': 'multicolor',
        'multi': 'multicolor'
    }
    
    color_primary = color_map.get(color, color)
    
    return {
        'item_id': item_id,
        'description': description,
        'color_primary': color_primary,
        'pattern': pattern,
        'fit': fit
    }

# Create new rows for unmapped images
new_rows = []

for img_file in temp_images:
    # Check if this image is already mapped in existing CSV
    # The file path in t_shirt folder would be: western/t_shirt/{filename}
    t_shirt_path = f"western/t_shirt/{img_file}"
    
    # Check if already exists
    if t_shirt_path in df_existing['file_path'].values:
        print(f"Skipping {img_file} - already mapped")
        continue
    
    # Extract attributes
    attrs = extract_attributes(img_file)
    
    # Create attributes JSON
    attributes_json = json.dumps({
        "color_primary": attrs['color_primary'],
        "gender": "women",
        "occasion_suitability": "casual",
        "season": "all",
        "pattern": attrs['pattern'],
        "fit": attrs['fit'],
        "year": "2024"
    })
    
    # Create product name
    product_name = f"{attrs['item_id']} Women {attrs['description']}"
    
    # Create new row
    new_row = {
        'file_path': t_shirt_path,
        'category': 't_shirt',
        'sub_category': 'western',
        'attributes_json': attributes_json,
        'gender': 'Women',
        'source': 'custom',
        'original_id': f"tshirt_{attrs['item_id']}",
        'product_name': product_name,
        'sub_class': 'top'
    }
    
    new_rows.append(new_row)

print(f"\nCreating {len(new_rows)} new mappings")

# Create new dataframe with new rows
df_new = pd.DataFrame(new_rows)

# Combine existing and new data
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Save to new CSV
output_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_sorted2_updated.csv"
df_combined.to_csv(output_path, index=False)

print(f"\nNew CSV created: {output_path}")
print(f"Total rows: {len(df_combined)}")
print(f"Original rows: {len(df_existing)}")
print(f"New rows added: {len(new_rows)}")

# Show sample of new rows
if len(new_rows) > 0:
    print("\nSample of new mappings:")
    print(df_new.head(10).to_string())
