import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('annotations/labels_reorganized.csv')

print("=== EXPLORING DATASET STRUCTURE ===\n")
print(f"Total items in dataset: {len(df)}")

print("\nUnique categories:")
print(df['category'].value_counts())

print("\nUnique sub_categories:")
print(df['sub_category'].value_counts())

# Check for blouse_choli in different columns
print("\nSearching for 'blouse_choli' in different columns:")
print(f"In 'category' column: {(df['category'] == 'blouse_choli').sum()}")
print(f"In 'sub_category' column: {(df['sub_category'] == 'blouse_choli').sum()}")

# Check file paths containing blouse_choli
blouse_choli_paths = df[df['file_path'].str.contains('blouse_choli', na=False)]
print(f"\nItems with 'blouse_choli' in file_path: {len(blouse_choli_paths)}")

if len(blouse_choli_paths) > 0:
    print("\nFirst few blouse_choli items:")
    print(blouse_choli_paths[['file_path', 'category', 'sub_category']].head())
    
    # Use the correct filtering
    blouse_choli_df = blouse_choli_paths.copy()
    
    print(f"\n=== ETHNIC/BLOUSE_CHOLI METADATA ANALYSIS ===")
    print(f"Total blouse_choli items: {len(blouse_choli_df)}")
    
    # Parse attributes JSON
    def parse_attributes(attr_str):
        try:
            return json.loads(attr_str.replace('""', '"'))
        except:
            return {}
    
    blouse_choli_df['parsed_attributes'] = blouse_choli_df['attributes_json'].apply(parse_attributes)
    
    # Extract color information
    colors = []
    fabrics = []
    patterns = []
    occasions = []
    
    for attrs in blouse_choli_df['parsed_attributes']:
        colors.append(attrs.get('color_primary', 'unknown'))
        fabrics.append(attrs.get('fabric_hint', 'unknown'))
        patterns.append(attrs.get('pattern', 'unknown'))
        occasions.append(attrs.get('occasion_suitability', 'unknown'))
    
    from collections import Counter
    
    color_counts = Counter(colors)
    fabric_counts = Counter(fabrics)
    pattern_counts = Counter(patterns)
    occasion_counts = Counter(occasions)
    
    total_items = len(blouse_choli_df)
    
    print(f"\n=== COLOR ANALYSIS ===")
    print(f"{'Color':<15} {'Count':<8} {'Percentage':<12}")
    print("-" * 35)
    for color, count in color_counts.most_common(20):
        percentage = (count / total_items) * 100
        print(f"{color:<15} {count:<8} {percentage:.1f}%")
    
    print(f"\n=== FABRIC ANALYSIS ===")
    print(f"{'Fabric':<15} {'Count':<8} {'Percentage':<12}")
    print("-" * 35)
    for fabric, count in fabric_counts.most_common(15):
        percentage = (count / total_items) * 100
        print(f"{fabric:<15} {count:<8} {percentage:.1f}%")
    
    print(f"\n=== PATTERN ANALYSIS ===")
    print(f"{'Pattern':<15} {'Count':<8} {'Percentage':<12}")
    print("-" * 35)
    for pattern, count in pattern_counts.most_common():
        percentage = (count / total_items) * 100
        print(f"{pattern:<15} {count:<8} {percentage:.1f}%")
    
    print(f"\n=== DOMINANCE & LAGGING ANALYSIS ===")
    
    print(f"\nTOP 10 DOMINATING COLORS:")
    for i, (color, count) in enumerate(color_counts.most_common(10), 1):
        percentage = (count / total_items) * 100
        print(f"{i:2d}. {color:<15} - {count:3d} items ({percentage:.1f}%)")
    
    print(f"\nTOP 10 LAGGING COLORS:")
    all_colors = list(color_counts.items())
    bottom_colors = sorted(all_colors, key=lambda x: x[1])[:10]
    for i, (color, count) in enumerate(bottom_colors, 1):
        percentage = (count / total_items) * 100
        print(f"{i:2d}. {color:<15} - {count:3d} items ({percentage:.1f}%)")
    
    print(f"\n=== SUMMARY INSIGHTS ===")
    print(f"• Total unique colors: {len(color_counts)}")
    print(f"• Total unique fabrics: {len(fabric_counts)}")
    print(f"• Total unique patterns: {len(pattern_counts)}")
    print(f"• Most dominant color: {color_counts.most_common(1)[0][0]} ({(color_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")
    print(f"• Most common fabric: {fabric_counts.most_common(1)[0][0]} ({(fabric_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")
    print(f"• Most common pattern: {pattern_counts.most_common(1)[0][0]} ({(pattern_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")
    
else:
    print("No blouse_choli items found in the dataset!")