import pandas as pd
import json

def fix_multicolor_in_fixed_csv():
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated_cleaned_fixed.csv"
    
    df = pd.read_csv(csv_file)
    print(f"Total rows: {len(df)}")
    
    fixed_count = 0
    
    # Process rows 3997 to 4423 (0-based indexing: 3996 to 4422)
    for idx in range(3996, min(4423, len(df))):
        product_name = str(df.iloc[idx]['product_name']).lower()
        
        # Parse current attributes
        current_attrs = json.loads(df.iloc[idx]['attributes_json'])
        
        # Fix color detection
        new_color = current_attrs['color_primary']  # Keep current as default
        
        # Check for multicolor keywords first
        if any(word in product_name for word in ['multi coloured', 'multicoloured', 'multi colored', 'multicolored']):
            new_color = 'multicolor'
        else:
            # Count individual colors
            colors_found = []
            color_words = {
                'red': ['red', 'maroon', 'crimson', 'rust'],
                'blue': ['blue', 'navy', 'teal', 'turquoise'],
                'green': ['green', 'olive', 'emerald', 'mint', 'lime', 'forest', 'sage', 'pista', 'mehendi'],
                'yellow': ['yellow', 'gold', 'golden', 'mustard', 'ochre', 'amber', 'beige', 'cream'],
                'pink': ['pink', 'rose', 'coral', 'peach', 'magenta', 'fuchsia'],
                'purple': ['purple', 'violet', 'lavender', 'lilac', 'plum', 'mauve'],
                'orange': ['orange', 'tangerine', 'saffron'],
                'black': ['black', 'charcoal', 'ebony'],
                'white': ['white', 'ivory', 'cream'],
                'grey': ['grey', 'gray', 'silver', 'ash'],
                'brown': ['brown', 'tan', 'chocolate', 'coffee', 'caramel', 'bronze']
            }
            
            for color, variants in color_words.items():
                if any(variant in product_name for variant in variants):
                    colors_found.append(color)
            
            # If 2+ colors found, it's multicolor
            if len(colors_found) >= 2:
                new_color = 'multicolor'
            elif len(colors_found) == 1:
                new_color = colors_found[0]
        
        # Update attributes if color changed
        if new_color != current_attrs['color_primary']:
            current_attrs['color_primary'] = new_color
            df.iloc[idx, df.columns.get_loc('attributes_json')] = json.dumps(current_attrs)
            fixed_count += 1
            
            if fixed_count <= 10:  # Show first 10 changes
                print(f"Row {idx+1}: {product_name[:50]} -> {new_color}")
    
    # Save the updated file
    df.to_csv(csv_file, index=False)
    print(f"\nFixed {fixed_count} color attributes in the _fixed.csv file!")

if __name__ == "__main__":
    fix_multicolor_in_fixed_csv()