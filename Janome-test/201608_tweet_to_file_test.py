"""
201608 複数のユーザーのツイートを取得し、男女別に語句の出現数をカウントする
"""
import sys
sys.path.append("../")

from Janome.logic.output_tweet_to_file import TweetToFileService

svc = TweetToFileService("../config.ini")

# 配列の1番目にはTwitterのアカウント名を、2番目には性別(男性=0, 女性=1)を入れる
account_list = [
    ['@アカウント名', 1],
    ['@アカウント名', 1],
    ['@アカウント名', 0],
    ['@アカウント名', 0],
    ['@アカウント名', 0],
]

svc.execute_get_tweets(account_list, 'tweet_list.csv')