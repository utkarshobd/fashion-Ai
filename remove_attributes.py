import csv
import json
import re

def remove_attributes_from_blouse_choli(input_file, output_file):
    """
    Remove fabric_hint, sleeve_length, and length_category attributes from blouse_choli entries
    """
    attributes_to_remove = ['fabric_hint', 'sleeve_length', 'length_category']
    
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
                    # Parse the JSON attributes
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
                    
                except (json.JSONDecodeError, IndexError) as e:
                    print(f"Error processing row: {row[:2] if len(row) >= 2 else row}")
                    print(f"Error: {e}")
                    # Keep the original row if there's an error
            
            writer.writerow(row)

if __name__ == "__main__":
    input_file = "c:\\Users\\utkarshh\\Desktop\\FAI\\FAII\\fashion_dataset_transformed\\annotations\\labels.csv"
    output_file = "c:\\Users\\utkarshh\\Desktop\\FAI\\FAII\\fashion_dataset_transformed\\annotations\\labels_updated.csv"
    
    remove_attributes_from_blouse_choli(input_file, output_file)
    print("Attributes removed successfully!")
    print(f"Updated file saved as: {output_file}")