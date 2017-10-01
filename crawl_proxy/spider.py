#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("../")
from config.config import *
from crawl_proxy.rules import *
from core.core import get_page,parse_page
from db.mongodb import MongoDB
from pymongo import ASCENDING, DESCENDING
import time


def run():
    result = []
    test_mongo = MongoDB(config = mongo_config).getClient().get_database('test')
    proxy_collection = test_mongo.proxy
    try:
        res = get_page('http://www.xicidaili.com/nn/', need_proxy=False)
        page_num = parse_page(res, para.get('xici')['page_num'])
        if page_num:
            page_num = int(page_num[0])
        else:
            page_num = 10
        page_num = 11
        result = []
        for p in [para.get('xici')['url'] % m for m in range(page_num)]:
            r = get_page(p, need_proxy=False)
            if r:
                for pattern in parse_page(r, para.get('xici')['pattern']):
                    data = {}
                    for k, v in para.get('xici')['position'].iteritems():
                        data[k] = pattern.xpath(str(v))[0]
                    #print data
                    result.append(data)
                #print result
                time.sleep(1)
        try:
            proxy_collection.create_index([('ip', '')], unique=True)
            proxy_collection.create_index([('score', DESCENDING)])
        except Exception as e:
            print e
        for r in result:
            try:
                r['score'] = 1
                print r
                proxy_collection.insert(r)
            except Exception as e:
                print e
                continue
        print proxy_collection.index_information()
    except Exception as e:
        print e



if __name__ == "__main__":
    run()