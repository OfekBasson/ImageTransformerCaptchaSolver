import os
from PIL import Image
from torch.utils.data import Dataset, Subset
import random


class CustomDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = [file for file in os.listdir(root_dir) if not file.startswith('.')] 

    def __len__(self):
        return len(self.images)

    def __getitem__(self, imageIndex):
        img_name = os.path.join(self.root_dir, self.images[imageIndex])
        image = Image.open(img_name)
        label = self.parse_label(self.images[imageIndex])

        if self.transform:
            image = self.transform(image)

        return image, label

    def parse_label(self, img_name):
        label = img_name.split('_')[0]
        return label
    
    def split_dataset(self, trainSize=0.8, shuffle=True):
        trainLen = int(trainSize * len(self))
        testAndValLen = (len(self) - trainLen) / 2

        indices = list(range(len(self)))
        if shuffle:
            random.shuffle(indices)

        trainIndices = indices[:trainLen]
        testIndices = indices[trainLen:int(trainLen + testAndValLen)]
        valIndices = indices[int(trainLen + testAndValLen):]

        trainSubset = Subset(self, trainIndices)
        testSubset = Subset(self, testIndices)
        valSubset = Subset(self, valIndices)

        return trainSubset, valSubset, testSubset




 