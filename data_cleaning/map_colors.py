import pandas as pd

# Define color mapping based on color theory and visual similarity
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
    
    # Multicolor corrections and invalid entries
    'mulicolor': 'multicolor',
    'umulticolor': 'multicolor',
    'unknown': 'multicolor',
    'na': 'multicolor',
    'v neck semi sheer fitted top': 'multicolor',
    'women solid tops black': 'black'  # This seems to be black based on name
}

# Apply mapping to both files
print("Mapping colors in labels_tested.csv...")
df_tested = pd.read_csv('labels_tested.csv')
print(f"Before mapping - unique colors: {df_tested['color_primary'].nunique()}")

# Apply mapping
for old_color, new_color in color_mapping.items():
    df_tested.loc[df_tested['color_primary'] == old_color, 'color_primary'] = new_color

df_tested.to_csv('labels_tested.csv', index=False)
print(f"After mapping - unique colors: {df_tested['color_primary'].nunique()}")

print("\nMapping colors in labels_train.csv...")
df_train = pd.read_csv('annotations/labels_train.csv')
print(f"Before mapping - unique colors: {df_train['color_primary'].nunique()}")

# Apply mapping
for old_color, new_color in color_mapping.items():
    df_train.loc[df_train['color_primary'] == old_color, 'color_primary'] = new_color

df_train.to_csv('annotations/labels_train.csv', index=False)
print(f"After mapping - unique colors: {df_train['color_primary'].nunique()}")

# Show final color distribution
print("\nFinal color distribution in labels_train.csv:")
final_colors = df_train['color_primary'].value_counts()
print(final_colors)
print(f"\nFinal unique colors: {sorted(df_train['color_primary'].unique())}")