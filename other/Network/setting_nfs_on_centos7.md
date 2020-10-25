# CentOS7 上での NFS の設定

### 背景
NFSの制限設定について詳しくないため，勉強

### やったこと
- FTPで接続できるIPアドレスの制限
  - TCP Wrapper の設定
  ```
# vi /etc/hosts.deny
rpcbind : ALL
locked : ALL
mountd : ALL
stated : ALL
```
```
# vi /etc/hosts.allow
rpcbind : 対象のIPアドレス/マスク
locked : 対象のIPアドレス/マスク
mountd : 対象のIPアドレス/マスク
stated : 対象のIPアドレス/マスク
```
  - iptablesの設定\
  ```
  # vi /etc/sysconfig/iptables
  #以下の2行をINPUTの下から3行目に追加する．
  基から記述されているINPUT部分の下部2行は
  全ての通信を通さないとしているのでこれより上に設定する必要あり
#行頭の\は表示の都合上いれたので無視．対応方法わからず......
\-A INPUT -s 対象のIPアドレス -p tcp --dport 21 -j ACCEPT
\-A INPUT -p tcp --dport 21 -j DROP
```

- 設定の反映\
マシンの起動時に自動反映するように設定
```
# systemctl enable nfs
# systemctl enable rpcbind
```
- 手動で実行・停止・再起動の方法
```
# systemctl start nfs
# systemctl start rpcbind

# systemctl stop nfs
# systemctl stop rpcbind

# systemctl restart nfs
# systemctl restart rpcbind
```

### 参考先
- iptablesの設定：https://qiita.com/hitobb/items/3ca7f47f7904f88c47be
- ループバックアドレス：https://milestone-of-se.nesuke.com/nw-basic/as-nw-engineer/loopback-address-interface/
- iptablesのオプション：https://kazmax.zpp.jp/cmd/i/iptables.8.html
- iptablesでのnfsの設定：https://www.cyberciti.biz/faq/centos-fedora-rhel-iptables-open-nfs-server-ports/
