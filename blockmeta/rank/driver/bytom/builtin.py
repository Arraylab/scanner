# -*- coding: utf-8 -*-

from blockmeta.db.mongo import MongodbClient
from blockmeta.utils.bytom import get_total_btm
from tools import flags

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    # Sorted by balance, top 1000
    def get_rank_address(self):
        address_info = self.mongo_cli.get_many(
            table=FLAGS.address_info,
            n=100,
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

        height = self.mongo_cli.get(FLAGS.db_status).get('height')
        total_btm = get_total_btm(height)

        result = []
        for n in range(len(lists)):
            bal = lists[n]['balance']
            info = {
                'rank': n + 1,
                'address': lists[n]['address'],
                'balance': bal,
                'percentage': float(bal) / total_btm,
                'tx_count': len(lists[n]['txs'])
            }
            result.append(info)
        return result

