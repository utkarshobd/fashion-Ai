import pandas as pd
import json

# Read both CSV files
labels_df = pd.read_csv('../annotations/labels.csv')
train_df = pd.read_csv('../annotations/labels_train.csv')

print(f"Labels.csv entries: {len(labels_df)}")
print(f"Labels_train.csv entries: {len(train_df)}")

# Extract color from attributes_json in labels.csv
unknown_images = []
for idx, row in labels_df.iterrows():
    try:
        # Parse the JSON attributes
        attrs = json.loads(row['attributes_json'])
        if attrs.get('color_primary') == 'unknown':
            # Extract image name from file_path
            image_name = row['file_path'].split('/')[-1]
            unknown_images.append(image_name)
    except:
        continue

print(f"Found {len(unknown_images)} images with unknown color in labels.csv")

# Update labels_train.csv for matching images
updated_count = 0
for image in unknown_images:
    mask = train_df['file_path'].str.endswith(image)
    if mask.any():
        train_df.loc[mask, 'color_primary'] = 'unknown'
        updated_count += 1

print(f"Updated {updated_count} entries in labels_train.csv")

# Save the updated file
train_df.to_csv('../annotations/labels_train.csv', index=False)
print("labels_train.csv updated successfully")