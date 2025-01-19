import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT).to(device)
model.fc = nn.Linear(model.fc.in_features, 13).to(device)
model.load_state_dict(torch.load('/home/cole/github/winter-ai-project/machine_learning_models/transfer_learning_model.pth'))

model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224))
])

img = cv2.imread('training_data/test.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
img_tensor = transform(img).unsqueeze(0).to(device)  


with torch.no_grad():
    output = model(img_tensor)  
    predicted_class = torch.argmax(output, dim=1).item()  


class_names = ['black_bishop', 'black_king', 'black_knight', 'black_pawn', 'black_queen', 'black_rook', 'empty_square', 'white_bishop', 'white_king', 'white_knight', 'white_pawn', 'white_queen', 'white_rook']
print(f'Predicted class: {class_names[predicted_class]}')