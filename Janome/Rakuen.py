# coding:UTF-8

import configparser
import os
import requests
import json
import time


class RakutenService:
    __URL_PREFIX = 'https://app.rakuten.co.jp/services/api/Travel/'
    __URL_SUFFIX = '20131024?format=json&applicationId='

    def __init__(self, file_path):
        """
        設定ファイルを元に初期化を行う
        :param file_path: 設定ファイル(iniファイル)へのパス
        """
        print("設定ファイルから読み込み:" + file_path)
        if os.path.exists(file_path):
            parser = configparser.ConfigParser()
            parser.read(file_path)

            self._application_id= parser.get('rakuten', 'application_id')
        else:
            print("ファイルが見つかりません:" + file_path)

    def __get(self, api_name, params):
        """
        与えられたパラメータを元に、楽天のAPIに対してGETリクエストを実行する
        :param api_name:
        :param params:
        :return:
        """

        # URLを組み立てる
        url = "%s%s/%s%s" % (self.__URL_PREFIX, api_name, self.__URL_SUFFIX, self._application_id)
        if params is not None:
            for key, value in params.items():
                if value is not None and value != '':
                    url += "&%s=%s" %(key, value)
        print("  処理対象URL: %s" % url)

        # 楽天のAPIは1秒に1回しかコールできないため、1秒ウェイトをかける
        time.sleep(1)
        res = requests.get(url)

        if (res.status_code == 200):
            content = res.content

            # json.loadsを実行するには、対象がstr型である必要があるが
            # contentがbytesで返ってくることがあるので、そのような場合には変換する
            if isinstance(content, bytes):
                content = content.decode('utf-8')

            print("    楽天からのデータ取得に成功しました:%s" % content)

            # json文字列を辞書型(または配列)に変換する
            data = json.loads(content)

            return data
        else:
            print("    楽天からのデータ取得に失敗しました:%d" % res.status_code)
            return None

    def get_location_directory(self):
        """
        楽天トラベルで指定可能なカテゴリコード一覧を取得する。
        コード一覧は受け取ったままだと使いにくいため、今回のプログラムで使いやすいように加工して返す
        :return:
        """
        original_dict = self.__get('GetAreaClass', None)
        if dict is None:
            print("APIの実行に失敗しました")
            return None

        """
        受け取ったデータは辞書になっており、「areaClasses」というキーが一つだけある。
        areaClassesは辞書になっており、「largeClasses」というキーが一つだけある。
        largeClassesは配列になっているが、要素は必ず一つしか入っていない(「日本」という情報が入っている)。
        その一つしかない要素の値は配列になっており、「largeClass」というキーが一つだけある。
        """
        large_classes = original_dict['areaClasses']['largeClasses'][0]['largeClass']

        """
        「largeClass」の中は、配列になっており、一番目にはそのカテゴリ自体の情報(名前, コード)が入っている。
        二番目には、その子供となるカテゴリの情報が入っている。
        二番目の要素は辞書になっており、「middleClasses」という名前の要素が一つだけ入っている
        middleClassesに対応する値は配列になっており、それが実際の子カテゴリのリストとなっている
        """
        large_class = large_classes[0]
        large_class_name = large_class['largeClassName']
        large_class_code = large_class['largeClassCode']

        middle_classes = large_classes[1]['middleClasses']

        # print('%s / %s' % (large_class_code, large_class_name))

        # 最後に値を返すためのマップを作成しておく
        result = {}

        """
        middle_classesは配列であるため、ここでループさせる。
        これが都道府県レベルの情報となる。
        """
        for middle_class in middle_classes:

            """
            「middleClasses」の各要素は辞書となっており、「middleClass」という名前のキー1つだけがある。
            middleClassに対応する値は配列になっており、1番目にはこのカテゴリ自体の情報(名前, コード)が入っている。
            2番目には子カテゴリの情報が入っている
            """
            m = middle_class['middleClass']
            middle_class_elem = m[0]
            middle_class_code = middle_class_elem['middleClassCode']
            middle_class_name = middle_class_elem['middleClassName']

            """
            配列の2番目(子カテゴリの情報)は辞書になっており、「smallClasses」という名前のキー1つだけがある。
            そのキーに対応する値が、実際の子カテゴリのリストとなっている。
            """
            small_classes = m[1]['smallClasses']

            # print('%s / %s' % (middle_class_code, middle_class_name))

            # ループの最後で、変数resultにデータを追加するためのリストを作成する。
            location_data = list()

            # それぞれのリストの一番目のは、large_categoryのコードを入れる
            location_data.append(large_class_code)

            # 二番目には、middle_categoryのコードを入れる
            location_data.append(middle_class_code)

            # 三番目には、small_categoryのコードを入れる。これは複数となるため、リストにしておく
            # small_categoryを処理するためにループを行うので、それが終わったら、変数item_listに追加する
            small_list = []

            """
            small_classesは配列であるため、更にループさせる。
            これが都市レベルの情報となる。
            """
            for small_class in small_classes:
                """
                「smallClasses」の各要素は辞書となっており、「smallClass」という名前の要素1つだけがある。
                smallClassに対応する値は配列になっており、1番目にはこのカテゴリ自体の情報(名前, コード)が入っている。
                2番目には子カテゴリの情報が入る。
                なお、2番目の要素は地域レベルの情報となるが、これは場所によっては無い場合もある。
                """
                s = small_class['smallClass']
                small_class_elem = s[0]

                small_class_name = small_class_elem['smallClassName']
                small_class_code = small_class_elem['smallClassCode']

                # print('  %s / %s' % (small_class_name, small_class_code))

                # small_categoryの各データは配列とし、一番目の要素をsmall_categoryのコードとする。
                # 二番目以降の要素は、より詳細なカテゴリの情報が存在する場合にのみ、データを追加する。
                small_items = list()
                small_items.append(small_class_code)

                # より詳細な地域データがある場合のみ、更にループを実行する
                if len(s) > 1:
                    """
                    地域の詳細データ(smallClassの2番目の要素)は、辞書となっており、「detailClasses」という名前の要素1つだけがある。
                    そのキーに対応する値が、詳細な地域情報のリストとなっている。
                    """
                    detail_classes = s[1]['detailClasses']
                    for detail_class in detail_classes:
                        """
                        detailClassesの各要素は辞書となっており、「detailClass」という名前の要素1つだけがある。
                        その中に、各カテゴリのデータ(名前, コード)が入っている
                        """
                        detail_class_elem = detail_class['detailClass']
                        detail_class_name = detail_class_elem['detailClassName']
                        detail_class_code = detail_class_elem['detailClassCode']

                        # print('    %s / %s' % (detail_class_name, detail_class_code))

                        # small_itemsの2番目以降に、detail_classの情報を追加する
                        small_items.append(detail_class_code)
                # small_classのループの最後で、各small_classの値リスト
                # (そのsmall_classのコードと、あればdetail_classのコードも入った配列)
                # をリストに追加する
                small_list.append(small_items)

            # small_classのループが終わったら、リストの3番目にsmall_classのリストを、要素として追加する
            location_data.append(small_list)

            # 最後に、middle_categoryの名前(=都道府県名)をキーに、large_category 〜 detail_categoryまで値の入ったリストを追加する。
            result[middle_class_name] = location_data
        return result

    def get_hotels(self, location):
        """
        地域に該当するホテルの一覧を取得する。
        :param location: get_location_directory()で取得した地域データ
        :return:
        """

        # get_location_directory()で取得したデータの一番目には、国情報が入っている
        large_class_code = location[0]

        # 二番目には、都道府県が入っている
        middle_class_code = location[1]

        # 三番目には都市データが入っているが、これは配列になっている
        small_class_code_list_collection = location[2]

        # 楽天APIを利用する際のパラメータを準備
        params = {
            'largeClassCode' : large_class_code,
            'middleClassCode' : middle_class_code
        }

        result = list()

        for small_class_code_list in small_class_code_list_collection:
            small_class_code = None
            detail_class_code = None

            # 都市レベルの情報をセット
            small_class_code = small_class_code_list[0]
            params['smallClassCode'] = small_class_code

            # 配列の長さが1以上の場合、さらに詳細地域の情報がある。
            # その情報がある場合には、それも送らないと楽天側からエラーを返されてしまうため、その場合には必ずセットする
            if len(small_class_code_list) > 1:
                small_class_code = small_class_code_list[0]

                # 詳細地域の情報は「detailClassCode」というパラメータに入れて送る
                for detail_class_code in small_class_code_list[1:]:
                    params['detailClassCode'] = detail_class_code
                    query_result = self.__get('SimpleHotelSearch', params)
                    result.extend(self.__get_hotel_info(query_result))

                # 最後に、detailClassCodeの情報をリセットしておく
                if 'detailClassCode' in params:
                    del params['detailClassCode']
            else:
                # detailClassCodeがない場合は、そのままクエリーを送る
                query_result = self.__get('SimpleHotelSearch', params)
                result.extend(self.__get_hotel_info(query_result))

        return result

    @classmethod
    def __get_hotel_info(cls, hotels):
        """
        ホテル情報の詳細を取得する
        :param hotels:
        :return:
        """
        hotels_result = list()

        if hotels is None:
            return hotels_result

        # ホテル情報取得のクエリー結果は辞書となっており、「hotels」という要素の中に配列としてデータが入っている
        for hotel_info in hotels['hotels']:
            # 配列の一つ一つの要素は辞書型で、「hotel」という要素にデータが入っている
            hotel = hotel_info['hotel']

            # ホテル情報は配列になっており、1番目には基本情報(ホテル名など)が入っている
            basic_info = hotel[0]['hotelBasicInfo']

            # 2番目にはホテルのランキング詳細情報(風呂、食事、場所などの各項目に対する評価点)が入っている
            ranking_info = hotel[1]['hotelRatingInfo']

            # 評価点は「serviceAverage」と「locationAverage」の平均を取る(＊入っていない場合もある)
            service_average = ranking_info['serviceAverage'] if ranking_info['serviceAverage'] is not None else 0
            location_average = ranking_info['locationAverage'] if ranking_info['locationAverage'] is not None else 0

            # どちらかが0点の場合は、一方の評価点のみを採用する
            if service_average <= 0:
                average = service_average
            elif location_average <= 0:
                average = location_average
            else:
                average = (service_average + location_average) / 2

            # 評価点の平均が3.5以上のホテルのみを候補とする
            if average > 3.5:
                hotels_result.append({
                    'hotel_name': basic_info['hotelName'],
                    'site_url': basic_info['hotelInformationUrl'],
                    'points': average,
                    'basic_info': basic_info,
                    'ranking_info': ranking_info
                })

        return hotels_result


