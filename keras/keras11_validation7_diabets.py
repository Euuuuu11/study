from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np  


datasets = load_diabetes()
x = datasets.data
y = datasets.target
x_train, x_test, y_train, y_test = train_test_split(x,y,
             train_size=0.8,random_state=72)


print(x)
print(y)
print(x.shape, y.shape) # (442, 10) (442, )

print(datasets.feature_names)    # ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
print(datasets.DESCR)   

#2. 모델구성
model = Sequential()
model.add(Dense(10, input_dim=10))
model.add(Dense(50))
model.add(Dense(40))
model.add(Dense(50))
model.add(Dense(60))
model.add(Dense(20))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(1))

#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=501,
          batch_size=15,validation_split=0.2)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)

y_predict = model.predict(x_test)

from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('r2스코어 : ', r2)

# [실습]
# R2 0.62 이상

# loss :  2119.338134765625
# r2스코어 :  0.6490527187925481

# validation 사용 후
# loss :  2177.955810546875
# r2스코어 :  0.6701675391497158
