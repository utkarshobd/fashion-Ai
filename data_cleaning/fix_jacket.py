import csv

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

fixed_rows = []
for row in rows:
    if len(row) > 2 and 'western/jacket' in row[0]:
        # Keep only first 9 fields (up to product_name) + sub_class field
        row = row[:9] + [row[-1]] if len(row) > 9 else row[:9]
    fixed_rows.append(row)

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fixed_rows)

print(f"Fixed {len([r for r in fixed_rows if len(r)>2 and 'western/jacket' in r[0]])} jacket rows")
