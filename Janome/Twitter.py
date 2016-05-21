# coding:UTF-8

import configparser
import os
from requests_oauthlib import OAuth1Session
import json


class TwitterService :
    API_TIMELINE_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?"

    consumer_key = ""
    consumer_secret = ""
    access_token_key = ""
    access_token_secret = ""

    def __init__(self, file_path):
        print("設定ファイルから読み込み:" + file_path)
        if os.path.exists(file_path):
            parser = configparser.ConfigParser()
            parser.read(file_path)

            self.consumer_key = parser.get('twitter', 'consumer_key')
            self.consumer_secret = parser.get('twitter', 'consumer_secret')
            self.access_token_key = parser.get('twitter', 'access_token_key')
            self.access_token_secret = parser.get('twitter', 'access_token_secret')
        else:
            print("ファイルが見つかりません:" + file_path)

    def __get_data(self, url, params):
        session = OAuth1Session(
            self.consumer_key,
            self.consumer_secret,
            self.access_token_key,
            self.access_token_secret
        )
        res = session.get(self.API_TIMELINE_URL, params=params)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            print(res)
            raise Exception("Twitterからのデータ取得に失敗しました:" + str(res.status_code))

    def get_tweets_by_user(self, screen_name):
        params = {
            "screen_name": screen_name,
            "result_type": "recent",
            "count": "15"
        }
        return self.__get_data(self.API_TIMELINE_URL, params)