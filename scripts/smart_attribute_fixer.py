import pandas as pd
import json
import re

def smart_color_extraction(product_name):
    """Smart color extraction that prioritizes multicolor detection"""
    product_name = product_name.lower()
    
    # First check for explicit multicolor keywords
    multicolor_patterns = r'\b(multicolor|multi.?color|multi|rainbow|mixed|combination)\b'
    if re.search(multicolor_patterns, product_name):
        return 'multicolor'
    
    # Define color patterns
    color_patterns = {
        'red': r'\b(red|maroon|crimson|burgundy|wine|cherry|rust|brick|deep red|bright red|dark red|light red|rani|ferrari)\b',
        'blue': r'\b(blue|navy|teal|turquoise|cobalt|sapphire|azure|indigo|royal blue|powder blue|sky blue|dusty blue|aqua|cerulean|midnight blue)\b',
        'green': r'\b(green|olive|emerald|mint|lime|forest|sage|bottle green|sea green|pista|mehendi|moss|jade|verdant|pine|parrot green)\b',
        'yellow': r'\b(yellow|gold|golden|mustard|ochre|amber|cream|beige|champagne|marigold|saffron|lemon|canary)\b',
        'pink': r'\b(pink|rose|blush|coral|salmon|peach|magenta|fuchsia|hot pink|rani pink|flamingo|dusty pink|soft pink|light pink)\b',
        'purple': r'\b(purple|violet|lavender|lilac|plum|mauve|amethyst|grape|eggplant|orchid)\b',
        'orange': r'\b(orange|tangerine|saffron|burnt orange|mango|apricot|papaya)\b',
        'black': r'\b(black|charcoal|ebony|jet|midnight|onyx|coal)\b',
        'white': r'\b(white|ivory|off white|pearl|snow|alabaster|chalk|vanilla)\b',
        'grey': r'\b(grey|gray|silver|ash|slate|steel|pewter)\b',
        'brown': r'\b(brown|tan|chocolate|coffee|caramel|bronze|mahogany|chestnut|cocoa)\b'
    }
    
    # Find all colors mentioned in the product name
    found_colors = []
    for color, pattern in color_patterns.items():
        if re.search(pattern, product_name):
            found_colors.append(color)
    
    # If more than one color is found, it's multicolor
    if len(found_colors) > 1:
        return 'multicolor'
    elif len(found_colors) == 1:
        return found_colors[0]
    
    # Special handling for cream (can be white or yellow)
    if re.search(r'\bcream\b', product_name):
        return 'white'  # Default cream to white
    
    return 'unknown'

def advanced_pattern_extraction(product_name):
    """Advanced pattern extraction with priority-based matching"""
    product_name = product_name.lower()
    
    # Priority-based pattern matching
    pattern_checks = [
        ('embroidered', r'\b(embroidered|embroidery|zardozi|sequin|sequins|beads|thread work|hand embroidered|resham|mirror work|cut dana|stone work|crystal|pearl work|zari)\b'),
        ('printed', r'\b(print|printed|floral print|geometric print|paisley print|digital print|block print)\b'),
        ('striped', r'\b(stripe|striped|stripes|linear)\b'),
        ('floral', r'\b(floral|flower|botanical|rose|lotus|jasmine)\b'),
        ('geometric', r'\b(geometric|paisley|mandarin|motif|pattern|tribal|ethnic motif)\b'),
        ('checked', r'\b(check|checked|checkered|plaid)\b'),
        ('polka', r'\b(polka|dot|dotted|spotted)\b'),
        ('solid', r'\b(solid|plain|simple)\b')
    ]
    
    # Check patterns in priority order
    for pattern_name, pattern_regex in pattern_checks:
        if re.search(pattern_regex, product_name):
            return pattern_name
    
    return 'solid'  # Default

def smart_occasion_extraction(product_name):
    """Smart occasion extraction with context awareness"""
    product_name = product_name.lower()
    
    occasion_patterns = {
        'wedding': r'\b(wedding|bridal|bride|marriage|shaadi|vivah)\b',
        'festive': r'\b(festive|festival|celebration|party|evening wear|diwali|holi|eid|christmas|new year)\b',
        'formal': r'\b(formal|office|work|business|corporate|professional)\b',
        'casual': r'\b(casual|daily|everyday|regular|comfort|home)\b'
    }
    
    # Check for specific occasions
    for occasion, pattern in occasion_patterns.items():
        if re.search(pattern, product_name):
            return occasion
    
    # If no specific occasion mentioned, default to casual
    return 'casual'

def update_csv_with_smart_extraction(csv_file_path, start_row, end_row):
    """Update CSV with smart attribute extraction"""
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    print(f"Total rows in CSV: {len(df)}")
    print(f"Updating rows {start_row} to {end_row} with smart extraction")
    
    updated_count = 0
    
    # Process the specified rows
    for idx in range(start_row - 1, min(end_row, len(df))):  # Convert to 0-based indexing
        product_name = str(df.iloc[idx]['product_name'])
        
        # Extract attributes using smart logic
        color = smart_color_extraction(product_name)
        pattern = advanced_pattern_extraction(product_name)
        occasion = smart_occasion_extraction(product_name)
        
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
        updated_count += 1
        
        if idx % 50 == 0:  # Progress indicator
            print(f"Row {idx + 1}: Color={color}, Pattern={pattern}, Occasion={occasion}")
            print(f"  Product: {product_name[:70]}...")
    
    # Save back to the original file
    df.to_csv(csv_file_path, index=False)
    print(f"\nSuccessfully updated {updated_count} rows!")
    
    return updated_count

def verify_color_extraction():
    """Test the color extraction logic with sample names"""
    test_names = [
        "FNF Red & Orange Evening Wear Sari",
        "FNF Multi Coloured Printed Sari", 
        "Women Red Blouse Choli",
        "FNF Pink & Yellow Printed Evening Wear Sari",
        "Prafful Red & Green Printed Sari",
        "FNF Blue Printed Sari",
        "Women Multicolor Resham Embroidery Blouse"
    ]
    
    print("Testing color extraction logic:")
    print("=" * 50)
    for name in test_names:
        color = smart_color_extraction(name)
        print(f"'{name}' -> Color: {color}")
    print("=" * 50)

# Main execution
if __name__ == "__main__":
    # First verify the logic
    verify_color_extraction()
    
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated_cleaned.csv"
    
    # Update rows 3997 to 4423 in the original file
    updated_count = update_csv_with_smart_extraction(csv_file, 3997, 4423)
    
    print(f"\nAttribute fixing completed! Updated {updated_count} rows.")
    
    # Show some examples of the updates
    print("\nVerifying updates in CSV:")
    df = pd.read_csv(csv_file)
    for i in range(3996, min(4006, len(df))):  # Show first 10 updated rows
        attrs = json.loads(df.iloc[i]['attributes_json'])
        product_name = df.iloc[i]['product_name']
        print(f"Row {i+1}: {attrs['color_primary']} | {attrs['pattern']} | {attrs['occasion_suitability']}")
        print(f"  Product: {product_name}")
        print()