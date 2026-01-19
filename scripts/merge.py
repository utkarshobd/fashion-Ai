import pandas as pd
import json

INPUT_CSV = "annotations/labels.csv"
OUTPUT_CSV = "annotations/labels_cleaned.csv"

# Load CSV safely
df = pd.read_csv(
    INPUT_CSV,
    engine="python",
    on_bad_lines="skip"
)

# Canonical color mapping
COLOR_MAP = {
    "navy blue": "navy_blue",
    "navy_blue": "navy_blue"
}

def normalize_color(attr_str):
    try:
        attr = json.loads(attr_str)

        if "color_primary" in attr:
            value = attr["color_primary"].strip().lower()
            if value in COLOR_MAP:
                attr["color_primary"] = COLOR_MAP[value]

        return json.dumps(attr, ensure_ascii=False)
    except Exception:
        return attr_str  # leave unchanged if malformed

# Apply ONLY to ethnic / sherwani
mask = (df["category"] == "sherwani") & (df["sub_category"] == "ethnic")

df.loc[mask, "attributes_json"] = df.loc[mask, "attributes_json"].apply(normalize_color)

# Save to new CSV
df.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)

print("Done: merged 'navy blue' + 'navy_blue' → 'navy_blue' for ethnic/sherwani")
