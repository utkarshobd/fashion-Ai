import csv

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

fixed_rows = []
count = 0

for row in rows:
    if len(row) > 9 and 'western/shirt' in row[0] and row[2] == '' and row[9] == 'western':
        # Misaligned: need to rearrange
        # Current: [file, category, '', '', gender, source, '', '', '', 'western', attrs_json, id, name, ...]
        # Target:  [file, category, 'western', attrs_json, gender, source, id, name, sub_class]
        fixed_row = [
            row[0],  # file_path
            row[1],  # category
            row[9],  # sub_category (was at position 9)
            row[10] if len(row) > 10 else '',  # attributes_json (was at position 10)
            row[4],  # gender
            row[5],  # source
            row[11] if len(row) > 11 else '',  # original_id (was at position 11)
            row[12] if len(row) > 12 else '',  # product_name (was at position 12)
            ''  # sub_class
        ]
        fixed_rows.append(fixed_row)
        count += 1
    else:
        fixed_rows.append(row)

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fixed_rows)

print(f"Fixed {count} misaligned shirt rows")
