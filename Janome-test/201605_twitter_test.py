"""
201605 - Twitterからユーザー指定でツイートを取得する
"""

import sys
sys.path.append("../")

from Janome.api.Twitter import TwitterService

# Twitterにアクセスするためのクラスのインスタンスを作成(実体はJanome/Twitter.pyに)
t = TwitterService("../config.ini")

profile = t.get_user_profile('@kou_i')
print(profile['description'])

tweets = t.get_tweets_by_user('@kou_i')

for tweet in tweets:
    print(tweet['text'])