import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
import os
from tqdm import tqdm

# Add the training_system_v2 directory to path to import modules
sys.path.append('training_system_v2')
from model import MultiHeadFashionModel
from config import *

# -----------------------------
# CONFIG
# -----------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMAGE_SIZE = 512
MODEL_PATH = "training_system_v2/checkpoints/checkpoint_epoch_10.pth"
TEST_CSV = "annotation_v2/labels_test.csv"
IMAGES_DIR = "images_resized512"

# Load checkpoint and setup
checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
encoders = checkpoint["encoders"]
LABELS = {k: list(v.keys()) for k, v in encoders.items()}

# Model
model = MultiHeadFashionModel().to(DEVICE)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

def predict_single(image_path):
    """Predict single image"""
    try:
        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(tensor)
        
        results = {}
        for head, logits in outputs.items():
            probs = F.softmax(logits, dim=1)
            idx = probs.argmax(1).item()
            results[head] = LABELS[head][idx]
        
        return results
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def evaluate_model():
    """Evaluate model on test set"""
    
    # Load test data
    df = pd.read_csv(TEST_CSV)
    print(f"Loaded {len(df)} test samples")
    
    # Initialize metrics
    metrics = {head: {"correct": 0, "total": 0} for head in LABELS.keys()}
    
    # Process each test sample
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Testing"):
        image_path = os.path.join(IMAGES_DIR, row['file_path'])
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue
            
        # Get prediction
        pred = predict_single(image_path)
        if pred is None:
            continue
            
        # Compare predictions with ground truth
        for head in LABELS.keys():
            if head in row and pd.notna(row[head]):
                ground_truth = row[head]
                predicted = pred[head]
                
                metrics[head]["total"] += 1
                if predicted == ground_truth:
                    metrics[head]["correct"] += 1
    
    # Calculate and display results
    print("\n" + "="*60)
    print("MODEL ACCURACY RESULTS")
    print("="*60)
    
    overall_correct = 0
    overall_total = 0
    
    for head, metric in metrics.items():
        if metric["total"] > 0:
            accuracy = metric["correct"] / metric["total"]
            print(f"{head:<20}: {accuracy:.3f} ({metric['correct']}/{metric['total']})")
            overall_correct += metric["correct"]
            overall_total += metric["total"]
        else:
            print(f"{head:<20}: No samples")
    
    if overall_total > 0:
        overall_accuracy = overall_correct / overall_total
        print("-" * 60)
        print(f"{'OVERALL':<20}: {overall_accuracy:.3f} ({overall_correct}/{overall_total})")
    
    print("="*60)
    
    return metrics

if __name__ == "__main__":
    print(f"Using device: {DEVICE}")
    print(f"Test CSV: {TEST_CSV}")
    print(f"Images directory: {IMAGES_DIR}")
    
    metrics = evaluate_model()