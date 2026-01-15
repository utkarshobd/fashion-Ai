import pandas as pd
import json

df = pd.read_csv('tshirt_processed.csv')
print(f'Total rows: {len(df)}')
print(f'\nFirst 5 entries:\n')

for i in range(min(5, len(df))):
    print(f'{i+1}. File: {df.iloc[i]["file_path"]}')
    print(f'   Category: {df.iloc[i]["category"]}')
    print(f'   Sub-class: {df.iloc[i]["sub_class"]}')
    attrs = json.loads(df.iloc[i]['attributes_json'])
    print(f'   Fit: {attrs.get("fit", "N/A")}')
    print(f'   Pattern: {attrs.get("pattern", "N/A")}')
    print(f'   Color: {attrs.get("color_primary", "N/A")}')
    print()
