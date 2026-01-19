import re

with open('annotations/labels.csv', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace actual \r characters with literal \r text
content = content.replace('\r', '\\r')

with open('annotations/labels.csv', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced actual \\r with literal \\r text")