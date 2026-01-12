#!/usr/bin/env python3
"""
Lehenga Dataset Analysis and Summary
"""

import pandas as pd
import json
import os
from collections import Counter

def analyze_lehenga_data(csv_file):
    """Analyze lehenga data from the fashion dataset"""
    
    print("🔍 LEHENGA DATASET ANALYSIS")
    print("=" * 50)
    
    try:
        # Read the dataset
        df = pd.read_csv(csv_file)
        
        # Filter lehenga records
        lehenga_df = df[df['category'].str.contains('lehenga', case=False, na=False) | 
                       df['sub_category'].str.contains('lehenga', case=False, na=False)]
        
        if lehenga_df.empty:
            print("❌ No lehenga records found in the dataset")
            return
        
        print(f"📊 BASIC STATISTICS")
        print(f"Total lehenga records: {len(lehenga_df)}")
        print(f"Percentage of dataset: {len(lehenga_df)/len(df)*100:.2f}%")
        
        # Gender distribution
        print(f"\n👥 GENDER DISTRIBUTION")
        gender_counts = lehenga_df['gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f"  {gender}: {count} ({count/len(lehenga_df)*100:.1f}%)")
        
        # Source distribution
        print(f"\n🏪 SOURCE DISTRIBUTION")
        source_counts = lehenga_df['source'].value_counts()
        for source, count in source_counts.items():
            print(f"  {source}: {count} ({count/len(lehenga_df)*100:.1f}%)")
        
        # Analyze attributes
        print(f"\n🎨 COLOR ANALYSIS")
        colors = []
        patterns = []
        occasions = []
        fits = []
        
        for idx, row in lehenga_df.iterrows():
            try:
                if pd.notna(row['attributes_json']):
                    # Clean the JSON string
                    json_str = str(row['attributes_json'])
                    if json_str.startswith('"') and json_str.endswith('"'):
                        json_str = json_str[1:-1].replace('""', '"')
                    
                    attrs = json.loads(json_str)
                    colors.append(attrs.get('color_primary', 'unknown'))
                    patterns.append(attrs.get('pattern', 'unknown'))
                    occasions.append(attrs.get('occasion_suitability', 'unknown'))
                    fits.append(attrs.get('fit', 'unknown'))
            except:
                colors.append('unknown')
                patterns.append('unknown')
                occasions.append('unknown')
                fits.append('unknown')
        
        # Color distribution
        color_counts = Counter(colors)
        print("Top colors:")
        for color, count in color_counts.most_common(10):
            print(f"  {color}: {count} ({count/len(lehenga_df)*100:.1f}%)")
        
        # Pattern distribution
        print(f"\n🎭 PATTERN ANALYSIS")
        pattern_counts = Counter(patterns)
        print("Top patterns:")
        for pattern, count in pattern_counts.most_common(10):
            print(f"  {pattern}: {count} ({count/len(lehenga_df)*100:.1f}%)")
        
        # Occasion distribution
        print(f"\n🎉 OCCASION ANALYSIS")
        occasion_counts = Counter(occasions)
        for occasion, count in occasion_counts.most_common():
            print(f"  {occasion}: {count} ({count/len(lehenga_df)*100:.1f}%)")
        
        # Fit distribution
        print(f"\n👗 FIT ANALYSIS")
        fit_counts = Counter(fits)
        for fit, count in fit_counts.most_common():
            print(f"  {fit}: {count} ({count/len(lehenga_df)*100:.1f}%)")
        
        # Sample products
        print(f"\n📝 SAMPLE LEHENGA PRODUCTS")
        sample_products = lehenga_df['product_name'].head(10).tolist()
        for i, product in enumerate(sample_products, 1):
            print(f"  {i}. {product}")
        
        # File path analysis
        print(f"\n📁 FILE PATH ANALYSIS")
        file_paths = lehenga_df['file_path'].tolist()
        path_prefixes = [path.split('/')[0] if '/' in path else path.split('\\')[0] for path in file_paths]
        prefix_counts = Counter(path_prefixes)
        for prefix, count in prefix_counts.most_common():
            print(f"  {prefix}: {count} files")
        
        # Save lehenga subset
        output_file = "lehenga_dataset_summary.csv"
        lehenga_df.to_csv(output_file, index=False)
        print(f"\n💾 Lehenga dataset saved to: {output_file}")
        
        # Generate summary report
        generate_summary_report(lehenga_df, color_counts, pattern_counts, occasion_counts)
        
    except Exception as e:
        print(f"❌ Error analyzing lehenga data: {e}")

def generate_summary_report(df, colors, patterns, occasions):
    """Generate a detailed summary report"""
    
    report = f"""
# LEHENGA DATASET SUMMARY REPORT

## Overview
- **Total Records**: {len(df)}
- **Data Quality**: {len(df[df['product_name'].notna()])} records with product names
- **Unique Products**: {df['product_name'].nunique()} unique product names

## Key Insights

### Color Preferences
- **Most Popular Color**: {colors.most_common(1)[0][0]} ({colors.most_common(1)[0][1]} items)
- **Color Diversity**: {len(colors)} different colors identified
- **Unknown Colors**: {colors.get('unknown', 0)} items need color classification

### Pattern Distribution
- **Most Common Pattern**: {patterns.most_common(1)[0][0]} ({patterns.most_common(1)[0][1]} items)
- **Pattern Variety**: {len(patterns)} different patterns
- **Embroidered Items**: {patterns.get('embroidered', 0)} items

### Occasion Suitability
- **Primary Occasion**: {occasions.most_common(1)[0][0]} ({occasions.most_common(1)[0][1]} items)
- **Festive Wear**: {occasions.get('festive', 0)} items
- **Ethnic Wear**: {occasions.get('ethnic', 0)} items

## Recommendations
1. **Data Cleaning**: {colors.get('unknown', 0)} items need color identification
2. **Category Standardization**: Ensure consistent lehenga categorization
3. **Attribute Enhancement**: Add more detailed attributes like fabric, work type, etc.
4. **Image Quality**: Verify all file paths are accessible

## Next Steps
- Validate image file accessibility
- Enhance attribute data quality
- Consider subcategory classification (bridal, party, casual lehengas)
- Add price range analysis if available
"""
    
    with open("lehenga_analysis_report.md", "w", encoding='utf-8') as f:
        f.write(report)
    
    print(f"📋 Detailed report saved to: lehenga_analysis_report.md")

if __name__ == "__main__":
    # File path
    csv_file = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_reorganized_updated.csv"
    
    if os.path.exists(csv_file):
        analyze_lehenga_data(csv_file)
    else:
        print(f"❌ File not found: {csv_file}")
        print("Please check the file path and try again.")