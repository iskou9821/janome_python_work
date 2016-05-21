# coding:UTF-8

import Janome.Twitter
import Janome.MeCab

t = Janome.Twitter.TwitterService("./config.ini")
data = t.get_tweets_by_user('@kou_i')


texts = list(map(lambda t: t['text'], data))

text = "\n".join(texts)

result = Janome.MeCab.MeCabService.parse(text)

# 「名詞」だけを抽出
items = list(filter(lambda n: n[3].find('名詞') >= 0 if len(n) > 3 else False, result))

for item in items:
    print(item)