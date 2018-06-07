# -*- coding: utf-8 -*-

from blockmeta.db.dbproxy import MongoProxy
from blockmeta.utils.bytom import get_total_btm
from flask import current_app
from tools import flags

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.logger = current_app.logger
        self.proxy = MongoProxy()

    def get_block_count(self):
        return self.proxy.get_recent_height()

    def get_difficulty(self):
        return self.proxy.get_difficulty()

    def get_recent_award(self):
        return self.proxy.get_recent_award()

    def get_last_block_interval(self):
        return self.proxy.get_last_block_interval()

    def get_latest_block_miner(self):
        return self.proxy.get_latest_block_miner()

    def get_tx_total_num(self):
        return self.proxy.get_total_tx_num()

    def get_addr_total_num(self):
        return self.proxy.get_total_addr_num()

    def get_btm_total_num(self):
        h = self.proxy.get_recent_height()
        return get_total_btm(h)

    def get_block_by_height(self, height):
        return self.proxy.get_block_info(height)

    def get_block_by_hash(self, hash_):
        return self.proxy.get_block_info(hash_)

    def get_tx_by_hash(self, hash_):
        return self.proxy.get_tx_info(hash_)

    def get_info_by_addr(self, address):
        return self.proxy.get_address_info(address)
