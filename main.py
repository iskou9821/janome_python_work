# coding:UTF-8

import Janome.Twitter
import Janome.MeCab

# Twitterにアクセスするためのクラスのインスタンスを作成(実体はJanome/Twitter.pyに)
t = Janome.Twitter.TwitterService("./config.ini")

# ユーザー名を指定してツイートのデータを取得
data = t.get_tweets_by_user('@kou_i')

# 取得したデータから、ツイートの本文だけを取得(ツイートのデータは辞書型で取得)
texts = list(map(lambda t: t['text'], data))

# 取得したツイート本文のリストを、改行で区切ってひとまとめのテキストにする。
text = "\n".join(texts)

# テキストを構文解析にかけ、結果を辞書の配列として受け取る
result = Janome.MeCab.MeCabService.parse(text)

# 「地域」のデータだけを抽出する
#
#  filter()で、条件に一致するもの
#   (配列の3番目のデータに「地域」と入っているもの。ただし、場合によっては配列の長さが3以下の場合もあるため、それは除くようにする）
#  を抽出して、新しいリストを作る。
#  ただし、filter()の結果はリスト型ではないため、list()でリスト型に変換する。
items = list(filter(lambda n: n[3].find('地域') >= 0 if len(n) > 3 else False, result))

# 地域の名前の出現回数を、地域の名前ごとにカウントする
# ループが終了すると、キーに地域名、値に出現回数の入ったmapが出来上がる
_map = {}
for item in items:
    name = item[0]
    if name in _map:
        _map[name] += 1
    else:
        _map[name] = 1

# カウントした結果を、出現回数でソートする
#
# リスト型が持っている「sort」という関数を使いたいが、先ほど出現回数を記録したのは辞書型であるため
# 一旦、リスト型に変換する。
# その後、ソートを実行するが、並び替えのキーは「地域名」と「出現回数」という2つのデータが入っているうちの
# 「出現回数」となるので、ラムダ式を使ってそれを指定する。
_list = list(_map.items())
_list.sort(key=lambda a: a[1])

# ソート結果が昇順なので、降順に直す
_list.reverse()

# 一番上から2番目まで切り出し、新しいリストを作成する
_tops = _list[:2]

# 結果表示
print(_tops)