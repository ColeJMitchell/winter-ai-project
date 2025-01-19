import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import models, transforms, datasets

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet152(weights=models.ResNet152_Weights.DEFAULT).to(device)
    for name, param in model.named_parameters():
        if "layer4" not in name and "fc" not in name:  
            param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, 13).to(device)
    data_path = "training_data"
    transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406) ,(0.229, 0.224, 0.225))
    ])
    data_folder = datasets.ImageFolder(data_path, transform=transform)
    data_loader = DataLoader(data_folder, batch_size=32, shuffle=True)
    loss = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=.001)
    model.train()
    for epoch in range(10):
        running_loss = 0.0
        for i,(data, label) in enumerate(data_loader):
            data, label = data.to(device), label.to(device)
            optimizer.zero_grad()
            output = model(data)
            val_loss = loss(output, label)
            running_loss += val_loss.item()
            val_loss.backward()
            optimizer.step()
            if i % 100 == 0:   
                print(f'[batch {i + 1}] Loss: {running_loss / 100:.3f}')
                running_loss = 0.0
    with torch.no_grad():
        correct = 0
        total = 0
        for data, label in data_loader:
            data, label = data.to(device), label.to(device)
            output = model(data)
            _, predicted = torch.max(output.data, 1)
            total += label.size(0)
            correct += (predicted == label).sum().item()
        print(f'Accuracy of the network on the training images: {100 * correct / total}%')
    torch.save(model.state_dict(), 'transfer_learning_model.pth')


if __name__ == "__main__":
    main()