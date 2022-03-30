# Importing Modules
from datetime import date
import json
import os
import random
import re
# Hide warnings
import warnings

import neattext as nfx
import pandas as pd
from configparser import ConfigParser

warnings.filterwarnings('ignore')


def appost_remove(text):
    appost_path = config['path']['static_jsonfiles']
    with open(os.path.join(appost_path, 'contractions.json'), 'r+') as file:
        contraction_dict = json.load(file)

    tokens = str(text).lower().replace('’', "'").replace('…', ' ').split()
    token_lis = []
    for token in tokens:
        for key, value in contraction_dict.items():
            if token == key or token == key.replace("'", ""):
                token = contraction_dict[key]
        token_lis.append(token)
    text = ' '.join(token_lis)
    return text


def cleanTxt(text):
    text = text.lower()
    text = nfx.remove_userhandles(text)
    text = nfx.remove_emojis(text)
    text = nfx.remove_urls(text)
    text = re.sub(r'#', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'&amp', '&', text)
    text = nfx.remove_stopwords(text)
    text = nfx.remove_puncts(text)
    text = nfx.remove_special_characters(text)
    text = nfx.remove_numbers(text)
    text = nfx.remove_multiple_spaces(text)
    text = text.strip()

    return text


# LOADING DATA SET
def load_data(path):
    df = pd.read_csv(os.path.join(path, 'testdata/labeledtest1.csv'))
    print("a: ", df.shape)
    df.dropna(subset=['tweet'], inplace=True)
    print(f"duplicated count: {df[df.duplicated()].shape}")
    df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True,
                       ignore_index=True)
    print("b: ", df.shape)
    df['clean_text'] = df['tweet'].apply(appost_remove)
    df['clean_text'] = df['clean_text'].apply(cleanTxt)
    # --------------------------------
    today = date.today()
    d1 = today.strftime("%d_%m_%Y")
    # ---------------------------------
    # print(os.path.join(path,f'CleanedData{d1}.csv'))
    df.to_csv(os.path.join(path, f'cleandata/CleanedData{d1}.csv'), index=False)


if __name__ == '__main__':
    config_path = os.path.join(os.getcwd(), 'config.ini')
    # file = r'H:\\MyLearningProjects\\PythonProjects\\TextAnalysisNlp\\config.ini'
    config = ConfigParser()
    config.read(config_path)
    path = config['path']['static_csvfiles']
    print(path)
    load_data(path)
