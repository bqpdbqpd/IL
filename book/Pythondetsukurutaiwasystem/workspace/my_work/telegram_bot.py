# telegramを使わないので一部編集

class TelegramBot:
    def __init__(self, system):
        self.system = system

    def start(self):
        # 辞書型 inputにユーザIDを設定
        input_dic = {'utt': None, 'sessionID': str(0)}

        # システムからの最初の発話をinitial_messageから取得し送信
        print('bot> '+self.system.initial_message(input_dic)["utt"])

    def message(self):
        input_message = str(input('you> '))
        # 辞書型 inputにユーザからの発話とユーザIDを設定
        input_dic = {'utt': input_message, 'sessionId': str(0)}

        # replyメソッドによりinputから発話を生成
        system_output = self.system.reply(input_dic)

        # 発話を送信
        print('bot> '+system_output["utt"])

    def run(self):
        self.start()

        while True:
            self.message()
