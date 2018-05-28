# coding=utf-8

from blockmeta.db.mongo import MongodbClient
from tools import flags

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def request_address_info(self, addr, page=1):
        addr_object = self.mongo_cli.get_one(table=FLAGS.address_info, cond={FLAGS.address: addr})
        addr_info = self._show_addr(addr_object, page)
        return addr_info

    def _show_addr(self, addr, page):
        if addr is None:
            return {
                'balance': 0,
                'sent': 0,
                'recv': 0,
                'tx_num': 0,
                'txs': [],
                'asset_balance': {}
            }

        fields = ['balance', 'sent', 'recv', 'asset_balances']
        result = {}
        for field in fields:
            result[field] = addr[field]

        start = (page - 1) * 10
        if start >= len(addr['txs']):
            raise Exception('page exceed the maximum')

        end = page * 10
        if end >= len(addr['txs']):
            end = len(addr['txs'])
        addr['txs'].reverse()
        tx_ids = addr['txs'][start:end]
        txs = []
        for tx_id in tx_ids:
            tx = self.mongo_cli.get_one(flags.FLAGS.transaction_info, cond={'id': tx_id})
            txs.append(self.normalize_tx(tx))
        result['txs'] = txs
        result['tx_num'] = len(addr['txs'])
        result['no_page'] = page
        result['pages'] = len(addr['txs']) / 10 + 1
        return result

    def normalize_tx(self, tx):
        fields = ['block_hash', 'block_height', 'id', 'inputs', 'outputs', 'size', 'status_fail', 'time_range',
                  'version']
        result = {}
        for field in fields:
            result[field] = tx[field]

        block = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: int(tx.get('block_height'))})
        if block:
            result['timestamp'] = block.get('timestamp')
        return result
