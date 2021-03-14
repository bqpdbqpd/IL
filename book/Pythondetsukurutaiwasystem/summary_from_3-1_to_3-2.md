# Pythonで作る対話システムの2章までやってみた

### 背景
- 言語処理を使ったシステムを何か作ってみたくなったため
- いきなり自力では作れないので，何か写経してシステム作成イメージが欲しかった
- タスク指向型の部分は写経して確認したので，非タスク指向の方も進める

### やったこと
- 3-1から3-2までの確認・写経
- 今回もプログラム内に利用するには登録が必要なAPIがあったが，個人的に登録が面倒なので登録なしでターミナル上に似たような結果が得られるようにした．

### 概要
- 非タスク指向型対話システムとは？
  - 対話することが目的のシステム
- このシステムは必要？
  - 必要：雑談によって，タスクが向上したとの研究報告がある
  - 対話に必要な情報が得られる
- ルールベース方式
  - 入力された文に対する返答をまとめたファイルを事前に作成
    - マークアップ言語のArtifical Intelligence Markup Language (AIML) を用いてルールをまとめる
  - ルールに基づいて返答を返す

### 変更した内容
- 今回もチャットアプリを使用せず，プログラムを実行したターミナルで対話が行われるようにした.
- 以下は編集したソースコード．ロードしているaiml.xmlは[こちら](https://github.com/dsbook/dsbook/blob/master/aiml.xml)で公開されている．

```python
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
```

### 感想
- ルール通りに動いているだけとわかっていても対話してくると，機械的ではない対話をしているような感覚があって面白かった．
- チャットAPIを使わない方法も公開してくださっている事に今更気づいた．．．次回から[こちら](https://github.com/dsbook/dsbook/blob/master/README_console_bot.md)で勉強していく．

### 次にやること
- 非タスク試行型対話システムである3.2章以降を進める
