# -*- coding: utf-8 -*-

from collector import log
from collector.stats.chain import ChainStats
from collector.stats.node import NodeStats
from tools import flags
import sys
import threading
import time

POLLTIMER = 86400


class StatusService(object):

    def __init__(self):
        self.logger = log.Logger('stats')
        self.logger.add_file_handler('stats')
        self.chain_stats = ChainStats()
        self.node_stats = NodeStats()

    def count(self):
        global timer
        start = time.time()

        self.chain_stats.save()
        self.node_stats.save()

        end = time.time()
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))
        self.logger.info('Stats end, cost %s sec, current time: %s' % (str(end-start), str(now)))
        timer = threading.Timer(POLLTIMER, self.count)
        timer.start()

    def start(self):
        self.logger.info('First stats starting')
        start = time.time()

        self.chain_stats.load()
        self.node_stats.save()

        end = time.time()
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))
        self.logger.info('First stats end, cost %s sec, current time: %s' % (str(end - start), str(now)))
        time.sleep(POLLTIMER)
        self.count()


if __name__ == '__main__':
    flags.FLAGS(sys.argv)
    ss = StatusService()
    ss.start()
