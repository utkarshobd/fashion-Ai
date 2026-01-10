#!/usr/bin/env python3
"""
Clean up the labels.csv file by fixing JSON formatting issues
"""

import pandas as pd
import json
import re

def clean_json_field(json_str):
    """Clean up malformed JSON strings"""
    if pd.isna(json_str) or json_str == '':
        return '{}'
    
    # Fix double quotes in JSON
    json_str = str(json_str)
    json_str = json_str.replace('""', '"')
    
    try:
        # Try to parse as JSON to validate
        parsed = json.loads(json_str)
        return json.dumps(parsed)
    except:
        # If parsing fails, return empty JSON
        return '{}'

def main():
    # Read the CSV file
    print("Reading labels.csv...")
    df = pd.read_csv('annotations/labels.csv')
    
    print(f"Original shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Clean the attributes_json column
    if 'attributes_json' in df.columns:
        print("Cleaning attributes_json column...")
        df['attributes_json'] = df['attributes_json'].apply(clean_json_field)
    
    # Remove any completely empty rows
    df = df.dropna(how='all')
    
    # Save the cleaned file
    output_file = 'annotations/labels_cleaned.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Cleaned data saved to {output_file}")
    print(f"Final shape: {df.shape}")
    
    # Show sample of cleaned data
    print("\nSample of cleaned data:")
    print(df.head(3).to_string())

if __name__ == "__main__":
    main()