import os
import shutil
import csv
import json
import re

# Paths
temp_dir = r"images_resized512\ethnic\temp"
kurta_dir = r"images_resized512\ethnic\kurta"
csv_file = "labels_sorted3.csv"

# Read existing CSV
rows = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Get all images from temp
temp_images = [f for f in os.listdir(temp_dir) if f.endswith('.jpg')]

# Process each image
for img_name in temp_images:
    # Extract ID and attributes from filename
    parts = img_name.replace('.jpg', '').split('_')
    img_id = parts[0]
    
    # Extract color (last part before .jpg)
    color = parts[-1] if len(parts) > 1 else 'unknown'
    
    # Extract pattern from description
    description = '_'.join(parts[1:-1]) if len(parts) > 2 else parts[1] if len(parts) > 1 else ''
    
    # Determine pattern
    pattern = 'solid'
    if 'printed' in description.lower() or 'print' in description.lower():
        pattern = 'printed'
    elif 'embroidered' in description.lower() or 'embroidery' in description.lower():
        pattern = 'embroidered'
    elif 'floral' in description.lower():
        pattern = 'floral'
    elif 'striped' in description.lower():
        pattern = 'striped'
    elif 'woven' in description.lower():
        pattern = 'woven'
    
    # New filename for kurta directory
    new_filename = img_name
    new_path = f"ethnic/kurta/{new_filename}"
    
    # Create attributes JSON
    attributes = {
        "color_primary": color,
        "pattern": pattern,
        "occasion_suitability": "ethnic",
        "gender": "female",
        "fit": "regular",
        "season": "all"
    }
    
    # Create new row
    new_row = [
        new_path,
        "kurta",
        "ethnic",
        json.dumps(attributes),
        "Women",
        "custom",
        f"kurta_{img_id}",
        f"{img_id} Women {description.replace('_', ' ')}",
        ""
    ]
    
    # Add to rows
    rows.append(new_row)
    
    # Move file
    src = os.path.join(temp_dir, img_name)
    dst = os.path.join(kurta_dir, new_filename)
    shutil.move(src, dst)
    print(f"Moved: {img_name} -> {new_filename}")

# Write updated CSV
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\nProcessed {len(temp_images)} images")
print(f"CSV updated with {len(temp_images)} new entries")
