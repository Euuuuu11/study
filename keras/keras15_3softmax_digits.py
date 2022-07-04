import numpy as np
from sklearn.datasets import load_wine, load_digits
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential   
from tensorflow.python.keras.layers import Dense

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

#2. 모델구성
model = Sequential()
model.add(Dense(100, input_dim=64,activation='relu'))
model.add(Dense(80))
model.add(Dense(50,activation='relu'))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(10, activation='softmax'))

#3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])

from tensorflow.python.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', patience=400, mode='min', 
              verbose=1, restore_best_weights=True) 

model.fit(x_train, y_train,
          epochs=500, batch_size=32,validation_split=0.2,
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

# loss :  0.12647540867328644
# acc스코어 :  0.9694444444444444































