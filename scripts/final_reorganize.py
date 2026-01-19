import pandas as pd

# Read the CSV file
df = pd.read_csv('annotations/labels.csv', on_bad_lines='skip', engine='python')

print(f"Total rows: {len(df)}")
print(f"Categories: {sorted(df['category'].unique())}")

# Define ethnic and western categories based on the data
ethnic_categories = ['saree', 'lehenga', 'kurta', 'sherwani', 'salwar_suit', 'blouse_choli', 'suit_salwar']
western_categories = ['shirt', 'jeans', 't_shirt', 'jacket', 'shorts', 'dress', 'trouser_chinos', 'skirt']

# Separate ethnic and western items
ethnic_items = df[df['category'].isin(ethnic_categories)].copy()
western_items = df[df['category'].isin(western_categories)].copy()

print(f"Ethnic items: {len(ethnic_items)}")
print(f"Western items: {len(western_items)}")

# Sort ethnic items by category, then by file_path
ethnic_sorted = ethnic_items.sort_values(['category', 'file_path'])

# Sort western items by category, then by file_path  
western_sorted = western_items.sort_values(['category', 'file_path'])

# Combine: ethnic first, then western
reorganized_df = pd.concat([ethnic_sorted, western_sorted], ignore_index=True)

# Save the reorganized CSV
reorganized_df.to_csv('annotations/labels.csv', index=False)

print(f"Reorganized CSV saved with {len(reorganized_df)} rows")

print("\nEthnic categories (in order):")
for cat in ethnic_categories:
    count = len(ethnic_sorted[ethnic_sorted['category'] == cat])
    if count > 0:
        print(f"  {cat}: {count} items")

print("\nWestern categories (in order):")
for cat in western_categories:
    count = len(western_sorted[western_sorted['category'] == cat])
    if count > 0:
        print(f"  {cat}: {count} items")

# Show first few rows of each major category for verification
print("\nFirst few ethnic items:")
print(ethnic_sorted[['file_path', 'category']].head(10))

print("\nFirst few western items:")
print(western_sorted[['file_path', 'category']].head(10))