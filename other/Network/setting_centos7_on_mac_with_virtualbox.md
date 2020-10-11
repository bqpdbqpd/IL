# setting centos7 on mac with virtualbox

### 動機
- Network周り（実機ではない部分）について詳しくないため，実際に設定して勉強するため

### やったこと
- Macの上でVirtuakBoxを用いてVM2台でネットワーク疎通が取れる環境の構築
  - pingで疎通が取れていることを確認

### 詰まったこと
- VirtuakBoxの設定で光学が優先されてHDDが読み込まれず，OSインストールが繰り返されたので，光学の優先度を下げる必要あり
- VirtuakBoxでcentos7が起動しなかった．
  - VirtuakBoxのバージョンを6.1から6.0にすると起動した．
- VM2台の内部ネットワークで疎通を通すためには，VirtuakBox上でネットワークの設定が必要だった．
  - 今回はNATネットワークを用いて設定した．
- 2代目のVMは1代目のVMをクローンして作成したため，IPが同じになっていた．
  - nmcliコマンドでenp0s3のIPを変更して対応
