import os
import shutil
import pandas as pd

# Paths
temp_folder = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_resized512\ethnic\temp"
target_folder = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_resized512\ethnic\blouse_choli"
csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_sorted2.csv"

# Get all images from temp folder
temp_images = sorted([f for f in os.listdir(temp_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])

# Get existing blouse_choli images to find next number
existing_images = [f for f in os.listdir(target_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
existing_numbers = []
for img in existing_images:
    try:
        num = int(img.split('_')[0])
        existing_numbers.append(num)
    except:
        pass

next_num = max(existing_numbers) + 1 if existing_numbers else 901

# Move images and create mapping
mapping = {}
for i, img in enumerate(temp_images):
    new_num = next_num + i
    # Extract product name from original filename (remove number and color suffix)
    parts = img.rsplit('_', 1)[0]  # Remove color suffix
    parts = parts.split('_', 1)  # Split number from name
    product_name = parts[1] if len(parts) > 1 else parts[0]
    
    new_name = f"{new_num:03d}_women_{product_name}.jpg"
    
    src = os.path.join(temp_folder, img)
    dst = os.path.join(target_folder, new_name)
    
    shutil.move(src, dst)
    mapping[new_name] = f"ethnic/blouse_choli/{new_name}"
    print(f"Moved: {img} -> {new_name}")

# Read CSV
df = pd.read_csv(csv_path, engine='python', on_bad_lines='skip')

# Create new rows for moved images
new_rows = []
for new_name, file_path in mapping.items():
    new_row = {
        'file_path': file_path,
        'category': 'blouse_choli',
        'sub_category': 'ethnic',
        'attributes_json': '{"color_primary": "red", "pattern": "solid", "occasion_suitability": "festive", "gender": "female", "fit": "regular", "season": "all"}',
        'gender': 'Women',
        'source': 'custom',
        'original_id': f'blouse_{new_name.split("_")[0]}',
        'product_name': new_name.replace('.jpg', '').replace('_', ' ').title(),
        'sub_class': ''
    }
    new_rows.append(new_row)

# Append new rows
df_new = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

# Filter only blouse_choli entries
df_blouse = df_new[df_new['category'] == 'blouse_choli'].copy()

# Save filtered CSV
output_csv = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\blouse_choli_only.csv"
df_blouse.to_csv(output_csv, index=False)

print(f"\nTotal images moved: {len(mapping)}")
print(f"Total blouse_choli entries in CSV: {len(df_blouse)}")
print(f"Filtered CSV saved to: {output_csv}")
