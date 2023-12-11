import os
from PIL import Image
from torch.utils.data import Dataset, Subset
import random
import numpy as np


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
        label = self.parse_label(self.images[imageIndex])

        if self.transform:
            image = self.transform(image)

        return image, label

    def parse_label(self, img_name):
        label = img_name.split('_')[0]
        return label
    
    def split_dataset(self, train_size=0.8, shuffle=True):
        train_len = int(train_size * len(self))

        indices = list(range(len(self)))
        if shuffle:
            random.shuffle(indices)

        train_indices = indices[:train_len]
        test_indices = indices[train_len:]

        train_subset = Subset(self, train_indices)
        test_subset = Subset(self, test_indices)

        return train_subset, test_subset




 