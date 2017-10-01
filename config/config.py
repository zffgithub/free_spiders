#coding: utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("../")

RETRY_TIME = 3
HEADER = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}
TIMEOUT = 3

redis_config = {
    "host": "127.0.0.1",
    "port": 6379,
    "user": "",
    "passwd": "",
    "db": 0,
}

mongo_config = {"url" : "mongodb://127.0.0.1:27017/",}



mysql_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'db': 0,
            'charset': 'utf8mb4',
            #"host": "mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8",
}



if __name__ == "__main__":
    pass