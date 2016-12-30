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
deviceName = '1'
device = rMonkeyRunner(__file__, deviceName)
FLAG.SCREENSHOT = False

DBName = 'db_news1'
DB_HOST = '101.200.74.101'
DB_USER = 'myuser'
DB_PWD = '123456'
DB_PORT = 3306
path = 'Z:/E/Sessions.txt'
startPath = 'Z:/E/start.txt'
start = 1
if os.path.exists(path):
    os.remove(path)
if os.path.exists(startPath):
    f = open(startPath, 'r')
    start = int(f.read())
    f.close()

end = 5000

def parserUrl(url):
    result = urlparse.urlparse(url)
    print result
    params = urlparse.parse_qs(result.query, True)
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


def selectIDData():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select name, tag, account from tb_wechat')

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


def getInsertData(item, ptime, source, ltype, boardid):
    title = item['title'].replace('amp;', '').replace('quot;', '').replace('&', '')
    try:
        highpoints = re.compile(u'[\u00010000-\u0010FFFF]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    title = re.sub(highpoints, '', title)
    digest = item['digest'].replace('amp;', '').replace('quot;', '').replace('&', '')
    digest = re.sub(highpoints, '', digest)
    url_3w = item['content_url'].encode('utf-8').replace('amp;', '')
    imgsrc = item['cover'].encode('utf-8').replace('amp;', '')
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
        text = text.replace("\"{", "{").replace("}\"", "}").replace("\\\"", "\"").replace('\\\\\\', '\\\\')
        text = re.sub(u'\\{7}', '', text)
        values = ""
        print text.decode('utf-8').encode(type)
        data = json.loads(text.decode("utf-8"))
        if data['ret'] == -3:
            return
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
    except Exception, e:
        print e


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
    os.remove(path)
    return session, cookies


startTime = time.time()
# results = selectIDData()
# length = len(results)

results = selectIDData()


def runTestCase(queue):
    length = len(results)
    ending = end > length and length or end
    for i in range(start, ending):
        files = open(startPath, 'w')
        files.write('%d'%i)
        files.close()
        result = results[i]
        print i, ":", result[2]
        if not result[2].strip():
            continue
        device.input(result[2])
        device.press('KEYCODE_ENTER')
        device.press('KEYCODE_ENTER')
        device.clickxy(540, 450)
        # device.sleep(1.0)
        activity = device.getCurrentActivityName()
        if activity.find('FTSSearchTabWebViewUI') == -1:
            while True:
                device.sleep(0.2)
                if not os.path.exists(path):
                    queue.put(result)

                    device.click(UIELEMENT.TEXT, u'View History')
                    device.sleep(1.0)
                    device.press('KEYCODE_BACK')
                    device.press('KEYCODE_BACK')
                    break
        device.click(UIELEMENT.SID, 'com.tencent.mm:id/f8')
    files = open(startPath, 'w')
    files.write(str(1))
    files.close()
		#device.sleep(1)
		#device.clickxy(1008, 132)


# createDB()

# urlpath = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA5ODE1MzA5Mg==&uin=MTU0ODA1NTIyMQ%3D%3D&key=c50f8b988e61749a12bccf95341ac62c0287d2974051bc4a650fdb234f4db9ab5714c1e1511959c757e979c3ad4d52478c10f488fc34c603&devicetype=android-21&version=26031732&lang=zh_CN&nettype=WIFI&ascene=3&pass_ticket=5ajTshLU%2B6TcY8NmVCNvx64AtilwKrVDMlepFKGAipXySw2z1j9LsFyIKTEcE14n'
# biz, uin, key = parserUrl(urlpath)
# print generatorJsonUrl(biz, uin, key)


def crawldata(queue):
    length = len(results)
    ending = end > length and length or end
    print ending
    for i in range(start, ending):
        result = results[i]
        while True:
            time.sleep(0.2)
            if os.path.exists(path):
                data = queue.get()
                source = data[0]
                tag = data[1]
		account = data[2]
                time.sleep(2)
                session, cookies = getSessionCookies(path)
                biz, uin, key = parserUrl(session)
                url = generatorJsonUrl(biz, uin, key)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36'
                headers = {
                    'Cookie': cookies,
                    'User-Agent': user_agent}
                print url
                try:
                    request = urllib2.Request(url, headers=headers)
                    response = urllib2.urlopen(request)
                    content = response.read().decode('utf-8')
                    # print content
                    # pattern = re.compile("<pre.*?>(.*?)</pre>")
                    # items = re.findall(pattern, content)
                    parserJson(content, source, tag, account)
                except urllib2.URLError, e:
                    print e.reason
                break


class runCase(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.queue = queue

    def run(self):
        while not self.thread_stop:
            runTestCase(self.queue)

            self.stop()

    def stop(self):
        self.thread_stop = True


class jsonParser(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.queue = queue

    def run(self):
        while not self.thread_stop:
            crawldata(self.queue)
            self.stop()

    def stop(self):
        self.thread_stop = True


def main():
    currentId = ""
    print 'start'
    queue = Queue()
    # for i in range(start, length):
    #     result = results[i]
    #     print i, ":", result[2]
    thread1 = runCase(queue)
    thread1.start()
    thread2 = jsonParser(queue)
    thread2.start()

    print 'end'
    end = time.time()
    print end - startTime


if __name__ == '__main__':
    main()
