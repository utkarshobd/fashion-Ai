import pandas as pd

# Read the CSV file
df = pd.read_csv('annotations/labels_train.csv')

# Check unique values in sub_category column
print("Unique sub_category values:")
print(df['sub_category'].value_counts())
print(f"\nTotal unique values: {df['sub_category'].nunique()}")

# Show some examples of 'straight' entries if they exist
if 'straight' in df['sub_category'].values:
    print("\nExamples of 'straight' sub_category entries:")
    straight_examples = df[df['sub_category'] == 'straight'].head(10)
    print(straight_examples[['file_path', 'category', 'sub_category']])