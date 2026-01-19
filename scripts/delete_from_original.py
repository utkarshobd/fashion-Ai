import csv
import os
import json

csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_sorted2.csv"
images_original_dir = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_original"

# Read CSV to find files to remove
to_remove = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        file_path = row['file_path']
        if file_path.startswith('ethnic/kurta/'):
            try:
                attrs = json.loads(row['attributes_json'])
                if attrs.get('color_primary') == 'unknown':
                    to_remove.append(file_path)
            except:
                pass

print(f"Found {len(to_remove)} files to remove from images_original")

removed = 0
for file_path in to_remove:
    original_path = os.path.join(images_original_dir, file_path)
    if os.path.exists(original_path):
        os.remove(original_path)
        removed += 1

print(f"Removed {removed} images from images_original/ethnic/kurta")
