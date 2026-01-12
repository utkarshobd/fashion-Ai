import pandas as pd

INPUT_CSV = "annotations/labels.csv"
OUTPUT_CSV = "annotations/labels_cleaned.csv"

df = pd.read_csv(
    INPUT_CSV,
    engine="python",
    on_bad_lines="skip"
)

# Normalize category
df["category"] = df["category"].astype(str).str.strip().str.lower()

# Correct replacement
df.loc[df["category"] == "lehenga", "category"] = "lehengas"

df.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)

print("Done: category 'lehenga' → 'lehengas'")
