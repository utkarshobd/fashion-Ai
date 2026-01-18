import pandas as pd
import json
import re

def extract_color_from_name(product_name):
    if not isinstance(product_name, str):
        return None

    product_name = product_name.lower()

    color_map = {
        'red': ['red', 'maroon', 'crimson', 'burgundy', 'wine', 'cherry', 'rust', 'brick'],
        'blue': ['blue', 'navy', 'teal', 'turquoise', 'cobalt', 'sapphire', 'indigo', 'royal blue', 'sky blue'],
        'green': ['green', 'olive', 'emerald', 'mint', 'lime', 'forest', 'sage', 'bottle green', 'pista', 'mehendi'],
        'yellow': ['yellow', 'gold', 'golden', 'mustard', 'ochre', 'sunshine'],
        'pink': ['pink', 'rose', 'blush', 'coral', 'peach', 'magenta', 'rani pink', 'rani'],
        'purple': ['purple', 'violet', 'lavender', 'lilac', 'plum', 'mauve'],
        'orange': ['orange', 'saffron'],
        'black': ['black', 'charcoal', 'ebony'],
        'white': ['white', 'ivory', 'cream', 'off white', 'pearl'],
        'grey': ['grey', 'gray', 'silver'],
        'brown': ['brown', 'tan', 'chocolate', 'coffee', 'fawn'],
        'beige': ['beige', 'nude', 'champagne'],
        'multicolor': ['multicolor', 'multi color', 'mixed', 'combination']
    }

    for color, variants in color_map.items():
        for v in variants:
            if re.search(rf'\b{re.escape(v)}\b', product_name):
                return color
    return None

# Load CSV
df = pd.read_csv("../labels_test_lehenga_color_fixed.csv")

changes_made = 0
total_processed = 0

for idx in range(len(df)):
    if df.iloc[idx]['category'].lower() not in ['lehenga', 'lehengas']:
        continue
    
    total_processed += 1
    
    try:
        attributes = json.loads(df.iloc[idx]['attributes_json'])
    except:
        continue
    
    if str(attributes.get('color_primary', '')).lower() != 'unknown':
        continue
    
    product_name = str(df.iloc[idx]['product_name'])
    detected_color = extract_color_from_name(product_name)
    
    if detected_color:
        attributes['color_primary'] = detected_color
        df.at[idx, 'attributes_json'] = json.dumps(attributes, ensure_ascii=False)
        changes_made += 1
        print(f"Fixed: {product_name} -> {detected_color}")

print(f"\nProcessed {total_processed} lehengas")
print(f"Fixed {changes_made} unknown colors")

df.to_csv("../labels_test_lehenga_color_fixed.csv", index=False)
print("Updated file saved!")