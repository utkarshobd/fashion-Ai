import pandas as pd

df = pd.read_csv('../annotations/labels_train.csv')

pattern_counts = df['pattern'].value_counts(dropna=False)
total = len(df)

print(f"PATTERN ANALYSIS - Total entries: {total}")
print("="*40)

for value, count in pattern_counts.items():
    percentage = (count / total) * 100
    print(f"{str(value):<15}: {count:>6} | {percentage:>6.2f}%")