from glob import glob
import os

import pandas as pd

from configparser import ConfigParser


def joincsv(path):
    """
        Function to join 2 or more csv files to single file
        parameters
        ["TweetsData*.csv", 'CleanedDatav*.csv', '49*.csv']
    """
    # fileexe = '49*.csv'
    # # path to the folder/

    folder_path = os.path.join(path, 'link\\*.csv')
    
    # list of all files_path present in path folder
    files_list = glob(folder_path)
    # print(files_list)
    # files_list = [os.path.join(path, 'start_22_03_10T00_00_end_2022_03_24_T20_49.csv'),
                #   os.path.join(path, 'lookup.csv'),
                #   os.path.join(path, 'start_22_03_23T05_21_end_2022_03_14_T18_49v2.csv')]

    # Joining csv files with concat, map
    # converting all csv data to DataFrame with !read_csv
    df = pd.concat(map(pd.read_csv, files_list), ignore_index=True)
    # df.drop(columns='Unnamed: 0')
    df.info()
    # # Removing Duplicate records
    # # -----
    print("Before drop_duplicates: ", df.shape)
    # # df2 = df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True, ignore_index=True)
    # # print("No of duplicated rows :", df2.shape)

    df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True, ignore_index=True)
    print("After drop_duplicates: ", df.shape)

    # # writing to new single Csv file
    df.to_csv(os.path.join(path, 'final_link.csv'),index=False)
    # print('completed')


if __name__ == "__main__":
    # ConfigParse Parses the config file
    file = r'H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\config.ini'
    config = ConfigParser()
    config.read(file)
    # path = r"H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\static\\csv_files\\"
    path = config['path']['scratch_csvfiles']
    # print(path)
    joincsv(path)
