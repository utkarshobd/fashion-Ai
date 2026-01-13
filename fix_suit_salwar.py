import pandas as pd
import json

INPUT_CSV = "annotations/labels.csv"
OUTPUT_CSV = "annotations/labels_fixed_suit_salwar.csv"

df = pd.read_csv(
    INPUT_CSV,
    engine="python",
    on_bad_lines="skip"
)

# Identify corrupted rows by pattern (NOT index)
mask = (
    (df["category"] == "salwar_suit") &
    (df["sub_category"] == "straight") &
    (df["file_path"].str.startswith("ethnic/suit_salwar"))
)

print("Corrupted rows found:", mask.sum())

ALLOWED_KEYS = {
    "color_primary",
    "pattern",
    "occasion_suitability",
    "gender",
    "fit",
    "season"
}

def fix_attributes(attr_str):
    try:
        attr = json.loads(attr_str)

        # keep only allowed keys
        attr = {k: v for k, v in attr.items() if k in ALLOWED_KEYS}

        # normalize values
        attr["gender"] = "female"
        attr["season"] = "all"
        attr["occasion_suitability"] = "ethnic"

        return json.dumps(attr, ensure_ascii=False)
    except Exception:
        return attr_str

# Apply fixes
df.loc[mask, "category"] = "suit_salwar"
df.loc[mask, "sub_category"] = "ethnic"
df.loc[mask, "attributes_json"] = df.loc[mask, "attributes_json"].apply(fix_attributes)

# Save result
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

print("Saved corrected file:", OUTPUT_CSV)
