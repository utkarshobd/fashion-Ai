import pandas as pd
import json
import re

def extract_color_intelligently(product_name):
    """Extract color with proper multi-color detection"""
    product_name = product_name.lower()
    
    # First check for explicit multicolor keywords
    multicolor_keywords = ['multicolor', 'multi color', 'multi coloured', 'multicoloured', 'multi-color', 'multi-coloured']
    if any(keyword in product_name for keyword in multicolor_keywords):
        return 'multicolor'
    
    # Define individual colors
    color_patterns = {
        'red': r'\b(red|maroon|crimson|burgundy|wine|cherry|rust|brick)\b',
        'blue': r'\b(blue|navy|teal|turquoise|cobalt|sapphire|azure|indigo)\b',
        'green': r'\b(green|olive|emerald|mint|lime|forest|sage|bottle green|sea green|pista|mehendi|moss)\b',
        'yellow': r'\b(yellow|gold|golden|mustard|ochre|amber|beige|champagne|marigold)\b',
        'pink': r'\b(pink|rose|blush|coral|salmon|peach|magenta|fuchsia|hot pink|rani pink|flamingo)\b',
        'purple': r'\b(purple|violet|lavender|lilac|plum|mauve|amethyst|grape)\b',
        'orange': r'\b(orange|tangerine|saffron|burnt orange|mango)\b',
        'black': r'\b(black|charcoal|ebony|jet|midnight)\b',
        'white': r'\b(white|ivory|cream|off white|pearl|snow)\b',
        'grey': r'\b(grey|gray|silver|ash|slate|steel)\b',
        'brown': r'\b(brown|tan|chocolate|coffee|caramel|bronze|mahogany)\b'
    }
    
    # Count how many different colors are mentioned
    found_colors = []
    for color, pattern in color_patterns.items():
        if re.search(pattern, product_name):
            found_colors.append(color)
    
    # If more than 2 colors found, it's multicolor
    if len(found_colors) >= 2:
        return 'multicolor'
    
    # If exactly one color found, return that color
    if len(found_colors) == 1:
        return found_colors[0]
    
    return 'unknown'

def extract_pattern_from_name(product_name):
    """Extract pattern from product name"""
    product_name = product_name.lower()
    
    # Check for embroidered patterns first (higher priority)
    if any(word in product_name for word in ['embroidered', 'embroidery', 'zardozi', 'sequin', 'sequins', 'beads', 'thread work', 'resham', 'mirror work']):
        return 'embroidered'
    
    # Check for printed patterns
    if any(word in product_name for word in ['print', 'printed']):
        return 'printed'
    
    # Check for other patterns
    if any(word in product_name for word in ['stripe', 'striped', 'stripes']):
        return 'striped'
    
    if any(word in product_name for word in ['floral', 'flower', 'botanical']):
        return 'floral'
    
    if any(word in product_name for word in ['geometric', 'paisley', 'motif']):
        return 'geometric'
    
    return 'solid'  # Default

def extract_occasion_from_name(product_name):
    """Extract occasion from product name"""
    product_name = product_name.lower()
    
    if any(word in product_name for word in ['wedding', 'bridal', 'bride']):
        return 'wedding'
    
    if any(word in product_name for word in ['festive', 'festival', 'party', 'evening wear']):
        return 'festive'
    
    if any(word in product_name for word in ['formal', 'office', 'work']):
        return 'formal'
    
    # Default to casual if no specific occasion mentioned
    return 'casual'

def fix_csv_attributes(csv_file_path, start_row, end_row):
    """Fix attributes for specified rows"""
    
    df = pd.read_csv(csv_file_path)
    print(f"Total rows: {len(df)}")
    print(f"Fixing rows {start_row} to {end_row}")
    
    fixed_count = 0
    
    for idx in range(start_row - 1, min(end_row, len(df))):
        product_name = str(df.iloc[idx]['product_name'])
        
        # Extract attributes
        color = extract_color_intelligently(product_name)
        pattern = extract_pattern_from_name(product_name)
        occasion = extract_occasion_from_name(product_name)
        
        # Create new attributes
        new_attributes = {
            "color_primary": color,
            "pattern": pattern,
            "occasion_suitability": occasion,
            "gender": "female",
            "fit": "regular",
            "season": "all"
        }
        
        # Update the row
        df.iloc[idx, df.columns.get_loc('attributes_json')] = json.dumps(new_attributes)
        fixed_count += 1
        
        if idx % 100 == 0:
            print(f"Row {idx + 1}: {color} | {pattern} | {occasion}")
            print(f"  Product: {product_name[:50]}...")
    
    # Save the updated file
    df.to_csv(csv_file_path, index=False)
    print(f"\nFixed {fixed_count} rows successfully!")
    
    # Show some examples
    print("\nExamples of fixed rows:")
    for i in range(start_row - 1, min(start_row + 5, len(df))):
        attrs = json.loads(df.iloc[i]['attributes_json'])
        print(f"Row {i+1}: Color={attrs['color_primary']}, Pattern={attrs['pattern']}, Occasion={attrs['occasion_suitability']}")
        print(f"  Product: {df.iloc[i]['product_name']}")
        print()

if __name__ == "__main__":
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated_cleaned.csv"
    
    # Fix rows 3997 to 4423
    fix_csv_attributes(csv_file, 3997, 4423)