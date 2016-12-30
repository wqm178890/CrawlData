#! /usr/bin/env python
# encoding=utf-8

from __future__ import unicode_literals

from multiprocessing.dummy import Pool as ThreadPool
import threading

import os
import sys
import cPickle
from collections import namedtuple
import urllib2
from urlparse import urlsplit
import ssl
import time
import hashlib
lock = threading.Lock()

# global lock



# default parameters
defaults = dict(
    thread_count=60,
    buffer_size=500 * 1024,
    block_size=1000 * 1024)


def progress(percent, width=50):
    print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * '='), percent),
    if percent >= 100:
        print
        sys.stdout.flush()


def write_data(filepath, data):
    with open(filepath, 'wb') as output:
        cPickle.dump(data, output)


def read_data(filepath):
    with open(filepath, 'rb') as output:
        return cPickle.load(output)


FileInfo = namedtuple('FileInfo', 'url name size lastmodified')


def get_file_info(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
    cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies,
        "Connection": 'keep-alive'
    }
    ssl._create_default_https_context = ssl._create_unverified_context
    class HeadRequest(urllib2.Request):

        def get_method(self):
            return "HEAD"
    try:
        req = urllib2.Request(url, headers=headers)
        res = urllib2.urlopen(req, timeout=10)
    except Exception, e:
        print e
       # return e.code
    #print res
    headers = dict(res.headers)
    size = int(headers.get('content-length', 100))
    lastmodified = headers.get('last-modified', '')
    name = None
    if headers.has_key('content-disposition'):
        name = headers['content-disposition'].split('filename=')[1]
        if name[0] == '"' or name[0] == "'":
            name = name[1:-1]
    else:
        name = os.path.basename(urlsplit(url)[2])
    print url
    return FileInfo(url, name, size, lastmodified)


def download(url, output,
             thread_count=defaults['thread_count'],
             buffer_size=defaults['buffer_size'],
             block_size=defaults['block_size']):
    # get latest file info
    file_info = get_file_info(url)
    if file_info == 400:
        return 400
    # init path
    if output is None:
        output = file_info.name
    workpath = '%s.ing' % output
    infopath = '%s.inf' % output

    # split file to blocks. every block is a array [start, offset, end],
    # then each greenlet download filepart according to a block, and
    # update the block' offset.
    blocks = []
    if os.path.exists(infopath):
        # load blocks
        _x, blocks = read_data(infopath)
        if (_x.url != url or
                _x.name != file_info.name or
                _x.lastmodified != file_info.lastmodified):
            blocks = []
    if len(blocks) == 0:
        # set blocks
        if block_size > file_info.size:
            blocks = [[0, 0, file_info.size]]
        else:
            block_count, remain = divmod(file_info.size, block_size)
            blocks = [[i * block_size, i * block_size,
                       (i + 1) * block_size - 1] for i in range(block_count)]
            blocks[-1][-1] += remain
        # create new blank workpath
        with open(workpath, 'wb') as fobj:
            fobj.write('')

    print 'Downloading %s' % url
    # start monitor
    threading.Thread(target=_monitor, args=(
        infopath, file_info, blocks)).start()

    # start downloading
    with open(workpath, 'rb+') as fobj:
        args = [(url, blocks[i], fobj, buffer_size)
                for i in range(len(blocks)) if blocks[i][1] < blocks[i][2]]

        if thread_count > len(args):
            thread_count = len(args)

        pool = ThreadPool(thread_count)
        pool.map(_worker, args)
        pool.close()
        pool.join()

    # rename workpath to output
    if os.path.exists(output):
        os.remove(output)
    os.rename(workpath, output)

    # delete infopath
    if os.path.exists(infopath):
        os.remove(infopath)
    return 0
    assert all([block[1] >= block[2] for block in blocks]) is True


def _worker((url, block, fobj, buffer_size)):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.0.1.1700 Chrome/47.0.2526.73 Safari/537.36"
    cookies = "__cfduid=d34936fd578ad277ab9d0e7039a7a77911477099319; csrftoken=90bKOC65S9FGW9Sbjbd9feV6SpRMiC8dpBkdAno2FiKSVAz9yENmPCQJOlUvZ6WQ; img_pp=100; sessionid=\".eJxVjVsKwyAUBfdyv0Oo1YjJVkqRG72JNg9LVAot3XtNPgr5HebM-YCdobsxyblg6l6BxpyczpE27S10wBvVsvYKFSSKyYQweSr4FbaJLJz8Hs1E6z56buFBJtU5-TnWJscUlkOs_aGuuJAOm6YF_fzfldiM65hx3B_e7lx3GF3BgpNSSKbFpreNUGK4DE0hlikhUfbcqqsQ0sL3B6oQSQo:1byJBC:YrpbzvLCTLnuBQwzuGxf4Wvf8A0\"; client_width=1907; _ga=GA1.2.434145257.1477060660"
    headers = {
        "User-Agent": user_agent,
        "Cookie": cookies,
        "Connection": 'keep-alive'
    }
    req = urllib2.Request(url, headers=headers)
    req.headers['Range'] = 'bytes=%s-%s' % (block[1], block[2])
    res = urllib2.urlopen(req, timeout=10)
    while 1:
        try:
            chunk = res.read(buffer_size)
        except Exception, e:
            print 'error', e
            _worker((url, block, fobj, buffer_size))
            return
        if not chunk:
            break
        with lock:
            fobj.seek(block[1])
            fobj.write(chunk)
            block[1] += len(chunk)


def get_md5(str):
    m = hashlib.md5()
    m.update(str)
    md5 = m.hexdigest()
    return md5

def _monitor(infopath, file_info, blocks):
    while 1:
        with lock:
            percent = sum([block[1] - block[0]
                           for block in blocks]) * 100 / file_info.size
            progress(percent)
            if percent >= 100:
                break
            write_data(infopath, (file_info, blocks))
        time.sleep(2)

if __name__ == '__main__':
    start_time = time.time()
    url = "http://app.tongbu.com/bizhi/iphone6plus-downpic-876383?url=KyIVKOyIsivUT8lVcKQza9rclozyNncvu%2BJ%2FwKHabHO5wp3KjJGM4TdUNARJVOmoah90BR1GiXLnXLZrGbt6Y37RqUKHJSpvWxDe2XvyUdsYGNZmV41odg%3D%3D&time=1478346016341"
    output = "D:/Test1.jpg"
    thread_count = defaults['thread_count']
    buffer_size = defaults['buffer_size']
    block_size = defaults['block_size']
    print download(url, output, thread_count,buffer_size, block_size)
    print '下载时间: %ds' % int(time.time() - start_time)