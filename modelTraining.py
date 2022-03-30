import pandas as pd
import numpy as np
import tensorflow
import datetime as dt

from sklearn.preprocessing import OneHotEncoder

# Reading cleaned data csv file
cleaned_data_path = ''
data = pd.read_csv(cleaned_data_path)

# Assigning x and y values from data

X = pd.DataFrame(data['clean_text'])
y = data[['label']]

print(f'the y value count : {y.value_counts()}')

# one-hot encoding for y
encoder = OneHotEncoder()
Y = encoder.fit_transform(y).toarray()

# Assigning values of X to var

tweets = X.clean_text.values

# word embedding the array of tweets
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from keras.layers import Embedding
from keras.models import load_model

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(tweets)
vocab_size = len(tokenizer.word_index) + 1
encoded_docs = tokenizer.texts_to_sequences(tweets)
padded_sequence = pad_sequences(encoded_docs, maxlen=200)

# Splitting data to train and test
x_train, x_test, y_train, y_test = train_test_split(padded_sequence, Y, random_state=0)

# model Initializing
np.random.seed(4)
tensorflow.compat.v1.set_random_seed(4)

embedding_vector_length = 32
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(2, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print(f'model summary: {model.summary()}')

# model Training
history = model.fit(x_train, y_train, epochs=6, batch_size=32, validation_split=0.2)

# predict for test data
y_pred = model.predict(x_test)

# Calculating accuracy score and confusion matrix
cm = pd.DataFrame(index=[0, 1], columns=[0, 1])
for i in range(2):
    for j in range(2):
        cm[i][j] = 0
for i in range(len(y_pred)):
    cm[y_test[i].argmax()][y_pred[i].argmax()] += 1
true = cm[0][0] + cm[1][1]
false = cm[0][1] + cm[1][0]

accuracy = round((true / (false + true)) * 100, 2)
print(f'Accuracy on test set = {str(accuracy)}')
print(f'confusion matrix : \n cm')

# saving trained model for future use
date_time_format = '%Y_%m_%d__%H_%M_%S'
current_date_time_dt = dt.datetime.now()
current_date_time_string = dt.datetime.strftime(current_date_time_dt, date_time_format)
model_name = f'static\\Model_Date_Time_{current_date_time_string}_Test_accuracy_{accuracy}.h5'
# Saving your Model
model.save(model_name)

# loading the saved model
model = load_model(r'static\\Model_Date_Time_2022_03_09__14_05_39_Test_accuracy_76.32.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# prediction function
def predict_sentiment(text):
    tw = tokenizer.texts_to_sequences([text])
    tw = pad_sequences(tw, maxlen=200)
    prediction = model.predict(tw)
    # print("Predicted label: ", prediction)
    if prediction[0][1] > prediction[0][0]:
        print('Positive Review')
        # return 1
    else:
        print('Negative Review')
        # return -1


# sample tests:
# test_sentence1 = "ukraine and russia are fighting"
# predict_sentiment(test_sentence1)
#
# test_sentence2 = "this movie was nice"
# predict_sentiment(test_sentence2)
#
# test_sentence3 = "the customer service is extremely bad.called multiple times but still no response"
# predict_sentiment(test_sentence3)
