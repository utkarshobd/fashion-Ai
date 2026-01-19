import pandas as pd
import json

# Read the original labels_tested.csv
df_original = pd.read_csv('labels_tested.csv')

# Extract all color values from JSON
def extract_color_from_json(attributes_json_str):
    try:
        attrs = json.loads(attributes_json_str)
        return attrs.get('color_primary', 'missing_key')
    except:
        return 'json_error'

df_original['extracted_color'] = df_original['attributes_json'].apply(extract_color_from_json)

# Check all unique extracted colors
print("All unique colors extracted from original JSON:")
unique_colors = df_original['extracted_color'].value_counts()
print(unique_colors)

# Check if there are any 'unknown' values
unknown_entries = df_original[df_original['extracted_color'] == 'unknown']
print(f"\nEntries with 'unknown' color: {len(unknown_entries)}")

if len(unknown_entries) > 0:
    print("Sample unknown entries:")
    print(unknown_entries[['file_path', 'attributes_json']].head())

# Check for any entries that might have been processed as 'unknown'
problem_entries = df_original[df_original['extracted_color'].isin(['missing_key', 'json_error', 'unknown'])]
print(f"\nProblem entries (missing_key, json_error, unknown): {len(problem_entries)}")

if len(problem_entries) > 0:
    print("Sample problem entries:")
    print(problem_entries[['file_path', 'attributes_json']].head())