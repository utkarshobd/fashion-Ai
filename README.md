# Fashion AI - Classification System

A comprehensive fashion item classification system supporting both ethnic and western wear categories.

## Project Structure

```
fashion_dataset_transformed/
├── annotations/
│   └── label_schema.yaml          # Classification schema (SAFE)
├── src/                          # Source code (SAFE)
├── config/                       # Configuration templates (SAFE)
├── tests/                        # Unit tests (SAFE)
├── docs/                         # Documentation (SAFE)
└── samples/                      # Sample images for demo (SAFE)
```

## Features

- **Multi-category Classification**: Ethnic, Western, and Accessories
- **Detailed Attributes**: Sleeve length, fit, pattern, fabric, color, etc.
- **Gender Classification**: Male, Female, Unisex
- **Occasion Suitability**: Casual, Formal, Party, Wedding, etc.

## Categories Supported

### Ethnic Wear
- Kurta, Saree, Lehenga, Blouse Choli, Sherwani, Suit Salwar

### Western Wear  
- Shirt, T-shirt, Jeans, Trousers, Shorts, Dress, Skirt, Jacket

### Accessories
- Belt, Watch, Bag, Sunglasses, Jewelry, Wallet, Footwear

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables (see config/template.env)
4. Run tests: `python -m pytest tests/`

## Usage

```python
from src.classifier import FashionClassifier

classifier = FashionClassifier()
result = classifier.predict(image_path)
```

## Security Note

This repository contains only safe, non-proprietary code and configurations. Sensitive data, trained models, and credentials are excluded via .gitignore.

## License

Private - All Rights Reserved