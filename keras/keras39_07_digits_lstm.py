import numpy as np
from sklearn.datasets import load_wine, load_digits
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential,  load_model
from tensorflow.python.keras.layers import Activation, Dense, Conv2D, Flatten, MaxPooling2D, Input, Dropout,LSTM
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler

#1. 데이터
datasets = load_digits()
x = datasets.data
y = datasets.target
print(x.shape,y.shape) # (1797, 64) (1797,)
print(np.unique(y,return_counts=True))    # [0 1 2 3 4 5 6 7 8 9]

# import matplotlib.pyplot as plt
# plt.gray()
# plt.matshow(datasets.images[1])
# plt.show()

from tensorflow.keras.utils import to_categorical
y = to_categorical(y)
# print(y.shape) # (1797, 10)

x_train, x_test, y_train, y_test = train_test_split(x,y,
             train_size=0.8, shuffle=True, random_state=66)

# scaler = MinMaxScaler()
# scaler = StandardScaler()
# scaler = MaxAbsScaler()
scaler = RobustScaler()

scaler.fit(x_train)
print(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(1437, 32, 2)
x_test = x_test.reshape(360, 32, 2)

#2. 모델구성
model = Sequential()
model.add(LSTM(170, return_sequences=True, activation= 'relu' ,input_shape = (32,2)))    
model.add(LSTM(90, return_sequences=False, activation = 'relu'))
model.add(Dense(60, activation = 'relu'))
model.add(Dense(20, activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(10))
model.summary()


#3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])

from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint
import datetime
# date= datetime.datetime.now()      # 2022-07-07 17:22:07.702644
# date = date.strftime("%m%d_%H%M")  # 0707_1723
# print(date)

# filepath = './_ModelCheckpoint/k26_7/'
# filename = '{epoch:04d}-{val_loss:.4f}.hdf5'


from tensorflow.python.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', patience=400, mode='min', 
              verbose=1, restore_best_weights=True) 
# mcp = ModelCheckpoint(monitor='val_loss', mode='auto',verbose=1,
#                       save_best_only=True,filepath= "".join([filepath,'k26_',date, '_', filename]))

model.fit(x_train, y_train,
          epochs=100, batch_size=32,validation_split=0.2,
          verbose=1, callbacks=[es])


#4. 평가,예측
result = model.evaluate(x_test,y_test)
print("loss : ", result[0])
print("accuracy : ", result[1])

print("============================================") 

from sklearn.metrics import accuracy_score
y_predict = model.predict(x_test)
y_predict = np.argmax(y_predict, axis=1)
y_test = np.argmax(y_test, axis=1)

acc = accuracy_score(y_test, y_predict)
print('acc스코어 : ', acc)

# dropout 적용 후 
# loss :  0.250651478767395
# acc스코어 :  0.9694444444444444

# loss :  9.58131217956543
# acc스코어 :  0.11388888888888889