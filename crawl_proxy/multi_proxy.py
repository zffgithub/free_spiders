#coding: utf-8

import threading
import time


class MultiTask(object):
    def __init__(self, *args, **kwargs):
        self.max_t = kwargs.get('max_t', 1)     # MAX thread nums
        #self.max_p = kwargs.get('max_p', 1)    # MAX process nums
        self.set_dae = kwargs.get('set_dae', False) # True 设置线程为后台线程
        #self.is_join = kwargs.get('is_join', False) # True 阻塞
        self.f = kwargs.get('f', None)
        self.f_args = kwargs.get('f_args', ())

    def task(self, arg):
        print  'sub thread start!the thread name is:%s\r' % threading.currentThread().getName()
        print 'the arg is:%s\r' % arg
        time.sleep(1)

    def run(self):
        while threading.activeCount() < self.max_t:
            try:
                if self.f:
                    t = threading.Thread(target = self.f, args = self.f_args)
                else:
                    t = threading.Thread(target=self.task, args=(1,))
                if self.set_dae:
                    t.setDaemon(True)
                #time.sleep(0.1)
                t.start()
                print 'Active thread count =', threading.activeCount()
            except Exception as e:
                print e
                #continue


if __name__ == "__main__":
    def test(a):
        print a
        time.sleep(1)
    task1 = MultiTask(max_t = 5)
    task1.run()
    #print 'main thread end!'
