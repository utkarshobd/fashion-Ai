import pandas as pd

PATTERN_MAP = {
    # solid
    "solid": "solid",
    "denim": "solid",
    "woven": "solid",
    "chino": "solid",
    "cargo": "solid",
    "bermuda": "solid",
    "hot_pants": "solid",

    # printed
    "printed": "printed",
    "floral": "printed",
    "geometric": "printed",
    "polka_dot": "printed",
    "animal_print": "printed",
    "camouflage": "printed",
    "self-design": "printed",
    "embellished": "printed",

    # striped / checked / embroidered
    "striped": "striped",
    "checked": "checked",
    "embroidered": "embroidered",

    # activity → solid
    "sports": "solid",
    "training": "solid",
    "running": "solid",
    "cycling": "solid",
    "yoga": "solid",
    "lounge": "solid",
    "biker": "solid"
}

df = pd.read_csv('../annotations/labels_train.csv')
df['pattern'] = df['pattern'].map(PATTERN_MAP)
df.to_csv('../annotations/labels_train.csv', index=False)

# Show new distribution
pattern_counts = df['pattern'].value_counts(dropna=False)
total = len(df)

print(f"UPDATED PATTERN DISTRIBUTION - Total: {total}")
print("="*40)
for value, count in pattern_counts.items():
    percentage = (count / total) * 100
    print(f"{str(value):<15}: {count:>6} | {percentage:>6.2f}%")