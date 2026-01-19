import os
import glob

images_original_dir = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_original\ethnic\kurta"

if os.path.exists(images_original_dir):
    files = os.listdir(images_original_dir)
    print(f"Found {len(files)} files in images_original/ethnic/kurta")
    print(f"Deleting all {len(files)} files...")
    
    for file in files:
        file_path = os.path.join(images_original_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    print(f"Deleted {len(files)} images from images_original/ethnic/kurta")
else:
    print(f"Directory not found: {images_original_dir}")
