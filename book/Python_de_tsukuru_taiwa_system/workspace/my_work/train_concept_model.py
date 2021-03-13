import json
import dill
import sklearn_crfsuite
from crf_util import word2features, sent2features, sent2labels

sents = []
lis = []

for line in open("data/concept_samples.dat", "r"):
    line = line.rstrip()

    if line == "":
        sents.append(lis)
        lis = []
    else:
        word, postag, label = line.split('\t')
        lis.append([word, postag, label])

X = [sent2features(s) for s in sents]

Y = [sent2labels(s) for s in sents]

crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=False
)
crf.fit(X, Y)

with open("data/crf.model", "wb") as f:
    dill.dump(crf, f)
