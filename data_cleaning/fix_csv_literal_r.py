import re

# Read the CSV file
with open('annotations/labels_reorganized_updated.csv', 'r', encoding='utf-8') as file:
    content = file.read()

# Replace multiple trailing commas with literal \r
content = re.sub(r',{2,}(\r?\n)', r'\\r\1', content)

# Write back to file
with open('annotations/labels_reorganized_updated.csv', 'w', encoding='utf-8') as file:
    file.write(content)

print("Fixed multiple trailing commas with literal \\r")