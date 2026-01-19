import pandas as pd

# Fix labels_tested.csv
print("Fixing labels_tested.csv...")
df_tested = pd.read_csv('labels_tested.csv')
print(f"Before fix - straight entries: {(df_tested['sub_category'] == 'straight').sum()}")

df_tested['sub_category'] = df_tested['sub_category'].replace('straight', 'ethnic')
df_tested.to_csv('labels_tested.csv', index=False)
print(f"After fix - straight entries: {(df_tested['sub_category'] == 'straight').sum()}")

# Fix labels_train.csv
print("\nFixing annotations/labels_train.csv...")
df_train = pd.read_csv('annotations/labels_train.csv')
print(f"Before fix - straight entries: {(df_train['sub_category'] == 'straight').sum()}")

df_train['sub_category'] = df_train['sub_category'].replace('straight', 'ethnic')
df_train.to_csv('annotations/labels_train.csv', index=False)
print(f"After fix - straight entries: {(df_train['sub_category'] == 'straight').sum()}")

# Verify final counts
print("\nFinal sub_category counts in labels_tested.csv:")
print(df_tested['sub_category'].value_counts())

print("\nFinal sub_category counts in labels_train.csv:")
print(df_train['sub_category'].value_counts())