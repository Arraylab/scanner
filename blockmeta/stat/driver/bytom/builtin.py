# -*- coding: utf-8 -*-

from chain import ChainStats
from node import NodeStats


class BuiltinDriver:
    def __init__(self):
        self.chain_stats = ChainStats()
        self.node_stats = NodeStats()

    def request_node_status(self):
        return self.node_stats.get_node_stats()

    def request_chain_status(self):
        return self.chain_stats.get_chain_status()


if __name__ == '__main__':
    b = BuiltinDriver()
    print b.request_chain_status()
    print b.request_node_status()
