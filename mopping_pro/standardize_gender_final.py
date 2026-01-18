import pandas as pd
import json

df = pd.read_csv("../labels_tested.csv")

gender_col_changes = 0
attributes_changes = 0

for idx in range(len(df)):
    # Fix gender column
    gender = str(df.iloc[idx]['gender']).lower()
    if gender in ['women', 'girl', 'girls']:
        df.at[idx, 'gender'] = 'Female'
        gender_col_changes += 1
    elif gender in ['boy', 'boys', 'men']:
        df.at[idx, 'gender'] = 'Male'
        gender_col_changes += 1
    
    # Fix attributes_json gender
    try:
        attributes = json.loads(df.iloc[idx]['attributes_json'])
        attr_gender = str(attributes.get('gender', '')).lower()
        
        if attr_gender in ['women', 'girl', 'girls']:
            attributes['gender'] = 'female'
            df.at[idx, 'attributes_json'] = json.dumps(attributes, ensure_ascii=False)
            attributes_changes += 1
        elif attr_gender in ['boy', 'boys', 'men']:
            attributes['gender'] = 'male'
            df.at[idx, 'attributes_json'] = json.dumps(attributes, ensure_ascii=False)
            attributes_changes += 1
    except:
        continue

print(f"Gender column changes: {gender_col_changes}")
print(f"Attributes_json gender changes: {attributes_changes}")

df.to_csv("../labels_tested.csv", index=False)
print("Updated labels_tested.csv!")