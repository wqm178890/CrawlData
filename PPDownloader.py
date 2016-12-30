# -*- coding:utf-8 -*-

import urllib
import urllib2
import ssl
import re
import os
import chardet
import time
import sys
import MySQLdb
import Downloader
import time
import threading
from collections import namedtuple

httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
#urllib2.install_opener(opener)
DBName = 'crawldata'
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PWD = '123456'
DB_PORT = 3306
reload(sys)

def select_paper_data(start, end):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select detail_url, source_url, category, data_h from pp_wallpaper where data_h >= 900 limit %d,%d' % (start, end))
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error, e:
        print e

def main(output, url):
    start_time = time.time()
    FileInfo = namedtuple('FileInfo', 'url name size lastmodified')
    #url = "https://pixabay.com/get/e833b20c2cf5093ecd1f4600ee45479fe16ae3d11eb6134290f0c578/auto-1633418.jpg"
    Downloader.download(url, output)
    print '下载时间: %ds' % int(time.time() - start_time)

def get_device_name(height):
    if height == 2048:
        return "ipad"
    if height == 1024:
        return "ipad_mini"
    if height >= 900 and height < 1136:
        return "iphone4"
    elif height < 1300:
        return "iphone5"
    elif height < 1800:
        return "iphone6"
    else:
        return "iphone6p"

root_path = "G:/pp_wallpaper"
start_index = 1
def run(start, end):
    i = start
    try:
        results = select_paper_data(i, end)
        for result in results:
            i += 1
            print i
            detail_url = result[0]
            source_url = result[1]
            category = result[2]
            data_h = result[3]
            device_name = get_device_name(data_h)
            device_path = "%s/%s/" % (root_path, device_name)
            suffix = detail_url.split(".")[-1]
            if not os.path.exists(device_path):
                os.mkdir(device_path)
            category_path = "%s/%s/%s" % (root_path, device_name, category)
            if not os.path.exists(category_path):
                os.mkdir(category_path)
            max_img_path = "%s/%s/%s/%s_max.%s" % (root_path, device_name, category, Downloader.get_md5(source_url), suffix)
            min_img_path = "%s/%s/%s/%s_min.%s" % (root_path, device_name, category, Downloader.get_md5(source_url), suffix)
            print max_img_path
            print min_img_path
            main(max_img_path, detail_url)
            main(min_img_path, source_url)
    except Exception:
        run(i, end)

run(60001, 130000)
