#!/usr/bin/env python3
"""
Process and clean kurta dataset CSV file
"""

import pandas as pd
import json
import re
import os

def clean_kurta_csv(input_file, output_file):
    """Clean and process the kurta dataset CSV file"""
    
    print(f"Processing {input_file}...")
    
    # Read the raw file content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove literal \r characters and fix formatting
    content = content.replace('\\r', '')
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')
    
    # Split into lines and process
    lines = content.split('\n')
    cleaned_lines = []
    
    # Expected header
    header = "file_path,category,sub_category,attributes_json,gender,source,original_id,product_name"
    cleaned_lines.append(header)
    
    for line in lines[1:]:  # Skip first line if it's header
        if not line.strip():
            continue
            
        # Remove trailing commas
        line = line.rstrip(',')
        
        # Skip malformed lines
        if line.count(',') < 7:
            continue
            
        # Parse the line
        parts = line.split(',')
        if len(parts) >= 8:
            file_path = parts[0].strip()
            category = parts[1].strip()
            sub_category = parts[2].strip()
            attributes_json = parts[3].strip()
            gender = parts[4].strip()
            source = parts[5].strip()
            original_id = parts[6].strip()
            product_name = ','.join(parts[7:]).strip()  # Join remaining parts for product name
            
            # Clean product name
            product_name = re.sub(r'\\r.*$', '', product_name)
            product_name = product_name.strip()
            
            # Validate attributes JSON
            try:
                if attributes_json.startswith('"') and attributes_json.endswith('"'):
                    json_str = attributes_json[1:-1].replace('""', '"')
                    json.loads(json_str)
                    attributes_json = f'"{json_str}"'
            except:
                # Default attributes for kurta
                attributes_json = '{"color_primary": "unknown", "pattern": "solid", "occasion_suitability": "ethnic", "gender": "male", "fit": "regular", "season": "all"}'
            
            # Create cleaned line
            cleaned_line = f"{file_path},{category},{sub_category},{attributes_json},{gender},{source},{original_id},{product_name}"
            cleaned_lines.append(cleaned_line)
    
    # Write cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
    print(f"Cleaned dataset saved to {output_file}")
    print(f"Total records processed: {len(cleaned_lines) - 1}")

def validate_dataset(file_path):
    """Validate the cleaned dataset"""
    try:
        df = pd.read_csv(file_path)
        print(f"\nDataset validation:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nSample records:")
        print(df.head())
        
        # Check for missing values
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        # Check categories
        print(f"\nCategories:")
        print(df['category'].value_counts())
        
        print(f"\nGender distribution:")
        print(df['gender'].value_counts())
        
        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False

if __name__ == "__main__":
    # File paths
    input_file = r"C:\Users\utkarshh\Documents\Downloads\labels_reorganized_kurta_cleaned.csv"
    output_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\kurta_dataset_cleaned.csv"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process the file
    clean_kurta_csv(input_file, output_file)
    
    # Validate the result
    validate_dataset(output_file)