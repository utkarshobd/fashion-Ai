import pandas as pd
import json

# Read labels.csv and extract primary_color from JSON attributes
df_labels = pd.read_csv('../annotations/labels.csv')
primary_colors = []

for _, row in df_labels.iterrows():
    try:
        attributes = json.loads(row['attributes'])
        primary_color = attributes.get('primary_color', 'N/A')
        primary_colors.append(primary_color)
    except:
        primary_colors.append('N/A')

# Read labels_train.csv
df_train = pd.read_csv('../annotations/labels_train.csv')

print("PRIMARY_COLOR ANALYSIS (labels.csv)")
print("="*50)
primary_color_counts = pd.Series(primary_colors).value_counts(dropna=False)
total_labels = len(primary_colors)

print(f"Total entries: {total_labels}")
print(f"Unique values: {len(primary_color_counts)}")

print("\nDistribution:")
for value, count in primary_color_counts.items():
    percentage = (count / total_labels) * 100
    print(f"  {str(value):<15}: {count:>6} | {percentage:>6.2f}%")

print("\n" + "="*50)
print("COLOR_PRIMARY ANALYSIS (labels_train.csv)")
print("="*50)

color_primary_counts = df_train['color_primary'].value_counts(dropna=False)
total_train = len(df_train)

print(f"Total entries: {total_train}")
print(f"Unique values: {len(color_primary_counts)}")

print("\nDistribution:")
for value, count in color_primary_counts.items():
    percentage = (count / total_train) * 100
    print(f"  {str(value):<15}: {count:>6} | {percentage:>6.2f}%")