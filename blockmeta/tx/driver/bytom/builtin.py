# -*- coding: utf-8 -*-


from flask import current_app

from blockmeta.block.manager import BlockManager
from blockmeta.db.mongo import MongodbClient
from blockmeta.utils.bytom import remove_0x
from tools import flags, exception

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
        self.block_manager = BlockManager()

    def request_tx_info(self, tx_hash):
        try:
            tx = self.get_tx_by_hash(remove_0x(tx_hash))
            if tx is None:
                raise Exception("Transaction not found!")

            tx_info = self._show_tx(tx)
        except Exception, e:
            self.logger.error("tx.driver.builtin Error: %s" % str(e))
            raise Exception(e)
        return tx_info

    def get_tx_list(self, start, end):
        try:
            txs = []
            result = self.mongo_cli.get_many(
                table=FLAGS.transaction_info,
                n=end - start,
                sort_key=FLAGS.block_height,
                ascend=False,
                skip=start)
            total_num = self.mongo_cli.count(table=FLAGS.transaction_info)

            for tx in result:
                tx_info = self._show_tx(tx)
                txs.append(tx_info)
            return txs, total_num
        except Exception, e:
            self.logger.error("tx.driver.builtin Error: %s" % str(e))
            raise Exception(e)

    def get_tx_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: txhash})

        except Exception, e:
            raise exception.DBError(e)
        return tx

    def select_txin_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: txhash})
            txin = tx.get[FLAGS.transaction_in]
        except Exception, e:
            raise exception.DBError(e)
        return txin

    def select_txout_by_id(self, txout_id):
        try:
            txout = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.txout_id: txout_id})
        except Exception, e:
            raise exception.DBError(e)
        return txout

    def select_txout_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: txhash})
            txouts = tx.get[FLAGS.transaction_out]
        except Exception, e:
            raise exception.DBError(e)
        return txouts

    def _show_tx(self, tx):
        fields = ['block_hash', 'block_height', 'id', 'inputs', 'outputs', 'size', 'status_fail', 'time_range',
                  'version']
        result = {}
        for field in fields:
            result[field] = tx[field]

        block = self.block_manager.handle_block(result['block_hash'])
        result['block'] = block

        state = self.mongo_cli.get(flags.FLAGS.db_status)
        height = 0 if state is None else state[flags.FLAGS.block_height]
        result['confirmation'] = height - result['block_height'] + 1

        return result
