# -*- coding: utf-8 -*-

from collector.stats.chain import ChainStats
from collector.stats.node import NodeStats
from tools import flags
import sys
import threading
import time

POLLTIMER = 6


class StatusService(object):

    def __init__(self):
        self.chain_stats = ChainStats()
        self.node_stats = NodeStats()

    def count(self):
        global timer
        print "meet you again"
        start = time.time()
        self.chain_stats.save()
        self.node_stats.save()
        end = time.time()
        print "cost ", end - start
        print "ready to poll"
        timer = threading.Timer(POLLTIMER, self.count)
        timer.start()

    def start(self):
        print "hello -- "
        start = time.time()
        self.chain_stats.load()
        end = time.time()
        print "time lapse:", end-start
        self.node_stats.save()
        print "haha, success!......"
        time.sleep(POLLTIMER)
        self.count()


if __name__ == '__main__':
    flags.FLAGS(sys.argv)
    ss = StatusService()
    ss.start()
