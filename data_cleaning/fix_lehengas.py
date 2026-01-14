import csv

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

fixed_rows = []
count = 0
for row in rows:
    if len(row) > 1 and 'ethnic/lehengas' in row[0] and row[1] == 'lehenga':
        row[1] = 'lehengas'
        count += 1
    fixed_rows.append(row)

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fixed_rows)

print(f"Fixed {count} rows: changed category from 'lehenga' to 'lehengas'")
