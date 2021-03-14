import sys
from da_concept_extractor import DA_Concept
import requests
import json
from datetime import datetime, timedelta, time

class FrameWeatherSystem:
    # 都道府県名のリスト
    prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
         '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
         '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
         '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
         '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

    # 日付のリスト
    dates = ["今日", "明日"]

    # 情報種別のリスト
    types = ["天気", "気温"]

    # 都道府県名から緯度と経度を取得するための辞書
    dic_pref_id = {'北海道': "016010", '青森': "020010", '岩手': "030010", '宮城': "040010",
                    '秋田': "050010", '山形': "060010", '福島': "070010", '茨城': "080010",
                    '栃木': "090010", '群馬': "100010", '埼玉': "110010", '千葉': "120010",
                    '東京': "130010", '神奈川': "140010", '新潟': "150010", '富山': "160010",
                    '石川': "170010", '福井': "180010", '山梨': "190010", '長野': "200010",
                    '岐阜': "210010", '静岡': "220010", '愛知': "230010", '三重': "240010",
                    '滋賀': "250010", '京都': "260010", '大阪': "270000", '兵庫': "280010",
                    '奈良': "290010", '和歌山': "300010", '鳥取': "310010", '島根': "320010",
                    '岡山': "330010", '広島': "340010", '山口': "350010", '徳島': "360010",
                    '香川': "370000", '愛媛': "380010", '高知': "390010", '福岡': "400010",
                    '佐賀': "410010", '長崎': "420010", '熊本': "430010", '大分': "440010",
                    '宮崎': "450010", '鹿児島': "460010", '沖縄': "471010"}

    # システムの対話行為とシステム発話を紐づけた辞書
    uttdic = {"open-prompt":"ご用件をどうぞ",
                "ask-place":"地名を言ってください",
                "ask-date":"日付を言ってください",
                "ask-type":"情報種別を言ってください"}

    # 天気予報 API（livedoor 天気互換）を利用　URL https://weather.tsukumijima.net
    current_weather_url = 'https://weather.tsukumijima.net/api/forecast/city/'


    def __init__(self):
        # 対話せっしょんを管理するための辞書
        self.sessiondic = {}
        # 対話行為タイプとコンセプトを抽出するためのモジュールの読み込み
        self.da_concept = DA_Concept()

    def get_current_weather(self, place_id):
        # 天気情報を取得
        responce = requests.get(self.current_weather_url+place_id)
        try:
            return responce.json()["forecasts"][0]
        except KeyError:
            return {"telop": "--情報取得失敗--",
                    "temperature":{"max": {"celsius": "--情報取得失敗--"},
                                    "min":{"celsius": "--情報取得失敗--"}}}

    def get_tommorow_weather(self, place_id):
        # 天気情報を取得
        responce = requests.get(self.current_weather_url+place_id)
        try:
            return responce.json()["forecasts"][0]
        except KeyError:
            return {"telop": "--情報取得失敗--",
                    "temperature":{"max": {"celsius": "--情報取得失敗--"},
                                    "min":{"celsius": "--情報取得失敗--"}}}


    # 発話から得られた情報をもとにフレームを更新
    def update_frame(self, frame, da, conceptdic):
        # 値の整合性を確認し，整合性のないものは空文字にする
        for k,v in conceptdic.items():
            if k == "place" and v not in self.prefs:
                conceptdic[k] = ""
            elif k == "date" and v not in self.dates:
                conceptdic[k] = ""
            elif k == "type" and v not in self.types:
                conceptdic[k] = ""
        if da == "request-weather":
            for k,v in conceptdic.items():
                # コンセプトの情報でスロットを埋める
                frame[k] = v
        elif da == "initialize":
            frame = {"place": "", "date": "", "type": ""}
        elif da == "correct-info":
            for k,v in conceptdic.items():
                if frame[k] == v:
                    frame[k] = ""
        return frame

    # フレームの状態から次のシステム対話行為を決定
    def next_system_da(self, frame):
        # 全てのスロットが空であればオープンな質問を行う
        if frame["place"] == "" and frame["date"] == "" and frame["type"] == "":
            return "open-prompt"
        # 空のスロットがあればその要素を質問する
        elif frame["place"] == "":
            return "ask-place"
        elif frame["date"] == "":
            return "ask-date"
        elif frame["type"] == "":
            return "ask-type"
        else:
            return "tell-info"

    def initial_message(self):
        self.frame = {"frame": {"place": "", "date": "", "type": ""}}
        return {"utt": "こちらは天気情報案内システムです．ご用件をどうぞ", "end": False}

    def reply(self, input_str):
        text = input_str

        # 現在のセッションのフレームを取得
        frame = self.frame["frame"]
        print("frame=", frame)

        # 発話から対話行為タイプとコンセプトを取得
        da, conceptdic = self.da_concept.process(text)
        print(da, conceptdic)

        # 対話行為タイプとコンセプトを用いてフレームを更新
        frame = self.update_frame(frame, da, conceptdic)
        print("updated frame=", frame)

        # 更新後のフレームを保存
        self.frame = {"frame": frame}

        # フレームからシステム対話行為を得る
        sys_da = self.next_system_da(frame)

        # 遷移先がtell-infoの場合には情報を伝えて終了
        if sys_da == "tell-info":
            utts = []
            utts.append("お伝えします")
            place = frame["place"]
            date = frame["date"]
            _type = frame["type"]
            place_id = self.dic_pref_id[place]
            print(str(place_id))

            if date == "今日":
                cw = self.get_current_weather(place_id)
                if _type == "天気":
                    utts.append(cw["telop"]+"です")
                elif _type == "気温":
                    utts.append(str("最高気温は"+cw["temperature"]["max"]["celsius"]+"です（最低気温は表示されません）"))
            elif date == "明日":
                tw = self.get_tommorow_weather(str(place_id))
                if _type == "天気":
                    utts.append(tw["telop"]+"です")
                elif _type == "気温":
                    utts.append(str("最高気温は"+tw["temperature"]["max"]["celsius"]+", 最低気温は"+tw["temperature"]["min"]["celsius"]+"です"))
            utts.append("ご利用ありがとうございました")
            del self.frame
            return {"utt": "．".join(utts), "end": True}

        else:
            # その他の遷移先の場合には状態に紐づいたシステム発話を生成
            sysutt = self.uttdic[sys_da]
            return {"utt": sysutt, "end": False}

if __name__ == '__main__':
    system = FrameWeatherSystem()

    while True:
        system_init = system.initial_message()
        print(system_init["utt"])
        while True:
            text = input("> ")
            system_reply = system.reply(text)
            if system_reply["end"] == True:
                print(system_reply["utt"])
                break
