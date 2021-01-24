# FTPからSFTPに変更する際に気づいたことまとめ

### 動機
- FTPからSFTPに移行する必要があり，その際調べたことをまとめようと思ったため

### 調べたこと
- データ送信時の形式について
  - FTPでは指定するオプションがあるが，SFTPにはなくバイナリとなっている
- 接続時のコマンドファイル作成の可否
  - FTPには無いが，SFTPにはオプション "-b コマンドファイル名" でコマンドファイル内に記載されたコマンドを実行することが可能．コマンドファイルにはコマンドを一行ごとに記載する．
- オプション "-b" を使用した際のSFTP挙動
  - もしコマンドの途中でエラーが見られた場合にはその時点でSFTPが終了する．その際のSTATUSはPIPESTATUSから参照することが可能であり，正常であれば0，以上があればそれ以外の値をとる．