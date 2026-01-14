import pandas as pd
import json
import requests

def extract_color_from_name(image_name):
    """Use Ollama LLM to extract color from fancy image names"""
    
    filename = image_name.split('/')[-1].replace('.jpg', '').replace('_', ' ')
    
    prompt = f"""Extract PRIMARY color from: "{filename}"

Fancy names: Magnetic Muse=purple, Wine=maroon, Fuchsia=pink, Earth=brown, Rani=pink, Mehendi=green

Return ONE word: red, blue, green, yellow, orange, pink, purple, black, white, grey, brown, beige, maroon, navy_blue, silver, gold, multicolor, unknown

Color:"""

    try:
        response = requests.post('http://localhost:11434/api/generate',
            json={'model': 'llama3.2', 'prompt': prompt, 'stream': False})
        color = response.json()['response'].strip().lower().split()[0]
        
        valid_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'purple', 
                       'black', 'white', 'grey', 'brown', 'beige', 'maroon', 'navy_blue', 
                       'silver', 'gold', 'multicolor', 'unknown']
        
        return color if color in valid_colors else 'unknown'
            
    except Exception as e:
        print(f"Error: {e}")
        return 'unknown'

def update_csv_colors(csv_path):
    df = pd.read_csv(csv_path)
    mask = (df['sub_category'] == 'ethnic') & (df['category'] == 'blouse_choli')
    updated_count = 0
    
    for idx, row in df[mask].iterrows():
        try:
            attributes = json.loads(row['attributes_json'])
            
            if attributes.get('color_primary') == 'unknown':
                print(f"Processing: {row['file_path']}")
                new_color = extract_color_from_name(row['file_path'])
                print(f"Color: {new_color}")
                
                if new_color != 'unknown':
                    attributes['color_primary'] = new_color
                    df.at[idx, 'attributes_json'] = json.dumps(attributes)
                    updated_count += 1
                    
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    df.to_csv(csv_path, index=False)
    print(f"\nUpdated {updated_count} rows")

if __name__ == "__main__":
    csv_path = r"c:\Users\utkarshh\Desktop\FAI\FAII\fashion_dataset_transformed\annotations\labels_cleaned.csv"
    update_csv_colors(csv_path)
    print("Done!")
