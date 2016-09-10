# coding:UTF-8

import MeCab


class MeCabService:
    """
    MeCabを利用し、テキストの構文解析を行うためのクラス
    """
    @classmethod
    def parse(cls, text):
        """
        テキストの構文解析を実行する
        :param text: 解析対象のテキスト
        :return:
        """

        # MeCabにアクセスするためのクラスのインスタンスを作成(mecab-python3モジュール)
        mecab = MeCab.Tagger("-Ochasen")

        # 構文解析を実行
        result = mecab.parse(text)

        # 構文解析の結果(=テキスト)を、行で区切って配列にする
        rows = result.split("\n")

        # 構文解析の結果テキストはタブ区切りのテキストとなっているため、タブを区切り文字として配列に変換する。
        #
        # タブ区切りのテキスト → 配列としているのがmap()の処理。
        # ただし、map()の結果はリスト型ではないためmap()の後にlist()でリスト型に変換する。
        return list(map(lambda r: r.split("\t"), rows))

        """
        余談だが、リストを返す処理はこのようにも書ける。
        (ラムダ式には式を一つしか書くことができないため、複雑な処理が必要な場合は関数を定義して引数に渡す)


        def parse_rows(row):
           return row.split("\t")


        return list(map(parse_rows, rows))
        """