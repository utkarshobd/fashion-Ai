import pandas as pd
import json

INPUT_CSV = "annotations/labels.csv"
OUTPUT_CSV = "annotations/labels_cleaned.csv"

df = pd.read_csv(
    INPUT_CSV,
    engine="python",
    on_bad_lines="skip"
)

# Row range to fix (0-based index)
START_ROW = 28650
END_ROW = 28975

# Canonical keys allowed for suit_salwar
ALLOWED_KEYS = {
    "color_primary",
    "pattern",
    "occasion_suitability",
    "gender",
    "fit",
    "season"
}

def fix_suit_salwar_metadata(attr_str):
    try:
        attr = json.loads(attr_str)

        # Keep only allowed keys
        attr = {k: v for k, v in attr.items() if k in ALLOWED_KEYS}

        # Normalize values
        if "gender" in attr:
            attr["gender"] = "female"

        if attr.get("season") in ["all-season", "all seasons"]:
            attr["season"] = "all"

        if "occasion_suitability" not in attr:
            attr["occasion_suitability"] = "ethnic"

        return json.dumps(attr, ensure_ascii=False)

    except Exception:
        return attr_str


# Slice affected rows
idx = df.index[START_ROW:END_ROW]

# Fix category & sub_category
df.loc[idx, "category"] = "suit_salwar"
df.loc[idx, "sub_category"] = "ethnic"

# Fix attributes_json
df.loc[idx, "attributes_json"] = df.loc[idx, "attributes_json"].apply(
    fix_suit_salwar_metadata
)

# Save cleaned dataset
df.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)

print("Done:")
print("- Fixed rows 28651–28975")
print("- Corrected suit_salwar schema")
print("- Saved to labels_cleaned.csv")
