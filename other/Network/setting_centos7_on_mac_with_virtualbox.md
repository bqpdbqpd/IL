# setting centos7 on mac with virtualbox

### 動機
- Network周り（実機ではない部分）について詳しくないため，実際に設定して勉強するため

### やったこと
- MacOSの上にVirtuakBoxを用いてCentOS7のVMを作成
- Macの上でVirtuakBoxを用いてVM4台でネットワーク疎通が取れる環境の構築
  - pingで疎通が取れていることを確認
- VM間のネットワーク構築
  - Virtualbox上で，ネットワークの設定で，NATと内部ネットワークを使用するようにする
  - nmcliコマンドでenp0s8のIPを変更して対応

    ```
    # nmcli device status
    # nmcli connection modify enp0s8 connection.autoconnect yes
    # nmcli connection modify enp0s8 ipv4.method manual ipv4.addresses 任意のIPアドレス/任意のマスク
    # systemctl restart NetworkManeger
    # systemctl restart network
    ```


### 詰まったこと
- VirtuakBoxの設定で光学が優先されてHDDが読み込まれず，OSインストールが繰り返されたので，光学の優先度を下げる必要あり
- VirtuakBoxでcentos7が起動しなかった．
  - VirtuakBoxのバージョンを6.1から6.0にすると起動した．
- VM2台の内部ネットワークで疎通を通すためには，VirtuakBox上でネットワークの設定が必要だった．
  - 今回はNATネットワークを用いて設定した．
    - NATネットワークではVM間の疎通が取れなかったので，ホストオンリーアダプターと内部ネットワークを使用した．が上手くいかなかった．
      - NATネットワークと内部ネットワークを使用するといけた．
- 2代目のVMは1代目のVMをクローンして作成したため，IPが同じになっていた．
