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
import json
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
        #count = cur.execute('select detail_url, source_url, category, data_h from wallpaper where data_w < data_h limit %d,%d' % (start, end))

        count = cur.execute('select detail_url, source_url, category, data_h, author from wallpaper GROUP BY author limit %d, %d '%(start, end))
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
    print url
    code = Downloader.download(url, output)
    if code == 400:
        return 400
    print '下载时间: %ds' % int(time.time() - start_time)
    return code

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

def get_download_urls(file_id):
    try:
        _url = "https://pixabay.com/api/?key=3589192-081aeb522d921b7cd7ae63922&lang=zh&id=%s" % file_id
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.3000 Chrome/47.0.2526.73 Safari/537.36"
        cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
        #cookies = "_ga=GA1.2.1025332067.1478178236; sessionid=\".eJxVi0sOwiAQQO_C2jS2HZqplyEDTAtawPDZaLy7tQuTbt_nLdRGcW20sriJlxMXoahVp1rhrBwVt2MYGZHYzCS1lYCwXBe5E9sjTDTp0eIAMNnz7O2-jhLnfh7ORpN5cPzpZ053NrVr1W-lM63UFI6w80caKbBKWXEgv_2_zxcJlz26:1c2KCA:x7dAJClbyz2x5s3ZHAKE-l2B_nA\"; client_width=1903"
        headers = {
            "User-Agent": user_agent,
            "Cookie": cookies,
            "Connection": 'keep-alive'
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib2.Request(_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        data = response.read()
        json_data = json.loads(data)
        webformat_url = json_data["hits"][0]["webformatURL"]
        key = webformat_url.split("/")[-1].split(".")[0].split("_")[0]
        return key[3:14]
    except Exception, e:
        print 'error', e
        return get_download_urls(file_id)

def download_urls(url):
    try:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.3000 Chrome/47.0.2526.73 Safari/537.36"
        cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
        #cookies = "_ga=GA1.2.1025332067.1478178236; sessionid=\".eJxVi0sOwiAQQO_C2jS2HZqplyEDTAtawPDZaLy7tQuTbt_nLdRGcW20sriJlxMXoahVp1rhrBwVt2MYGZHYzCS1lYCwXBe5E9sjTDTp0eIAMNnz7O2-jhLnfh7ORpN5cPzpZ053NrVr1W-lM63UFI6w80caKbBKWXEgv_2_zxcJlz26:1c2KCA:x7dAJClbyz2x5s3ZHAKE-l2B_nA\"; client_width=1903"
        headers = {
            "User-Agent": user_agent,
            "Cookie": cookies,
            "Connection": 'keep-alive'
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        real_url = response.geturl()
        session = real_url.split("/")[-2][-6:56]
        return session
    except Exception, e:
        print 'error', e
        return download_urls(url)


root_path = "G:/head_img"
start_index = 1

def get_filename(url_data):
    return url_data.split(",")[0].split(" ")[0].split("/")[-1].split("__")[0], url_data.split(",")[0].strip().split(" ")[0], url_data.split(",")[1].strip().split(" ")[0].split(".")[-1]

def run(start, end):
    i = start
    try:
        results = select_paper_data(i, end)
        session = "3ecd1f4600ee45479fe16ae3d11eb9124595f8c07f"
        for result in results:
            i += 1
            if i > end:
                return
            print i
            #detail_url = result[0]
            url_data = result[1]
            filename, detail_url, suffix = get_filename(url_data)
            file_id = filename.split("-")[-1]
            #code = get_download_urls(file_id)
            source_url = "https://pixabay.com%s" % detail_url
            #detail_url = "https://pixabay.com/get/e83%s%s/%s.%s" % (code, session, filename, suffix)
            download_url = "http://pixabay.com/zh/photos/download/%s.%s" % (filename, suffix)
            category = result[2]
            data_h = result[3]
            author = result[4]
            device_name = "Iphone"
            device_path = "%s/%s/" % (root_path, device_name)
            #suffix = detail_url.split(".")[-1]
            if not os.path.exists(device_path):
                os.mkdir(device_path)
            category_path = "%s/%s/%s" % (root_path, device_name, category)
            if not os.path.exists(category_path):
                os.mkdir(category_path)
            max_img_path = "%s/%s/%s/%s_max.%s" % (root_path, device_name, category, Downloader.get_md5(source_url), suffix)
            min_img_path = "%s/%s.%s" % (root_path, author, suffix)

            main(min_img_path, source_url)
            # code = main(max_img_path, detail_url)
            # if code == 400:
            #     print download_url
            #     session = "3ecd1f4600ee45479fe16ae3d11eb9124595f8c07f"
            #     # while session == "wnload":
            #     #     time.sleep(60 * 20)
            #     #     session = download_urls(download_url)
            #     print session
            #     detail_url = "https://pixabay.com/get/se83%s%s/%s.%s" % (code, session, filename, suffix)
            #     print detail_url
            #     main(max_img_path, detail_url)
            #time.sleep(10)
    except Exception:
        run(i, end)

run(33000, 40000)

# https://pixabay.com/get/e832b5092ef6003 ecd1f4600ee45479fe16ae3d11eb913469 4f2c57e/thermometer-galilee-1674323.jpg
# https://pixabay.com/get/e832b20c2bf2043 ecd1f4600ee45479fe16ae3d11eb913469 4f2c57e/woman-1701625.jpg
# https://pixabay.com/get/e833b60b2bf6023 ecd1f4600ee45479fe16ae3d11eb913469 4f7c07f/thermometer-galilee-1674323.jpg
# https://pixabay.com/get/e833b60b2bf6023 ecd1f4600ee45479fe16ae3d11eb913469 4f9c57d/thermometer-galilee-1674323.jpg
# https://pixabay.com/get/e832b3062cf3013ecd1f4600ee45479fe16ae3d11eb913469 7f4c57e/science-1729470.png
# https://pixabay.com/get/e832b3062cf3013ecd1f4600ee45479fe16ae3d11eb913469 7f4c671/science-1729470.png