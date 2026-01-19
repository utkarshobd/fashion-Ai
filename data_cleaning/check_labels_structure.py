import pandas as pd

# Check the structure of labels.csv
print("Checking structure of annotations/labels.csv...")
df_labels = pd.read_csv('annotations/labels.csv')

print(f"Shape: {df_labels.shape}")
print(f"Columns: {list(df_labels.columns)}")
print("\nFirst few rows:")
print(df_labels.head())

# Check if there's a color_primary column or similar
color_columns = [col for col in df_labels.columns if 'color' in col.lower()]
print(f"\nColor-related columns: {color_columns}")

# Check for unknown values in any column
for col in df_labels.columns:
    if df_labels[col].dtype == 'object':  # Only check string columns
        unknown_count = (df_labels[col] == 'unknown').sum()
        if unknown_count > 0:
            print(f"Column '{col}' has {unknown_count} 'unknown' values")