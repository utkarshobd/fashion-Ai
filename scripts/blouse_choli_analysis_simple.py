import pandas as pd
import json
from collections import Counter

# Read the CSV file
df = pd.read_csv('annotations/labels_reorganized.csv')

# Filter for ethnic/blouse_choli category
blouse_choli_df = df[df['sub_category'] == 'blouse_choli'].copy()

print("=== ETHNIC/BLOUSE_CHOLI METADATA ANALYSIS ===\n")
print(f"Total blouse_choli items: {len(blouse_choli_df)}")

# Parse attributes JSON
def parse_attributes(attr_str):
    try:
        return json.loads(attr_str.replace('""', '"'))
    except:
        return {}

blouse_choli_df['parsed_attributes'] = blouse_choli_df['attributes_json'].apply(parse_attributes)

# Extract individual attributes
attributes_data = {}
for attr in ['color_primary', 'fabric_hint', 'pattern', 'occasion_suitability', 'gender', 'sleeve_length', 'fit', 'length_category', 'season']:
    attributes_data[attr] = [attrs.get(attr, 'unknown') for attrs in blouse_choli_df['parsed_attributes']]

# Create DataFrame for analysis
attr_df = pd.DataFrame(attributes_data)

print("\n=== ATTRIBUTE DISTRIBUTION ANALYSIS ===\n")

# Color Analysis
print("1. COLOR PRIMARY DISTRIBUTION:")
color_counts = Counter(attr_df['color_primary'])
total_items = len(attr_df)

print(f"{'Color':<15} {'Count':<8} {'Percentage':<12} {'Visual Bar':<20}")
print("-" * 55)
max_count = max(color_counts.values())
for color, count in color_counts.most_common():
    percentage = (count / total_items) * 100
    bar_length = int((count / max_count) * 20)
    bar = "█" * bar_length
    print(f"{color:<15} {count:<8} {percentage:>6.1f}%     {bar:<20}")

# Fabric Analysis
print("\n2. FABRIC HINT DISTRIBUTION:")
fabric_counts = Counter(attr_df['fabric_hint'])
print(f"{'Fabric':<15} {'Count':<8} {'Percentage':<12} {'Visual Bar':<20}")
print("-" * 55)
max_count = max(fabric_counts.values())
for fabric, count in fabric_counts.most_common():
    percentage = (count / total_items) * 100
    bar_length = int((count / max_count) * 20)
    bar = "█" * bar_length
    print(f"{fabric:<15} {count:<8} {percentage:>6.1f}%     {bar:<20}")

# Pattern Analysis
print("\n3. PATTERN DISTRIBUTION:")
pattern_counts = Counter(attr_df['pattern'])
print(f"{'Pattern':<15} {'Count':<8} {'Percentage':<12} {'Visual Bar':<20}")
print("-" * 55)
max_count = max(pattern_counts.values())
for pattern, count in pattern_counts.most_common():
    percentage = (count / total_items) * 100
    bar_length = int((count / max_count) * 20)
    bar = "█" * bar_length
    print(f"{pattern:<15} {count:<8} {percentage:>6.1f}%     {bar:<20}")

# Occasion Analysis
print("\n4. OCCASION SUITABILITY:")
occasion_counts = Counter(attr_df['occasion_suitability'])
print(f"{'Occasion':<15} {'Count':<8} {'Percentage':<12} {'Visual Bar':<20}")
print("-" * 55)
max_count = max(occasion_counts.values())
for occasion, count in occasion_counts.most_common():
    percentage = (count / total_items) * 100
    bar_length = int((count / max_count) * 20)
    bar = "█" * bar_length
    print(f"{occasion:<15} {count:<8} {percentage:>6.1f}%     {bar:<20}")

