import pandas as pd
import json

def extract_color_from_attributes(attributes_json):
    """Extract color_primary from attributes_json string"""
    try:
        if isinstance(attributes_json, str):
            cleaned_json = attributes_json.replace('""', '"')
            data = json.loads(cleaned_json)
            return data.get('color_primary', None)
    except:
        return None
    return None

def check_unknown_colors():
    """Check for unknown colors in labels.csv"""
    
    # Read labels.csv
    labels_df = pd.read_csv('annotations/labels.csv')
    
    # Extract color_primary from attributes_json
    labels_df['extracted_color'] = labels_df['attributes_json'].apply(extract_color_from_attributes)
    
    # Find entries with unknown color
    unknown_entries = labels_df[labels_df['extracted_color'] == 'unknown']
    
    print(f"Total entries in labels.csv: {len(labels_df)}")
    print(f"Entries with 'unknown' color_primary: {len(unknown_entries)}")
    
    if len(unknown_entries) > 0:
        print("\nFiles with unknown color_primary:")
        for idx, row in unknown_entries.iterrows():
            print(f"  {row['file_path']}")
    else:
        print("No unknown colors found in labels.csv")
    
    # Show color distribution
    color_counts = labels_df['extracted_color'].value_counts()
    print(f"\nColor distribution in labels.csv:")
    for color, count in color_counts.head(15).items():
        print(f"  {color}: {count}")

if __name__ == "__main__":
    check_unknown_colors()