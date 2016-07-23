# coding:UTF-8

import configparser
import os
from requests_oauthlib import OAuth1Session
import json


class TwitterService:
    """
    Twitterにアクセスし、ツイートの情報を取得するためのクラス
    """
    __API_TIMELINE_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?"

    __consumer_key = ""
    __consumer_secret = ""
    __access_token_key = ""
    __access_token_secret = ""

    def __init__(self, file_path):
        """
        設定ファイルを指定し、その内容を元に初期化を行うコンストラクタ
        :param file_path: 設定ファイル(iniファイル)のパス
        """
        # 設定ファイルからTwitterへのアクセスに必要なユーザー情報を読み込む
        print("設定ファイルから読み込み:" + file_path)
        if os.path.exists(file_path):
            parser = configparser.ConfigParser()
            parser.read(file_path)

            self.__consumer_key = parser.get('twitter', 'consumer_key')
            self.__consumer_secret = parser.get('twitter', 'consumer_secret')
            self.__access_token_key = parser.get('twitter', 'access_token_key')
            self.__access_token_secret = parser.get('twitter', 'access_token_secret')
        else:
            print("ファイルが見つかりません:" + file_path)

    def __get_data(self, url, params):
        # TwitterにアクセスするためのOAuthセッション情報を作成
        session = OAuth1Session(
            self.__consumer_key,
            self.__consumer_secret,
            self.__access_token_key,
            self.__access_token_secret
        )

        # ユーザーのタイムライン情報を取得
        res = session.get(self.__API_TIMELINE_URL, params=params)

        # レスポンスが正常に取得できた(=200 OKが返ってきた)場合は、レスポンスのjsonデータを辞書型にparseして返す
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            print(res)
            raise Exception("Twitterからのデータ取得に失敗しました:" + str(res.status_code))

    def get_tweets_by_user(self, screen_name):
        """
        ユーザー名を指定してツイートを取得
        :param screen_name: ツイート取得対象のユーザー名
        :return:
        """
        # ユーザーを指定してツイートを取得するためのパラメータ指定。result_typeやcountは可変にしても良いかも。
        params = {
            "screen_name": screen_name,
            "result_type": "recent",
            "count": "15"
        }
        return self.__get_data(self.__API_TIMELINE_URL, params)