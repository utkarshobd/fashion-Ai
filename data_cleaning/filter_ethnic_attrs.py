import csv
import json

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

keep_attrs = ['color_primary', 'pattern', 'occasion_suitability', 'gender', 'fit', 'season']
fixed_rows = []
count = 0

for row in rows:
    if len(row) > 3 and row[0].startswith('ethnic/'):
        try:
            attrs = json.loads(row[3])
            filtered = {k: attrs[k] for k in keep_attrs if k in attrs}
            row[3] = json.dumps(filtered)
            count += 1
        except:
            pass
    fixed_rows.append(row)

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fixed_rows)

print(f"Filtered attributes for {count} ethnic rows")
