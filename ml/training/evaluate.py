"""Evaluate a trained checkpoint on the validation/test split.

Produces overall accuracy and a per-class report. Used to populate
Chapter 5 (Results & Evaluation) of the final report.

Usage:
    python ml/training/evaluate.py --data-dir ml/data --split val
"""
import argparse
import json
import os
from collections import defaultdict

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import efficientnet_b0

INPUT_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", default="ml/data")
    p.add_argument("--split", default="val")
    p.add_argument("--model-dir", default="ml/saved_models")
    args = p.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tf = transforms.Compose([
        transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD),
    ])
    ds = datasets.ImageFolder(os.path.join(args.data_dir, args.split), tf)
    loader = DataLoader(ds, batch_size=32, shuffle=False, num_workers=2)

    with open(os.path.join(args.model_dir, "class_index.json")) as f:
        class_map = json.load(f)
    classes = [class_map[str(i)] for i in range(len(class_map))]

    model = efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(in_features, len(classes))
    model.load_state_dict(torch.load(os.path.join(args.model_dir, "leafguard_efficientnet.pt"), map_location=device))
    model.eval().to(device)

    per_class_correct = defaultdict(int)
    per_class_total = defaultdict(int)
    correct = total = 0
    with torch.inference_mode():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            preds = model(x).argmax(dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)
            for t, pr in zip(y.tolist(), preds.tolist()):
                per_class_total[t] += 1
                if t == pr:
                    per_class_correct[t] += 1

    print(f"Overall accuracy: {correct / total:.4f}  ({correct}/{total})")
    print("\nPer-class accuracy:")
    for i, name in enumerate(classes):
        tot = per_class_total[i]
        acc = per_class_correct[i] / tot if tot else 0.0
        print(f"  {name:35s} {acc:.4f}  (n={tot})")


if __name__ == "__main__":
    main()
