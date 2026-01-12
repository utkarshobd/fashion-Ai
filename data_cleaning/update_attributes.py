import pandas as pd
import json
import re

def advanced_color_extraction(product_name):
    """Advanced color extraction with better pattern matching"""
    product_name = product_name.lower()
    
    # Enhanced color mapping with more variants
    color_patterns = {
        'red': r'\b(red|maroon|crimson|burgundy|wine|cherry|rust|brick|deep red|bright red|dark red|light red|rani|ferrari)\b',
        'blue': r'\b(blue|navy|teal|turquoise|cobalt|sapphire|azure|indigo|royal blue|powder blue|sky blue|dusty blue|aqua|cerulean|midnight blue)\b',
        'green': r'\b(green|olive|emerald|mint|lime|forest|sage|bottle green|sea green|pista|mehendi|moss|jade|verdant|pine|parrot green)\b',
        'yellow': r'\b(yellow|gold|golden|mustard|ochre|amber|cream|beige|champagne|marigold|saffron|lemon|canary)\b',
        'pink': r'\b(pink|rose|blush|coral|salmon|peach|magenta|fuchsia|hot pink|rani pink|flamingo|dusty pink|soft pink|light pink)\b',
        'purple': r'\b(purple|violet|lavender|lilac|plum|mauve|amethyst|grape|eggplant|orchid|indigo)\b',
        'orange': r'\b(orange|tangerine|saffron|burnt orange|mango|coral|apricot|papaya)\b',
        'black': r'\b(black|charcoal|ebony|jet|midnight|onyx|coal)\b',
        'white': r'\b(white|ivory|cream|off white|pearl|snow|alabaster|chalk|vanilla)\b',
        'grey': r'\b(grey|gray|silver|ash|slate|steel|charcoal|pewter)\b',
        'brown': r'\b(brown|tan|chocolate|coffee|caramel|bronze|mahogany|chestnut|cocoa)\b',
        'multicolor': r'\b(multicolor|multi|rainbow|mixed|combination|multi.?color)\b'
    }
    
    # Check for color matches using regex
    for color, pattern in color_patterns.items():
        if re.search(pattern, product_name):
            return color
    
    return 'unknown'

def advanced_pattern_extraction(product_name):
    """Advanced pattern extraction with priority-based matching"""
    product_name = product_name.lower()
    
    # Priority-based pattern matching
    pattern_checks = [
        ('embroidered', r'\b(embroidered|embroidery|zardozi|sequin|sequins|beads|thread work|hand embroidered|resham|mirror work|cut dana|stone work|crystal|pearl work)\b'),
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

def advanced_occasion_extraction(product_name):
    """Advanced occasion extraction with context awareness"""
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
    
    # Context-based logic
    if any(word in product_name for word in ['saree', 'lehenga', 'blouse', 'choli']):
        # Check if it's a simple/basic item
        if any(word in product_name for word in ['simple', 'basic', 'plain', 'cotton']):
            return 'casual'
        else:
            return 'festive'  # Ethnic wear is typically festive
    
    return 'casual'  # Default

def update_original_csv(csv_file_path, start_row, end_row):
    """Update the original CSV file with fixed attributes"""
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    print(f"Total rows in CSV: {len(df)}")
    print(f"Updating rows {start_row} to {end_row}")
    
    updated_count = 0
    
    # Process the specified rows
    for idx in range(start_row - 1, min(end_row, len(df))):  # Convert to 0-based indexing
        product_name = str(df.iloc[idx]['product_name'])
        
        # Extract attributes intelligently
        color = advanced_color_extraction(product_name)
        pattern = advanced_pattern_extraction(product_name)
        occasion = advanced_occasion_extraction(product_name)
        
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
            print(f"Updated row {idx + 1}: Color={color}, Pattern={pattern}, Occasion={occasion}")
            print(f"  Product: {product_name[:60]}...")
    
    # Save back to the original file
    df.to_csv(csv_file_path, index=False)
    print(f"\nSuccessfully updated {updated_count} rows in the original file!")
    print(f"File updated: {csv_file_path}")
    
    return updated_count

# Main execution
if __name__ == "__main__":
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated_cleaned.csv"
    
    # Update rows 3997 to 4423 in the original file
    updated_count = update_original_csv(csv_file, 3997, 4423)
    
    print(f"\nAttribute fixing completed! Updated {updated_count} rows.")
    
    # Show some examples of the updates
    df = pd.read_csv(csv_file)
    print("\nSample of updated rows:")
    for i in range(3996, min(4006, len(df))):  # Show first 10 updated rows
        attrs = json.loads(df.iloc[i]['attributes_json'])
        print(f"Row {i+1}: {attrs['color_primary']} | {attrs['pattern']} | {attrs['occasion_suitability']}")
        print(f"  Product: {df.iloc[i]['product_name'][:50]}...")
        print()