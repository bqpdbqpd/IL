from gensim.models import word2vec, KeyedVectors
from gensim.models.wrappers import FastText
from janome.tokenizer import Tokenizer
import numpy as np
import datetime

def sum_vec_error(A, B):
    result = 0
    for a, b in zip(A, B):
        #print(a,b)
        x = abs(a-b)
        #print(x)
        result += x

    result = result / A.shape[0]

    return result

def sentense_ave_vec(sentense):
    cnt_sentense = 0
    vec_sentence = np.zeros_like(w2v_model.wv['今日'])


    for token in tokenizer.tokenize(sentense):
        #print(token.surface)
        #print(w2v_model[token.surface])
        if token.part_of_speech.split(',')[0] in ['名詞', '動詞', '形容詞','形容動詞','副詞']:
            cnt_sentense += 1
            vec_sentence += w2v_model.wv[token.surface]

    vec_sentence = vec_sentence / cnt_sentense

    return vec_sentence


if __name__ == '__main__':
    # しろやぎコーポレーションが公開してくれている分散表現
    #w2v_model = word2vec.Word2Vec.load('data/latest-ja-word2vec-gensim-model/word2vec.gensim.model')
    # fatstext 読み込みに１０分程度かかる
    w2v_model = KeyedVectors.load_word2vec_format('data/cc.ja.300.vec')

    #print(w2v_model['今日'])

    tokenizer = Tokenizer()

    while True:
        #input_sentense = '本日の日付は？'
        input_sentense = input('御用は何でしょうか？:')
        input_sentense = str(input_sentense)
        #print(input_sentense)
        #input_sentense = [input_sentense]
        input_sentense_ave_vec = sentense_ave_vec(input_sentense)

        sentenses = ['今日の日付は？','明日の日付は？','昨日の日付は？']
        list_sentenses_error = []

        for sentense in sentenses:
            sav = sentense_ave_vec(sentense)
            list_sentenses_error.append(sum_vec_error(input_sentense_ave_vec, sav))

        #print(list_sentenses_error)


        #返答
        min_sum_vec_error = min(list_sentenses_error)
        #print(min_sum_vec_error)
        min_sum_vec_error_index = list_sentenses_error.index(min_sum_vec_error)

        if min_sum_vec_error < 0.04:　#閾値は人手なので改善の余地あり
            if sentenses[min_sum_vec_error_index] == sentenses[0]:
                now = datetime.datetime.now()
                print(now.strftime('%Y/%m/%d です'))
                exit
            elif sentenses[min_sum_vec_error_index] == sentenses[1]:
                now = datetime.datetime.now()
                yesterday = now + datetime.timedelta(days=1)
                print(yesterday.strftime('%Y/%m/%d です'))
                exit
            elif sentenses[min_sum_vec_error_index] == sentenses[2]:
                now = datetime.datetime.now()
                tommorow = now - datetime.timedelta(days=1)
                print(yesterday.strftime('%Y/%m/%d です'))
                exit
        else:
            print('お答えできません')
