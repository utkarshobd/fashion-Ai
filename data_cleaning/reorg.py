import pandas as pd
import json
import re

def extract_color_from_name(product_name):
    """Extract color from product name using safe word-boundary matching"""
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


def fix_attributes_for_rows(csv_file_path, start_row, end_row):
    """Fix color_primary ONLY when it is 'unknown' AND category is lehenga"""

    df = pd.read_csv(csv_file_path)

    print(f"Total rows in CSV: {len(df)}")
    print(f"Fixing lehenga color_primary from rows {start_row} to {end_row}")

    for idx in range(start_row - 1, min(end_row, len(df))):

        # ---- CATEGORY FILTER (lehenga only) ----
        category = str(df.iloc[idx]['category']).lower()
        if category not in ['lehenga', 'lehengas']:
            continue

        product_name = str(df.iloc[idx]['product_name'])

        try:
            attributes = json.loads(df.iloc[idx]['attributes_json'])
        except Exception:
            continue

        # ---- UPDATE ONLY IF color_primary IS unknown ----
        existing_color = str(attributes.get('color_primary', '')).lower()
        if existing_color != 'unknown':
            continue

        detected_color = extract_color_from_name(product_name)

        if detected_color:
            attributes['color_primary'] = detected_color
            df.at[idx, 'attributes_json'] = json.dumps(attributes, ensure_ascii=False)

        if (idx + 1) % 50 == 0:
            print(f"Processed row {idx + 1}")

    output_file = csv_file_path.replace('.csv', '_lehenga_color_fixed.csv')
    df.to_csv(output_file, index=False)

    print(f"Fixed CSV saved as: {output_file}")
    return output_file


# Main execution
if __name__ == "__main__":
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\labels_test.csv"

    fixed_file = fix_attributes_for_rows(csv_file, 4428, 5921)

    print("Lehenga color correction completed!")
    print(f"Fixed file: {fixed_file}")
