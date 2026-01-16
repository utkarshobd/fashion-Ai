import csv
import json

csv_file = "labels_sorted3.csv"

rows = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 3 and row[3]:
            try:
                attrs = json.loads(row[3])
                # Reorder: color_primary, gender, pattern, occasion_suitability, fit, year
                new_attrs = {}
                if 'color_primary' in attrs:
                    new_attrs['color_primary'] = attrs['color_primary']
                if 'gender' in attrs:
                    new_attrs['gender'] = attrs['gender']
                if 'pattern' in attrs:
                    new_attrs['pattern'] = attrs['pattern']
                if 'occasion_suitability' in attrs:
                    new_attrs['occasion_suitability'] = attrs['occasion_suitability']
                if 'fit' in attrs:
                    new_attrs['fit'] = attrs['fit']
                if 'year' in attrs:
                    new_attrs['year'] = attrs['year']
                # season is dropped (not included)
                
                row[3] = json.dumps(new_attrs)
            except:
                pass
        rows.append(row)

with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Updated {len(rows)} rows")
