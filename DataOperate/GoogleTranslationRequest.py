# -*- coding:utf-8 -*-

import urllib
import urllib2
import hashlib
import json
import ssl
import chardet, time, sys,getopt
reload(sys)
sys.setdefaultencoding('utf-8')
opts, args = getopt.getopt(sys.argv[1:], "h",["content=","output="])

content = "Good Morning";
output = "C:/Result.txt";

for op, value in opts:
    print op
    if op == "--content":
        print value
        content = value
    elif op == "--output":
        print value
        output = value



list = {"zh-Hans": "zh-CN", "zh-Hant":"zh-TW",
        "da":"da", "nl-NL": "nl", "en-AU": "en",
        "en-CA": "en", "en-GB": "en", "en-US": "en",
        "fi": "fi", "fr-CA": "fr", "fr-FR": "fr",
        "de-DE": "de", "el": "el", "id": "id",
        "it": "it", "ja":"ja", "ko": "ko",
        "ms": "ms", "no": "no", "pt-BR": "pt",
        "pt-PT": "pt", "ru": "ru", "es-MX": "es",
        "es-ES": "es", "sv": "sv", "th": "th",
        "tr": "tr", "vi": "vi"}

def get_google_translation(key, value, msg):
    localtime = time.localtime(time.time() - 24 * 60 * 60 * 1)
    str_startTime = "20170101"
    str_data = time.strftime("%Y%m%d", localtime)
    ssl._create_default_https_context = ssl._create_unverified_context
    values = {}
    values['client'] = "at"
    values['sl'] = "en"
    values['tl'] = value
    values['dt'] = "t"
    values['q'] = msg
    data = urllib.urlencode(values)
    url = 'http://translate.google.cn/translate_a/single'

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14"
    cookie = "NID=123=H6zJmB81AJdrFAEzJSz35XOrf7jqbanJ2Rw5R2xlmm24v-ke6VfHJR9Jht4Agmvg0dyrenJ97WDWlXO8ZdadItgRfoYN9mgsncRI4zqhY52XhhFjvN5U2JRenXjQr1Cg; _ga=GA1.3.1168397811.1517816083; _gid=GA1.3.1574029587.1517816083; 1P_JAR=2018-2-5-7"
    Content_Type = "application/x-www-form-urlencoded"
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,
        "Content-Type": Content_Type,
        "Accept-Language": "zh-cn"
    }
    request = urllib2.Request(url, data, headers=headers)
    response = urllib2.urlopen(request)
    json_data = response.read()
    data = unicode(json_data, "utf-8")
    str = data.split(",")[0].split("[")[-1].replace("\"", "")
    return "%s:%s"%(key, str)

if __name__ == "__main__":
    str_id = ""
    for key, value in list.items():
        str_id = str_id + get_google_translation(key, value, content)+"\n"
    print str_id
    fo = open(output, "w")
    fo.write(str_id)





