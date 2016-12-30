# -*- coding:utf-8 -*-

import urllib
import urllib2
import ssl
import re
import os
import chardet
import time
import Downloader
import sys
import MySQLdb
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
#urllib2.install_opener(opener)
root_path = "D:/WallPapaer/"
DBName = 'crawldata'
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PWD = '123456'
DB_PORT = 3306
reload(sys)
sys.setdefaultencoding('utf8')
device_dic = {'64': [1920, 1080],
              '32': [1334, 750],
              '16': [1136, 640],
              '5': [960, 640],
              '4': [320, 480],
              '8': [2048, 2048],
              '2': [1024, 1024]}
def select_category_data():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select category, type_id from tongbu_wallpaper_category')

        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error, e:
        print e

def select_devices_data():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select device_id, device_name from tongbu_device')

        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error, e:
        print e

def insert_data(sql):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES utf8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e

def insert_sql(data_str):
    # sql = "insert into data (digest, content_url, cover, author, title, times) values %s" % (dataStr)
    sql = 'INSERT ignore INTO tongbu_wallpaper (data_w, data_h, detail_url, source_url, tag, likes, favorite, author, category, md5) VALUES  %s' % data_str
    return sql

def get_insert_data(data_w, data_h, detail_url, source_url, tag, like, favorite, author, category, md5):
    return '(%s, %s, \"%s\",  \"%s\", \"%s\", %s, %s, \"%s\", \"%s\", \"%s\"),' % (data_w, data_h, detail_url, source_url, tag, like, favorite, author, category, md5)

#获取页面html信息
def get_page(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
    #cookies = "_ga=GA1.2.567593064.1476934351; sessionid=\".eJxVzMsOgjAQheF3mTUhLdBO66sY00zpcFEuhrYbje8usjBhdTb_d97gJlr6TD3DBV4DFBAmuFylwgqtLaRGK6Tat64baW4FOMppcDny5gaKw66C5RAqwxa96ggFau6YDGr0nm1g3whbCanhhD21D17C7p_beuc2lTmNUyzbHNM6H2E5HulCM7t1czzTOP3d6Wz8_dRKa2EQPl-Sm0Uo:1bxQMZ:a-rGd6bduSUmmD0b1LAYeaUAMw4\"; client_width=1600; img_pp=100; g_rated=1; csrftoken=2xtbaa8dI1jIBA9m4icGfXcNabAUAiQdlosm98TbLQ9SOeeINVwbLdaGndnEff3O"
    headers = {
        "User-Agent": user_agent,
        "Connection": 'keep-alive'
    }

    print url
    #context = ssl._create_unverified_context()
    #ssl._create_default_https_context = ssl._create_unverified_context
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request, timeout=20)
        return response.read()
    except Exception, e:
        return None
        print 'error', e.message
        return get_page(url)

#解析HTML并返回关键信息   高度:宽度:详情地址：地址:标签
def get_contents(pageIndex, category, type_id, device_name, device_id):
    url = "http://app.tongbu.com/bizhi/%s-cateshow-%s-%s" % (device_name, type_id, pageIndex)
    page = get_page(url)
    #print page
    if page is None:
        return
    next_re = re.compile('<a.*?">下一页.*?</a>', re.S)
    
    result = re.search(next_re, page)
    if result is None:
        return None

    pattern = re.compile('<li>.*?class="pic".*?<img alt="(.*?)".*?src="(.*?)".*?<div class="downnum">(.*?)<.*?href="(.*?)">', re.S)
    items = re.findall(pattern, page)
    data_str = ""
    for item in items:
        source_url = item[1]
        detail_url = item[3]
        data_w = device_dic[device_id][1]
        data_h = device_dic[device_id][0]
        favorite = item[2].split(":")[-1]
        tag = item[0]
        like = favorite
        author = 'test321546'
        md5 = Downloader.get_md5(source_url)
        #print data_w, data_h, detail_url, source_url, tag, favorite, md5, '\n'
        data_str += get_insert_data(data_w, data_h, detail_url, source_url, tag, like, favorite, author, category, md5)
        #contents.append([data_w, data_h, detail_url, source_url, tag, like, favorite, comment, author])
    return data_str

#下载图片
def download_img(url, filename):
    urllib.urlretrieve(url, filename)

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

#根据分类下载分类下的所有图片
def download_by_type(category):
    download_path = "%s%s"%(root_path, category)
    create_dir(download_path)
    i = 1
    contents = get_contents(i, category)
    while not contents is None :
        i += 1
        contents = get_contents(i, category)

def main():
    print 'start'
    results = select_category_data()
    devices = select_devices_data()
    #for device in devices:
    device = devices[3]
    device_id = device[0]
    device_name = device[1]
    for result in results:
        category = result[0]
        type_id = result[1]
        for i in range(1, 1000):
            print i, ":", type_id, ":", device_id
            data_str = get_contents(i, category, type_id, device_name, device_id)
            if data_str is None:
                print 'can return'
                break
            data_str = data_str.rstrip(',')
            sql = insert_sql(data_str)
            insert_data(sql)
    #print "end"
if __name__ == '__main__':
    #create_dir(root_path)
    #print "%.f"%(time.time()*1000)
    main()
    # data_str = get_contents(13, 'buildings')
    # data_str = data_str.rstrip(',')
    # sql = insert_sql(data_str)
    # insert_data(sql)
    #get_detail_info(test_detail_url)