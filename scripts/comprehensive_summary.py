import pandas as pd

df = pd.read_csv('../annotations/labels_train.csv')

print(f"COMPREHENSIVE SUMMARY - labels_train.csv")
print(f"Total entries: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print("="*60)

columns_to_analyze = ['category', 'sub_category', 'color_primary', 'pattern', 'sub_class']

for col in columns_to_analyze:
    print(f"\n{col.upper()} ANALYSIS:")
    print("-" * 40)
    
    value_counts = df[col].value_counts(dropna=False)
    total = len(df)
    
    print(f"Unique values: {len(value_counts)}")
    print(f"Non-null entries: {df[col].notna().sum()}")
    print(f"Null entries: {df[col].isna().sum()}")
    
    print("\nTop values (Count | Percentage):")
    for value, count in value_counts.head(10).items():
        percentage = (count / total) * 100
        print(f"  {str(value):<20}: {count:>6} | {percentage:>6.2f}%")
    
    if len(value_counts) > 10:
        print(f"  ... and {len(value_counts) - 10} more values")
    
    print("="*60)