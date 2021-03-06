# Setting_Network (iptables, ftp, nfs)
### 背景
- ネットワークのFW周りやアクセス権限・管理に関わることになったため勉強

### 目的
- iptables, ftp, nfsの設定ができるようになる

### 参考先
- iptablesの設定：https://qiita.com/hitobb/items/3ca7f47f7904f88c47be
- ループバックアドレス：https://milestone-of-se.nesuke.com/nw-basic/as-nw-engineer/loopback-address-interface/
- iptablesのオプション：https://kazmax.zpp.jp/cmd/i/iptables.8.html
- iptablesでのnfsの設定：https://www.cyberciti.biz/faq/centos-fedora-rhel-iptables-open-nfs-server-ports/
- ftpのanonyousログインを禁止にする：http://manpages.ubuntu.com/manpages/bionic/ja/man5/vsftpd.conf.5.html
- FTPで接続できるIPアドレスの制限：https://www.searchman.info/tips/1480.html
- FTPの制限設定：http://park1.wakwak.com/~ima/centos4_vsftpd0001.html

### 事前準備
- ホストOSがWindows10，virtualBoxでUbuntu20をゲストOSの環境を作成
- ホストとゲストの関係にはホストオンリーアダプターを設定し，ホストゲスト間をつなぐ

### iptables

iptables -F\
iptables -t nat -F

iptables -P INPUT ACCEPT\
iptables -P FORWARD DROP\
iptables -P OUTPUT ACCEPT

iptables -A INPUT -p tcp --dport 2049 -j DROP

iptables -A INPUT -s 対象IPアドレス/マスク -m state --state NEW -p tcp --dport 2049 -j ACCEPT
