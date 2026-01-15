import pandas as pd
import json
import os
import shutil

# Read the original CSV to get the deleted rows
df_original = pd.read_csv("labels_sorted2_backup.csv", engine="python", on_bad_lines="skip") if os.path.exists("labels_sorted2_backup.csv") else None

# Since we don't have backup, we'll identify images to move based on the pattern
# Images with "unknown" color_primary that were in ethnic/blouse_choli

# Read current CSV to see what's left
df_current = pd.read_csv("labels_sorted2.csv", engine="python", on_bad_lines="skip")

# Get all blouse_choli files that are still in the CSV
def get_color_primary(attr_json):
    try:
        attr = json.loads(attr_json)
        return attr.get("color_primary", "")
    except:
        return ""

df_current["color_primary"] = df_current["attributes_json"].apply(get_color_primary)
remaining_blouse_files = set(df_current[df_current["category"] == "blouse_choli"]["file_path"].tolist())

# Get all files in the images_resized512/ethnic/blouse_choli directory
source_dir = "images_resized512/ethnic/blouse_choli"
temp_dir = "images_resized512/ethnic/temp"

if not os.path.exists(source_dir):
    print(f"Source directory not found: {source_dir}")
    exit(1)

os.makedirs(temp_dir, exist_ok=True)

# Get all image files in source directory
all_images = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

moved_count = 0
for img_file in all_images:
    # Check if this image is in the remaining CSV
    img_path = f"ethnic/blouse_choli/{img_file}"
    
    if img_path not in remaining_blouse_files:
        # This image was deleted from CSV, move it
        source_path = os.path.join(source_dir, img_file)
        dest_path = os.path.join(temp_dir, img_file)
        
        try:
            shutil.move(source_path, dest_path)
            moved_count += 1
            print(f"Moved: {img_file}")
        except Exception as e:
            print(f"Error moving {img_file}: {e}")

print(f"\nTotal images moved: {moved_count}")
print(f"Destination: {temp_dir}")
