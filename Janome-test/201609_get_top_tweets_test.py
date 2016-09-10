"""
201609 - 男女別によく出現するツイートの語句リストを作成する
"""

import sys
sys.path.append("../")

from Janome.logic.output_tweet_to_file import TweetToFileService

TweetToFileService.execute_process_tweets('tweet_list.csv')
