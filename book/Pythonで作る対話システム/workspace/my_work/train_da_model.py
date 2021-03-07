import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import dill

mecab = MeCab.Tagger()
mecab.parse('')

sents = []
labels = []

for line in open("data/da_samples.dat", "r"):
    line = line.rstrip()

    da, utt = line.split("\t")
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word = line.split("\t")[0]
            feature_str = line.split("\t")[1:]
            words.append(word)

    sents.append(" ".join(words))
    labels.append(da)

vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split(), ngram_range=(1,3))
X = vectorizer.fit_transform(sents)

label_encoder = LabelEncoder()
Y = label_encoder.fit_transform(labels)

svc = SVC(gamma="scale")
svc.fit(X,Y)

with open("svc.model", "wb") as f:
    dill.dump(vectorizer, f)
    dill.dump(label_encoder, f)
    dill.dump(svc, f)
