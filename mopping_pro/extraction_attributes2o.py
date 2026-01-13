import pandas as pd
import json
import re

INPUT_CSV = "annotations/labels_cleaned.csv"
OUTPUT_CSV = "annotations/labels_with_extracted_attributes.csv"

# -------------------------
# Keyword vocabularies
# -------------------------

COLORS = {
    "black", "white", "pink", "red", "blue", "green", "yellow",
    "orange", "purple", "maroon", "beige", "cream", "grey",
    "gold", "silver", "brown", "navy"
}

GENDER_MAP = {
    "women": "female",
    "woman": "female",
    "men": "male",
    "man": "male",
    "girl": "female",
    "boy": "male"
}

pattern_keywords = {
    'printed': ['print', 'printed', 'floral print', 'geometric print', 'paisley print'],
    'embroidered': ['embroidered', 'embroidery', 'zardozi', 'sequin', 'sequins', 'beads',
                     'thread work', 'hand embroidered', 'resham', 'mirror work'],
    'solid': ['solid', 'plain'],
    'striped': ['stripe', 'striped', 'stripes'],
    'floral': ['floral', 'flower', 'botanical'],
    'geometric': ['geometric', 'paisley', 'mandarin', 'motif', 'pattern'],
    'checked': ['check', 'checked', 'checkered'],
    'polka': ['polka', 'dot', 'dotted']
}

occasion_keywords = {
    'wedding': ['wedding', 'bridal', 'bride', 'marriage'],
    'festive': ['festive', 'festival', 'celebration', 'party', 'evening wear'],
    'formal': ['formal', 'office', 'work'],
    'casual': ['casual', 'daily', 'everyday']
}

# -------------------------
# Helper functions
# -------------------------

def find_from_keywords(text, keyword_map):
    for canonical, keywords in keyword_map.items():
        for kw in keywords:
            if kw in text:
                return canonical
    return None

def extract_attributes_from_path(file_path):
    text = file_path.lower()
    tokens = re.split(r"[_/]", text)

    attr = {}

    # Color
    for t in tokens:
        if t in COLORS:
            attr["color_primary"] = t
            break

    # Gender
    for t in tokens:
        if t in GENDER_MAP:
            attr["gender"] = GENDER_MAP[t]
            break

    # Pattern
    pattern = find_from_keywords(text, pattern_keywords)
    if pattern:
        attr["pattern"] = pattern

    # Occasion
    occasion = find_from_keywords(text, occasion_keywords)
    if occasion:
        attr["occasion_suitability"] = occasion

    # Safe defaults (only if missing)
    attr.setdefault("pattern", "solid")
    attr.setdefault("occasion_suitability", "ethnic")
    attr.setdefault("fit", "regular")
    attr.setdefault("season", "all")

    return json.dumps(attr, ensure_ascii=False)

# -------------------------
# Apply extraction
# -------------------------

df = pd.read_csv(
    INPUT_CSV,
    engine="python",
    on_bad_lines="skip"
)

# Apply only where attributes_json is missing or empty
mask = df["attributes_json"].isna() | (df["attributes_json"].astype(str).str.strip() == "")

df.loc[mask, "attributes_json"] = df.loc[mask, "file_path"].apply(
    extract_attributes_from_path
)

# Save result
df.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)

print("Done:")
print("• pattern extracted using pattern_keywords")
print("• occasion extracted using occasion_keywords")
print("• source used: file_path ONLY")
print("• product_name ignored completely")
