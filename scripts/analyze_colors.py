import pandas as pd

# Read the current data
df = pd.read_csv('annotations/labels_train.csv')

print("Current color_primary values and their counts:")
color_counts = df['color_primary'].value_counts()
print(color_counts)

print(f"\nTotal unique colors: {df['color_primary'].nunique()}")
print(f"Total entries: {len(df)}")

# Show all unique colors for mapping analysis
print("\nAll unique color values:")
unique_colors = sorted(df['color_primary'].unique())
for i, color in enumerate(unique_colors, 1):
    print(f"{i:2d}. {color}")