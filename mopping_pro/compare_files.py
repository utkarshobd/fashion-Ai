import pandas as pd
import json

# Load both files
original_df = pd.read_csv("../labels_test.csv")
fixed_df = pd.read_csv("../labels_test_lehenga_color_fixed.csv")

print(f"Original file rows: {len(original_df)}")
print(f"Fixed file rows: {len(fixed_df)}")

# Filter for lehengas only
orig_lehengas = original_df[original_df["category"] == "lehengas"].copy()
fixed_lehengas = fixed_df[fixed_df["category"] == "lehengas"].copy()

def get_color_primary(attributes_json):
    try:
        attrs = json.loads(attributes_json)
        return attrs.get("color_primary", "unknown")
    except:
        return "unknown"

# Get color counts
orig_colors = orig_lehengas["attributes_json"].apply(get_color_primary).value_counts()
fixed_colors = fixed_lehengas["attributes_json"].apply(get_color_primary).value_counts()

print("\nOriginal lehenga color counts:")
print(orig_colors.head(10))

print("\nFixed lehenga color counts:")  
print(fixed_colors.head(10))

print(f"\nOriginal unknown count: {orig_colors.get('unknown', 0)}")
print(f"Fixed unknown count: {fixed_colors.get('unknown', 0)}")

# Check if any changes were made
changes_made = orig_colors.get('unknown', 0) - fixed_colors.get('unknown', 0)
print(f"Changes made: {changes_made} unknown colors were fixed")