import pandas as pd
import torch
import torch.nn.functional as F
import timm
from PIL import Image
from torchvision import transforms
import os
from tqdm import tqdm

# Config
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMAGE_SIZE = 512
MODEL_PATH = "training_system_v2/checkpoints/checkpoint_epoch_10.pth"
TEST_CSV = "annotation_v2/labels_test.csv"
IMAGES_DIR = "images_resized512"

NUM_CLASSES = {
    "sub_category": 2,
    "category": 16,
    "garment_type": 4,
    "construction_type": 4,
    "length_type": 6,
    "color_primary": 15,
    "pattern": 5,
    "sub_class": 10
}

# Load checkpoint
checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
encoders = checkpoint["encoders"]
LABELS = {k: list(v.keys()) for k, v in encoders.items()}

# Transform
transform = transforms.Compose([
    transforms.Resize(550),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Model
class MultiHeadFashionModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = timm.create_model("efficientnet_b3", pretrained=False, num_classes=0)
        feat = self.backbone.num_features
        self.heads = torch.nn.ModuleDict({
            k: torch.nn.Linear(feat, NUM_CLASSES[k]) for k in NUM_CLASSES
        })

    def forward(self, x):
        feat = self.backbone(x)
        return {k: h(feat) for k, h in self.heads.items()}

model = MultiHeadFashionModel().to(DEVICE)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

def predict_single(image_path):
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
        print(f"Error: {image_path}: {e}")
        return None

def evaluate():
    df = pd.read_csv(TEST_CSV)
    print(f"Testing on {len(df)} samples")
    
    metrics = {head: {"correct": 0, "total": 0} for head in LABELS.keys()}
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        image_path = os.path.join(IMAGES_DIR, row['file_path'])
        
        if not os.path.exists(image_path):
            continue
            
        pred = predict_single(image_path)
        if pred is None:
            continue
            
        for head in LABELS.keys():
            if head in row and pd.notna(row[head]):
                ground_truth = row[head]
                predicted = pred[head]
                
                metrics[head]["total"] += 1
                if predicted == ground_truth:
                    metrics[head]["correct"] += 1
    
    print("\n" + "="*50)
    print("ACCURACY RESULTS")
    print("="*50)
    
    for head, metric in metrics.items():
        if metric["total"] > 0:
            acc = metric["correct"] / metric["total"]
            print(f"{head:<18}: {acc:.3f} ({metric['correct']}/{metric['total']})")
    
    print("="*50)

if __name__ == "__main__":
    evaluate()