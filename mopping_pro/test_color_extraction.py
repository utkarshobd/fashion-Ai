import re

def extract_color_from_name(product_name):
    """Extract color from product name using safe word-boundary matching"""
    if not isinstance(product_name, str):
        return None

    product_name = product_name.lower()

    color_map = {
        'red': ['red', 'maroon', 'crimson', 'burgundy', 'wine', 'cherry', 'rust', 'brick'],
        'blue': ['blue', 'navy', 'teal', 'turquoise', 'cobalt', 'sapphire', 'indigo', 'royal blue', 'sky blue'],
        'green': ['green', 'olive', 'emerald', 'mint', 'lime', 'forest', 'sage', 'bottle green', 'pista', 'mehendi'],
        'yellow': ['yellow', 'gold', 'golden', 'mustard', 'ochre', 'sunshine'],
        'pink': ['pink', 'rose', 'blush', 'coral', 'peach', 'magenta', 'rani pink', 'rani'],
        'purple': ['purple', 'violet', 'lavender', 'lilac', 'plum', 'mauve'],
        'orange': ['orange', 'saffron'],
        'black': ['black', 'charcoal', 'ebony'],
        'white': ['white', 'ivory', 'cream', 'off white', 'pearl'],
        'grey': ['grey', 'gray', 'silver'],
        'brown': ['brown', 'tan', 'chocolate', 'coffee', 'fawn'],
        'beige': ['beige', 'nude', 'champagne'],
        'multicolor': ['multicolor', 'multi color', 'mixed', 'combination']
    }

    for color, variants in color_map.items():
        for v in variants:
            if re.search(rf'\b{re.escape(v)}\b', product_name):
                return color

    return None

# Test with sample names
test_names = [
    "006 Women Lehenga Wine Hued Elegance Lehenga",
    "010 Women Lehenga Rani Art Silk Lehenga Set", 
    "028 Women Lehenga Sunshine Sparkle Lehenga",
    "029 Women Lehenga Fawn Glory Net Bridal Lehenga",
    "033 Women Lehenga Regal Wine Velvet Bridal Lehenga"
]

print("Testing color extraction:")
for name in test_names:
    color = extract_color_from_name(name)
    print(f"'{name}' -> {color}")

# Test individual color words
print("\nTesting individual words:")
test_words = ["wine", "rani", "fawn"]
for word in test_words:
    color = extract_color_from_name(word)
    print(f"'{word}' -> {color}")