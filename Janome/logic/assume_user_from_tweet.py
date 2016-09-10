from Janome.api.MeCab import MeCabService
import csv

MALE = 'male'
FEMALE = 'female'
UNKNOWN = 'unknown'


def parse_tweets(tweets):
    """
    TwitterServiceで取得したツイートリストを、MeCabで語句に分割する
    :param tweets:
    :return:
    """

    # 取得したデータから、ツイートの本文だけを取得(ツイートのデータは辞書型で取得)
    texts = list(map(lambda t: t['text'], tweets))

    # 取得したツイート本文のリストを、改行で区切ってひとまとめのテキストにする。
    text = "\n".join(texts)

    # テキストを構文解析にかけ、結果を辞書の配列として受け取る
    return MeCabService.parse(text)


class AssumeUserFromTweetService:

    def __init__(self, male_word_file_name, female_word_file_name, furo_word_file_name):
        self.__male_map = self.__file_to_map(male_word_file_name)
        self.__female_map = self.__file_to_map(female_word_file_name)
        self.__furo_map = self.__file_to_map(furo_word_file_name)

    @classmethod
    def __file_to_map(cls, file_name):
        """
        男性, 女性の判別に利用する語句リストを読み込む
        :param file_name:
        :return:
        """
        file = open(file_name, 'r')
        try:
            res = {}
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    continue
                res[row[0]] = row[1]
            return res
        finally:
            file.close()

    def assume_gender(self, tweets):
        """
        ツイートのリストから性別を推定する。
        また、風呂に関連するワードが現れているかどうかも同時に判断する。
        TwitterServiceで取得したツイートのリストを、parse_tweets()で語句に分割したリストを引数にとる。
        :param tweets:
        :return:
        """
        male_count = 0
        female_count = 0
        furo_count = 0
        for tweet in tweets:
            word = tweet[0]

            # 男女のツイートを取得した際、重複は除いている
            if word in self.__male_map:
                male_count += 1
            if word in self.__female_map:
                female_count += 1
            if word in self.__furo_map:
                furo_count += 1

        print('male_count:%d, female_count:%d, furo_count:%d' % (male_count, female_count, furo_count))
        res = {}
        if male_count > female_count:
            res['gender'] = MALE
        elif male_count < female_count:
            res['gender'] = FEMALE
        else:
            res['gender'] = UNKNOWN
        res['furo'] = furo_count > 0

        return res

    @classmethod
    def get_areas(cls, tweets):
        """
        ツイートの中に出現する地名の中から、上位2番目までを取得する。
        TwitterServiceで取得したツイートのリストを、parse_tweets()で語句に分割したリストを引数にとる。
        :param tweets:
        :return:
        """

        # 「地域」のデータだけを抽出する
        #
        #  filter()で、条件に一致するもの
        #   (配列の3番目のデータに「地域」と入っているもの。ただし、場合によっては配列の長さが3以下の場合もあるため、それは除くようにする）
        #  を抽出して、新しいリストを作る。
        #  ただし、filter()の結果はリスト型ではないため、list()でリスト型に変換する。
        items = list(filter(lambda n: n[3].find('地域') >= 0 if len(n) > 3 else False, tweets))

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

        return _tops


