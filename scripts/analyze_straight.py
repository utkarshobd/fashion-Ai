import pandas as pd

# Read the original CSV file
df = pd.read_csv('labels_tested.csv')

# Filter for 'straight' sub_category
straight_data = df[df['sub_category'] == 'straight']

print("Analysis of 'straight' sub_category entries:")
print(f"Total 'straight' entries: {len(straight_data)}")
print("\nCategories with 'straight' sub_category:")
print(straight_data['category'].value_counts())

print("\nFile paths pattern for 'straight' entries:")
print(straight_data['file_path'].head(10).tolist())

print("\nSample of 'straight' entries:")
print(straight_data[['file_path', 'category', 'sub_category', 'gender']].head(10))