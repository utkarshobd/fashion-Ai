import os
import pandas as pd
import shutil

# Paths
blouse_folder = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_resized512\ethnic\blouse_choli"
csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\blouse_choli_only.csv"

# Color mapping from filename suffix to color_primary
color_map = {
    'green': 'green',
    'black': 'black',
    'pink': 'pink',
    'blue': 'blue',
    'gold': 'yellow',
    'red': 'red',
    'white': 'white',
    'purple': 'purple',
    'orange': 'orange',
    'brown': 'brown',
    'grey': 'grey',
    'multicolor': 'multicolor'
}

# Read CSV
df = pd.read_csv(csv_path)

# Process images from 921 to 1420 (the newly added ones)
updates = []
for idx, row in df.iterrows():
    if pd.isna(row['file_path']):
        continue
    
    filename = os.path.basename(row['file_path'])
    num = int(filename.split('_')[0])
    
    if 921 <= num <= 1420:
        # Get current file path
        current_path = os.path.join(blouse_folder, filename)
        
        if not os.path.exists(current_path):
            continue
        
        # Extract product name and determine color from original mapping
        # Map number ranges to colors based on the original temp folder pattern
        if 921 <= num <= 1032:  # Originally green (1-101) and black (102-201)
            if num <= 920 + 101:
                color = 'green'
            else:
                color = 'black'
        elif 1033 <= num <= 1143:  # Originally pink (202-301) and blue start
            if num <= 1032 + 100:
                color = 'pink'
            else:
                color = 'blue'
        elif 1144 <= num <= 1254:  # Originally blue (302-401) and gold start
            if num <= 1143 + 100:
                color = 'blue'
            else:
                color = 'gold'
        elif 1255 <= num <= 1420:  # Originally gold (402-501) and remaining
            color = 'gold'
        
        # Create new filename with color
        parts = filename.split('_', 2)
        if len(parts) >= 3:
            new_filename = f"{parts[0]}_women_{parts[2].replace('.jpg', '')}_{color}.jpg"
            new_path = os.path.join(blouse_folder, new_filename)
            
            # Rename file
            os.rename(current_path, new_path)
            
            # Update dataframe
            df.at[idx, 'file_path'] = f"ethnic/blouse_choli/{new_filename}"
            df.at[idx, 'product_name'] = new_filename.replace('.jpg', '').replace('_', ' ').title()
            
            # Update color in attributes_json
            import json
            try:
                attrs = json.loads(row['attributes_json'])
                attrs['color_primary'] = color_map.get(color, color)
                df.at[idx, 'attributes_json'] = json.dumps(attrs)
            except:
                pass
            
            print(f"Renamed: {filename} -> {new_filename}")

# Save updated CSV
df.to_csv(csv_path, index=False)
print(f"\nUpdated CSV saved with color information")
print(f"Total entries updated: {len([r for r in df.iterrows() if 921 <= int(os.path.basename(r[1]['file_path']).split('_')[0]) <= 1420])}")
