# -*- coding: utf-8 -*-
import os
import urlparse
import urllib2
import sys
import json
import MySQLdb
import re
import jieba
import math
import thread
import time
import hashlib
from Queue import Queue
import threading
from threading import Thread
from automatormonkey.monkeyrunnercore.MonkeyRunner import rMonkeyRunner
from automatormonkey.monkeyrunnercore.info.Enum import *

reload(sys) 
sys.setdefaultencoding('utf8')
type = sys.getfilesystemencoding()

DBName = 'db_news1'
DB_HOST = '101.200.74.101'
DB_USER = '5hito'
DB_PWD = 'Com.5hito91.com'
DB_PORT = 3306
path = 'c://Sessions.txt'

def get_proxy_ip():
    headers = {
            'Host': 'www.xicidaili.com',
            'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Accept': r'application/json, text/javascript, */*; q=0.01',
            'Referer': r'http://www.xicidaili.com/',
            }
    req = urllib2.Request(r'http://www.xicidaili.com/nn/', headers=headers)
    response = urllib2.urlopen(req)
    html = response.read().decode('utf-8')
    proxy_list = []
    ip_list = re.findall(r'\d+\.\d+\.\d+\.\d+',html)
    port_list = re.findall(r'<td>\d+</td>',html)
    for i in range(len(ip_list)):
        ip = ip_list[i]
        port = re.sub(r'<td>|</td>', '', port_list[i])
        proxy = '%s:%s' %(ip,port)
        proxy_list.append(proxy)
    return proxy_list

proxy_list = get_proxy_ip()


def parserUrl(url):
    print 'start parserUrl'
    result = urlparse.urlparse(url)
    params = urlparse.parse_qs(result.query, True)
    print 'end parserUrl'
    return params['__biz'][0], params['uin'][0], params['key'][0]


def generatorJsonUrl(biz, uin, key):
    format = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s&uin=%s&key=%s&f=json&frommsgid=1000010000&count=10000'
    return format % (biz, uin, key)

def createDB():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')

        createTable = "CREATE TABLE IF NOT EXISTS data (id int(11) NOT NULL auto_increment,digest text,content_url varchar(255) default NULL,cover varchar(255) default NULL,author varchar(50) default NULL,title text,times double DEFAULT NULL, UNIQUE KEY content_url (content_url), KEY id (id)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

        cur.execute('create database if not exists CrawlData')
        cur.execute('set character_set_server=\'utf8\'')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        cur.execute(createTable)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print e


def getInsertSql(dataStr):
    # sql = "insert into data (digest, content_url, cover, author, title, times) values %s" % (dataStr)

    sql = 'INSERT ignore INTO tb_news (postid, url_3w, digest, title,source, lmodify, imgsrc, ptime,keywords, ltype, boardid) VALUES  %s' % (
    dataStr)
    return sql


def selectIDData(start, end):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select name, tag, account,biz from tb_wechat where biz is not null limit %d, %d' % (start, end))

        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results

    except MySQLdb.Error, e:
        print e


def insertData(sql):
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


def getMD5(str):
    m = hashlib.md5()
    m.update(str)
    md5 = m.hexdigest()
    return md5

def check_url(url):
    ip_list = re.findall(r'\d+\.\d+\.\d+\.\d+',url)
    if len(ip_list) >0:
        url = url.replace(ip_list[0]+'/', '')   
    return url

