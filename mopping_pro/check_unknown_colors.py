import pandas as pd
import json

# Load the CSV file
df = pd.read_csv("../labels_test_lehenga_color_fixed.csv")

# Filter for lehengas only
lehenga_df = df[df["category"] == "lehengas"].copy()

# Parse attributes_json
def safe_json_load(x):
    try:
        return json.loads(x)
    except:
        return {}

lehenga_df["attributes_parsed"] = lehenga_df["attributes_json"].apply(safe_json_load)

# Extract color_primary from parsed attributes
lehenga_df["color_primary"] = lehenga_df["attributes_parsed"].apply(
    lambda x: x.get("color_primary", "unknown")
)

# Filter for unknown colors
unknown_colors = lehenga_df[lehenga_df["color_primary"] == "unknown"]

print(f"Total lehengas with unknown color: {len(unknown_colors)}")
print("\nSample product names with unknown colors:")
print("=" * 50)

# Show first 10 product names
for i, (idx, row) in enumerate(unknown_colors.head(10).iterrows()):
    print(f"{i+1}. {row['product_name']}")

print("\n" + "=" * 50)
print("Checking if any color words are present in these names...")

# Check for color words in unknown entries
color_words = ['red', 'blue', 'green', 'yellow', 'pink', 'purple', 'orange', 
               'black', 'white', 'grey', 'gray', 'brown', 'maroon', 'navy',
               'gold', 'silver', 'cream', 'ivory', 'coral', 'peach']

found_colors = 0
for idx, row in unknown_colors.iterrows():
    name = str(row['product_name']).lower()
    for color in color_words:
        if color in name:
            print(f"Found '{color}' in: {row['product_name']}")
            found_colors += 1
            break

print(f"\nTotal unknown entries with color words in name: {found_colors}")