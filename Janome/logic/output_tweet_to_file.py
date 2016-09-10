from Janome.api.MeCab import MeCabService
from Janome.api.Twitter import TwitterService

import csv
import io


class TweetToFileService:
    def __init__(self, config_file_name):
        self.__twitter_service = TwitterService(config_file_name)

    def execute_get_tweets(self, twitter_account_list, output_file_name):
        """
        引数に指定したユーザーリストからツイートを取得し、MeCabで解析して語句の出現回数をCSVに出力します。
        各ユーザーの情報は配列とし、一番目にアカウント名, 2番目に性別(0=男性, 1=女性)を入力するものとします。
        :param twitter_account_list:
        :param output_file_name:
        :return:
        """
        # 解析結果を保存する辞書
        word_counts_male = dict()
        word_counts_female = dict()

        for user in twitter_account_list:
            account_name = user[0] # 配列の各データは配列とし、一番目にアカウント名を入れる
            account_gender = user[1] # 一番目には性別を入れる。0=男性, 1=女性とする

            # ユーザー名を指定してツイートのデータを取得
            try:
                data = self.__twitter_service.get_tweets_by_user(account_name)
            except BaseException as e:
                # エラーが発生した場合には次のアカウントに進む。
                print("ツイートを取得できませんでした:%s -> %s" % (account_name, str(e)))
                continue

            # 取得したデータから、ツイートの本文だけを取得(ツイートのデータは辞書型で取得)
            texts = list(map(lambda t: t['text'], data))

            # 取得したツイート本文のリストを、改行で区切ってひとまとめのテキストにする。
            text = "\n".join(texts)

            # テキストを構文解析にかけ、結果を辞書の配列として受け取る
            result = MeCabService.parse(text)

            # 全ての語句について、出現回数を記録する
            for res in result:
                word = res[0]

                # 正常にparse出来ていれば、配列のデータ数は6以上になるはず
                if len(res) < 6:
                    continue

                if account_gender == 0:
                    word_counts = word_counts_male
                else:
                    word_counts = word_counts_female
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

        # 男性と女性で重複しているものを取り除く
        word_counts_male_filtered = list(filter(lambda _v: _v[0] not in word_counts_female, word_counts_male.items()))
        word_counts_female_filtered = list(filter(lambda _v: _v[0] not in word_counts_male, word_counts_female.items()))

        # 書き込み用にファイルをオープン(Excelで文字化けしないよう、utf-16で出力する)
        file = open(output_file_name, 'w', encoding='utf-16')
        try:
            def do_output(_w, _c, _g):
                file.write(('"%s","%d","%s"\n' % (_w, _c, _g)))

            for v in word_counts_male_filtered:
                do_output(v[0], v[1], 'male')
            for v in word_counts_female_filtered:
                do_output(v[0], v[1], 'female')
            """
            for w,c in word_counts_male.items():
                file.write(('"%s","%d","%s"\n' % (w, c, 'male')))
            for w, c in word_counts_female.items():
                file.write(('"%s","%d","%s"\n' % (w, c, 'female')))
            """
        finally:
            file.close()
            print('%s を出力しました' % output_file_name)

    @classmethod
    def execute_process_tweets(cls, input_file_name,
                               output_male_file_name='male_tweets.csv', output_female_file_name='female_tweets.csv'):
        """
        execute_get_tweetsで出力したCSVを解析し、トップ200の語句を出力します。
        結果は男性、女性で別々のファイルに出力します。
        :param input_file_name:
        :param output_male_file_name:
        :param output_female_file_name:
        :return:
        """
        file = io.open(input_file_name, 'r', encoding='utf-16-le')
        reader = csv.reader(file)

        male_map = {}
        female_map = {}
        try:
            for row in reader:
                # リストのサイズが3の場合のみ処理(うまくデータが分割されない場合がある)
                if len(row) != 3:
                    continue

                # 一番目に語句, 2番目に出現回数, 3番目に性別が入っている
                word = row[0]
                count = row[1]
                gender = row[2]

                # 男性と女性で、出力先のファイルを変える
                if gender == 'male':
                    dct = male_map
                else:
                    dct = female_map

                # 語句と出現回数が正しく取得できている場合のみ、リストに追加
                if len(word) > 0 and len(count) > 0:
                    dct[word] = int(count)
        finally:
            file.close()

        # トップ200のデータだけを取得する
        male_list = cls.__sort_list(male_map)
        female_list = cls.__sort_list(female_map)

        # ファイルに出力
        cls.__output_file(male_list, output_male_file_name)
        cls.__output_file(female_list, output_female_file_name)

    @classmethod
    def __sort_list(cls, target_map):
        # 逆順でソートされたリストを作成する
        tmp = sorted(target_map.items(), key=lambda v: v[1], reverse=True)
        return tmp[0:200]

    @classmethod
    def __output_file(cls, target_list, file_name):
        print('ファイル %s を出力します' % file_name)
        f = open(file_name, 'w')
        try:
            for item in target_list:
                f.write('"%s","%s"\n' % (item[0], item[1]))
        finally:
            f.close()

