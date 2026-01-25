"""
Stratified Data Splitting - Split Once, Freeze Forever
Creates train/val/test splits stratified by category only
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os

def create_stratified_splits():
    """Create stratified splits: 70% train, 15% val, 15% test"""
    
    # Load full labels file
    labels_path = "annotations/labels_train.csv"
    if not os.path.exists(labels_path):
        print(f"ERROR: {labels_path} not found!")
        return False
    
    df = pd.read_csv(labels_path)
    print(f"Loaded {len(df)} samples from {labels_path}")
    
    # Check category distribution
    cat_counts = df["category"].value_counts()
    print(f"\nCategory distribution:")
    for cat, count in cat_counts.items():
        print(f"  {cat}: {count}")
    
    # Handle categories with very few samples
    min_samples_needed = 6  # Need at least 6 for double stratification (2 splits)
    rare_categories = cat_counts[cat_counts < min_samples_needed].index.tolist()
    
    if rare_categories:
        print(f"\nWARNING: Categories with <{min_samples_needed} samples: {rare_categories}")
        print("These will be handled manually...")
        
        # Separate rare and common categories
        rare_df = df[df["category"].isin(rare_categories)]
        common_df = df[~df["category"].isin(rare_categories)]
        
        print(f"Rare samples: {len(rare_df)}, Common samples: {len(common_df)}")
        
        # Split common categories with stratification
        train_common, temp_common = train_test_split(
            common_df,
            test_size=0.30,
            stratify=common_df["category"],
            random_state=42
        )
        
        val_common, test_common = train_test_split(
            temp_common,
            test_size=0.50,
            stratify=temp_common["category"],
            random_state=42
        )
        
        # Handle rare categories manually - put all in train
        train_df = pd.concat([train_common, rare_df], ignore_index=True)
        val_df = val_common.copy()
        test_df = test_common.copy()
        
    else:
        # Normal stratified split
        train_df, temp_df = train_test_split(
            df,
            test_size=0.30,
            stratify=df["category"],
            random_state=42
        )
        
        val_df, test_df = train_test_split(
            temp_df,
            test_size=0.50,
            stratify=temp_df["category"],
            random_state=42
        )
    
    # Save splits
    train_df.to_csv("annotations/labels_train_split.csv", index=False)
    val_df.to_csv("annotations/labels_val.csv", index=False)
    test_df.to_csv("annotations/labels_test.csv", index=False)
    
    print(f"\nSplits created:")
    print(f"  Train: {len(train_df)} samples ({len(train_df)/len(df)*100:.1f}%)")
    print(f"  Val:   {len(val_df)} samples ({len(val_df)/len(df)*100:.1f}%)")
    print(f"  Test:  {len(test_df)} samples ({len(test_df)/len(df)*100:.1f}%)")
    
    # Mandatory sanity checks
    print("\n" + "="*50)
    print("MANDATORY SANITY CHECKS")
    print("="*50)
    
    splits = [("Train", train_df), ("Val", val_df), ("Test", test_df)]
    
    for split_name, split_df in splits:
        print(f"\n{split_name} Split:")
        
        # Category distribution
        cat_dist = split_df["category"].value_counts(normalize=True)
        print("  Category distribution:")
        for cat, pct in cat_dist.items():
            print(f"    {cat}: {pct:.3f}")
        
        # Check for major categories (allow missing rare ones)
        major_categories = ["t_shirt", "shirt", "jacket", "saree", "dress", "kurta"]
        missing_major = [cat for cat in major_categories if cat not in split_df["category"].unique()]
        if missing_major:
            print(f"  X MISSING MAJOR CATEGORIES: {missing_major}")
            return False
        
        # Check jacket samples (critical for sub_class)
        jacket_count = (split_df["category"] == "jacket").sum()
        t_shirt_count = (split_df["category"] == "t_shirt").sum()
        if jacket_count == 0:
            print(f"  X ZERO JACKET SAMPLES")
            return False
        if t_shirt_count == 0:
            print(f"  X ZERO T_SHIRT SAMPLES")
            return False
        print(f"  OK Jacket samples: {jacket_count}")
        print(f"  OK T-shirt samples: {t_shirt_count}")
        
        # Check non-null sub_class
        sub_class_valid_pct = split_df["sub_class"].notna().mean()
        print(f"  Sub_class valid: {sub_class_valid_pct:.3f}")
        if sub_class_valid_pct == 0:
            print(f"  X ZERO NON-NULL SUB_CLASS")
            return False
        print(f"  OK Non-null sub_class: {sub_class_valid_pct:.3f}")
    
    print("\n" + "="*50)
    print("OK ALL SANITY CHECKS PASSED")
    print("OK SPLITS ARE VALID AND FROZEN")
    print("="*50)
    
    # Final summary
    print(f"\nFINAL SPLIT SUMMARY:")
    print(f"  Train: {len(train_df):,} samples ({len(train_df)/len(df)*100:.1f}%)")
    print(f"  Val:   {len(val_df):,} samples ({len(val_df)/len(df)*100:.1f}%)")
    print(f"  Test:  {len(test_df):,} samples ({len(test_df)/len(df)*100:.1f}%)")
    print(f"  Total: {len(df):,} samples")
    
    return True

if __name__ == "__main__":
    success = create_stratified_splits()
    if success:
        print("\nSUCCESS: Data splits created and validated")
        print("Files created:")
        print("  - annotations/labels_train_split.csv")
        print("  - annotations/labels_val.csv") 
        print("  - annotations/labels_test.csv")
    else:
        print("\nFAILED: Split creation failed sanity checks")