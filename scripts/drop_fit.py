import pandas as pd

df = pd.read_csv('../annotations/labels_train.csv')
df = df.drop('fit', axis=1)
df.to_csv('../annotations/labels_train.csv', index=False)

print(f"Fit column dropped. New columns: {list(df.columns)}")
print(f"Total entries: {len(df)}")