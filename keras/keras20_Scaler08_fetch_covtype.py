import numpy as np
from sklearn.datasets import fetch_covtype
from tensorflow.python.keras.models import Sequential   
from tensorflow.python.keras.layers import Dense
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler


#1. 데이터
datasets = fetch_covtype()
x = datasets.data
y = datasets.target
print(x.shape,y.shape) # (581012, 54) (581012,)
print(np.unique(y, return_counts=True))    # [1 2 3 4 5 6 7]
# (array([1, 2, 3, 4, 5, 6, 7]),
# array([211840, 283301,  35754,   2747,   9493,  17367,  20510],
# dtype=int64))
#1. tensorflow의 to_categorical
# from tensorflow.keras.utils import to_categorical
# y = to_categorical(y) #categorical은 앞에 0부터 시작 그래서 8로 나옴

#2. pandas의 get_dummies
y=pd.get_dummies(y)
# print(y.shape)  # (581012, 7)
x_train, x_test, y_train, y_test = train_test_split(x,y,
             train_size=0.8, shuffle=True, random_state=66)

# scaler = MinMaxScaler()
# scaler = StandardScaler()
scaler = MaxAbsScaler()
# scaler = RobustScaler()

scaler.fit(x_train)
print(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)


#2. 모델구성
model = Sequential()
model.add(Dense(100, input_dim=54,activation='relu'))
model.add(Dense(90))
model.add(Dense(60,activation='relu'))
model.add(Dense(60))
model.add(Dense(10))
model.add(Dense(7, activation='softmax'))

#3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])

from tensorflow.python.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', patience=100, mode='min', 
              verbose=1, restore_best_weights=True) 

model.fit(x_train, y_train,
          epochs=55, batch_size=100,validation_split=0.2,
          verbose=1, callbacks=[es])

#4. 평가,예측
result = model.evaluate(x_test,y_test)
print("loss : ", result[0])
print("accuracy : ", result[1])

print("============================================") 
from sklearn.metrics import accuracy_score
y_predict = model.predict(x_test)
y_predict = tf.argmax(y_predict,axis=1)
y_test = tf.argmax(y_test,axis=1)

# from sklearn.metrics import accuracy_score
# y_predict = model.predict(x_test)
# # print(y_predict.shape)
# y_predict = np.argmax(y_predict, axis=1)
# y_test = np.argmax(y_test, axis=1)

acc = accuracy_score(y_test, y_predict)
print('acc스코어 : ', acc)

#1. 스케일러 하기 전
#  loss :  0.4399690330028534
#  acc스코어 :  0.8155727476915398

#2. MinMaxScaler 
# loss :   0.25421804189682007
# acc스코어 : 0.8962161045756134

#3. StandardScaler  
# loss :  0.2370000034570694
# acc스코어 :   0.9066633391564761

#4. MaxAbsScaler 
# loss :  0.2800651490688324
# acc스코어 :   0.8863024190425376

#5. RobustScaler 
#  loss :  
#  acc스코어 :  
