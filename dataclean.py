# Importing Modules
import json
import os
import re
# Hide warnings
import warnings

from dotenv import load_dotenv
import neattext as nfx
import pandas as pd

warnings.filterwarnings('ignore')
load_dotenv()


# -------------------------------------Replacing appost's in text with full words----------------------------------#
# def appost_removal(df, appost_dict):
#     def _get_contractions(appost_dict):
#         """
#         Parameters
#         ----------
#         appost_dict : object
#         """
#         contraction_re = re.compile('(%s)' % '|'.join(appost_dict.keys()))
#         return appost_dict, contraction_re
#
#     contractions, contractions_re = _get_contractions(appost_dict)
#
#     def replace_contractions(text):
#         text = text.lower()
#
#         def replace(match):
#             return contractions[match.group(0)]
#
#         return contractions_re.sub(replace, text.replace("’", "'"))
#
#     df['clean_text'] = df['tweet'].apply(replace_contractions)
#     return df

def appost_remove(text):
    with open(f'{os.getenv("STATIC_JSONFILES")}contractions.json', 'r+') as file:
        contraction_dict = json.load(file)

    tokens = text.lower().replace('’', "'").replace('…', ' ').split()
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
def load_data():
    df = pd.read_csv('static/csvfiles/newraw.csv')
    # print(df.shape)
    # df.dropna(inplace=True)
    # df.isnull().sum()
    print(df.shape)
    print(f"duplicated count: {df[df.duplicated()].shape}")
    df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True, ignore_index=False)
    # df.info()
    # with open('static/json_files/contractions.json', 'r+') as file:
    #     contraction_dict = json.load(file)
    # appost_removal(df, contraction_dict)
    df['clean_text'] = df['tweet'].apply(appost_remove)

    # print("-------------------------------------------------")
    # # print(df.shape)
    df['clean_text'] = df['clean_text'].apply(cleanTxt)
    # print(df[['tweet', 'clean_text']])
    # df['get_repliedTo_tweet_link'] = df.apply(
    #     lambda x: os.getenv('REPLIEDTWEET').format(x['replied_to_id']) if x['replied_to_id'] != 'Null' else 'null',
    #     axis=1)
    # df['get_tweet_link'] = df.apply(lambda x: os.getenv('TWEET').format(x['user_id'], x['tweet_id']), axis=1)
    # df.to_csv(f"{os.getenv('SCRATCH_CSVFILES')}start_22_03_23T05_21_end_2022_03_14_T18_49v2.csv", index=False)
    if 'dreamholiday' in df['clean_text']:
        df[df['label']] = 1
    df.to_csv('static/csvfiles/CleanedDatav3.csv', index=False)
    print("completed.............")


if __name__ == '__main__':
    load_data()
