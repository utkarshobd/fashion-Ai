import csv
import json
import re

def remove_attributes_from_blouse_choli(input_file, output_file):
    """
    Remove fabric_hint, sleeve_length, and length_category attributes from blouse_choli entries
    """
    attributes_to_remove = ['fabric_hint', 'sleeve_length', 'length_category']
    processed_count = 0
    error_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            if len(row) >= 3 and row[1] == 'blouse_choli':  # Check if it's a blouse_choli entry
                try:
                    # Check if attributes_json exists and is not empty
                    if len(row) > 2 and row[2].strip():
                        attributes_json = row[2]
                        # Handle double-escaped quotes
                        attributes_json = attributes_json.replace('""', '"')
                        attributes_dict = json.loads(attributes_json)
                        
                        # Remove the specified attributes
                        for attr in attributes_to_remove:
                            if attr in attributes_dict:
                                del attributes_dict[attr]
                        
                        # Convert back to JSON string with double-escaped quotes
                        updated_json = json.dumps(attributes_dict, separators=(',', ': '))
                        updated_json = updated_json.replace('"', '""')
                        
                        # Update the row
                        row[2] = updated_json
                        processed_count += 1
                    else:
                        # Skip rows with empty or missing attributes_json
                        error_count += 1
                        print(f"Skipping row with missing attributes_json: {row[0] if len(row) > 0 else 'Unknown'}")
                        
                except (json.JSONDecodeError, IndexError) as e:
                    error_count += 1
                    print(f"Error processing row: {row[0] if len(row) > 0 else 'Unknown'}")
                    # Keep the original row if there's an error
            
            writer.writerow(row)
    
    print(f"\nProcessed {processed_count} blouse_choli entries successfully")
    print(f"Encountered {error_count} entries with errors or missing data")

if __name__ == "__main__":
    input_file = "c:\\Users\\utkarshh\\Desktop\\FAI\\FAII\\fashion_dataset_transformed\\annotations\\labels.csv"
    output_file = "c:\\Users\\utkarshh\\Desktop\\FAI\\FAII\\fashion_dataset_transformed\\annotations\\labels_updated.csv"
    
    remove_attributes_from_blouse_choli(input_file, output_file)
    print("Attributes removed successfully!")
    print(f"Updated file saved as: {output_file}")