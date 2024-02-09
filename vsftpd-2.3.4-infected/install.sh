#!/usr/bin/env bash
useradd nobody
mkdir /usr/share/empty
cp /vsftpd/vsftpd /usr/local/sbin/vsftpd
cp /vsftpd/vsftpd.8 /usr/local/man/man8
cp /vsftpd/vsftpd.conf.5 /usr/local/man/man5
cp /vsftpd/vsftpd.conf /etc

mkdir /var/ftp
useradd -d /var/ftp ftp
chown root:root /var/ftp
chmod og-w /var/ftp
/usr/local/sbin/vsftpd