# Sleeve Length Analysis
print("\n5. SLEEVE LENGTH DISTRIBUTION:")
sleeve_counts = Counter(attr_df['sleeve_length'])
print(f"{'Sleeve Length':<15} {'Count':<8} {'Percentage':<12} {'Visual Bar':<20}")
print("-" * 55)
max_count = max(sleeve_counts.values())
for sleeve, count in sleeve_counts.most_common():
    percentage = (count / total_items) * 100
    bar_length = int((count / max_count) * 20)
    bar = "█" * bar_length
    print(f"{sleeve:<15} {count:<8} {percentage:>6.1f}%     {bar:<20}")

print("\n=== COLOR DOMINANCE ANALYSIS ===\n")

# Top dominating colors
top_colors = color_counts.most_common(15)
print("TOP 15 DOMINATING COLORS:")
print(f"{'Rank':<5} {'Color':<15} {'Count':<8} {'Percentage':<12} {'Dominance Level':<15}")
print("-" * 65)
for i, (color, count) in enumerate(top_colors, 1):
    percentage = (count / total_items) * 100
    if percentage >= 10:
        dominance = "Very High"
    elif percentage >= 5:
        dominance = "High"
    elif percentage >= 2:
        dominance = "Medium"
    elif percentage >= 1:
        dominance = "Low"
    else:
        dominance = "Very Low"
    print(f"{i:<5} {color:<15} {count:<8} {percentage:>6.1f}%     {dominance:<15}")

# Lagging colors (bottom 15)
all_colors = color_counts.most_common()
bottom_colors = all_colors[-15:] if len(all_colors) >= 15 else all_colors
print(f"\nTOP {len(bottom_colors)} LAGGING COLORS:")
print(f"{'Rank':<5} {'Color':<15} {'Count':<8} {'Percentage':<12} {'Status':<15}")
print("-" * 65)
for i, (color, count) in enumerate(reversed(bottom_colors), 1):
    percentage = (count / total_items) * 100
    status = "Underrepresented" if percentage < 1 else "Rare"
    print(f"{i:<5} {color:<15} {count:<8} {percentage:>6.1f}%     {status:<15}")

print("\n=== FABRIC DOMINANCE ANALYSIS ===\n")

# Top dominating fabrics
top_fabrics = fabric_counts.most_common(10)
print("TOP 10 DOMINATING FABRICS:")
print(f"{'Rank':<5} {'Fabric':<15} {'Count':<8} {'Percentage':<12} {'Market Share':<15}")
print("-" * 65)
for i, (fabric, count) in enumerate(top_fabrics, 1):
    percentage = (count / total_items) * 100
    if percentage >= 20:
        share = "Dominant"
    elif percentage >= 10:
        share = "Major"
    elif percentage >= 5:
        share = "Significant"
    else:
        share = "Minor"
    print(f"{i:<5} {fabric:<15} {count:<8} {percentage:>6.1f}%     {share:<15}")

print("\n=== PATTERN DOMINANCE ANALYSIS ===\n")

print("PATTERN DOMINANCE RANKING:")
print(f"{'Rank':<5} {'Pattern':<15} {'Count':<8} {'Percentage':<12} {'Popularity':<15}")
print("-" * 65)
for i, (pattern, count) in enumerate(pattern_counts.most_common(), 1):
    percentage = (count / total_items) * 100
    if percentage >= 30:
        popularity = "Extremely Popular"
    elif percentage >= 20:
        popularity = "Very Popular"
    elif percentage >= 10:
        popularity = "Popular"
    elif percentage >= 5:
        popularity = "Moderate"
    else:
        popularity = "Limited"
    print(f"{i:<5} {pattern:<15} {count:<8} {percentage:>6.1f}%     {popularity:<15}")

print("\n=== COMPREHENSIVE SUMMARY INSIGHTS ===\n")

# Key insights
print("🎨 COLOR INSIGHTS:")
most_dominant_color = color_counts.most_common(1)[0]
print(f"   • Most dominant color: {most_dominant_color[0]} with {most_dominant_color[1]} items ({(most_dominant_color[1]/total_items)*100:.1f}%)")

