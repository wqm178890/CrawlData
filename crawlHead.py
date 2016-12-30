# -*- coding: utf-8 -*-
import os
import urlparse
import urllib2
import sys
import json
import MySQLdb
import re
import time
import hashlib
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *

deviceName='1'
device=rMonkeyRunner(__file__,deviceName)
FLAG.SCREENSHOT=False

DBName = 'db_news'
DB_HOST = '101.200.74.101'
DB_USER = 'myuser'
DB_PWD = '123456'
DB_PORT = 3306
headPath = 'C:/mmhead.txt'
def selectIDData():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        conn.select_db(DBName)  
        count = cur.execute('select name, tag, account from tb_wechat LIMIT 500 OFFSET 0;')

        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
        
    except MySQLdb.Error, e:
        print e

def testcase(id):
    device.input(id)
    #device.click(UIELEMENT.TEXT, '搜索')
    device.press('KEYCODE_ENTER')
    device.press('KEYCODE_ENTER')
    device.sleep(2.0)    
    device.click(UIELEMENT.SID, 'com.tencent.mm:id/g_')
    
def insertHeadData(sql):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        conn.select_db(DBName)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e   
        
def updatedata(account):
    if os.path.exists(headPath):
        print headPath
        f = open(headPath, 'r')
        url = f.readline()
        f.close()
        os.remove(headPath)
        sql = 'UPDATE tb_wechat SET icon=\'%s\' WHERE account = \'%s\'' % (url, account)
        print sql
        insertHeadData(sql)  
        
print 'start'
results = selectIDData()
length = len(results)
start = 1
startPath = 'D://start.txt'
if os.path.exists(headPath):
    os.remove(headPath)
    
if os.path.exists(startPath):
    f = open(startPath, 'r')
    start = int(f.read())
    f.close()

def main():
    for i in range(start, length):
        files = open(startPath, 'w')
        files.write('%d' % i)
        files.close()    
        result = results[i]
        print i, ":", result[2]      
        testcase(result[2])
        updatedata(result[2])
main()


