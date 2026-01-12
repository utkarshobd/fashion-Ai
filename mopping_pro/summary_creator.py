import pandas as pd
import json

# Load CSV (use the correct file)
df = pd.read_csv(
    "annotations/labels_reorganized_updated.csv",
    engine="python",
    on_bad_lines="skip"
)

# Filter lehengas
lehenga_df = df[df["category"] == "lehenga"].copy()

# Ensure attributes_json is string
lehenga_df["attributes_json"] = lehenga_df["attributes_json"].astype(str)

# Safe JSON parsing
def safe_json_load(x):
    try:
        return json.loads(x)
    except Exception:
        return {}

lehenga_df["attributes_json"] = lehenga_df["attributes_json"].apply(safe_json_load)

# Expand attributes into columns
attr_df = pd.json_normalize(lehenga_df["attributes_json"])

lehenga_df = pd.concat(
    [lehenga_df.reset_index(drop=True), attr_df],
    axis=1
)

# -------- SUMMARY --------
attributes_to_summarize = [
    "color_primary",
    "pattern",
    "occasion_suitability",
    "fit",
    "season"
]

total = len(lehenga_df)

for attr in attributes_to_summarize:
    if attr in lehenga_df.columns:
        summary = lehenga_df[attr].value_counts(dropna=False)
        percent = (summary / total * 100).round(2)

        print(f"\n===== {attr.upper()} =====")
        print(pd.DataFrame({
            "count": summary,
            "percentage": percent
        }))
