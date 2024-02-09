#!/usr/bin/bash
mkdir /usr/share/empty
cp /vuln/vsftpd /usr/local/sbin/
cp /vuln/vsftpd.conf /etc/
cp /vuln/flag /root/
useradd ftp
/usr/local/sbin/vsftpd &

