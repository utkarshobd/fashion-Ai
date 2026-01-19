import pandas as pd
import csv

def reorganize_labels_csv():
    # Read the CSV file more carefully
    print("Reading CSV file...")
    
    # First, let's read it line by line to handle any parsing issues
    rows = []
    with open('annotations/labels.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        print(f"Header: {header}")
        
        for i, row in enumerate(csv_reader):
            if len(row) >= len(header):  # Only keep rows with enough columns
                rows.append(row[:len(header)])  # Trim to header length
            else:
                print(f"Skipping malformed row {i+2}: {len(row)} columns instead of {len(header)}")
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=header)
    print(f"Successfully loaded {len(df)} rows")
    
    # Clean up any extra whitespace
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Separate ethnic and western items
    ethnic_df = df[df['sub_category'] == 'ethnic'].copy()
    western_df = df[df['sub_category'] == 'western'].copy()
    
    print(f"Ethnic items: {len(ethnic_df)}")
    print(f"Western items: {len(western_df)}")
    print(f"Other items: {len(df) - len(ethnic_df) - len(western_df)}")
    
    # Sort ethnic items by category
    ethnic_df_sorted = ethnic_df.sort_values(['category'], kind='stable')
    
    # Sort western items by category  
    western_df_sorted = western_df.sort_values(['category'], kind='stable')
    
    # Get any other items (if any)
    other_df = df[(df['sub_category'] != 'ethnic') & (df['sub_category'] != 'western')].copy()
    
    # Combine: ethnic first, then western, then others
    if len(other_df) > 0:
        reorganized_df = pd.concat([ethnic_df_sorted, western_df_sorted, other_df], ignore_index=True)
    else:
        reorganized_df = pd.concat([ethnic_df_sorted, western_df_sorted], ignore_index=True)
    
    print(f"Reorganized dataset has {len(reorganized_df)} rows")
    
    # Save the reorganized CSV
    reorganized_df.to_csv('annotations/labels_reorganized.csv', index=False)
    
    # Replace the original file
    reorganized_df.to_csv('annotations/labels.csv', index=False)
    
    print("Successfully reorganized labels.csv")
    print("Ethnic items grouped by category first")
    print("Western items grouped by category second")
    print("Original file updated and backup saved as labels_reorganized.csv")
    
    # Show category distribution
    print("\nCategory distribution in reorganized file:")
    category_counts = reorganized_df['category'].value_counts()
    for category, count in category_counts.items():
        print(f"  {category}: {count} items")
    
    # Show ethnic categories first
    print("\nEthnic categories:")
    ethnic_categories = ethnic_df_sorted['category'].value_counts()
    for category, count in ethnic_categories.items():
        print(f"  {category}: {count} items")
    
    print("\nWestern categories:")
    western_categories = western_df_sorted['category'].value_counts()
    for category, count in western_categories.items():
        print(f"  {category}: {count} items")

if __name__ == "__main__":
    reorganize_labels_csv()