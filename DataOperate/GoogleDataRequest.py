# -*- coding:utf-8 -*-

import urllib
import urllib2
import hashlib
import json
import ssl
import chardet, time

def get_google_data(days=1):
    localtime = time.localtime(time.time() - 24*60*60*days)
    str_data = time.strftime("%Y%m%d", localtime)    
    ssl._create_default_https_context = ssl._create_unverified_context
    values = {}
    values['t'] = "ADMOB_NETWORK"
    values['rs'] = "{\"2\":[{\"1\":3,\"2\":%s,\"3\":%s}],\"3\":[1,4],\"4\":\"USD\"}"%(str_data, str_data)
    values['rs'] = "{\"2\":[{\"1\":3,\"2\":%s,\"3\":%s}],\"3\":[1,4],\"4\":\"USD\"}"%(str_data, str_data)
    values['cc'] = "USD"
    
    data = urllib.urlencode(values)
    url = 'https://apps.admob.com/monetize-reports'
    
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
    cookie = "S=ads-app-monetization=iRAzG7EOEixEBO0r5EHyJvSZ-TURVc8R:ads-publisher-controls-ui=1qb-_7OpOZCtpAVaTHOXuMIwYAF5n4Z_; ADMOB=xwOdZ1NGkUOTyO3RmzizvpCmvs0RPjqgAuJxaoquHJxoQ3TgdWxrsdXuuRJ16hDG0BJAAA.; _ga=GA1.2.1238477904.1474244209"
    Content_Type = "application/x-www-form-urlencoded"
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,
        "Content-Type": Content_Type,
        "Referer": "https://apps.admob.com/?pli=1",
        "Accept-Language": "en-US"
    }
    
    request = urllib2.Request(url, data, headers=headers)
    response = urllib2.urlopen(request)
    json_data = response.read()
    data = unicode(json_data, "utf-16")  
    print data
    data_list = []
    row = 0
    for i in data.split('\n'):
        if row == 0:
            row += 1
            continue
        if len(i) > 0:
            lists = i.split('\t')
            data_list.append(lists)
        row += 1
    return data_list

print get_google_data()





