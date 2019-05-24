#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Conf
"""
__author__ = 'RYB'

import configparser

'''
get value from conf
'''
def getValue(section, key, path="/etc/performanceTest/performanceTest.conf"):
    conf = configparser.ConfigParser()
    try:
        conf.read(path)
        value = conf.get(section, key)
    except Exception as e:
        pass
    try:
        return value
    except Exception:
        print "Config value get fail: %s - %s" % (section, key)


