import pandas as pd
import json

# Load CSV
df = pd.read_csv(
    "annotations/labels.csv",
    engine="python",
    on_bad_lines="skip"
)

# Columns to remove from attributes_json
REMOVE_KEYS = {"fabric_hint", "sleeve_length", "length_category"}

# Function to clean attributes_json
def clean_attributes(attr_str):
    try:
        attr = json.loads(attr_str)
        for key in REMOVE_KEYS:
            attr.pop(key, None)
        return json.dumps(attr, ensure_ascii=False)
    except Exception:
        return attr_str  # leave unchanged if broken

# Apply ONLY to ethnic / salwar_suit
mask = (df["category"] == "suit_salwar") & (df["sub_category"] == "ethnic")

df.loc[mask, "attributes_json"] = df.loc[mask, "attributes_json"].apply(clean_attributes)

# Save updated CSV
df.to_csv(
    "annotations/labels_cleaned.csv",
    index=False,
    encoding="utf-8"
)

print("Done: attributes cleaned for ethnic/salwar_suit")
