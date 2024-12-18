import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms

import os

class IntelCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(512, 1024, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(1024, 1024, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            
            nn.Flatten(),
            nn.Linear(1024*8*8, 512),
            nn.ReLU(),
            nn.Linear(512, 64),
            nn.ReLU(),
            nn.Linear(64, 6)
        )
    
    def forward(self, image):
        output = self.model(image)
        return output

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")

# Define paths relative to the module's base directory
BASE_DATA_DIR = os.path.join(SAMPLES_DIR, "data")
BASE_MODELS_DIR = os.path.join(SAMPLES_DIR, "models")


models_dict = {
    "intel": {
        "model": IntelCNN(),
        "num_classes": 6,
        "transform": transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Resize((64, 64))
                    ]),
    },
    "emotions": {
        "model": models.resnet18(pretrained=True),
        "num_classes": 7,
        "transform": transforms.Compose([
                        transforms.ToTensor(),
                        transforms.Resize((224, 224)),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                    ]),
    }
}

def get_sample_model(key):
    model_dict = models_dict[key]

    return model_dict["model"], model_dict["num_classes"], model_dict["transform"]
