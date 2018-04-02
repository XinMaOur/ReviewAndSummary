#!/usr/bin/env python
#coding:utf8
import threading
from time import sleep, ctime

loops = [4, 2]

class ThreadFunc(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args

    def gerResult(self):
        return self.gerResult

    def run(self):
        print 'staring', self.name, 'at:',\
            ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:',\
            ctime()

def loop(nloop, nsec):
    print 'start loop', nloop, 'at', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at', ctime()


def main():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))
    for i in nloops:                        ## create Tread
        t=ThreadFunc(loop,(i, loops[i]),
            loop.__name__)
        threads.append(t)
    
    for i in nloops:            # start Tread 
        threads[i].start()
    
    for i in nloops:            # wait for all
        threads[i].join()       # threads to finish


    print 'all Done at:', ctime()

if __name__ == "__main__":
    main()

