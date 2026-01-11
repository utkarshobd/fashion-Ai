import re

# Read the CSV file
with open('annotations/labels_reorganized_updated.csv', 'r', encoding='utf-8') as file:
    content = file.read()

# Replace multiple commas at the end of blouse_choli lines with \r
# Pattern: blouse_choli lines ending with multiple commas
pattern = r'(,blouse_choli,ethnic,.*?),{2,}\r'
replacement = r'\1\r'

# Apply the replacement
updated_content = re.sub(pattern, replacement, content)

# Write back to the file
with open('annotations/labels_reorganized_updated.csv', 'w', encoding='utf-8') as file:
    file.write(updated_content)

print("Fixed blouse_choli entries - replaced multiple commas with \\r")