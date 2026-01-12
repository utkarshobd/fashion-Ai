import pandas as pd

# Load CSV
df = pd.read_csv(
    "annotations/labels_reorganized_updated.csv",
    engine="python",
    on_bad_lines="skip"
)

# Replace category value
df.loc[df["category"] == "lehenga", "category"] = "lehengas"

# Save updated CSV
df.to_csv(
    "annotations/labels_reorganized_updated_cleaned.csv",
    index=False,
    encoding="utf-8"
)

print("Done: category 'lehenga' replaced with 'lehengas'")
