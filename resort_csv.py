import csv
import re
from collections import defaultdict

with open('annotations/labels_sorted.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

def extract_number(filepath):
    match = re.search(r'_(\d+)\.jpg$', filepath)
    return int(match.group(1)) if match else 0

ethnic_rows = defaultdict(list)
western_rows = defaultdict(list)

for row in rows:
    if len(row) < 3:
        continue
    file_path = row[0]
    category = row[1]
    sub_category = row[2]
    
    if sub_category == 'ethnic':
        ethnic_rows[category].append(row)
    else:
        western_rows[category].append(row)

for category in ethnic_rows:
    ethnic_rows[category].sort(key=lambda x: extract_number(x[0]))

for category in western_rows:
    western_rows[category].sort(key=lambda x: extract_number(x[0]))

sorted_rows = []
for category in sorted(ethnic_rows.keys()):
    sorted_rows.extend(ethnic_rows[category])

for category in sorted(western_rows.keys()):
    sorted_rows.extend(western_rows[category])

with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(sorted_rows)

print(f"Re-sorted CSV with {len(sorted_rows)} rows")
shirt_rows = [r for r in sorted_rows if 'western/shirt' in r[0]]
print(f"\nShirt rows: {len(shirt_rows)}")
print("First 5 shirt rows:")
for r in shirt_rows[:5]:
    print(f"  {r[0]}")
