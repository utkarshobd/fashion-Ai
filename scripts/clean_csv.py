import csv

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = [row for row in reader]

# Remove trailing empty fields
cleaned_rows = []
for row in rows:
    while row and row[-1] == '':
        row.pop()
    cleaned_rows.append(row)

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(cleaned_rows)

print(f"Cleaned {len(cleaned_rows)} rows - removed trailing commas")
