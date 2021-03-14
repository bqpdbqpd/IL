import aiml
import MeCab
from telegram_bot import TelegramBot

class AimlSystem:
    def __init__(self):
        # AIMLを読み込むためのインスタンスを用意
        self.kernel = aiml.Kernel()
        # 形態素解析器を用意
        self.tagger = MeCab.Tagger('-Owakati')

    def initial_message(self):
        # aiml.xmlを読み込む
        self.kernel.learn("data/aiml.xml")
        return {'utt':'はじめまして，雑談を始めましょう', 'end':False}

    def reply(self, dic_input):
        utt = dic_input['utt']
        utt = self.tagger.parse(utt)
        # 対応するセッションのkernelを取り出し，respondでマッチするルールを探す
        response = self.kernel.respond(utt)
        # print(utt, response)
        return {'utt': response, 'end':False}

if __name__ == '__main__':
    system = AimlSystem()
    dic_input = system.initial_message()
    #print('dic_input', dic_input)
    print("bot>"+dic_input['utt'])

    while True:
        raw_input = str(input("me>"))
        dic_input['utt'] = raw_input
        dic_input = system.reply(dic_input)
        print("bot>"+dic_input['utt'])
