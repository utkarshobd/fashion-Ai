import csv
import re
from collections import defaultdict

# Read CSV
with open('annotations/labels_new.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

print(f"Total rows read: {len(rows)}")

# Extract numeric part from filename for sorting
def extract_number(filepath):
    match = re.search(r'_(\d+)\.jpg$', filepath)
    return int(match.group(1)) if match else 0

# Separate ethnic and western, group by category
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

# Sort each category by filename number
for category in ethnic_rows:
    ethnic_rows[category].sort(key=lambda x: extract_number(x[0]))

for category in western_rows:
    western_rows[category].sort(key=lambda x: extract_number(x[0]))

# Combine: ethnic first (sorted by category name), then western (sorted by category name)
sorted_rows = []

for category in sorted(ethnic_rows.keys()):
    sorted_rows.extend(ethnic_rows[category])

for category in sorted(western_rows.keys()):
    sorted_rows.extend(western_rows[category])

# Write to new CSV
with open('annotations/labels_sorted.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(sorted_rows)

print(f"\nReorganized CSV saved to labels_sorted.csv with {len(sorted_rows)} rows")
print(f"\nFirst 15 rows (file_path | category | sub_category):")
for i, row in enumerate(sorted_rows[:15]):
    print(f"{row[0]:<50} | {row[1]:<20} | {row[2]}")

print(f"\nLast 15 rows (file_path | category | sub_category):")
for i, row in enumerate(sorted_rows[-15:]):
    print(f"{row[0]:<50} | {row[1]:<20} | {row[2]}")
