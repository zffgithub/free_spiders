#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from multi_proxy import MultiTask
sys.path.append("../")
from rules import vali_rule
import requests
from config.config import mongo_config, redis_config
from db.mongodb import MongoDB
from db.redisdb import RedisDB
import json


class Validate(object):
    def __init__(self):
        self.redis_db = RedisDB(config=redis_config).getRedisConn()
        self.test_mongo = MongoDB(config = mongo_config).getClient().get_database('test')
        self.tmp_key = 'proxy_tmp'
        self.key = 'proxy_list'
        self.redis_db.delete(self.tmp_key)
        self.redis_db.delete(self.key)
        self.n = 50

    def mongo_redis(self):
        proxy_collection = self.test_mongo.proxy
        proxy_count = proxy_collection.count()
        page_num = 500
        pages = proxy_count / page_num
        i = 0
        while i < (pages + 1):
            print i
            skip_num = i * page_num
            try:
                for item in proxy_collection.find().skip(skip_num).limit(page_num):
                    if item:
                        item['_id'] = str(item.get('_id', '0'))
                        self.redis_db.rpush(self.tmp_key, json.dumps(item))
                    else:
                        continue
                i += 1
            except Exception as e:
                print e
        print pages

    def val_tmp_data(self):
        proxy_collection = self.test_mongo.proxy
        while True:
            if self.redis_db.llen(self.tmp_key):
                try:
                    item = self.redis_db.lpop(self.tmp_key)
                    item = json.loads(item)
                    proxy = {'http': 'http://' + str(item.get('ip') + ':' + item.get('port')),
                             'https': 'http://' + str(item.get('ip') + ':' + item.get('port'))}
                    print proxy
                    score = 0
                    detail = {}
                    for url, weight in vali_rule.iteritems():
                        special_url = url.replace('.', '_')
                        detail[special_url] = 0
                        try:
                            for i in range(3):
                                response = requests.get(url=url, proxies=proxy, timeout=2)
                                if response.status_code == 200:
                                    score += weight
                                    detail[special_url] += 1
                        except Exception as e:
                            #print e
                            continue
                    proxy_collection.update({'_id': item.get('_id')}, {'$set': {'score': score, 'detail': detail}})
                except Exception as e:
                    pass
                    #print e
            else:
                break

    def update_proxy_list(self):
        proxy_collection = self.test_mongo.proxy
        try:
            for item in proxy_collection.find({}, {'ip': 1, 'port': 1, 'score': 1}).sort([('score', -1)]).limit(self.n):
                proxy = {'http': 'http://' + str(item.get('ip') + ':' + item.get('port')),
                         'https': 'http://' + str(item.get('ip') + ':' + item.get('port'))}
                for i in xrange(item.get('score', 1)):
                    self.redis_db.rpush(self.key, json.dumps(proxy))
        except Exception as e:
            print e

    def clear_bad_mongo_proxy(self):
        proxy_collection = self.test_mongo.proxy
        proxy_collection.remove({'score': {'$lt': 10}})

    def run(self):
        self.mongo_redis()
        multi_val = MultiTask(max_t = 100, f = self.val_tmp_data())
        multi_val.run()
        self.update_proxy_list()
        self.clear_bad_mongo_proxy()



if __name__ == "__main__":
    validate = Validate()
    validate.run()