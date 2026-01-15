import pandas as pd
import json
import os
import shutil

# Read CSV
df = pd.read_csv("labels_sorted2.csv", engine="python", on_bad_lines="skip")

# Parse attributes_json to extract color_primary
def get_color_primary(attr_json):
    try:
        attr = json.loads(attr_json)
        return attr.get("color_primary", "")
    except:
        return ""

df["color_primary"] = df["attributes_json"].apply(get_color_primary)

# Filter rows to delete: category=blouse_choli, sub_category=ethnic, color_primary=unknown
mask = (df["category"] == "blouse_choli") & (df["sub_category"] == "ethnic") & (df["color_primary"] == "unknown")
rows_to_delete = df[mask].copy()

print(f"Found {len(rows_to_delete)} rows to delete")

# Create temp directory
temp_dir = "images/ethnic/temp"
os.makedirs(temp_dir, exist_ok=True)

# Move images
moved_count = 0
for idx, row in rows_to_delete.iterrows():
    file_path = row["file_path"]
    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        dest_path = os.path.join(temp_dir, filename)
        shutil.move(file_path, dest_path)
        moved_count += 1
        print(f"Moved: {file_path} -> {dest_path}")
    else:
        print(f"File not found: {file_path}")

print(f"\nMoved {moved_count} images to {temp_dir}")

# Delete rows from dataframe
df_cleaned = df[~mask].copy()
df_cleaned = df_cleaned.drop(columns=["color_primary"])

# Save cleaned CSV
df_cleaned.to_csv("labels_sorted2.csv", index=False)
print(f"\nDeleted {len(rows_to_delete)} rows from labels_sorted2.csv")
print(f"Remaining rows: {len(df_cleaned)}")
