"""
Single Image Fashion Prediction
Upload any fashion image and get predictions for all 5 attributes
"""

import torch
import sys
import os
from PIL import Image
from torchvision import transforms

# Add training_system to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'training_system'))

from model import MultiHeadFashionModel
from config import LABEL_MAPPINGS

class FashionPredictor:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model(model_path)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def load_model(self, model_path):
        model = MultiHeadFashionModel()
        checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
        
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        
        model = model.to(self.device)
        model.eval()
        return model
    
    def predict(self, image_path):
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(image_tensor)
        
        # Convert to predictions
        predictions = {}
        confidences = {}
        
        for head, output in outputs.items():
            probs = torch.softmax(output, dim=1)
            pred_idx = torch.argmax(probs, dim=1).item()
            confidence = probs[0, pred_idx].item()
            
            predictions[head] = LABEL_MAPPINGS[head][pred_idx]
            confidences[head] = confidence
        
        return predictions, confidences

def main():
    # Get image path from user
    image_path = input("Enter the path to your fashion image: ").strip().strip('"')
    
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    # Load model
    model_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 'final_model_v1.pth')
    predictor = FashionPredictor(model_path)
    
    # Make predictions
    predictions, confidences = predictor.predict(image_path)
    
    # Display results
    print(f"\n🔍 Fashion Analysis for: {os.path.basename(image_path)}")
    print("=" * 50)
    
    print(f"👔 Category: {predictions['category']} ({confidences['category']:.1%})")
    print(f"🏷️  Type: {predictions['sub_category']} ({confidences['sub_category']:.1%})")
    print(f"🎨 Color: {predictions['color_primary']} ({confidences['color_primary']:.1%})")
    print(f"🎭 Pattern: {predictions['pattern']} ({confidences['pattern']:.1%})")
    
    # Sub_class only for t_shirt and jacket
    if predictions['category'] in ['t_shirt', 'jacket']:
        print(f"📝 Sub-class: {predictions['sub_class']} ({confidences['sub_class']:.1%})")
    else:
        print(f"📝 Sub-class: Not applicable for {predictions['category']}")

if __name__ == "__main__":
    main()