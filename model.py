"""Exact ResidualSteelCNN architecture from steel_defect.ipynb (CPU-compatible)."""
from pathlib import Path

import torch
from torch import nn
from torchvision import transforms
from PIL import Image

CLASS_CODES = ["Cr", "In", "PS", "Pa", "RS", "Sc"]
CLASS_INFO = {
    "Cr": {"en": "Crazing", "description": "Fine, interconnected cracks across the surface."},
    "In": {"en": "Inclusion", "description": "Foreign material or irregular marks embedded in the surface."},
    "PS": {"en": "Pitted Surface", "description": "Small pits and indentations across the surface."},
    "Pa": {"en": "Patches", "description": "Irregular areas with a visibly different texture."},
    "RS": {"en": "Rolled-in Scale", "description": "Scale marks pressed into the steel during rolling."},
    "Sc": {"en": "Scratches", "description": "Linear marks or scratches on the steel surface."},
}



class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
        )
        self.relu = nn.ReLU()

    def forward(self, x):
        return self.relu(x + self.layers(x))


class ResidualSteelCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            ResidualBlock(32),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            ResidualBlock(64),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            ResidualBlock(128),
            nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(128, 6),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class SteelPredictor:
    def __init__(self, weights_path: Path):
        self.weights_path = weights_path
        self.device = torch.device("cpu")
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        self.model = None
        self.load_error = None
        self.load()

    def load(self):
        self.model = None
        self.load_error = None
        if not self.weights_path.is_file():
            self.load_error = "Model weights are missing. Place steel_residual_best.pth in the models folder."
            return
        try:
            model = ResidualSteelCNN().to(self.device)
            state = torch.load(str(self.weights_path), map_location=self.device, weights_only=True)
            model.load_state_dict(state, strict=True)
            model.eval()
            self.model = model
        except Exception as exc:
            self.load_error = f"Could not load model weights: {type(exc).__name__}: {exc}"

    @property
    def ready(self):
        return self.model is not None

    def predict(self, image: Image.Image) -> dict:
        if not self.ready:
            raise RuntimeError(self.load_error or "The model is not ready")
        tensor = self.transform(image.convert("L")).unsqueeze(0).to(self.device)
        with torch.inference_mode():
            logits = self.model(tensor)
            scores = torch.softmax(logits, dim=1)[0].cpu().tolist()
        best_idx = int(max(range(len(scores)), key=scores.__getitem__))
        code = CLASS_CODES[best_idx]
        return {
            "defect_code": code,
            "defect_english": CLASS_INFO[code]["en"],
            "description": CLASS_INFO[code]["description"],
            "confidence": round(scores[best_idx], 5),
            "probabilities": [
                {"code": c, "name_en": CLASS_INFO[c]["en"], "probability": round(scores[i], 5)}
                for i, c in enumerate(CLASS_CODES)
            ],
        }
