import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill

#なぜかchasenの出力以外にできないので別の環境でやるときは注意
mecab = MeCab.Tagger() #MeCab.Tagger(-Ochasen)
mecab.parse('')

# モデルの読み込み
with open("svc.model", "rb") as f:
    vectorizer = dill.load(f)
    label_encoder = dill.load(f)
    svc = dill.load(f)

# 発話から対話行為タイプを推定
def extract_da(utt):
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word = line.split("\t")[0]
            feature_str = line.split("\t")[1:]
            words.append(word)
    tokens_str = " ".join(words)
    X = vectorizer.transform([tokens_str])
    Y = svc.predict(X)
    da = label_encoder.inverse_transform(Y)[0]
    return da

for utt in ["大阪の明日の天気","もう一度はじめから","東京じゃなくて"]:
    da = extract_da(utt)
    print(utt,da)
