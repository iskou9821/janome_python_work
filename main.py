# coding:UTF-8

import Janome.Twitter
import Janome.MeCab

t = Janome.Twitter.TwitterService("./config.ini")
data = t.get_tweets_by_user('@7x3x7x3')


texts = list(map(lambda t: t['text'], data))

text = "\n".join(texts)

result = Janome.MeCab.MeCabService.parse(text)

# 「名詞」だけを抽出
_map = {}
items = list(filter(lambda n: n[3].find('地域') >= 0 if len(n) > 3 else False, result))

# 件数のカウント
for item in items:
    name = item[0]
    if name in _map:
        _map[name] += 1
    else:
        _map[name] = 1

# リストのソート
_list = []
for key in _map.keys():
    _list.append((key, _map.get(key)))
_list.sort(key=lambda a: a[1])
_list.reverse()

print(_list)