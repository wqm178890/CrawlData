import ssl
import urllib2
import json
import time
def get_download_urls(file_id):
    try:
        _url = "https://pixabay.com/api/?key=3589192-081aeb522d921b7cd7ae63922&lang=zh&id=%s" % file_id
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.3000 Chrome/47.0.2526.73 Safari/537.36"
        cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
        #cookies = "_ga=GA1.2.1025332067.1478178236; sessionid=\".eJxVi0sOwiAQQO_C2jS2HZqplyEDTAtawPDZaLy7tQuTbt_nLdRGcW20sriJlxMXoahVp1rhrBwVt2MYGZHYzCS1lYCwXBe5E9sjTDTp0eIAMNnz7O2-jhLnfh7ORpN5cPzpZ053NrVr1W-lM63UFI6w80caKbBKWXEgv_2_zxcJlz26:1c2KCA:x7dAJClbyz2x5s3ZHAKE-l2B_nA\"; client_width=1903"
        headers = {
            "User-Agent": user_agent,
            "Cookie": cookies,
            "Connection": 'keep-alive'
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib2.Request(_url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        data = response.read()
        json_data = json.loads(data)
        webformat_url = json_data["hits"][0]["webformatURL"]
        key = webformat_url.split("/")[-1].split(".")[0].split("_")[0]
        print key
        return key[3:14]
    except Exception, e:
        print 'error', e
        return get_download_urls(file_id)

def download_urls(url):
    try:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.3000 Chrome/47.0.2526.73 Safari/537.36"
        cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
        #cookies = "_ga=GA1.2.1025332067.1478178236; sessionid=\".eJxVi0sOwiAQQO_C2jS2HZqplyEDTAtawPDZaLy7tQuTbt_nLdRGcW20sriJlxMXoahVp1rhrBwVt2MYGZHYzCS1lYCwXBe5E9sjTDTp0eIAMNnz7O2-jhLnfh7ORpN5cPzpZ053NrVr1W-lM63UFI6w80caKbBKWXEgv_2_zxcJlz26:1c2KCA:x7dAJClbyz2x5s3ZHAKE-l2B_nA\"; client_width=1903"
        headers = {
            "User-Agent": user_agent,
            "Cookie": cookies,
            "Connection": 'keep-alive'
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request, timeout=10)
        print response
        real_url = response.geturl()
        print real_url

        session = real_url.split("/")[-2][-6:56]
        return session
    except Exception, e:
        print 'error', e
        return download_urls(url)
# strs = "https://pixabay.com/get/e832b30e28f2063ecd1f4600ee45479fe16ae3d11eb912409df6c87c/portrait-1721067.jpg"
# print strs.split("/")[-2][14:56]
#print download_urls("https://pixabay.com/zh/photos/download/portrait-1721067.jpg")

#print "%.f" % (time.time() * 1000)
#https://pixabay.com/get/e832b80e2efd00 3ecd1f4600ee45479fe16ae3d11eb9124595f8c07f/rhino-1791691.png?attachment

for i in range(0, 2):
    print i