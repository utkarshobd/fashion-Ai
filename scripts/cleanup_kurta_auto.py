import csv
import os
import json

# Paths
csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_sorted2.csv"
images_resized_dir = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_resized512"
images_dir = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images"

# Step 1: Count images to be removed
print("Step 1: Counting images to be removed...")
count = 0
to_remove = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        file_path = row['file_path']
        if file_path.startswith('ethnic/kurta/'):
            try:
                attrs = json.loads(row['attributes_json'])
                if attrs.get('color_primary') == 'unknown':
                    count += 1
                    to_remove.append(file_path)
            except:
                pass

print(f"Found {count} ethnic/kurta images with color_primary='unknown'")
print(f"\nFirst 10 files to be removed:")
for i, fp in enumerate(to_remove[:10]):
    print(f"  {i+1}. {fp}")

# Step 2: Remove images from both folders
print(f"\nStep 2: Removing {count} images from folders...")
removed_resized = 0
removed_original = 0
missing_resized = 0
missing_original = 0

for file_path in to_remove:
    # Remove from images_resized512
    resized_path = os.path.join(images_resized_dir, file_path)
    if os.path.exists(resized_path):
        os.remove(resized_path)
        removed_resized += 1
    else:
        missing_resized += 1
    
    # Remove from images
    original_path = os.path.join(images_dir, file_path)
    if os.path.exists(original_path):
        os.remove(original_path)
        removed_original += 1
    else:
        missing_original += 1

print(f"Removed {removed_resized} images from images_resized512/ethnic/kurta (missing: {missing_resized})")
print(f"Removed {removed_original} images from images/ethnic/kurta (missing: {missing_original})")

# Step 3: Update CSV file
print("\nStep 3: Updating CSV file...")
rows_to_keep = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    
    for row in reader:
        file_path = row['file_path']
        if file_path.startswith('ethnic/kurta/'):
            try:
                attrs = json.loads(row['attributes_json'])
                if attrs.get('color_primary') == 'unknown':
                    continue  # Skip this row
            except:
                pass
        rows_to_keep.append(row)

# Write updated CSV
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_to_keep)

print(f"Removed {count} rows from CSV file")
print(f"Remaining rows in CSV: {len(rows_to_keep)}")
print("\n✓ Cleanup completed successfully!")
