import pandas as pd
import json

def fix_beige_yellow_colors():
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated_cleaned_fixed.csv"
    
    df = pd.read_csv(csv_file)
    print(f"Total rows: {len(df)}")
    
    fixed_count = 0
    
    # Process rows 3997 to 4423 (0-based indexing: 3996 to 4422)
    for idx in range(3996, min(4423, len(df))):
        product_name = str(df.iloc[idx]['product_name']).lower()
        
        # Parse current attributes
        current_attrs = json.loads(df.iloc[idx]['attributes_json'])
        current_color = current_attrs['color_primary']
        
        new_color = current_color  # Keep current as default
        
        # Skip if already multicolor
        if current_color == 'multicolor':
            continue
            
        # Check for beige specifically
        if 'beige' in product_name:
            new_color = 'beige'
        # Check for yellow specifically  
        elif 'yellow' in product_name:
            new_color = 'yellow'
        
        # Update if color changed
        if new_color != current_color:
            current_attrs['color_primary'] = new_color
            df.iloc[idx, df.columns.get_loc('attributes_json')] = json.dumps(current_attrs)
            fixed_count += 1
            print(f"Row {idx+1}: {product_name[:60]} -> {new_color}")
    
    # Save the updated file
    df.to_csv(csv_file, index=False)
    print(f"\nFixed {fixed_count} beige/yellow color attributes!")

if __name__ == "__main__":
    fix_beige_yellow_colors()