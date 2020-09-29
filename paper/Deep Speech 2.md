# Deep Speech 2: End-to-End Speech Recognition in English and Mandarin
- https://arxiv.org/pdf/1512.02595.pdf

## 何を良くした？
- 処理をGPUを並列で一つずつ使い，処理を早めた
- 精度も以前より40％ほど上がった

## なぜ良くした？
- モデルの計算時間を減らすため

## 方法は？
- 最大11層のアーキテクチャ
- 双方向再帰層と畳み込み層
- RNNのためのバッチノーマライゼーションとSoraGradを使用し，計算時間を削減
- 損失関数にCTCを使用
- 評価方法は，英語ではWord Error Rate，北京語ではCharacter Error Rateで行っている

## 感想
- 音声データの増強方法
  - 雑音の付加
  - 話者の声帯長や発話率の変化をシミュレート
  - ブートストラップ
- バッチノーマライゼーションが何かを調べ，確認する必要あり．

### 3.2まで既読
