# coding:UTF-8

import MeCab


class MeCabService:
    @classmethod
    def parse(cls, text):
        mecab = MeCab.Tagger("-Ochasen")
        result = mecab.parse(text)

        rows = result.split("\n")
        # def parse_rows(row):
        #   return row.split("\t")

        return list(map(lambda r: r.split("\t"), rows))