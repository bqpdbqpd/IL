# CentOS7 上でのFTPの設定

### 背景
FTPの制限設定について詳しくないため，勉強

### やったこと
- FTPで接続できるIPアドレスの制限
  - TCP Wrapper の設定
  ```
# vi /etc/hosts.deny
vsftpd: ALL
```
```
# vi /etc/hosts.allow
vsftpd: 対象のIPアドレス
```
  - iptablesの設定\
  ```
  # vi /etc/sysconfig/iptables
  #以下の2行をINPUTの下から3行目に追加する．
  基から記述されているINPUT部分の下部2行は
  全ての通信を通さないとしているのでこれより上に設定する必要あり
#行頭の\は表示の都合上いれたので無視．対応方法わからず......
\-A INPUT -s 対象のIPアドレス -p tcp --dport 2049 -j ACCEPT
\-A INPUT -p tcp --dport 2049 -j DROP
```

- 設定の反映\
マシンの起動時に自動反映するように設定
```
# systemctl enable vsftpd
```
- 手動で実行・停止・再起動の方法
```
# systemctl start vsftpd
# systemctl stop vsftpd
# systemctl restart vsftpd
```

### 参考先
- iptablesの設定：https://qiita.com/hitobb/items/3ca7f47f7904f88c47be
- ループバックアドレス：https://milestone-of-se.nesuke.com/nw-basic/as-nw-engineer/loopback-address-interface/
- iptablesのオプション：https://kazmax.zpp.jp/cmd/i/iptables.8.html
- ftpのanonyousログインを禁止にする：http://manpages.ubuntu.com/manpages/bionic/ja/man5/vsftpd.conf.5.html
- FTPで接続できるIPアドレスの制限：https://www.searchman.info/tips/1480.html
- FTPの制限設定：http://park1.wakwak.com/~ima/centos4_vsftpd0001.html