def getInsertData(item, ptime, source, ltype, boardid):
    title = item['title'].replace('amp;', '').replace('quot;', '').replace('&', '').replace('nbsp;', '')
    try:
        highpoints = re.compile(u'[\u00010000-\u0010FFFF]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    title = re.sub(highpoints, '', title)
    digest = item['digest'].replace('amp;', '').replace('quot;', '').replace('&', '').replace('nbsp;', '')
    digest = re.sub(highpoints, '', digest)
    url_3w = item['content_url'].encode('utf-8').replace('amp;', '')
    url_3w = check_url(url_3w)
    imgsrc = item['cover'].encode('utf-8').replace('amp;', '')
    imgsrc = check_url(imgsrc)
    postid = getMD5(url_3w)
    lmodify = int(math.floor(time.time()))
    strs = re.sub(u'[^\u4e00-\u9fa5_a-zA-Z0-9_\s]', '', title)
    result = jieba.cut(strs)
    keywords = ",".join(result).replace(' ,', "")
    return '(\'%s\', \'%s\', \'%s\',  \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\'),' % (
    postid, url_3w, digest, title, source, lmodify, imgsrc, ptime, keywords, ltype, boardid)
    # return '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\'),' % (digest, content_url, cover, author, title, times)


def parserJson(text, source, tag, account):
    try:
        #print "start insertData"
        text = text.replace("\"{", "{").replace("}\"", "}").replace('\\\\\\\\', '').replace("\\\"", "\"").replace('\\\\\\', '\\\\')
        text = re.sub(u'\\{7}', '', text)
        values = ""
        #print text.decode('utf-8').encode(type)
        data = json.loads(text.decode("utf-8"))
        #print data
        if data['ret'] == -3:
            print 'no session'
            return 'no session'
        if data['ret'] == -6:
            return "reset"
        dataList = data['general_msg_list']['list']
        for i in range(len(dataList)):
            try:
                item = dataList[i]['app_msg_ext_info']
            except KeyError, e:
                continue
            times = dataList[i]['comm_msg_info']['datetime']
            if item['title'] != "":
                values += getInsertData(item, times, source, tag, account)
            itemList = dataList[i]['app_msg_ext_info']['multi_app_msg_item_list']
            for j in range(len(itemList)):
                values += getInsertData(itemList[j], times, source, tag, account)
        sql = getInsertSql(values.rstrip(','))
        # print sql.decode('utf-8').encode(type)
        insertData(sql)
        #print "end insertData"
    #return "OK"
    except Exception, e:
        print "error_parser:", e, data
    return "OK"


def getSessionCookies(path):
    f = open(path, 'r')
    session = ""
    cookies = ""
    ls = [line.strip() for line in f]
    for i in ls:
        if i.find('Request url:') != -1:
            session = i.replace('Request url:', '').strip()
        if i.find('Cookie:') != -1:
            cookies = i.replace('Cookie:', '').strip()
    f.close()
    time.sleep(0.1)
    return session, cookies

# results = selectIDData()
# length = len(results)

lock = threading.Lock()


# createDB()

# urlpath = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA5ODE1MzA5Mg==&uin=MTU0ODA1NTIyMQ%3D%3D&key=c50f8b988e61749a12bccf95341ac62c0287d2974051bc4a650fdb234f4db9ab5714c1e1511959c757e979c3ad4d52478c10f488fc34c603&devicetype=android-21&version=26031732&lang=zh_CN&nettype=WIFI&ascene=3&pass_ticket=5ajTshLU%2B6TcY8NmVCNvx64AtilwKrVDMlepFKGAipXySw2z1j9LsFyIKTEcE14n'
# biz, uin, key = parserUrl(urlpath)
# print generatorJsonUrl(biz, uin, key)

def request_data(result, proxy_index):
    source = result[0]
    tag = result[1]
    account = result[2]
    biz = result[3]
    session, cookies = getSessionCookies(path)
    _biz_out, uin, key = parserUrl(session)
    print biz, uin, key
    url = generatorJsonUrl(biz, uin, key)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36'
    headers = {
        'Cookie': cookies,
        'User-Agent': user_agent}
    print url
    try:
        #print 'start crawl'
        if proxy_index > 0:
            proxy_support = urllib2.ProxyHandler({'http': proxy_list[proxy_index]})
            print proxy_list[proxy_index]
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        content = response.read().decode('utf-8')
        #print 'end crawl'
        print content
        # pattern = re.compile("<pre.*?>(.*?)</pre>")
        # items = re.findall(pattern, content)
        if parserJson(content, source, tag, account) == 'reset':
            print "reset"
            #time.sleep(30)
            request_data(result, proxy_index + 1)
    except Exception, e:
        print 'error', e
        request_data(result, proxy_index + 1)

def crawldata(start, end, i):
    start_time = time.time()
    results = selectIDData(start, end)
    length = len(results)
    # global _session
    # global _cookies
    start_index = 0
    start_path = "c:/start%d.txt"%i
    if os.path.exists(start_path):
        f = open(start_path, 'r')
        start_index = int(f.read())
        f.close()

    for i in range(start_index, length):
        files = open(start_path, 'w')
        files.write('%d'%i)
        files.close()
        result = results[i]
        while True:
            time.sleep(0.3)
            if os.path.exists(path):
                request_data(result, 0)
                break
    files = open(start_path, 'w')
    files.write(str(1))
    files.close()


class jsonParser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            crawldata()
            self.stop()

    def stop(self):
        self.thread_stop = True


def main():
    print ""

threads = []
if __name__ == '__main__':
    #main()

    count = 10
    total = 1200
    start = time.time()
    for i in range(0, count):
        start = i * total/count
        end = start + total/count + 2
        thread = threading.Thread(target=crawldata, args=(start, end, i, ))
        threads.append(thread)
        #main(result)
    for t in threads:
        #t.setDaemon(True)
        t.start()
    t.join()

    #crawldata(0, 1200)
    end = time.time()
    print (end - start)