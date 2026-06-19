"""Inference service. Loads the trained EfficientNet checkpoint and
performs single-image classification with top-k probabilities.

The model is loaded lazily and cached. If no checkpoint is present, the
service raises a clear error so the API surfaces a 503 rather than crashing.
"""
import json
import os
from typing import List, Dict

import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b0

from app.core.config import settings


class InferenceService:
    def __init__(self) -> None:
        self._model = None
        self._classes: List[str] = []
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._transform = transforms.Compose([
            transforms.Resize((settings.MODEL_INPUT_SIZE, settings.MODEL_INPUT_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

    @property
    def is_ready(self) -> bool:
        return self._model is not None

    def load(self) -> None:
        if self._model is not None:
            return
        if not os.path.exists(settings.MODEL_PATH):
            raise FileNotFoundError(
                f"Model checkpoint not found at {settings.MODEL_PATH}. "
                "Train the model first (see ml/training/train.py)."
            )
        if not os.path.exists(settings.CLASS_INDEX_PATH):
            raise FileNotFoundError(
                f"Class index not found at {settings.CLASS_INDEX_PATH}."
            )

        with open(settings.CLASS_INDEX_PATH) as f:
            # stored as {index: label}
            class_map: Dict[str, str] = json.load(f)
        self._classes = [class_map[str(i)] for i in range(len(class_map))]

        model = efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = torch.nn.Linear(in_features, len(self._classes))
        state = torch.load(settings.MODEL_PATH, map_location=self._device)
        model.load_state_dict(state)
        model.eval().to(self._device)
        self._model = model

    @torch.inference_mode()
    def predict(self, image: Image.Image, top_k: int = 3) -> Dict:
        if self._model is None:
            self.load()
        tensor = self._transform(image.convert("RGB")).unsqueeze(0).to(self._device)
        logits = self._model(tensor)
        probs = F.softmax(logits, dim=1)[0]
        k = min(top_k, len(self._classes))
        values, indices = torch.topk(probs, k)
        top = [
            {"label": self._classes[int(idx)], "confidence": float(val)}
            for val, idx in zip(values, indices)
        ]
        return {
            "predicted_label": top[0]["label"],
            "confidence": top[0]["confidence"],
            "top_k": top,
        }


inference_service = InferenceService()
