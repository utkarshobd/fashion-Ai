import pandas as pd

df = pd.read_csv('labels_sorted4.csv')
ethnic = df[df['sub_category'] == 'ethnic'].reset_index(drop=True)
western = df[df['sub_category'] == 'western'].reset_index(drop=True)

result = []
for i in range(max(len(ethnic), len(western))):
    if i < len(ethnic):
        result.append(ethnic.iloc[i])
    if i < len(western):
        result.append(western.iloc[i])

pd.DataFrame(result).to_csv('labels_sorted4.csv', index=False)
print(f'Done: {len(ethnic)} ethnic, {len(western)} western, {len(result)} total')
