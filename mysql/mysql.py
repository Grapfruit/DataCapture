#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
mysql
"""
__author__ = 'RYB'

import pymysql

'''
create table to storage mongo test data
'''
def creat(db, table, logger):
    cursor = db.cursor()
    try:
        sql = """CREATE TABLE %s (
            id int AUTO_INCREMENT,
            time int NOT NULL,
            iops int NOT NULL,
            readLatency int NOT NULL,
            insertLatency int NOT NULL,
            updateLatency int NOT NULL,
            PRIMARY KEY (`id`)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8 """ % table
        cursor.execute(sql)
        db.commit()
        logger.info('create success: %s.%s' % (db, table))
    except Exception as e:
        logger.error(e)
        db.rollback()

'''
storage mongo test data to db
'''
def write(db, table, time, iops, readLatency, insertLatency, updateLatency, logger):
    cursor = db.cursor()
    try:
        sql = """INSERT INTO %s (time, iops, readLatency, insertLatency, updateLatency) 
            VALUES ('%s', '%s', '%s', '%s', '%s')""" % (table, time, iops, readLatency, insertLatency, updateLatency)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        logger.error(e)
        db.rollback()


def read(connection, sql):
    pass


