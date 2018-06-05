# -*- coding: utf-8 -*-

from flask import current_app

from blockmeta.db.mongo import MongodbClient
from blockmeta.service.driver.bytom.builtin import BuiltinDriver as ServiceDriver
from tools import flags

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.logger = current_app.logger
        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    # Sorted by balance, top 1000
    def get_rank_address(self):
        address_info = self.mongo_cli.get_many(
            table=FLAGS.address_info,
            n=1000,
            items={
                'address': 1,
                'balance': 1,
                'txs': 1,
                '_id': 0},
            sort_key='balance',
            ascend=False
        )
        result = self._show_rank_info(address_info)
        return result

    def _show_rank_info(self, lists):
        if not isinstance(lists, list):
            return None
        # fields = ['rank', 'address', 'balance', 'percentage', 'tx_count']

        driver = ServiceDriver()
        total_btm = driver.get_total_btm()

        result = []
        for n in range(len(lists)):
            info = {}
            info['rank'] = n + 1
            info['address'] = lists[n]['address']
            info['balance'] = lists[n]['balance']
            info['percentage'] = float(info['balance']) / total_btm * 100
            info['tx_count'] = len(lists[n]['txs'])
            result.append(info)
        return result

