"""
201606 - ユーザーのツイートから地域情報を抽出する
"""

import sys
sys.path.append("../")

from Janome.api.Twitter import TwitterService
import Janome.logic.assume_user_from_tweet as tw

svc = TwitterService("../config.ini")
tweets = svc.get_tweets_by_user('@kou_i')
parsed_tweets = tw.parse_tweets(tweets)

areas = tw.AssumeUserFromTweetService.get_areas(parsed_tweets)

print(areas)