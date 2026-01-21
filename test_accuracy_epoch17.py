"""
Test Accuracy Calculator for Fashion AI Model
Loads the saved model and calculates accuracy on test dataset
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
import sys
from PIL import Image
from torchvision import transforms
import json

# Add training_system to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'training_system'))

from model import MultiHeadFashionModel
from config import *
# Import dataset class
class TestFashionDataset:
    def __init__(self, csv_file, images_dir, transform=None):
        self.images_dir = images_dir
        self.transform = transform
        
        # Load test data
        self.df = pd.read_csv(csv_file)
        self.df = self.df.dropna(subset=['file_path', 'category', 'sub_category', 'color_primary', 'pattern'])
        
        # Create label encoders
        self.label_encoders = {}
        for head in LABEL_MAPPINGS:
            self.label_encoders[head] = {label: idx for idx, label in enumerate(LABEL_MAPPINGS[head])}
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        
        # Load image
        img_path = os.path.join(self.images_dir, row['file_path'])
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            # Return a black image as fallback
            image = Image.new('RGB', (224, 224), (0, 0, 0))
        
        if self.transform:
            image = self.transform(image)
        
        # Prepare labels
        sample = {'image': image}
        
        # Standard heads
        for head in ['sub_category', 'category', 'color_primary', 'pattern']:
            label_str = str(row[head]).strip()
            if label_str in self.label_encoders[head]:
                sample[head] = self.label_encoders[head][label_str]
            else:
                sample[head] = 0  # Default to first class
        
        # Sub_class head with masking
        category_str = str(row['category']).strip()
        sub_class_str = str(row['sub_class']).strip()
        
        if (category_str in SUB_CLASS_VALID_CATEGORIES and 
            sub_class_str != 'nan' and 
            sub_class_str in self.label_encoders['sub_class']):
            sample['sub_class'] = self.label_encoders['sub_class'][sub_class_str]
        else:
            sample['sub_class'] = 0  # Default class
        
        return sample

class TestAccuracyCalculator:
    def __init__(self, model_path, test_csv_path, images_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_path = model_path
        self.test_csv_path = test_csv_path
        self.images_path = images_path
        
        # Load model
        self.model = self.load_model()
        
        # Create test dataset and dataloader
        self.test_loader = self.create_test_loader()
        
        print(f"Device: {self.device}")
        print(f"Model loaded from: {model_path}")
        print(f"Test dataset size: {len(self.test_loader.dataset)}")
    
    def load_model(self):
        """Load the trained model"""
        model = MultiHeadFashionModel()
        
        # Try to load the checkpoint
        try:
            if torch.cuda.is_available():
                checkpoint = torch.load(self.model_path, weights_only=False)
            else:
                checkpoint = torch.load(self.model_path, map_location='cpu', weights_only=False)
            
            # Handle different checkpoint formats
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
                epoch = checkpoint.get('epoch', 'unknown')
                print(f"Loaded model from epoch: {epoch}")
            elif 'state_dict' in checkpoint:
                model.load_state_dict(checkpoint['state_dict'])
            else:
                # Assume the checkpoint is just the state dict
                model.load_state_dict(checkpoint)
            
            model = model.to(self.device)
            model.eval()
            return model
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def create_test_loader(self):
        """Create test data loader"""
        # Define transforms (same as training)
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Create dataset
        test_dataset = TestFashionDataset(
            csv_file=self.test_csv_path,
            images_dir=self.images_path,
            transform=transform
        )
        
        # Create dataloader
        test_loader = DataLoader(
            test_dataset,
            batch_size=32,
            shuffle=False,
            num_workers=2
        )
        
        return test_loader
    
    def calculate_accuracy(self):
        """Calculate test accuracy for all heads"""
        self.model.eval()
        
        # Initialize storage for predictions and targets
        all_predictions = {head: [] for head in ['sub_category', 'category', 'color_primary', 'pattern', 'sub_class']}
        all_targets = {head: [] for head in ['sub_category', 'category', 'color_primary', 'pattern', 'sub_class']}
        
        total_samples = 0
        
        print("Calculating test accuracy...")
        
        with torch.no_grad():
            for batch_idx, batch in enumerate(self.test_loader):
                images = batch['image'].to(self.device)
                targets = {key: batch[key].to(self.device) for key in batch if key != 'image'}
                
                # Forward pass
                outputs = self.model(images)
                
                # Store predictions and targets
                for head in all_predictions.keys():
                    if head in outputs and head in targets:
                        # Get predictions (argmax)
                        preds = torch.argmax(outputs[head], dim=1)
                        all_predictions[head].extend(preds.cpu().numpy())
                        all_targets[head].extend(targets[head].cpu().numpy())
                
                total_samples += images.size(0)
                
                if (batch_idx + 1) % 50 == 0:
                    print(f"Processed {batch_idx + 1}/{len(self.test_loader)} batches")
        
        # Calculate accuracies
        results = {}
        
        for head in all_predictions.keys():
            if len(all_predictions[head]) > 0 and len(all_targets[head]) > 0:
                accuracy = accuracy_score(all_targets[head], all_predictions[head])
                results[f'{head}_accuracy'] = accuracy
                
                # Generate classification report
                try:
                    if head in LABEL_MAPPINGS:
                        labels = LABEL_MAPPINGS[head]
                        report = classification_report(
                            all_targets[head], 
                            all_predictions[head],
                            target_names=labels,
                            output_dict=True,
                            zero_division=0
                        )
                        results[f'{head}_classification_report'] = report
                except Exception as e:
                    print(f"Warning: Could not generate classification report for {head}: {e}")
        
        results['total_samples'] = total_samples
        
        return results
    
    def save_results(self, results, output_path):
        """Save results to JSON file"""
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Clean results for JSON serialization
        clean_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                clean_results[key] = {k: convert_numpy(v) for k, v in value.items()}
            else:
                clean_results[key] = convert_numpy(value)
        
        with open(output_path, 'w') as f:
            json.dump(clean_results, f, indent=2)
        
        print(f"Results saved to: {output_path}")

def main():
    # Paths
    base_dir = os.path.dirname(__file__)
    
    # Use the final_model.pth as specified by user
    model_path = os.path.join(base_dir, 'checkpoints', 'final_model.pth')
    
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        return
    
    test_csv_path = os.path.join(base_dir, 'annotations', 'labels_test.csv')
    images_path = os.path.join(base_dir, 'images_resized512')
    
    # Check if paths exist
    if not os.path.exists(test_csv_path):
        print(f"Test CSV not found: {test_csv_path}")
        return
    
    if not os.path.exists(images_path):
        print(f"Images directory not found: {images_path}")
        return
    
    print(f"Using model: {model_path}")
    print(f"Test CSV: {test_csv_path}")
    print(f"Images path: {images_path}")
    
    # Calculate test accuracy
    calculator = TestAccuracyCalculator(model_path, test_csv_path, images_path)
    results = calculator.calculate_accuracy()
    
    # Print results
    print("\n" + "="*50)
    print("TEST ACCURACY RESULTS")
    print("="*50)
    
    for key, value in results.items():
        if key.endswith('_accuracy'):
            head_name = key.replace('_accuracy', '')
            print(f"{head_name.upper()} Accuracy: {value:.4f} ({value*100:.2f}%)")
    
    print(f"\nTotal test samples: {results['total_samples']}")
    
    # Save detailed results
    output_path = os.path.join(base_dir, 'test_accuracy_results.json')
    calculator.save_results(results, output_path)
    
    # Check success criteria
    print("\n" + "="*50)
    print("SUCCESS CRITERIA CHECK")
    print("="*50)
    
    success_criteria = {
        'category_accuracy': 0.85,
        'color_primary_accuracy': 0.80,
        'pattern_accuracy': 0.75,
        'sub_class_accuracy': 0.60,
        'sub_category_accuracy': 0.90
    }
    
    passed_criteria = 0
    total_criteria = len(success_criteria)
    
    for criterion, threshold in success_criteria.items():
        if criterion in results:
            actual = results[criterion]
            status = "PASS" if actual >= threshold else "FAIL"
            print(f"{criterion}: {actual:.4f} >= {threshold:.4f} {status}")
            if actual >= threshold:
                passed_criteria += 1
        else:
            print(f"{criterion}: Not available")
    
    print(f"\nOverall: {passed_criteria}/{total_criteria} criteria passed")
    
    if passed_criteria == total_criteria:
        print("ALL SUCCESS CRITERIA MET!")
    else:
        print(f"{total_criteria - passed_criteria} criteria need improvement")

if __name__ == "__main__":
    main()