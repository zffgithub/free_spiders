#coding: utf-8
import redis


class RedisDB():
    def __init__(self, *args, **kwargs):
        db_config = kwargs.get("config")
        if db_config.get("url",None):
            REDIS_CLS = redis.StrictRedis
            self.server = REDIS_CLS.from_url(url=db_config.get("url"))
        else:
            host = db_config.get("host", "127.0.0.1")
            port = db_config.get("port", 6379)
            db = db_config.get("db", 0)
            password = db_config.get("passwd")
            self.pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
            self.server = redis.Redis(connection_pool=self.pool)

    def getRedisConn(self):
        return self.server#redis.Redis(connection_pool=self.pool)



if __name__ == '__main__':
    redisdb1 = RedisDB().getRedisConn()
    redisdb1.set("key", "test")
    print redisdb1.get("key")

