import pandas as pd
import json

# Load CSV
df = pd.read_csv("labels_test_lehenga_color_fixed.csv", engine="python", on_bad_lines="skip")

# Filter lehengas
lehenga_df = df[df["category"] == "lehengas"].copy()

print(f"Total lehengas: {len(lehenga_df)}")
print("\nFirst 10 lehenga product names:")
for i, row in lehenga_df.head(10).iterrows():
    print(f"{i}: {row['product_name']}")
    
    # Check attributes
    try:
        attrs = json.loads(row['attributes_json'])
        color = attrs.get('color_primary', 'N/A')
        print(f"   Color: {color}")
    except:
        print("   Color: Error parsing JSON")
    print()