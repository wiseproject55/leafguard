"""Train an EfficientNet-B0 crop-disease classifier.

Expected data layout (ImageFolder convention):
    ml/data/train/<class_label>/*.jpg
    ml/data/val/<class_label>/*.jpg

Class labels should match the PlantVillage convention (Crop___Condition)
so they align with the seeded catalog in app.db.seed.

Usage:
    python ml/training/train.py --data-dir ml/data --epochs 10 --batch-size 32

Outputs:
    ml/saved_models/leafguard_efficientnet.pt   (state_dict)
    ml/saved_models/class_index.json            ({index: label})
"""
import argparse
import json
import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import EfficientNet_B0_Weights, efficientnet_b0

INPUT_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


def build_loaders(data_dir: str, batch_size: int):
    train_tf = transforms.Compose([
        transforms.RandomResizedCrop(INPUT_SIZE, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(MEAN, STD),
    ])
    train_ds = datasets.ImageFolder(os.path.join(data_dir, "train"), train_tf)
    val_ds = datasets.ImageFolder(os.path.join(data_dir, "val"), val_tf)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=2)
    return train_loader, val_loader, train_ds.classes


def build_model(num_classes: int):
    model = efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


def evaluate(model, loader, device):
    model.eval()
    correct = total = 0
    with torch.inference_mode():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            preds = model(x).argmax(dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)
    return correct / total if total else 0.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", default="ml/data")
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--out-dir", default="ml/saved_models")
    args = p.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader, classes = build_loaders(args.data_dir, args.batch_size)
    print(f"Device: {device} | classes: {len(classes)}")

    model = build_model(len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    os.makedirs(args.out_dir, exist_ok=True)
    best_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        model.train()
        running = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            loss = criterion(model(x), y)
            loss.backward()
            optimizer.step()
            running += loss.item() * x.size(0)
        scheduler.step()
        train_loss = running / len(train_loader.dataset)
        val_acc = evaluate(model, val_loader, device)
        print(f"Epoch {epoch}/{args.epochs} | loss {train_loss:.4f} | val_acc {val_acc:.4f}")

        if val_acc >= best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), os.path.join(args.out_dir, "leafguard_efficientnet.pt"))
            with open(os.path.join(args.out_dir, "class_index.json"), "w") as f:
                json.dump({str(i): c for i, c in enumerate(classes)}, f, indent=2)

    print(f"Best val accuracy: {best_acc:.4f}")


if __name__ == "__main__":
    main()
