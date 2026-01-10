import pandas as pd
import csv

# First, let's examine the CSV structure
print("Examining CSV structure...")

# Try to read with different parameters to handle parsing issues
try:
    # Read with error handling
    df = pd.read_csv('annotations/labels.csv', on_bad_lines='skip', engine='python')
    print(f"Successfully read {len(df)} rows")
except Exception as e:
    print(f"Error reading CSV: {e}")
    
    # Try alternative approach - read line by line
    print("Trying line-by-line reading...")
    
    lines = []
    with open('annotations/labels.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"Header: {header}")
        print(f"Number of columns in header: {len(header)}")
        
        for i, row in enumerate(reader):
            if len(row) == len(header):
                lines.append(row)
            else:
                print(f"Skipping line {i+2}: expected {len(header)} fields, got {len(row)}")
                if i < 10:  # Show first few problematic lines
                    print(f"  Content: {row}")
    
    # Create DataFrame from valid lines
    df = pd.DataFrame(lines, columns=header)
    print(f"Created DataFrame with {len(df)} valid rows")

print(f"Columns: {df.columns.tolist()}")
print(f"Sample data:")
print(df.head())

# Check unique values in category column
if 'category' in df.columns:
    print(f"Categories in 'category' column: {df['category'].unique()}")
elif 'sub_category' in df.columns:
    print(f"Categories in 'sub_category' column: {df['sub_category'].unique()}")

# Check file_path patterns
if 'file_path' in df.columns:
    print(f"Sample file paths:")
    print(df['file_path'].head(10).tolist())