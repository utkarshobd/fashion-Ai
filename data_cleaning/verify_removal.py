import pandas as pd
import json

# Read the updated CSV file
df = pd.read_csv('annotations/labels_reorganized_updated.csv')

# Filter blouse_choli items
blouse_choli_df = df[df['category'] == 'blouse_choli'].head(5)

print("=== VERIFICATION: BLOUSE_CHOLI ATTRIBUTES AFTER REMOVAL ===\n")

for idx, row in blouse_choli_df.iterrows():
    print(f"Item {idx + 1}: {row['file_path']}")
    
    # Parse attributes
    try:
        attrs = json.loads(row['attributes_json'].replace('""', '"'))
        print("Attributes:", list(attrs.keys()))
        
        # Check if removed attributes are still present
        removed_attrs = ['fabric_hint', 'sleeve_length', 'length_category']
        still_present = [attr for attr in removed_attrs if attr in attrs]
        
        if still_present:
            print(f"❌ ERROR: These attributes are still present: {still_present}")
        else:
            print("✅ SUCCESS: All specified attributes removed")
            
        print("Full attributes:", attrs)
        print("-" * 60)
        
    except Exception as e:
        print(f"Error parsing attributes: {e}")
        print("-" * 60)

print(f"\nTotal blouse_choli items processed: {len(df[df['category'] == 'blouse_choli'])}")