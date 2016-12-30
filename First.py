# -*- coding:utf-8 -*-

import urllib
import urllib2
import ssl
import os
import requests

httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
#urllib2.install_opener(opener)

# user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
# cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
# headers = {
#     "User-Agent": user_agent,
#     "Cookie": cookies,
#     "Connection": 'keep-alive'
# }
# _url = "http://pixabay.com/zh/photos/download/auto-1633418.jpg"
# _filename = "D:/transportation/auto-1633418.jpg"
# #context = ssl._create_unverified_context()
# ssl._create_default_https_context = ssl._create_unverified_context
# request = urllib2.Request(_url, headers=headers)
def auto_down(url, filename):
    try:
        urllib.urlretrieve(url, filename)
    except urllib.ContentTooShortError:
        print 'Network conditions is not good.Reloading.'
        auto_down(url, filename)

def download(url, filename):
    print 'download start'
    try:
        req = urllib2.Request(url)
        u = urllib2.urlopen(req, timeout=10)
        data = u.read()
        f = open(filename, 'wb')
        f.write(data)
        f.close()
    except Exception, e:
        print e
        download(url, filename)


def get_download_url():
    #request = urllib2.Request(_url, headers=headers)
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
        #cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
        headers = {
            "User-Agent": user_agent,
            #"Cookie": cookies,
            "Connection": 'keep-alive'
        }
        _url = "http://pixabay.com/zh/photos/download/auto-1633418.jpg"
        _filename = "D:/transportation/auto-1633418.jpg"
        #context = ssl._create_unverified_context()
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib2.Request(_url, headers=headers)
        response = urllib2.urlopen(request, timeout=20)
        return response
    except Exception, e:
        print 'error', e.message
        return get_download_url()

def main_tests():
    try:
        # response = get_download_url()
        # print response.geturl()
        # print response.info()
        # _size = response.headers['Content-Length']
        url = "http://app.tongbu.com/bizhi/iphone6plus-downpic-876383?url=KyIVKOyIsivUT8lVcKQza9rclozyNncvu%2BJ%2FwKHabHO5wp3KjJGM4TdUNARJVOmoah90BR1GiXLnXLZrGbt6Y37RqUKHJSpvWxDe2XvyUdsYGNZmV41odg%3D%3D&time=1478346016341"
        print download(url, _filename)
        # response = requests.get(response.geturl(), stream=True, verify=False)
        # # if status == 200:
        # total_size = int(response.headers['Content-Length'])
        # with open(filename, 'wb') as of:
        #     for chunk in response.iter_content(chunk_size=102400):
        #         if chunk:
        #             of.write(chunk)

        # u = urllib2.urlopevkn(response.geturl())
        # data = u.read()
        # f = open(filename, 'wb')
        # f.write(data)
        # f.close()
    except Exception, e:
        print e.message

def main():
    print ""

if __name__ == '__main__':
    main_tests()


