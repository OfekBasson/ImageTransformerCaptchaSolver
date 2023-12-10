import os
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = os.listdir(root_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, imageIndex):
        img_name = os.path.join(self.root_dir, self.images[imageIndex])
        image = Image.open(img_name)
        label = self.parse_label(self.images[imageIndex])  # You need to define this function

        if self.transform:
            image = self.transform(image)

        return image, label

    def parse_label(self, img_name):
        label = img_name.split('_')[0]
        return label


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

 