import MeCab
import re
import random
import json
import xml.etree.ElementTree

# 都道府県名のリスト
prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
         '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
         '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
         '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
         '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

# 日付のリスト
dates = ["今日","明日"]

# 情報種別のリスト
types = ["天気","気温"]

# サンプル文に含まれる単語を置き換えることで学習用事例を作成
def random_generate(root):
    buf = ""
    pos = 0
    posdic = {}
    # タグなしの場合はそのまま
    if len(root) == 0:
        return root.text, posdic
    #この方法だとタグより最初に文字列から始まる文には対応できないので対応が必要？
    for elem in root:
        if elem.tag == "place":
            pref = random.choice(prefs)
            buf += pref
            posdic["place"] = (pos, pos+len(pref))
            pos += len(pref)
        elif elem.tag == "date":
            date = random.choice(dates)
            buf += date
            posdic["date"] = (pos, pos+len(date))
            pos += len(date)
        elif elem.tag == "type":
            _type = random.choice(types)
            buf += _type
            posdic["type"] = (pos, pos+len(_type))
        if elem.tail is not None:
            #print(pos, elem.tail)
            buf += elem.tail
            pos += len(elem.tail)
    return buf, posdic

def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"

mecab = MeCab.Tagger()
mecab.parse("")

fp = open("data/concept_samples.dat","w")

da = ""

for line in open("examples.txt","r"):
    line = line.rstrip()

    if re.search(r'^da=',line):
        da = line.replace('da=','')
    # 空行は無視
    elif line == "":
        pass
    else:
        # タグの部分を取得するため，周囲にダミーのタグをつけて解析
        root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
        # 各サンプル文を1000倍に増やす
        for i in range(1000):
            sample, posdic = random_generate(root)

            # lisには単語、品詞，ラベルの順に入る
            lis = []
            pos = 0
            prev_label = ""
            for line in mecab.parse(sample).splitlines():
                if line == "EOS":
                    break
                else:
                    word = line.split("\t")[0]
                    feature_str = line.split("\t")[1:]
                    features = feature_str#feature_str.split(',')

                    #print(features)
                    postag = features[3].split("-")[0]
                    label = get_label(pos, posdic)

                    if label == "O":
                        lis.append([word, postag, "O"])
                    elif label == prev_label:
                        lis.append([word, postag, "I-" + label])
                    else:
                        lis.append([word, postag, "B-" + label])
                    pos += len(word)
                    prev_label = label

        for word, postag, label in lis:
            fp.write(word + "\t" + postag + "\t" + label + "\n")
        fp.write("\n")

fp.close()
