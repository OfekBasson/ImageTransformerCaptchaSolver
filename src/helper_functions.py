import numpy as np
import matplotlib.pyplot as plt

def imageShow(img):
    img = img / 2 + 0.5
    imageAsRGBNumpyArray = img.numpy()[:3,:,:]
    plt.imshow(np.transpose(imageAsRGBNumpyArray, (1, 2, 0)))

data_types = ['loss', 'acc']

def graphShow(model):
    for i in range(2):
        plt.subplot(1, 2, i+1)
        train_data_list = [x for x in model.data_tracking_for_visualization['train'][data_types[i]]]
        val_data_list = [x for x in model.data_tracking_for_visualization['val'][data_types[i]]]

        plt.plot(train_data_list, label='train')
        plt.plot(val_data_list, label='val')
        plt.title(f'{data_types[i]} as a function ot epochs')
    plt.show()


