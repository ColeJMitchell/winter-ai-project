
import cv2
import torch
import torchvision.transforms as transforms
from chess_piece_classifier import chessAi  

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = chessAi().to(device)
model.load_state_dict(torch.load('chess_piece_classifier.pth'), map_location="cpu")
model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((128, 128))
])

img = cv2.imread('training_data/black_bishop/1,1.jpg')  
img_tensor = transform(img).unsqueeze(0).to(device)  


with torch.no_grad():
    output = model(img_tensor)  
    predicted_class = torch.argmax(output, dim=1).item()  


class_names = ['white_pawn', 'black_pawn', 'white_knight', 'black_knight', 
               'white_bishop', 'black_bishop', 'white_rook', 'black_rook',
               'white_queen', 'black_queen', 'white_king', 'black_king', 'empty-square']
print(f'Predicted class: {class_names[predicted_class]}')