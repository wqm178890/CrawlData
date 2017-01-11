# -*- coding:utf-8 -*-

import time
import xlsxwriter
import xlrd, csv, re, chardet
import hashlib
import codecs
import urllib
import urllib2
import json
import ssl

def get_md5(str):
    m = hashlib.md5()
    m.update(str.encode("gb2312"))
    md5 = m.hexdigest()
    return md5

def collect_gdt(filepath):
    data = []
    row = 0
    first_file = True
    first_row_data = 0
    file_data = open(filepath, 'rb')

    reader = csv.reader(file_data)
    for row_data in reader:
        data_time = ""
        app_name = ""
        ad_type = ""
        list_data = []
        if first_file == False:
            if first_row_data == 0:
                first_row_data += 1
                continue
        first_file = False
        col = 0
        for i in row_data:
            i = i.replace(',', '')
            if row == 0:
                continue
            else:
                if col < 3 or col > 6:
                    list_data.append(unicode(i, "utf-8"))
                else:
                    list_data.append(i)
            col += 1
        
        if len(list_data) > 0:
            md5 = get_md5('%s%s%s%s%s'%(list_data[0], list_data[1], list_data[2], list_data[3], list_data[4]))
            list_data.append(md5)            
            data.append(list_data)
        row += 1
    print data
    return data



def get_google_data(days=1):
    localtime = time.localtime(time.time() - 24*60*60*days)
    str_data = time.strftime("%Y%m%d", localtime)    
    ssl._create_default_https_context = ssl._create_unverified_context
    values = {}
    values['t'] = "ADMOB_NETWORK"
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
        "Accept-Language": "zh-cn"
    }
    
    request = urllib2.Request(url, data, headers=headers)
    response = urllib2.urlopen(request)
    json_data = response.read()
    data = unicode(json_data, "utf-16")  
    data_list = []
    row = 0
    for i in data.split('\n'):
        if row == 0:
            row += 1
            continue
        if len(i) > 0:
            lists = i.split('\t')
            md5 = get_md5('%s%s'%(lists[0], lists[1]))
            lists.append(md5)
            data_list.append(lists)
        row += 1
    return data_list

def collect_umeng(file_path):
    localtime = time.localtime(time.time() - 24*60*60)
    str_data = time.strftime("%Y_%m_%d", localtime)     
    workbook_test = xlrd.open_workbook(file_path)
    sheet = workbook_test.sheet_by_index(0)    
    data_list = []
    for row in range(1, sheet.nrows):
        data = []
        data.append(time.strftime("%Y-%m-%d", localtime))
        data.append(sheet.cell_value(row, 0))
        data.append(str(sheet.cell_value(row, 2)))
        data.append(str(sheet.cell_value(row, 4)))
        data.append(str(sheet.cell_value(row, 6)))
        data.append(str(sheet.cell_value(row, 7)))
        md5_str = '%s%s'%(data[0], data[1])    
        data.append(get_md5(md5_str))
        data_list.append(data)
    print data_list
    return data_list

        

