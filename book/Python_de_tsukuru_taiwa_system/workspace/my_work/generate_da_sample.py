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

# サンプル分に含まれる単語を置き換えることで学習用事例を作成
def random_generate(root):
    buf = ""
    # タグがない文の場合には置き換えなしで返す
    if len(root) == 0:
        return root.text
    # タグが囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "place":
            pref = random.choice(prefs)
            buf += pref
        elif elem.tag == "date":
            date = random.choice(dates)
            buf += date
        elif elem.tag == "type":
            _type = random.choice(types)
            buf += _type
        if elem.tail is not None:
            buf += elem.tail
    return buf

# 学習用ファイルの出力先
fp = open("data/da_samples.dat","w")

da = ""
# examples.txt の読み込み
for line in open("examples.txt", "r"):
    line = line.rstrip()

    if re.search(r"^da=", line):
        da = line.replace("da=","")
    elif line == "":
        pass
    else:
        # xmlではトップレベルに要素が一つでないとダメなためダミータグを最上位に設定
        root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
        # 各サンプル文を１０００倍に
        for i in range(1000):
            sample = random_generate(root)
            # 書き出し
            print(da + "\t" + sample + "\n")
            fp.write(da + "\t" + sample + "\n")

fp.close()
