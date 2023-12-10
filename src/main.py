#tests
##try/catch

from data_fetcher import DataFetcher
from dataset_creator import CustomDataset
import matplotlib.pyplot as plt
import numpy as np
import time


# df = DataFetcher()
# df.createDatabase()

def imshow(img):
    # img = img / 2 + 0.5     # unnormalize
    npimg = np.asarray(image)
    print(np.transpose(npimg, (0, 1, 2))[:,:3,:].shape)
    plt.imshow(np.transpose(npimg, (0, 1, 2))[:,:,:3])
    plt.show()

dataset = CustomDataset(root_dir='/Users/wpqbswn/Desktop/Ofek/8200-learning/NadlanCaptchaNumbersClassification/Data')

image, label = dataset[1]
imshow(image)
print(label)


# time.sleep(20)





        
    



