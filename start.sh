#!/bin/bash
# Author：RYB

performanceTestPath=`pwd`

# create server
echo "
[Unit]
Description=Job that runs your user script

[Service]
ExecStart= /bin/bash -c 'nohup python $performanceTestPath/main.py &'
Type=forking
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target" > /lib/systemd/system/performanceTest.service

# chmod
chmod 644 /lib/systemd/system/performanceTest.service

# /etc/performanceTest
mkdir /etc/performanceTest
mv performanceTest /etc/performanceTest

# pip
pip install pymysql configparser psutil

# start server
systemctl daemon-reload
systemctl enable performanceTest.service
systemctl restart performanceTest.service
systemctl status performanceTest.service


