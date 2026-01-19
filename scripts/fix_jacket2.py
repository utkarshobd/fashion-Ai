import csv

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

fixed_rows = []
for row in rows:
    if len(row) > 2 and 'western/jacket' in row[0]:
        row = row[:8] + row[9:]
    fixed_rows.append(row)

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fixed_rows)

print(f"Fixed jacket rows - removed extra comma")