# Top 5 colors
top_5_colors = color_counts.most_common(5)
print(f"   • Top 5 colors represent {sum([count for _, count in top_5_colors])} items ({(sum([count for _, count in top_5_colors])/total_items)*100:.1f}% of total)")

# Color diversity
unique_colors = len([color for color in color_counts.keys() if color != 'unknown'])
print(f"   • Color diversity: {unique_colors} unique colors identified")

print(f"\n🧵 FABRIC INSIGHTS:")
most_common_fabric = fabric_counts.most_common(1)[0]
print(f"   • Most common fabric: {most_common_fabric[0]} with {most_common_fabric[1]} items ({(most_common_fabric[1]/total_items)*100:.1f}%)")

# Fabric diversity
unique_fabrics = len([fabric for fabric in fabric_counts.keys() if fabric != 'unknown'])
print(f"   • Fabric diversity: {unique_fabrics} unique fabric types identified")

print(f"\n🎭 PATTERN INSIGHTS:")
most_common_pattern = pattern_counts.most_common(1)[0]
print(f"   • Most common pattern: {most_common_pattern[0]} with {most_common_pattern[1]} items ({(most_common_pattern[1]/total_items)*100:.1f}%)")

print(f"\n🎪 OCCASION INSIGHTS:")
primary_occasion = occasion_counts.most_common(1)[0]
print(f"   • Primary occasion: {primary_occasion[0]} with {primary_occasion[1]} items ({(primary_occasion[1]/total_items)*100:.1f}%)")

print(f"\n📊 DATA QUALITY METRICS:")
print(f"   • Unknown color entries: {color_counts.get('unknown', 0)} ({(color_counts.get('unknown', 0)/total_items)*100:.1f}%)")
print(f"   • Unknown fabric entries: {fabric_counts.get('unknown', 0)} ({(fabric_counts.get('unknown', 0)/total_items)*100:.1f}%)")
print(f"   • Unknown sleeve length: {sleeve_counts.get('unknown', 0)} ({(sleeve_counts.get('unknown', 0)/total_items)*100:.1f}%)")

# Market gaps analysis
print(f"\n🔍 MARKET GAPS & OPPORTUNITIES:")
rare_colors = [color for color, count in color_counts.items() if count == 1 and color != 'unknown']
if rare_colors:
    print(f"   • Single-item colors (potential gaps): {len(rare_colors)} colors")
    print(f"     Examples: {', '.join(rare_colors[:5])}")

low_rep_colors = [color for color, count in color_counts.items() if count <= 3 and color != 'unknown']
print(f"   • Underrepresented colors (≤3 items): {len(low_rep_colors)} colors")

print(f"\n✨ COLLECTION CHARACTERISTICS:")
print(f"   • Dataset completeness: {((total_items - color_counts.get('unknown', 0))/total_items)*100:.1f}% colors identified")
print(f"   • Fabric identification: {((total_items - fabric_counts.get('unknown', 0))/total_items)*100:.1f}% fabrics identified")
print(f"   • Average items per color: {total_items/len(color_counts):.1f}")
print(f"   • Average items per fabric: {total_items/len(fabric_counts):.1f}")

print(f"\n📈 BUSINESS INSIGHTS:")
# Calculate concentration ratios
top_3_colors_share = sum([count for _, count in color_counts.most_common(3)]) / total_items * 100
top_5_colors_share = sum([count for _, count in color_counts.most_common(5)]) / total_items * 100
print(f"   • Top 3 colors concentration: {top_3_colors_share:.1f}%")
print(f"   • Top 5 colors concentration: {top_5_colors_share:.1f}%")

if top_3_colors_share > 50:
    print(f"   • Market concentration: HIGH - Top 3 colors dominate the collection")
elif top_5_colors_share > 60:
    print(f"   • Market concentration: MEDIUM - Top 5 colors represent majority")
else:
    print(f"   • Market concentration: LOW - Well-distributed color portfolio")

print(f"\n" + "="*70)
print("ANALYSIS COMPLETE - ETHNIC/BLOUSE_CHOLI METADATA SUMMARY")
print("="*70)