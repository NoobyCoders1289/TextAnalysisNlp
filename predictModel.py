import pandas as pd
import neattext.functions as nfx
import re
from keras.models import load_model
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import OneHotEncoder


# Function to clean text
def cleanText(text):
    text = text.lower()
    text = nfx.remove_userhandles(text)
    text = nfx.remove_emojis(text)
    text = nfx.remove_urls(text)
    text = re.sub("#[A-Za-z0-9_]+", "", text)  # removing hashtags
    text = re.sub(r'[0-9]', '', text)  # removing numbers
    text = re.sub(r'\n', ' ', text)
    text = nfx.remove_puncts(text)
    text = nfx.remove_special_characters(text)
    text = nfx.remove_multiple_spaces(text)
    text = text.strip()

    return text


# loading the data
data = pd.read_csv(r"RapidApp\\static\\cleaned_data.csv")

X = pd.DataFrame(data['clean_text'])  # type: ignore
y = data[['label']]

# declaring the encoder
enc = OneHotEncoder()
Y = enc.fit_transform(y).toarray()

# removing stopwords from training data
stop_words = stopwords.words('english')
X['clean_text'] = X['clean_text'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# fitting the tokenizer on training data
tweets = X.clean_text.values
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(tweets)
encoded_docs = tokenizer.texts_to_sequences(tweets)
padded_sequence = pad_sequences(encoded_docs, maxlen=200)

# loading the model
model = load_model(r'RapidApp\\static\\Model_Date_Time_2022_03_09__14_05_39_Test_accuracy_76.32.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# method for predicting sentiment
def predict_sentiment(text):
    tw = tokenizer.texts_to_sequences([text])
    tw = pad_sequences(tw, maxlen=200)
    prediction = model.predict(tw)
    return prediction


def get_accuracy(y_test, y_pred):
    cm = pd.DataFrame(index=[0, 1], columns=[0, 1])

    for i in range(2):
        for j in range(2):
            cm[i][j] = 0
    for i in range(len(y_pred)):
        cm[y_test[i].argmax()][y_pred[i].argmax()] += 1

    true = cm[0][0] + cm[1][1]
    false = cm[0][1] + cm[1][0]

    accuracy = round((true / (false + true)) * 100, 2)  # type: ignore
    return accuracy


# -------------------------------------------------------------------------------------------------------------------------------------------------------#
"""
    testing on unseen data
    0 is negative after onehot encoding
    1 is positive
    give path to the file you want to predict sentiment on
"""
df = pd.read_csv(r"RapidApp\\static\\test_data.csv")

# data preprocessing
df = df.dropna()
df.loc[(df.label == 0.0), 'label'] = 1
df['predicted_labels'] = None
df['clean_text'] = df['text'].apply(cleanText)

# predicting for new data
x_test = df.clean_text.values
x_test = tokenizer.texts_to_sequences(x_test)
x_test = pad_sequences(x_test, maxlen=200)
y_pred = model.predict(x_test)
y_test = df[['label']]
y_test = enc.transform(y_test).toarray()  # type: ignore
df['predicted_labels'] = [i.argmax() for i in y_pred]
df.loc[(df.predicted_labels == 0), 'predicted_labels'] = -1

# give path where you want to save updated data
df.to_csv(r"RapidApp\\static\\predicted.csv", index=False)

# printing accuracy on current dataset
# print(get_accuracy(y_test,y_pred))
