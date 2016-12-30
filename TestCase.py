# -*- coding:utf-8 -*-

import urllib
import urllib2
import hashlib
import json


s = '职场'
print urllib.quote(s)

s = '资讯'
print urllib.quote(s)

def get_text_params(name, group_name):
        text_params = '/xdnphb/list/week/rank?AppKey=joker&end=2016-10-23&rank_name=%s&rank_name_group=%s&start=2016-10-17&nonce=fb5f92444'%(name, group_name)
        return text_params


print(get_text_params('职场', '资讯'))

m2 = hashlib.md5()
m2.update(get_text_params('职场', '资讯'))
xyz = m2.hexdigest()

#end=2016-10-23&rank_name=%E6%B1%BD%E8%BD%A6&rank_name_group=%E8%B5%84%E8%AE%AF&start=2016-10-17&nonce=fb5f92444&xyz=46f1167673c2efb69ba9ad521354c696

#end=2016-10-23&rank_name=%E8%81%8C%E5%9C%BA&rank_name_group=%E8%B5%84%E8%AE%AF&start=2016-10-17&nonce=fb5f92444&xyz=46f1167673c2efb69ba9ad521354c696

#texts = 'end=2016-10-23&rank_name=%E8%81%8C%E5%9C%BA&rank_name_group=%E8%B5%84%E8%AE%AF&start=2016-10-17&nonce=fb5f92444&xyz=46f1167673c2efb69ba9ad521354c696'
values = {}
values['end'] = '2016-10-23'
values['rank_name'] = '职场'
values['rank_name_group'] = '资讯'
values['start'] = '2016-10-17'
values['nonce'] = 'fb5f92444'
values['xyz'] = '46f1167673c2efb69ba9ad521354c696'

data = urllib.urlencode(values)
url = 'http://www.newrank.cn/xdnphb/list/week/rank'
print values

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
Content_Type = "application/x-www-form-urlencoded; charset=UTF-8"
headers = {
    "User-Agent": user_agent,
    "Content-Type": Content_Type
}

request = urllib2.Request(url, data, headers=headers)
response = urllib2.urlopen(request)
json_data = response.read()
data = json.loads(json_data)
values = data['value']
print len(values)
for value in values:
    print value


