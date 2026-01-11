import re

# Read the CSV file
with open('annotations/labels_reorganized_updated.csv', 'r', encoding='utf-8') as file:
    content = file.read()

# Replace multiple commas at the end of lines with \r
# This pattern matches 2 or more commas followed by \r or end of line
content = re.sub(r',{2,}(\r|\n|$)', r'\r\n', content)

# Write back to the file
with open('annotations/labels_reorganized_updated.csv', 'w', encoding='utf-8') as file:
    file.write(content)

print("Fixed multiple trailing commas in CSV file")