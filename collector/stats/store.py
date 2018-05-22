# -*- coding: utf-8 -*-

from collector.stats.chain import ChainStats
import threading


class StatusAgent(object):

    def __int__(self):
        self.chain_status = ChainStats()

    def count(self):
        global timer
        self.chain_status.save()
        timer = threading.Timer(600, self.count)
        timer.start()

    def start(self):
        self.chain_status.load()
        self.count()
