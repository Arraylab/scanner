# -*- coding: utf-8 -*-

from collector.stats.chain import ChainStats
from collector.stats.node import NodeStats
import threading
import time

POLLTIMER = 86400


class StatusService(object):

    def __int__(self):
        self.chain_status = ChainStats()
        self.node_status = NodeStats()

    def count(self):
        global timer
        self.chain_status.save()
        self.node_status.save()
        timer = threading.Timer(POLLTIMER, self.count)
        timer.start()

    def start(self):
        self.chain_status.load()
        self.node_status.save()
        time.sleep(POLLTIMER)
        self.count()
