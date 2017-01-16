# -*- coding:utf-8 -*-


import urllib2
import os
import Downloader
import time
from collections import namedtuple
import MySQLdb
import urlparse

DBName = 'db_news1'
DB_HOST = '101.200.74.101'
DB_USER = 'myuser'
DB_PWD = '123456'
DB_PORT = 3306

slq = "select url_3w, boardid from tb_news where url_3w like '%biz%' and boardid is not null group by source"

# start_time = time.time()
# FileInfo = namedtuple('FileInfo', 'url name size lastmodified')
# url = "https://pixabay.com/get/e833b20c2cf5093ecd1f4600ee45479fe16ae3d11eb6134290f0c578/auto-1633418.jpg"
# output = "/Users/nd/Desktop/Test2.jpg"
# Downloader.download(url, output)
# print '下载时间: %ds' % int(time.time() - start_time)
def select_paper_data():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute(slq)
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error, e:
        print e

def update_paper_data(results):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        for result in results:
            url_3w = result[0]
            boardid = result[1]
            result = urlparse.urlparse(url_3w)
            params = urlparse.parse_qs(result.query, True)
            biz = params['__biz'][0]
           # md5 = Downloader.get_md5(source_url)
            sql = 'update tb_wechat set biz=\'%s\' where account=\'%s\'' % (biz, boardid)
            #print sql
            cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error, e:
        print e

appid = 2
coopen_id = 3 
source_list_id = 4
source_detail_id = 5
file_object = open('E:/tst.xml', 'w')
file_object.write("<?xml version=\"1.0\"?><values><key>应用</key><value>%s</value><key>开屏</key><value>%s</value><key>原生列表</key><value>%s</value><key>原生详情</key><value>%s</value></values>"%(appid, coopen_id, source_list_id, source_detail_id))
file_object.close( )  

                                                                         #windows下为：d:\data\query_text\EL_00154

#results = select_paper_data()
#update_paper_data(results)
#print Downloader.get_md5("http://img.25pp.com/uploadfile/bizhi/iphone6p/20160817/1471396483909209_390x690.jpg")
#update_paper_data(select_paper_data())
#print "%.f"%(time.time()*1000)
