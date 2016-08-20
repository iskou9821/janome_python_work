# coding:UTF-8

from Janome.Twitter import TwitterService
from Janome.MeCab import MeCabService

# Twitterにアクセスするためのクラスのインスタンスを作成(実体はJanome/Twitter.pyに)
t = TwitterService("./config.ini")

# 解析対象とするTwitterアカウントのリスト
users = ['@kou_i']

# 解析結果を保存する辞書
word_counts = dict()

for user in users:
    # ユーザー名を指定してツイートのデータを取得
    data = t.get_tweets_by_user(user)

    # 取得したデータから、ツイートの本文だけを取得(ツイートのデータは辞書型で取得)
    texts = list(map(lambda t: t['text'], data))

    # 取得したツイート本文のリストを、改行で区切ってひとまとめのテキストにする。
    text = "\n".join(texts)

    # テキストを構文解析にかけ、結果を辞書の配列として受け取る
    result = MeCabService.parse(text)

    # 全ての語句について、出現回数を記録する
    for res in result:
        word = res[0]
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

# 解析結果をファイルに保存
file_name = 'output.csv'

# 書き込み用にファイルをオープン(Excelで文字化けしないよう、utf-16で出力する)
file = open(file_name, 'w',encoding='utf-16')
try:
    for w,c in word_counts.items():
        file.write(('"%s",%d\n' % (w, c)))
finally:
    file.close()
    print('%s を出力しました' % file_name)
