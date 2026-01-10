import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('annotations/labels_reorganized.csv')

# Function to remove specified attributes from JSON string
def remove_attributes(attr_str):
    try:
        # Handle the triple quote format properly
        attrs = json.loads(attr_str.replace('"""', '"'))
        
        # Remove the specified attributes
        attrs.pop('fabric_hint', None)
        attrs.pop('sleeve_length', None)
        attrs.pop('length_category', None)
        
        # Convert back to JSON string with triple quotes to match original format
        return json.dumps(attrs).replace('"', '"""')
    except:
        return attr_str

# Filter blouse_choli items and update their attributes
blouse_choli_mask = df['category'] == 'blouse_choli'
df.loc[blouse_choli_mask, 'attributes_json'] = df.loc[blouse_choli_mask, 'attributes_json'].apply(remove_attributes)

# Save the updated CSV
df.to_csv('annotations/labels_reorganized_corrected.csv', index=False)

print(f"Updated {blouse_choli_mask.sum()} blouse_choli items")
print("Removed attributes: fabric_hint, sleeve_length, length_category")
print("Fixed JSON format with proper triple quotes")
print("Updated file saved as: annotations/labels_reorganized_corrected.csv")