import pandas as pd

def reorganize_labels_csv():
    # Read the CSV file with error handling
    try:
        df = pd.read_csv('annotations/labels.csv', quoting=1, on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        # Try with different parameters
        df = pd.read_csv('annotations/labels.csv', sep=',', quotechar='"', on_bad_lines='skip', engine='python')
    
    print(f"Original dataset has {len(df)} rows")
    
    # Separate ethnic and western items
    ethnic_df = df[df['sub_category'] == 'ethnic'].copy()
    western_df = df[df['sub_category'] == 'western'].copy()
    
    print(f"Ethnic items: {len(ethnic_df)}")
    print(f"Western items: {len(western_df)}")
    
    # Sort ethnic items by category (subcategory within ethnic)
    ethnic_df_sorted = ethnic_df.sort_values(['category'], kind='stable')
    
    # Sort western items by category (subcategory within western)  
    western_df_sorted = western_df.sort_values(['category'], kind='stable')
    
    # Combine: ethnic first, then western
    reorganized_df = pd.concat([ethnic_df_sorted, western_df_sorted], ignore_index=True)
    
    print(f"Reorganized dataset has {len(reorganized_df)} rows")
    
    # Verify no data loss
    assert len(reorganized_df) == len(df), "Data loss detected!"
    
    # Save the reorganized CSV
    reorganized_df.to_csv('annotations/labels_reorganized.csv', index=False)
    
    print("✓ Successfully reorganized labels.csv")
    print("✓ Ethnic items grouped by category (blouse_choli, kurta, lehenga, saree, sherwani, suit_salwar)")
    print("✓ Western items grouped by category (dress, jacket, jeans, shirt, shorts, t_shirt, trouser_chinos)")
    print("✓ Saved as labels_reorganized.csv")
    
    # Show category distribution
    print("\nCategory distribution in reorganized file:")
    category_counts = reorganized_df['category'].value_counts()
    for category, count in category_counts.items():
        print(f"  {category}: {count} items")

if __name__ == "__main__":
    reorganize_labels_csv()