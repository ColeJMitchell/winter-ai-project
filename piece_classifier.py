import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader, ConcatDataset
import torch.nn.functional as F

class chessAi(nn.Module):
    def __init__(self):
        super(chessAi, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.maxpool = nn.MaxPool2d(2, 2)
        self.linear2 = nn.Linear(64 * 8 * 8, 120)
        self.linear3 = nn.Linear(120, 84)
        self.linear4 = nn.Linear(84, 13)
    
    def forward(self, x):
        x = self.maxpool(F.relu(self.conv1(x)))
        x = self.maxpool(F.relu(self.conv2(x)))
        x = self.maxpool(F.relu(self.conv3(x)))
        x = self.maxpool(self.conv3(x))
        x = F.relu(self.linear2(torch.flatten(x, 1)))
        x = F.relu(self.linear3(x))
        return self.linear4(x)
        
def main():
    
    transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((128, 128))
    ])

    dataset = []
    whitePawn = datasets.ImageFolder(root="training_data/white_pawn", transform=transform)
    whiteRook = datasets.ImageFolder(root="training_data/white_rook", transform=transform)
    whiteKnight = datasets.ImageFolder(root="training_data/white_knight", transform=transform)
    whiteBishop = datasets.ImageFolder(root="training_data/white_bishop", transform=transform)
    whiteQueen = datasets.ImageFolder(root="training_data/white_queen", transform=transform)
    whiteKing = datasets.ImageFolder(root="training_data/white_king", transform=transform)
    blackPawn = datasets.ImageFolder(root="training_data/black_pawn", transform=transform)
    blackRook = datasets.ImageFolder(root="training_data/black_rook", transform=transform)
    blackKnight = datasets.ImageFolder(root="training_data/black_knight", transform=transform)
    blackBishop = datasets.ImageFolder(root="training_data/black_bishop", transform=transform)
    blackQueen = datasets.ImageFolder(root="training_data/black_queen", transform=transform)
    blackKing = datasets.ImageFolder(root="training_data/black_king", transform=transform)
    emptySquare = datasets.ImageFolder(root="training_data/empty_square", transform=transform)
    dataset.extend([whitePawn, whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, blackPawn, blackRook, blackKnight, blackBishop, blackQueen, blackKing, emptySquare])
    dataset = ConcatDataset(dataset)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = chessAi().to(device)
    loss = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    
    for epoch in range(10):
        for i, (data, label) in enumerate(dataloader):
            data, label = data.to(device), label.to(device)
            optimizer.zero_grad()
            output = model(data)
            lossVal = loss(output, label)
            lossVal.backward()
            optimizer.step()
            unning_loss += loss.item()
            if i % 100 == 99:   
                print(f'[Epoch {epoch + 1}, Batch {i + 1}] Loss: {running_loss / 100:.3f}')
                running_loss = 0.0

    print('Finished Training')
    torch.save(model.state_dict(), 'chess_piece_classifier.pth')
             

if __name__ == "__main__":
    main()