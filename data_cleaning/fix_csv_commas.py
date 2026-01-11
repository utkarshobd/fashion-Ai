import re

def fix_csv_commas(input_file, output_file):
    """
    Remove multiple trailing commas from CSV lines and replace with \r
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        # Remove trailing whitespace and newlines
        line = line.rstrip()
        
        # Remove multiple trailing commas using regex
        # This pattern matches 2 or more commas at the end of the line
        fixed_line = re.sub(r',{2,}$', r'\\r', line)
        
        # Add back the newline
        fixed_lines.append(fixed_line + '\n')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed {len(fixed_lines)} lines")
    print("Replaced multiple trailing commas with \\r")

if __name__ == "__main__":
    input_file = "annotations/labels_reorganized_updated.csv"
    output_file = "annotations/labels_reorganized_updated.csv"
    
    fix_csv_commas(input_file, output_file)