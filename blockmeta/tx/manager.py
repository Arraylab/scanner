#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app

from blockmeta.constant import DISPLAY_LEN
from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class TxManager:
    """Manages the tx query"""
    def __init__(self):
        self.logger = current_app.logger
        self.driver = BuiltinDriver()

    def handle_tx(self, tx_hash):
        try:
            return self.driver.request_tx_info(tx_hash)
        except Exception, e:
            self.logger.error("TxManager.handle_tx Error: %s" % str(e))
            raise Exception("handle_tx error: %s", e)

    def list_txs(self, start, end):
        txs = {}
        try:
            result, total_num = self.driver.get_tx_list(start, end)
            if result:
                txs['total_page'] = total_num / DISPLAY_LEN + 1
                txs['txs'] = result
            return txs
        except Exception, e:
            self.logger.error("TxManager.list_txs Error: %s" % str(e))
            raise Exception("list_txs error: %s", e)
