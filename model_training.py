import torch
from torch.utils.data import random_split
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from utils import handle_errors, logger

# Define data transformations
data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Load dataset
data_dir = "data"
dataset = datasets.ImageFolder(data_dir, transform=data_transforms)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Initialize model
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, len(dataset.classes))

# Define loss and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

@handle_errors
def train_model(model, dataloaders, criterion, optimizer, num_epochs=10):
    for epoch in range(num_epochs):
        logger.info(f"Epoch {epoch + 1}/{num_epochs}")
        running_loss = 0.0
        for inputs, labels in dataloaders['train']:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        epoch_loss = running_loss / len(dataloaders['train'])
        logger.info(f"Training Loss: {epoch_loss:.4f}")
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in dataloaders['val']:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
        
        val_loss /= len(dataloaders['val'])
        logger.info(f"Validation Loss: {val_loss:.4f}")
        model.train()

    # Save the trained model
    model_path = "model.pth"
    torch.save(model.state_dict(), model_path)
    logger.info(f"Model training complete and saved to {model_path}")

dataloaders = {'train': train_loader, 'val': val_loader}
train_model(model, dataloaders, criterion, optimizer)
