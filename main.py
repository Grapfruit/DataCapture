#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
main
"""
__author__ = 'RYB'

import os
import time
import pymysql
import logging
from conf import conf
from mysql import mysql
from ycsb import mongoTest

ip = conf.getValue('database', 'ip')
port = int(conf.getValue('database', 'port'))
username = conf.getValue('database', 'username')
password = conf.getValue('database', 'password')
dbname = conf.getValue('database', 'dbname')
mongo_logPath = conf.getValue('ycsb', 'logPath')
mongo_logName = conf.getValue('ycsb', 'logName')
timeInterval = float(conf.getValue('ycsb', 'interval'))
performanceTest_logPath = conf.getValue('default', 'logPath')
performanceTest_logName = '%s/%s' % (conf.getValue('default', 'logPath'), conf.getValue('default', 'logName'))

try:
    os.makedirs(performanceTest_logPath)
    os.mknod(performanceTest_logName)
except Exception:
    pass

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(performanceTest_logName)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

db = pymysql.connect(
    host = ip,
    user = username,
    password = password,
    port = port,
    database = dbname
)
mysql.creat(db, 'mongoTest_data', logger)
db.close()

# for file in mongo_logName.split(','):
file = mongo_logName
file = '%s/%s' % (mongo_logPath, file.strip())
lastPosition = 0

while True:
    while mongoTest.checkTestStatus(logger):
        db = pymysql.connect(
            host = ip,
            user = username,
            password = password,
            port = port,
            database = dbname
        )
        mongoData = mongoTest.dataFilter(file, logger, lastPosition)
        for i in mongoData[1]:
            try:
                mysql.write(db, 'mongoTest_data', i['time'], i['iops'], i['readLatency'], i['insertLatency'], i['updateLatency'], logger)
            except Exception as e:
                logger.error(e)
        lastPosition = mongoData[0]
        if not mongoTest.checkTestStatus(logger):
            nowTime = int(time.time())
            try:
                mysql.write(db, 'mongoTest_data', nowTime, 0, 0, 0, 0, logger)
            except Exception as e:
                logger.error(e)
        db.close()
    time.sleep(timeInterval)




