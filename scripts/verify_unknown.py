import pandas as pd

# Read the updated labels_train.csv
df = pd.read_csv('../annotations/labels_train.csv')

# Check for unknown colors
unknown_count = (df['color_primary'] == 'unknown').sum()
print(f"Unknown colors in labels_train.csv: {unknown_count}")

if unknown_count > 0:
    print("\nSample entries with unknown color:")
    unknown_entries = df[df['color_primary'] == 'unknown'][['file_path', 'color_primary']].head(5)
    for _, row in unknown_entries.iterrows():
        print(f"  {row['file_path']} -> {row['color_primary']}")

# Show all unique colors
all_colors = df['color_primary'].value_counts()
print(f"\nAll colors ({len(all_colors)} total):")
for color, count in all_colors.items():
    print(f"  {color}: {count}")