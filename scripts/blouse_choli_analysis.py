import pandas as pd
import json
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

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

print(f"{'Color':<15} {'Count':<8} {'Percentage':<12}")
print("-" * 35)
for color, count in color_counts.most_common():
    percentage = (count / total_items) * 100
    print(f"{color:<15} {count:<8} {percentage:.1f}%")

# Fabric Analysis
print("\n2. FABRIC HINT DISTRIBUTION:")
fabric_counts = Counter(attr_df['fabric_hint'])
print(f"{'Fabric':<15} {'Count':<8} {'Percentage':<12}")
print("-" * 35)
for fabric, count in fabric_counts.most_common():
    percentage = (count / total_items) * 100
    print(f"{fabric:<15} {count:<8} {percentage:.1f}%")

# Pattern Analysis
print("\n3. PATTERN DISTRIBUTION:")
pattern_counts = Counter(attr_df['pattern'])
print(f"{'Pattern':<15} {'Count':<8} {'Percentage':<12}")
print("-" * 35)
for pattern, count in pattern_counts.most_common():
    percentage = (count / total_items) * 100
    print(f"{pattern:<15} {count:<8} {percentage:.1f}%")

# Occasion Analysis
print("\n4. OCCASION SUITABILITY:")
occasion_counts = Counter(attr_df['occasion_suitability'])
print(f"{'Occasion':<15} {'Count':<8} {'Percentage':<12}")
print("-" * 35)
for occasion, count in occasion_counts.most_common():
    percentage = (count / total_items) * 100
    print(f"{occasion:<15} {count:<8} {percentage:.1f}%")

# Sleeve Length Analysis
print("\n5. SLEEVE LENGTH DISTRIBUTION:")
sleeve_counts = Counter(attr_df['sleeve_length'])
print(f"{'Sleeve Length':<15} {'Count':<8} {'Percentage':<12}")
print("-" * 35)
for sleeve, count in sleeve_counts.most_common():
    percentage = (count / total_items) * 100
    print(f"{sleeve:<15} {count:<8} {percentage:.1f}%")

# Fit Analysis
print("\n6. FIT DISTRIBUTION:")
fit_counts = Counter(attr_df['fit'])
print(f"{'Fit':<15} {'Count':<8} {'Percentage':<12}")
print("-" * 35)
for fit, count in fit_counts.most_common():
    percentage = (count / total_items) * 100
    print(f"{fit:<15} {count:<8} {percentage:.1f}%")

print("\n=== COLOR DOMINANCE ANALYSIS ===\n")

# Top dominating colors
top_colors = color_counts.most_common(10)
print("TOP 10 DOMINATING COLORS:")
for i, (color, count) in enumerate(top_colors, 1):
    percentage = (count / total_items) * 100
    print(f"{i:2d}. {color:<15} - {count:3d} items ({percentage:.1f}%)")

# Lagging colors (bottom 10)
bottom_colors = color_counts.most_common()[-10:]
print("\nTOP 10 LAGGING COLORS:")
for i, (color, count) in enumerate(reversed(bottom_colors), 1):
    percentage = (count / total_items) * 100
    print(f"{i:2d}. {color:<15} - {count:3d} items ({percentage:.1f}%)")

print("\n=== FABRIC DOMINANCE ANALYSIS ===\n")

# Top dominating fabrics
top_fabrics = fabric_counts.most_common(10)
print("TOP 10 DOMINATING FABRICS:")
for i, (fabric, count) in enumerate(top_fabrics, 1):
    percentage = (count / total_items) * 100
    print(f"{i:2d}. {fabric:<15} - {count:3d} items ({percentage:.1f}%)")

print("\n=== PATTERN DOMINANCE ANALYSIS ===\n")

# Pattern dominance
print("PATTERN DOMINANCE:")
for i, (pattern, count) in enumerate(pattern_counts.most_common(), 1):
    percentage = (count / total_items) * 100
    print(f"{i:2d}. {pattern:<15} - {count:3d} items ({percentage:.1f}%)")

print("\n=== SUMMARY INSIGHTS ===\n")

# Key insights
print("KEY INSIGHTS:")
print(f"• Most dominant color: {color_counts.most_common(1)[0][0]} ({(color_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")
print(f"• Most common fabric: {fabric_counts.most_common(1)[0][0]} ({(fabric_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")
print(f"• Most common pattern: {pattern_counts.most_common(1)[0][0]} ({(pattern_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")
print(f"• Primary occasion: {occasion_counts.most_common(1)[0][0]} ({(occasion_counts.most_common(1)[0][1]/total_items)*100:.1f}%)")

# Color diversity
unique_colors = len([color for color in color_counts.keys() if color != 'unknown'])
print(f"• Color diversity: {unique_colors} unique colors identified")

# Fabric diversity
unique_fabrics = len([fabric for fabric in fabric_counts.keys() if fabric != 'unknown'])
print(f"• Fabric diversity: {unique_fabrics} unique fabric types identified")

print(f"\n=== DATA QUALITY METRICS ===\n")
print(f"• Unknown color entries: {color_counts.get('unknown', 0)} ({(color_counts.get('unknown', 0)/total_items)*100:.1f}%)")
print(f"• Unknown fabric entries: {fabric_counts.get('unknown', 0)} ({(fabric_counts.get('unknown', 0)/total_items)*100:.1f}%)")
print(f"• Unknown sleeve length: {sleeve_counts.get('unknown', 0)} ({(sleeve_counts.get('unknown', 0)/total_items)*100:.1f}%)")

# Create visualizations
plt.figure(figsize=(15, 12))

# Color distribution pie chart
plt.subplot(2, 3, 1)
top_10_colors = dict(color_counts.most_common(10))
others_count = sum(color_counts.values()) - sum(top_10_colors.values())
if others_count > 0:
    top_10_colors['Others'] = others_count

plt.pie(top_10_colors.values(), labels=top_10_colors.keys(), autopct='%1.1f%%', startangle=90)
plt.title('Top 10 Colors Distribution')

# Fabric distribution
plt.subplot(2, 3, 2)
fabric_data = dict(fabric_counts.most_common(8))
plt.bar(fabric_data.keys(), fabric_data.values())
plt.title('Fabric Distribution')
plt.xticks(rotation=45)

# Pattern distribution
plt.subplot(2, 3, 3)
pattern_data = dict(pattern_counts.most_common())
plt.bar(pattern_data.keys(), pattern_data.values())
plt.title('Pattern Distribution')
plt.xticks(rotation=45)

# Occasion distribution
plt.subplot(2, 3, 4)
occasion_data = dict(occasion_counts.most_common())
plt.bar(occasion_data.keys(), occasion_data.values())
plt.title('Occasion Suitability')
plt.xticks(rotation=45)

# Sleeve length distribution
plt.subplot(2, 3, 5)
sleeve_data = dict(sleeve_counts.most_common())
plt.bar(sleeve_data.keys(), sleeve_data.values())
plt.title('Sleeve Length Distribution')
plt.xticks(rotation=45)

# Fit distribution
plt.subplot(2, 3, 6)
fit_data = dict(fit_counts.most_common())
plt.bar(fit_data.keys(), fit_data.values())
plt.title('Fit Distribution')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('blouse_choli_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nAnalysis complete! Visualization saved as 'blouse_choli_analysis.png'")