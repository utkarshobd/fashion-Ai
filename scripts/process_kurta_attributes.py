import csv
import json
import re

def process_csv():
    input_file = r'c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated.csv'
    output_file = r'c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated_processed.csv'
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Process each row
        for row in reader:
            if len(row) >= 3:  # Ensure we have enough columns
                # Check if this is a kurta entry
                if len(row) > 1 and 'kurta' in row[1]:
                    # Process the attributes_json column (index 2)
                    if len(row) > 2:
                        attributes_json = row[2]
                        try:
                            # Parse the JSON string
                            # Handle the double-quoted JSON format
                            cleaned_json = attributes_json.replace('""', '"')
                            attributes = json.loads(cleaned_json)
                            
                            # Remove fabric_hint and sleeve_length if they exist
                            if 'fabric_hint' in attributes:
                                del attributes['fabric_hint']
                            if 'sleeve_length' in attributes:
                                del attributes['sleeve_length']
                            
                            # Convert back to the original format
                            updated_json = json.dumps(attributes)
                            updated_json = updated_json.replace('"', '""')
                            row[2] = updated_json
                            
                        except (json.JSONDecodeError, Exception) as e:
                            print(f"Error processing row: {e}")
                            print(f"Problematic JSON: {attributes_json}")
                            # Keep the original row if there's an error
            
            writer.writerow(row)
    
    print("Processing completed. Output saved to:", output_file)

if __name__ == "__main__":
    process_csv()