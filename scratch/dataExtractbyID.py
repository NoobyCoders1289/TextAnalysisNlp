import json
import os
import time

import pandas as pd
from configparser import ConfigParser
import requests
from dotenv import load_dotenv

load_dotenv()


class TwitterAPIData:
    """
    A class used to Extract Twitter Mentions Data.

    Attributes
    ----------
    urls : list
        list contains the url endpoints to call the API.
    next_token : dict
        dict contains the next_token (i.e, address to next page)
    params : dict
        dict contains the fields those needs to be extracted.
    json_data : list
        the list of dict's which contains formatted extracted tweets data in required form.
    json_response : dict
        dict contains the api endpoint json response.
    user_id : list
        list contains the Twitter user id's whose data to be collected.

    bearer_token : str
        str contains authentication token

    Methods
    -------
    create_url()

        It uses user_ids to creates API endpoints and stores in urls list.

    bearer_oauth()

        Method required by bearer token authentication.

    getting_next_page()

        Method to get next_token and pass it to api endpoints to get more data.

    connect_to_endpoint()

        It calls the Api endpoints and stores the response into json_response dict.

    join_json()

        It is used to extract and join the data in required format, stores into json_data list.

    write2csvFile()
        It is used to write json data to csv.

    """

    def __init__(self):
        """
        Attributes
        ----------
        urls : list
            list contains the url endpoints to call the API.
        params : dict
            dict contains the fields those needs to be extracted.
        json_data : list
            the list of dict's which contains formatted extracted tweets data in required form.
        json_response : dict
            dict contains the api endpoint json response.
        user_id : list
            list contains the Twitter user id's whose data to be collected.

        bearer_token : str
            str contains authentication token

        """
        """
            TWITTER ID |TWITTER USERNAME
            20678384   |@VodafoneUK
            15133627   |@O2
            158368965  |@ThreeUK
            361268597  |@ThreeUKSupport
            7117212    |@EE
            118750085  |@bt_uk
            17872077   |@virginmedia
        """

        self.urls = []
        self.json_data = []
        self.json_response = {}
        self.bearer_token = os.getenv('BEARER_TOKEN')

    def create_url(self, tweet_lis):
        """
        It uses user_ids to creates API endpoints and stores in urls list.
        """

        tweet_fields = "expansions=referenced_tweets.id,author_id&tweet.fields=id,author_id,created_at&user.fields=name,location,id,username"
        i = 0
        for ids in tweet_lis:
            i += 1
            if i:
                self.urls.append(f'https://api.twitter.com/2/tweets?ids={ids[:-1]}&{tweet_fields}')
        print("urls len: ", len(self.urls))


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserMentionsPython"
        return r

    def connect_to_endpoint(self, url):
        """
            It calls the Api endpoints and stores the response into json_response dict.
        """
        time.sleep(5)
        response = requests.request("GET", url, auth=self.bearer_oauth)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        self.json_response = response.json()
        if response.status_code == 200:
            self.write2csvfile()
        # return response.json()

    def join_json(self):
        """
            It is used to extract and join the data in required format, stores into json_data list.
        """

        def getDataframe(dic, tweet, user):
            dic['tweet_id'] = str(tweet['id'])
            dic['user_id'] = str(tweet['author_id'])
            dic['created_at'] = tweet['created_at']
            dic['tweet'] = tweet['text']
            dic['username'] = user['username']
            dic['name'] = user['name']
            if 'location' in user.keys():
                dic['location'] = user['location']
            else:
                dic['location'] = ""
            if 'referenced_tweets' in tweet.keys():
                dic['tweet_type'] = [r['type'] for r in tweet['referenced_tweets']][0]
                dic['replied_to_id'] = [r['id'] for r in tweet['referenced_tweets']][0]
            else:
                dic['tweet_type'] = "Original_tweet"
                dic['replied_to_id'] = "Null"

            return dic

        tweet_list = []
        for data in self.json_response['data']:
            tweet_dic = {}
            for user in self.json_response['includes']['users']:
                if data['author_id'] == user['id']:
                    tweet_dic = getDataframe(tweet_dic, data, user)
            tweet_list.append(tweet_dic)

        # ------------self.json_response['tweets'] vs self.json_response['users']----------#
        with open(os.getenv('COMAPANY_DATA'), 'r+', encoding='utf-8') as f:  # type: ignore
            telecom_ids = json.load(f)
        reply_tweet = []
        for tweet in self.json_response['includes']['tweets']:
            reply_dic = {}
            for user in self.json_response['includes']['users']:
                if user['id'] == tweet['author_id']:
                    reply_dic = getDataframe(reply_dic, tweet, user)

                elif tweet['author_id'] in telecom_ids.keys():
                    # ids = {'20678384':'Vodafone','7117212':'EE','118750085':'BT'}
                    reply_dic = getDataframe(reply_dic, tweet, telecom_ids[tweet['author_id']])
            reply_tweet.append(reply_dic)
        # ------------------------------------------------------------------------------------
        [self.json_data.append(j) or j for j in tweet_list]
        [self.json_data.append(k) or k for k in reply_tweet]
        print(f'len of tweet_list: {len(tweet_list)}')
        print(f'len of reply_tweet list in api call : {len(reply_tweet)}')
        print(f'len of final list : {len(self.json_data)}')
        return self.json_data

    def write2csvfile(self):
        data = self.join_json()
        df = pd.DataFrame(data)
        # df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True, ignore_index=True)
        df['get_repliedTo_tweet_link'] = df.apply(
            lambda x: f"https://twitter.com/i/web/status/{x['replied_to_id']}" if x['replied_to_id'] != 'Null' else 'null',
            axis=1)
        df['get_tweet_link'] = df.apply(lambda x: f"https://twitter.com/{x['user_id']}/status/{x['tweet_id']}", axis=1)
        df.to_csv(f"{os.getenv('SCRATCH_CSVFILES')}final_no_refered_2.csv", index=False)
        print("...........................................................")


def main():
    file = r'H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\config.ini'
    config = ConfigParser()
    config.read(file)
    path = config['path']['scratch_csvfiles']
    df = pd.read_csv(os.path.join(path, 'final_no_refered_type.csv'))
    tweet_ids = df['tweet_id'].to_list()
    n = 80
    final = [tweet_ids[i * n:(i + 1) * n] for i in range((len(tweet_ids) + n - 1) // n)]
    i = 0
    tweet_lis = []
    for tweet_id in final:
        sent = ''
        for idss in tweet_id:
            sent += str(idss) + ","
        tweet_lis.append(sent)
    # print(len(tweet_lis))

    apidata = TwitterAPIData()
    apidata.create_url(tweet_lis)
    i=1
    for url in apidata.urls:
        # print(url)
        print(i)
        i+=1
        apidata.connect_to_endpoint(url)



if __name__ == "__main__":
    main()
