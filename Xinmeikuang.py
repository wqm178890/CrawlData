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
import urlparse

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
sys.setdefaultencoding('utf8')
def select_category_data():
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute('select wechat_id, detail_url from xin_mei_kuang where biz is null')

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
    sql = 'INSERT ignore INTO xin_mei_kuang (detail_url, wechat_name, wechat_id, read_num, fans, sex, type_area, category, ages) VALUES  %s' % data_str
    return sql

def get_insert_data(detail_url, wechat_name, wechat_id, read_num, fans, sex, type_area, category, ages):
    return '(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"),' % (detail_url, wechat_name, wechat_id, read_num, fans, sex, type_area, category, ages)

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
        print 'error', e.message
        return get_page(url)

#解析HTML并返回关键信息   微信号，ID，阅读数，粉丝数，性别，大类别，小类别，年龄层，详情链接
def get_contents(pageIndex):
    url = "http://www.xinmeikuang.com/common/product.html?c=8-2,3,4&pageNo=%d#shop_productlist" % (pageIndex)
    page = get_page(url)
    page_re = re.compile('<div class="nogoods_info">(.*?)<', re.S)
    pageItems = re.findall(page_re, page)
    #item = pageItems[0]
    #print len(pageItems)
    if len(pageItems) != 0:
        return None
    pattern = re.compile('<li>.*?<div class="productlist_info">(.*?)</div>', re.S)

    #pattern = re.compile('<li>.*?<span class="productName">.*?<a href="(.*?)".*?>(.*?)</a>.*?\
                          #<span class="product_weChatId">(.*?)</span>.*?\
                          #<span title="15天头条平均(.*?)".*?</span>.*?\
                          #<span title="粉丝：(.*?)".*?</span>.*?\
                          #<span title="受众性别(.*?)".*?</span>.*?\
                          #<span title="行业领域(.*?)".*?</span>.*?\
                          #<div title="受众年龄(.*?)".*?</li>', re.S)
    #pattern = re.compile('<span title="受众性别.*?".*?</span>', re.S)
    items = re.findall(pattern, page)
    contents = []
    
    #for item in items:
        #pattern_item = re.compile('<span class="productName"><a href="(.*?)".*?/a></span>.*?<span class="product_weChatId">(.*?)</span>.*?<span title="(.*?)".*?</span>.*?<span title="(.*?)".*?</span>.*?<span title="(.*?)".*?</span>.*?<span title="(.*?)".*?</span>', re.S)
        #pattern_items = re.findall(pattern_item, item)
       # print pattern_items
        #print item
    data_str = ""
    for item in items:
        pattern_item = re.compile('<span class="productName"><a href="(.*?)" target.*?>(.*?)</a></span>.*?<span class="product_weChatId">(.*?)</span>.*?<span title="(.*?)".*?</span>.*?<span title="(.*?)".*?</span>.*?<span title="(.*?)".*?</span>.*?<span title="(.*?)".*?</span>.*?<div title="(.*?)">', re.S)
        pattern_items = re.findall(pattern_item, item)   
        if len(pattern_items) == 0:
            continue
        data = pattern_items[0]
        
        detail_url = data[0]
        wechat_name = data[1]
        wechat_id = data[2]
        read_num = data[3]
        fans = data[4].split('：')[-1]
        sex = data[5].split('：')[-1]
        types = data[6]
        type_area = types.split('：')[-1].split('-')[0]
        category = types.split('：')[-1].split('-')[1]
        ages = data[7].split('：')[-1]
        #print detail_url, wechat_name, wechat_id, read_num, fans, sex, types, ages ,'\n'
        data_str += get_insert_data(detail_url, wechat_name, wechat_id, read_num, fans, sex, type_area, category, ages)
        #contents.append([data_w, data_h, detail_url, source_url, tag, like, favorite, comment, author])
    return data_str

def parserUrl(url):
    #print 'start parserUrl'
    result = urlparse.urlparse(url)
    params = urlparse.parse_qs(result.query, True)
    #print 'end parserUrl'
    return params['__biz'][0]

def get_biz(url):
    page = get_page(url)    
    
    page_re = re.compile('<div class="publish_data">(.*?)</div>.*?<div class="article_title">.*?<a href="(.*?)" target.*?>', re.S)
    pageItems = re.findall(page_re, page)   

    if len(pageItems) != 0:
        biz = parserUrl(pageItems[0][1])
        return pageItems[0][0], biz
    return "2015-10-01", 0
 
def main():
    print 'start'
    for i in range(1, 167):
        data_str = get_contents(i)
        if data_str is None:
            print 'can return'
            break
        data_str = data_str.rstrip(',')
        sql = insert_sql(data_str)
        insert_data(sql)
    print "end"


def xin_biz():
    a = "2016-10-01"
    print time.mktime(time.strptime(a,'%Y-%m-%d'))
    results = select_category_data()
    for result in results:
        wechat_id = result[0]
        detail_url = result[1].replace('.html', '/list_new_article.html')
        data, biz = get_biz(detail_url)
        if time.mktime(time.strptime(a,'%Y-%m-%d')) < time.mktime(time.strptime(data,'%Y-%m-%d')):
            insert_data("update xin_mei_kuang set biz=\'%s\' where wechat_id=\'%s\'"%(biz, wechat_id))    
    
if __name__ == '__main__':
    xin_biz()

