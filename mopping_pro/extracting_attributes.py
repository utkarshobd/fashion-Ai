import pandas as pd
import json
import re

def extract_color_from_name(product_name):
    """Extract color from product name using intelligent pattern matching"""
    product_name = product_name.lower()
    
    # Color mapping dictionary
    color_map = {
        'red': ['red', 'maroon', 'crimson', 'burgundy', 'wine', 'cherry', 'rust', 'brick'],
        'blue': ['blue', 'navy', 'teal', 'turquoise', 'cobalt', 'sapphire', 'azure', 'indigo', 'royal blue', 'powder blue', 'sky blue', 'dusty blue'],
        'green': ['green', 'olive', 'emerald', 'mint', 'lime', 'forest', 'sage', 'bottle green', 'sea green', 'pista', 'mehendi', 'moss'],
        'yellow': ['yellow', 'gold', 'golden', 'mustard', 'ochre', 'amber', 'cream', 'beige', 'champagne', 'marigold'],
        'pink': ['pink', 'rose', 'blush', 'coral', 'salmon', 'peach', 'magenta', 'fuchsia', 'hot pink', 'rani pink', 'flamingo'],
        'purple': ['purple', 'violet', 'lavender', 'lilac', 'plum', 'mauve', 'amethyst', 'grape','wine'],
        'orange': ['orange', 'tangerine', 'saffron', 'burnt orange', 'mango'],
        'black': ['black', 'charcoal', 'ebony', 'jet', 'midnight'],
        'white': ['white', 'ivory', 'cream', 'off white', 'pearl', 'snow'],
        'grey': ['grey', 'gray', 'silver', 'ash', 'slate', 'steel'],
        'brown': ['brown', 'tan', 'chocolate', 'coffee', 'caramel', 'bronze', 'mahogany','fawn'],
        'multicolor': ['multicolor', 'multi', 'rainbow', 'mixed', 'combination']
    }
    
    # Check for color matches
    for color, variants in color_map.items():
        for variant in variants:
            if variant in product_name:
                return color
    
    return 'unknown'

def extract_pattern_from_name(product_name):
    """Extract pattern from product name"""
    product_name = product_name.lower()
    
    pattern_keywords = {
        'printed': ['print', 'printed', 'floral print', 'geometric print', 'paisley print'],
        'embroidered': ['embroidered', 'embroidery', 'zardozi', 'sequin', 'sequins', 'beads', 'thread work', 'hand embroidered', 'resham', 'mirror work'],
        'solid': ['solid', 'plain'],
        'striped': ['stripe', 'striped', 'stripes'],
        'floral': ['floral', 'flower', 'botanical'],
        'geometric': ['geometric', 'paisley', 'mandarin', 'motif', 'pattern'],
        'checked': ['check', 'checked', 'checkered'],
        'polka': ['polka', 'dot', 'dotted']
    }
    
    # Check for embroidered patterns first (higher priority)
    if any(word in product_name for word in ['embroidered', 'embroidery', 'zardozi', 'sequin', 'sequins', 'beads', 'thread work', 'resham', 'mirror work']):
        return 'embroidered'
    
    # Check for printed patterns
    if any(word in product_name for word in ['print', 'printed']):
        return 'printed'
    
    # Check for other patterns
    for pattern, keywords in pattern_keywords.items():
        if any(keyword in product_name for keyword in keywords):
            return pattern
    
    return 'solid'  # Default to solid if no pattern found

def extract_occasion_from_name(product_name):
    """Extract occasion from product name"""
    product_name = product_name.lower()
    
    occasion_keywords = {
        'wedding': ['wedding', 'bridal', 'bride'],
        'festive': ['festive', 'festival', 'celebration', 'party', 'evening wear'],
        'formal': ['formal', 'office', 'work'],
        'casual': ['casual', 'daily', 'everyday']
    }
    
    # Check for specific occasions
    for occasion, keywords in occasion_keywords.items():
        if any(keyword in product_name for keyword in keywords):
            return occasion
    
    # Default logic based on item type
    if any(word in product_name for word in ['saree', 'lehenga', 'blouse', 'choli']):
        return 'festive'  # Ethnic wear is typically festive
    
    return 'casual'  # Default to casual

def fix_attributes_for_rows(csv_file_path, start_row, end_row):
    """Fix attributes for specified rows using intelligent extraction"""
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    print(f"Total rows in CSV: {len(df)}")
    print(f"Fixing rows {start_row} to {end_row}")
    
    # Process the specified rows
    for idx in range(start_row - 1, min(end_row, len(df))):  # Convert to 0-based indexing
        product_name = str(df.iloc[idx]['product_name'])
        
        # Extract attributes intelligently
        color = extract_color_from_name(product_name)
        pattern = extract_pattern_from_name(product_name)
        occasion = extract_occasion_from_name(product_name)
        
        # Create new attributes JSON
        new_attributes = {
            "color_primary": color,
            "pattern": pattern,
            "occasion_suitability": occasion,
            "gender": "female",  # As specified
            "fit": "regular",    # As specified
            "season": "all"      # Default
        }
        
        # Update the attributes_json column
        df.iloc[idx, df.columns.get_loc('attributes_json')] = json.dumps(new_attributes)
        
        if idx % 50 == 0:  # Progress indicator
            print(f"Processed row {idx + 1}: {product_name[:50]}...")
    
    # Save the updated CSV
    output_file = csv_file_path.replace('.csv', '_fixed.csv')
    df.to_csv(output_file, index=False)
    print(f"Fixed CSV saved as: {output_file}")
    
    return output_file

# Main execution
if __name__ == "__main__":
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_fixed_suit_salwar.csv"
    
    # Fix rows 3997 to 4423
    fixed_file = fix_attributes_for_rows(csv_file, 24287, 24611)
    
    print("Attribute fixing completed!")
    print(f"Fixed file: {fixed_file}")