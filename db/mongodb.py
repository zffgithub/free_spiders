#coding: utf-8
import pymongo

class MongoDB(object):
    client = None
    def __init__(self,*args, **kwargs):
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        mongo_conifg = kwargs.get('config')
        url = mongo_conifg.get("url", None)
        if not self.client:
            self.client = pymongo.MongoClient(host=url)

    def getClient(self):
        if not self.client:
            self.init()
        return self.client


if __name__ == "__main__":
    pass
