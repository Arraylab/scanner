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
        self.logger.info('handle tx, tx hash: %s' % str(tx_hash))
        return self.driver.request_tx_info(tx_hash)

    def list_txs(self, start, end):
        self.logger.info('list txs, pages: %s - %s' % (str(start), str(end)))
        txs = {}
        result, total_num = self.driver.get_tx_list(start, end)
        if result:
            txs['total_page'] = total_num / DISPLAY_LEN + 1
            txs['txs'] = result
        return txs

