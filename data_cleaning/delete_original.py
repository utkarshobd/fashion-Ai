import os

images_original_dir = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\images_original"

# List of files to remove (from previous run)
to_remove = []
with open('files_to_remove.txt', 'r') as f:
    to_remove = [line.strip() for line in f if line.strip()]

print(f"Attempting to remove {len(to_remove)} images from images_original folder...")

removed = 0
missing = 0

for file_path in to_remove:
    original_path = os.path.join(images_original_dir, file_path)
    if os.path.exists(original_path):
        os.remove(original_path)
        removed += 1
    else:
        missing += 1

print(f"Removed: {removed}")
print(f"Missing: {missing}")
print("Done!")
