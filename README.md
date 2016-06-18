# 概要
Python勉強会のソースコードです。

「ユーザーのツイートを解析し、おすすめの旅行先を提案する」という機能を想定しています。

 * Twitterから、あるユーザーのツイートを取得する。
 * MeCabで解析。
 * その後、いろいろ。。。
 
ワードを取り出して以降の処理はまだあまり決まっていません。。。。

# セットアップ
## Pythonのセットアップ
プログラムはPython3を前提にしています。先にbrewなどでインストールしてください。

```
brew install python3
```

python3を起動するときは「python3」コマンド, pipを利用するときは「pip3」となります。

## MeCabのインストール
Macの場合は以下のとおりです。

```
brew install mecab
brew install mecab-ipadic
```

## 必要なライブラリのインストール
Twitterからデータを取得するために「requests_oauthlib」, MeCabを利用するために「mecab-python3」をインストールします。

```
pip3 install requests_oauthlib
pip3 install mecab-python3
```

## 設定
プログラムを起動するために「config.ini.sample」をコピーし、「config.ini」というファイルを作成して下さい。

作成したら、その中にTwitterの認証トークンを入力します。

Twitterの認証トークンは、Twitterの開発者登録を行うことで取得できます。

https://dev.twitter.com/

の下の方にある「Manage Your Apps」からアプリの登録を行っておきます。

## 起動
プログラムを起動するには

```
python3 main.py
```

のようになります。