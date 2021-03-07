import MeCab

mecab = MeCab.Tagger()

# バグ回避用にから文字をパースとのこと
mecab.parse('')

text = input(">")

node = mecab.parseToNode(text)
while node:
    print(node.surface, node.feature)
    node = node.next
