"""
201609 - ツイートの語句から、ユーザーの性別を推定する
"""

import sys
sys.path.append("../")

from Janome.api.Twitter import TwitterService
import Janome.logic.assume_user_from_tweet as tw

tw_svc = TwitterService("../config.ini")
tweets = tw_svc.get_tweets_by_user('@kou_i')
parsed_tweets = tw.parse_tweets(tweets)

as_svc = tw.AssumeUserFromTweetService('male_tweets.csv', 'female_tweets.csv', 'furo.csv')
res = as_svc.assume_gender(parsed_tweets)

print(res)