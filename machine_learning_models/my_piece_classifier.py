import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F

class chessAi(nn.Module):
    def __init__(self):
        super(chessAi, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.bn2 = nn.BatchNorm2d(32)
        self.bn3 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(2, 2)
        self.linear2 = nn.Linear(64 * 15 * 15, 120)
        self.linear3 = nn.Linear(120, 84)
        self.linear4 = nn.Linear(84, 13)
    
    def forward(self, x):
        x = self.maxpool(F.relu(self.bn1(self.conv1(x))))
        x = self.maxpool(F.relu(self.bn2(self.conv2(x))))
        x = self.maxpool(F.relu(self.bn3(self.conv3(x))))
        x = F.relu(self.linear2(torch.flatten(x, 1)))
        x = F.relu(self.linear3(x))
        return self.linear4(x)
        
#Trains the convolutional neural network to classify chess pieces
def main():
    
    transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.RandomRotation(30),
    transforms.Resize((120, 120)),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    dataset = datasets.ImageFolder(root='training_data', transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = chessAi().to(device)
    loss = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(30):
        running_loss = 0.0
        for i, (data, label) in enumerate(dataloader):
            data, label = data.to(device), label.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss_val = loss(output, label)
            loss_val.backward()
            optimizer.step()
            running_loss += loss_val.item()
            if i % 100 == 0:   
                print(f'[Epoch {epoch + 1}, Batch {epoch}] Loss: {running_loss / 100:.3f}')
                running_loss = 0.0
    with torch.no_grad():
        correct = 0
        total = 0
        for data, label in dataloader:
            data, label = data.to(device), label.to(device)
            output = model(data)
            _, predicted = torch.max(output.data, 1)
            total += label.size(0)
            correct += (predicted == label).sum().item()
        print(f'Accuracy of the network on the training images: {100 * correct / total}%')
    print('Finished Training')
    torch.save(model.state_dict(), 'chess_piece_classifier.pth')
             

if __name__ == "__main__":
    main()