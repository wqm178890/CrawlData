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
import threading

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
def select_category_data():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select category from wallpaper_category')

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
    sql = 'INSERT ignore INTO wallpaper (data_w, data_h, detail_url, source_url, tag, likes, favorite, author, category) VALUES  %s' % data_str
    return sql

def get_insert_data(data_w, data_h, detail_url, source_url, tag, like, favorite, author, category):
    return '(%s, %s, \"%s\",  \"%s\", \"%s\", %s, %s, \"%s\", \"%s\"),' % (data_w, data_h, detail_url, source_url, tag, like, favorite, author, category)

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
    ssl._create_default_https_context = ssl._create_unverified_context
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request, timeout=20)
        return response.read()
    except Exception, e:
        print 'error', e.message
        return get_page(url)

#获取详情页信息
def get_detail_info(url):
    #print page
    page_info = get_page(url)
    #print page_info
    # camera_re = re.compile('<a href="/zh/cameras/.*?">(.*?)</a>.*?>(.*?)</div> ', re.S)
    # camera = re.findall(camera_re, page_info)
    # print camera
    #print page_info
    table_re = re.compile('<table id="details">(.*?)</table>', re.S)
    table = re.findall(table_re, page_info)[0]

    td_re = re.compile('<tr>.*?<td>(.*?)</td>', re.S)
    tdList = re.findall(td_re, table)
   # print tdList
    if len(tdList) >= 7:
        pic_type = tdList[0]
        dpi = tdList[1]
        create_time = tdList[2]
        upload_time = tdList[3]
        category = tdList[4]
        view = tdList[5]
        download = tdList[6]
    else:
        pic_type = tdList[0]
        dpi = tdList[1]
        create_time = time.time()
        upload_time = tdList[2]
        category = tdList[3]
        view = tdList[4]
        download = tdList[5]

    print pic_type, dpi.decode('utf-8'), create_time, upload_time.decode('utf-8'), category, view, download

#解析HTML并返回关键信息   高度:宽度:详情地址：地址:标签
def get_contents(pageIndex, category):
    url = "https://pixabay.com/zh/photos/?cat=%s&pagi=%d" % (category, pageIndex)
    page = get_page(url)
    #print page
    page_re = re.compile('<input name="pagi".*?>(.*?)<', re.S)
    pageItems = re.findall(page_re, page)
    total_page = pageItems[0].strip().split(' ')[-1].split('&')[0]
    print total_page
    if int(total_page) < pageIndex:
        return None

    pattern = re.compile('<div class="item".*?data-w="(.*?)".*?data-h="(.*?)".*?<a href="(.*?)".*?<img.*?srcset="(.*?)".*?alt="(.*?)".*?</a>.*?<i.*?</i>(.*?)<i.*?</i>(.*?)<i.*?</i>(.*?)</div>.*?<a.*?>(.*?)</a>', re.S)
    items = re.findall(pattern, page)
    contents = []
    #print items
    data_str = ""
    for item in items:
        data_w = item[0]
        data_h = item[1]
        detail_url = item[2]
        source_url = item[3]
        tag = item[4]
        like = item[5].strip()
        favorite = item[6].strip()
        comment = item[7].strip()
        author = item[8].strip()
        #print data_w, data_h, detail_url, source_url, tag.decode('utf-8'), chardet.detect(tag), like, favorite, comment, author, '\n'
        data_str += get_insert_data(data_w, data_h, detail_url, source_url, tag, like, favorite, author, category)
        contents.append([data_w, data_h, detail_url, source_url, tag, like, favorite, comment, author])
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

def main(_result):
    print 'start'
    for i in range(1, 1000):
        print i, ":", _result
        data_str = get_contents(i, _result)
        if data_str is None:
            print 'can return'
            break
        data_str = data_str.rstrip(',')
        sql = insert_sql(data_str)
        insert_data(sql)
    print "end"
test_detail_url = 'https://pixabay.com/zh/%E5%A5%B3%E5%AD%A9-%E5%8E%9F%E9%87%8E-%E5%A5%B3%E6%80%A7-%E6%97%A5%E8%90%BD-%E9%A3%8E%E6%A0%BC-%E6%A8%A1%E5%9E%8B-%E5%A5%B3%E5%AD%90-%E5%B9%B4%E8%BD%BB-%E6%80%A7%E6%84%9F-1733368/'
if __name__ == '__main__':
    create_dir(root_path)
    results = select_category_data()
    threads = []

    for result in results:
        result = result[0]
        thread = threading.Thread(target=main, args=(result, ))
        threads.append(thread)
        #main(result)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print "all end"
