from tensorflow.keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

(x_train, y_train), (x_test, y_test) = mnist.load_data()

train_datagen = ImageDataGenerator(
    horizontal_flip=True,
    # vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5,
    zoom_range=0.1,
    # shear_range=0.7,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator()



################################### 스케일링 ######################################
from sklearn.preprocessing import MinMaxScaler, StandardScaler
x_train1 = x_train.reshape((x_train.shape[0]), (x_train.shape[1])*(x_train.shape[2]))
x_test1 = x_test.reshape((x_test.shape[0]), (x_test.shape[1])*(x_test.shape[2]))

scaler = MinMaxScaler()
x_train1 = scaler.fit_transform(x_train1)
x_test1 = scaler.transform(x_test1)

x_train = x_train1.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
x_test = x_test1.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

###################################################################################


augument_size = 40000 # 증폭
randindx = np.random.randint(x_train.shape[0], size = augument_size)
# print(randindx,randindx.shape) # (40000,)
# print(np.max(randindx), np.min(randindx)) # 59997 2
# print(type(randindx)) # <class 'numpy.ndarray'>

x_augumented = x_train[randindx].copy()
# print(x_augumented,x_augumented.shape) # (40000, 28, 28, 1)
y_augumented = y_train[randindx].copy()
# print(y_augumented,y_augumented.shape) # (40000,)

# x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
# x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
# x_augumented = x_augumented.reshape(x_augumented.shape[0], 
#                                     x_augumented.shape[1], x_augumented.shape[2], 1)

x_augumented = train_datagen.flow(x_augumented, y_augumented,
                                  batch_size=augument_size,
                                  shuffle=False).next()[0]
# print(x_augumented[0][1])

x_train = np.concatenate((x_train, x_augumented))
y_train = np.concatenate((y_train, y_augumented))



xy_train = test_datagen.flow(x_train, y_train,
                                  batch_size=100000,
                                  shuffle=False)  


np.save('d:/study_data/_save/_npy/keras49_2_train_x.npy', arr=xy_train[0][0])
np.save('d:/study_data/_save/_npy/keras49_2_train_y.npy', arr=xy_train[0][1])
np.save('d:/study_data/_save/_npy/keras49_2_test_x.npy', arr=x_test)
np.save('d:/study_data/_save/_npy/keras49_2_test_y.npy', arr=y_test)