#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
ycsb mongo log
"""
__author__ = 'RYB'

import os
import re
import time
import psutil

'''
input:
2019-03-25 02:06:35:407 4591 sec: 20000000 operations; 265.04 current ops/sec; [READ AverageLatency(us)=3918.74] [CLEANUP AverageLatency(us)=12787] [INSERT AverageLatency(us)=3144.71] [UPDATE AverageLatency(us)=3908.52]  

return:
(1, [{'readLatency': 3918.74, 'updateLatency': 3908.52, 'iops': 265.04, 'insertLatency': 3144.71, 'time': 1553479595}])
'''
def dataFilter(dataLog, logger, lastPosition=0):
    record = []
    try:
        with open(dataLog, 'r') as f:
            f.seek(lastPosition)
                for line in f:
                if re.match(r'^\d\d\d\d-', line):
                    getTime = re.search(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d', line).group()
                    unixTimestamp = int(time.mktime(time.strptime(getTime, "%Y-%m-%d %H:%M:%S")))
                    try:
                        iops = float(re.findall(r'; (.*?) current ops/sec;', line)[0])
                    except Exception:
                        iops = 0
                    try:
                        readLatency = float(re.findall(r'\[READ AverageLatency\(us\)=(.*?)\]', line)[0])
                    except Exception:
                        readLatency = 0
                    try:
                        insertLatency = float(re.findall(r'\[INSERT AverageLatency\(us\)=(.*?)\]', line)[0])
                    except Exception:
                        insertLatency = 0
                    try:
                        updateLatency = float(re.findall(r'\[UPDATE AverageLatency\(us\)=(.*?)\]', line)[0])
                    except Exception:
                        updateLatency = 0
                    record.append({'time':unixTimestamp, 'iops':iops, 'readLatency':readLatency, 'insertLatency':insertLatency, 'updateLatency':updateLatency})
                    logger.info('Get mongo data: %s' % record)
            lastPosition = f.tell()
        return lastPosition, record
    except Exception:
        logger.error('open file fail: %s' % dataLog)
        return False


'''
check if mongo test is running, if running, return True
'''
def checkTestStatus(logger):
    for pid in psutil.pids():
        try:
            pidCmd = ' '.join(psutil.Process(pid).cmdline())
            if 'ycsb' in pidCmd:
                if 'mongo' in pidCmd:
                return True
        except Exception:
            logger.warning('Get pid info fail: %d' % pid)


