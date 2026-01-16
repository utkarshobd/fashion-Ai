import csv
import os

csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_sorted3.csv"
images_original_dir = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_original\ethnic\kurta"

# Get all kurta files from CSV
csv_files = set()
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['file_path'].startswith('ethnic/kurta/'):
            csv_files.add(os.path.basename(row['file_path']))

print(f"Found {len(csv_files)} kurta images in CSV")

# Get all files in images_original/ethnic/kurta
folder_files = os.listdir(images_original_dir)
print(f"Found {len(folder_files)} files in images_original/ethnic/kurta")

# Find files to delete (in folder but not in CSV)
to_delete = [f for f in folder_files if f not in csv_files]
print(f"\nFiles to delete: {len(to_delete)}")

# Delete orphaned files
for file in to_delete:
    os.remove(os.path.join(images_original_dir, file))

print(f"Deleted {len(to_delete)} orphaned images from images_original/ethnic/kurta")
