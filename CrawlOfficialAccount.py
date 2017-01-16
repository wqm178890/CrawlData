# -*- coding: utf-8 -*-

import hashlib
import urllib
import urllib2
import json
import MySQLdb
import unicodedata
import hashlib, re, urlparse

DBName = 'db_news1'
DB_HOST = '59.110.0.42'
DB_USER = 'remote'
DB_PWD = 'Combeemans91'
DB_PORT = 3306
path = 'c://Sessions.txt'

sql_select_newrank = "select rank_name, rank_name_group, type_id, type_name from tb_newrank_types"
sql_select_types = "select name, type from tb_types"
sql_select_wechat_id = "select account from tb_wechat"
sql_select_wechat_info = "select wechat_name, wechat_id, type_id, type_name, biz from xin_mei_kuang where type_id is not null limit 200, 3000"

def select_data(sql):
    try:
        conn = MySQLdb.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PWD, db=DBName, charset="utf8")
        cur = conn.cursor()
        cur.execute('SET NAMES UTF8')
        cur.execute('set global max_allowed_packet = 2*1024*1024*10')
        conn.select_db(DBName)
        count = cur.execute(sql)
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except MySQLdb.Error, e:
        print e

def insert_data(sql):
    print sql
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

def get_key(name, group_name, start_data, end_data):
    m2 = hashlib.md5()
    m2.update(get_text_params(name, group_name, start_data, end_data))
    xyz = m2.hexdigest()
    return xyz

def get_xyz(key):
    template = "/xdnphb/detail/getAccountArticle?AppKey=joker&flag=true&uuid=%s&nonce=5bd1c09c6"%key
    m2 = hashlib.md5()
    m2.update(template)
    xyz = m2.hexdigest()
    return xyz

def get_text_params(name, group_name, start_data, end_data):
    text_params = '/xdnphb/list/week/rank?AppKey=joker&end=%s&rank_name=%s&rank_name_group=%s&start=%s&nonce=fb5f92444'\
                  % (end_data, name, group_name, start_data)
    print text_params
    return text_params.encode('utf-8')

def get_title_json_data(key):
    values = {}

    values['flag'] = "true"
    values['uuid'] = key
    values['nonce'] = '5bd1c09c6'
    values['xyz'] = get_xyz(key)
    #print values
    data = urllib.urlencode(values)
    url = 'http://www.newrank.cn/xdnphb/detail/getAccountArticle'

    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
    cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
    content_type = "application/x-www-form-urlencoded;"
    #referer = "http://www.newrank.cn/public/info/detail.html?account=%s" % (account)
    headers = {
        "User-Agent": user_agent,
        "Content-Type": content_type,
    }

    request = urllib2.Request(url, data, headers=headers)
    response = urllib2.urlopen(request)
    json_data = response.read()
    pattern = re.compile('"url":"(.*?)"', re.S)
    items = re.findall(pattern, json_data)
    return parserUrl(items[0])
    #data = json.loads(json_data)
    #values = data['value']
    #return values
    
def parserUrl(url):
    #print 'start parserUrl'
    result = urlparse.urlparse(url)
    params = urlparse.parse_qs(result.query, True)
    #print 'end parserUrl'
    return params['__biz'][0]   

def get_json_data(name, group_name, start_data, end_data):
    values = {}

    values['end'] = end_data
    values['rank_name'] = name.encode('utf-8')
    values['rank_name_group'] = group_name.encode('utf-8')
    values['start'] = start_data
    values['nonce'] = 'fb5f92444'
    values['xyz'] = get_key(name, group_name, start_data, end_data)
    print values
    data = urllib.urlencode(values)
    url = 'http://www.newrank.cn/xdnphb/list/week/rank'

    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
    cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
    content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    headers = {
        "User-Agent": user_agent,
        "Content-Type": content_type
    }

    request = urllib2.Request(url, data, headers=headers)
    response = urllib2.urlopen(request)
    json_data = response.read()
    data = json.loads(json_data)
    values = data['value']
    return values
    # print len(values)
    # for value in values:
    #     print value['name'], ':', value['account']

def sync_rank_data():
    results = select_data(sql_select_types)
    for result in results:
        type_name = result[0]
        type_id = result[1]
        insert_data("UPDATE tb_newrank_types SET type_id = \'%s\' WHERE type_name = \'%s\'" % (type_id, type_name))

def main():
    results = select_data(sql_select_newrank)
    i = 0
    for result in results:
        print i
        i += 1
        #result = results[18]
        rank_name = result[0]
        rank_name_group = result[1]
        type_id = result[2]
        json_data = get_json_data(rank_name, rank_name_group, '2016-11-14', '2016-11-20')
        data = ""
        for value in json_data:
            name = value['name']
            name = unicodedata.normalize('NFKD', name).strip()
            account = value['account']
            data += '(\'%s\', \'%s\', \'%s\'),' % (name, type_id, account)
        data = data.rstrip(',')
        insert_data('INSERT ignore INTO tb_wechat (name, tag, account) VALUES %s'%data)
        #get_json_data('创业', '资讯', '2016-10-17', '2016-10-23')
        print ""
        
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
    
def get_contents(wechat_id):
    url = "http://www.newrank.cn/public/info/detail.html?account=%s" % (wechat_id)
    page = get_page(url)
    
    pattern = re.compile('"uuid":"(.*?)"', re.S)
    items = re.findall(pattern, page)
    print items
    return items[0]
    
def getMD5(str):
    m = hashlib.md5()
    m.update(str)
    md5 = m.hexdigest()
    return md5

if __name__ == '__main__':
    #main()
    #print getMD5("hzfm918")
    results = select_data(sql_select_wechat_info)
    for result in results:
        wechat_name = result[0].replace(u'\xa0', u' ')
        wechat_id = result[1]
        type_id = result[2]
        type_name = result[3]
        biz = result[4]
        sql_insert = 'INSERT ignore INTO tb_wechat (name, account, tag, biz) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')'% (wechat_name, wechat_id, type_id, biz)
        #sql_update_biz = "insert  tb_wechat set name = \'%s\', account = \'%s\', type_id = \'%s\', biz = \'%s\' where account = \'%s\'" % (wechat_name, wechat_id, type_id, biz)
        insert_data(sql_insert)
        #print biz
    #print get_xyz("4571A5B3A7D6BCF067EBDA7C1D07AF57")