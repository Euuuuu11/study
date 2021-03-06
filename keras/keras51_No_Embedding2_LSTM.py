from keras.preprocessing.text import Tokenizer
import numpy as np

#1. 데이터
docs = ['너무 재밋어요', '참 최고에요', '참 잘 만든 영화에요',
        '추천하고 싶은 영화입니다.', '한 번 더 보고 싶네요', '글세요',
        '별로에요', '생각보다 지루해요', '연기가 어색해요',
        '재미없어요', '너무 재미없다', '참 재밋네요', '민수가 못 생기긴 했어요',
        '안결 혼해요']
a = ['나는 형권이가 정말 재미없다 너무 정말']

# 긍정 1, 부정 0
labels = np.array([1,1,1,1,1,0,0,0,0,0,0,1,1,0])        # (14, )


token = Tokenizer()
token.fit_on_texts(docs)
# print(token.word_index)
# {'참': 1, '너무': 2, '재밋어요': 3, '최고에요': 4, '잘': 5, '만든': 6, '영화에요': 7, '추천하고': 8, '싶은': 9,
#  '영화입니다': 10, '한': 11, '번': 12, '더': 13, '보고': 14, '싶네요': 15, '글세요': 16, '별로
# 에요': 17, '생각보다': 18, '지루해요': 19, '연기가': 20, '어색해요': 21, '재미없어요': 22, '재미없다': 23, '재밋네요': 24,
# '민수가': 25, '못': 26, '생기긴': 27, '했어요': 28, '안결': 29, '혼해요': 30}  
token.fit_on_texts(a)
print(token.word_index)

x = token.texts_to_sequences(docs)
b = token.texts_to_sequences(a) 
# print(x)
# [[2, 3], [1, 4], [1, 5, 6, 7], [8, 9, 10], [11, 12, 13, 14, 15], [16], [17], 
# [18, 19], [20, 21], [22], [2, 23], [1, 24], [25, 26, 27, 28], [29, 30]]
print(b)


from keras.preprocessing.sequence import pad_sequences
# 앞에 0을 채워주는게 더 효율적이다.
pad_x = pad_sequences(x, padding='pre', maxlen=5)       # pre 앞 post 뒤
pad_b = pad_sequences(b, padding='pre', maxlen=4, truncating='post')
pad_b = pad_sequences(pad_b, padding='pre', maxlen=5)       
print(pad_x)
print(pad_x.shape)      # (14, 5)
print(pad_b)
print(pad_b.shape)      # (21, 5)
pad_x = pad_x.reshape(14,5,1)
pad_b = pad_b.reshape(1,5,1)

word_size = len(token.word_index)
print("word_size :", word_size) # 단어사전의 개수 : 30

print(np.unique(pad_x, return_counts=True))
# (array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
#        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
from tensorflow.python.keras.utils.np_utils import to_categorical

#2. 모델 구성
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, LSTM, Embedding

model = Sequential()            # input (14, 5)
                   # 단어사전의 개수                
# model.add(Embedding(input_dim=30, output_dim=11, input_length=5))     # Embedding layer는  input_length 알아서 잡아준다. output_dim 개수는 상관없다.
# model.add(Embedding(31, 10, 5))       # error
# model.add(Embedding(31, 10, input_length=5))
# model.add(Embedding(input_dim=30, output_dim=10))
# model.add(Embedding(34,10))
model.add(LSTM(32, input_shape=(5,1)))
model.add(Dense(32, input_shape=(5,)))
model.add(Dense(1, activation='sigmoid'))
# model.summary()


#3. 컴파일, 훈련
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
model.fit(pad_x,labels, epochs=20, batch_size=16)

#4. 평가, 예측
acc = model.evaluate(pad_x, labels)[1]
print('acc : ', acc)

######### 실습 ########
x_predict = model.predict(pad_b)
print(x_predict[-1])
# 결과는 ? 긍정? 부정 ?
