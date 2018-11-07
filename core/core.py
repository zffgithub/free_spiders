#coding: utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")
import requests
from lxml import etree
from config.config import *
import chardet
import json
from db.redisdb import RedisDB

__author__ = 'zff'

redis_db = RedisDB(config=redis_config).getRedisConn()

def parse_page(response, parser):
    root = etree.HTML(response)
    lists = root.xpath(parser)
    return lists

def get_page(url, need_js=False, need_proxy=True, retry_time=RETRY_TIME):
    r = requests.get(url=url, headers=HEADER, timeout=TIMEOUT)
    r.encoding = chardet.detect(r.content)['encoding']
    if (not r.ok) or len(r.content) < 500:
        print 'Connection Fail'
        try:
            key = 'proxy_list'
            for i in xrange(retry_time):
                proxy = json.loads(redis_db.lpop(key))
                r = requests.get(url=url, headers=HEADER, proxies=proxy, timeout=TIMEOUT)
                redis_db.rpush(key, json.dumps(proxy))
                print r
                r.encoding = chardet.detect(r.content)['encoding']
                if (not r.ok) or len(r.content) < 500:
                    print 'Connection Fail'
                else:
                    return r.text
        except Exception as e:
            print e
    else:
        return r.text
    return None

def post_page():
    pass

if __name__ == "__main__":
    pass