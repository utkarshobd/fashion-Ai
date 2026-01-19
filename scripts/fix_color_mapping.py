import pandas as pd

# Define color mapping - keeping 'unknown' as separate color
color_mapping = {
    # Blue family
    'navy_blue': 'blue',
    'teal': 'blue', 
    'teal blue': 'blue',
    'turquoise': 'blue',
    'turquoise_blue': 'blue',
    'aqua': 'blue',
    
    # Red family
    'maroon': 'red',
    'wine': 'red',
    'burgundy': 'red',
    'rust': 'red',
    
    # Green family
    'emerald': 'green',
    'sea_green': 'green',
    'lime_green': 'green',
    'verdant green': 'green',
    'olive': 'green',
    
    # Purple family
    'lavender': 'purple',
    'magenta': 'purple',
    'mauve': 'purple',
    
    # White family
    'cream': 'white',
    'cream color': 'white',
    'off_white': 'white',
    'silver': 'white',
    
    # Grey family
    'charcoal': 'grey',
    'grey_melange': 'grey',
    
    # Brown family
    'coffee_brown': 'brown',
    'mushroom_brown': 'brown',
    'tan': 'brown',
    'khaki': 'brown',
    
    # Yellow family
    'mustard': 'yellow',
    'gold': 'yellow',
    
    # Orange family
    'peach': 'orange',
    
    # Multicolor corrections only (not unknown)
    'mulicolor': 'multicolor',
    'umulticolor': 'multicolor',
    'na': 'multicolor',
    'v neck semi sheer fitted top': 'multicolor',
    'women solid tops black': 'black'
    
    # Note: 'unknown' is NOT mapped - it stays as 'unknown'
}

print("Correcting color mapping in labels_train.csv...")
df_train = pd.read_csv('annotations/labels_train.csv')
print(f"Before mapping - unique colors: {df_train['color_primary'].nunique()}")

# Apply mapping to the color_primary column
for old_color, new_color in color_mapping.items():
    df_train.loc[df_train['color_primary'] == old_color, 'color_primary'] = new_color

df_train.to_csv('annotations/labels_train.csv', index=False)
print(f"After mapping - unique colors: {df_train['color_primary'].nunique()}")

# Show final color distribution
print("\nFinal color distribution in labels_train.csv:")
final_colors = df_train['color_primary'].value_counts()
print(final_colors)
print(f"\nFinal unique colors: {sorted(df_train['color_primary'].unique())}")
print(f"Total colors: {len(df_train['color_primary'].unique())}")