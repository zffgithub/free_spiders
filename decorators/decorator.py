#coding: utf-8

import time
import logging
import functools


"""
A decorator that prints the time a func takes to execute.
"""
def benchmark(func):
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print "{0} {1}".format(func.__name__, time.clock() - t)
        return res
    return wrapper

"""
A decorator that logs the activity of the func.
"""
def easylog(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print "{0} {1} {2}".format(func.__name__, args, kwargs)
        return res
    return wrapper

def create_logger():
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("./log/test.log")

    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

#logger = create_logger()

def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                err = "There was an exception in "
                err += func.__name__
                logger.exception(err)
            raise
        return wrapper
    return decorator
    
if __name__ == "__main__":
    pass    
