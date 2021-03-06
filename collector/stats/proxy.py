# -*- coding: utf-8 -*-

from collector.db.mongodriver import MongodbClient
from tools import exception, flags
import sys

FLAGS = flags.FLAGS


class DbProxy(object):

    def __init__(self):
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(flags.FLAGS.mongo_bytom)

    def get_recent_height(self):
        try:
            state = self.mongo_cli.get(flags.FLAGS.db_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if state is None else state[flags.FLAGS.block_height]

    # TODO 索引
    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})

    def get_hash_rate_in_range(self, start, end):
        try:
            hash_rates = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                items={"hash_rate": 1, "_id": 0},
                n=end-start,
                skip=start)
        except Exception as e:
            raise exception.DBError(e)
        return hash_rates

    def get_timestamps_in_range(self, start, end):
        try:
            timestamps = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                items={"timestamp": 1, "_id": 0},
                n=end-start,
                skip=start)
        except Exception as e:
            raise exception.DBError(e)
        return timestamps

    def get_status(self):
        try:
            state = self.mongo_cli.get_one(
                    table=FLAGS.chain_status, cond={
                        FLAGS.block_height: 0})
        except Exception as e:
            raise exception.DBError(e)
        return None if state is None else state

    def get_chain_stats_list(self):
        try:
            stats = self.mongo_cli.get_many(table=FLAGS.chain_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if stats is None else stats

    def get_node_stats_list(self):
        try:
            stats = self.mongo_cli.get_many(table=FLAGS.node_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if stats is None else stats

    def save_chain(self, status):
        try:
            self.mongo_cli.insert(flags.FLAGS.node_status, status)
        except Exception as e:
            raise exception.DBError(e)

    def save_chain_patch(self, status_list):
        try:
            self.mongo_cli.insert_many(flags.FLAGS.chain_status, status_list)
        except Exception as e:
            raise exception.DBError(e)

    def save_node(self, status):
        try:
            self.mongo_cli.insert(flags.FLAGS.node_status, status)
        except Exception as e:
            raise exception.DBError(e)

    def request_node_status(self):
        try:
            stats = self.mongo_cli.get_many(
                table=FLAGS.node_status,
                n=1,
                sort_key=FLAGS.timestamp,
                ascend=False
            )
        except Exception as e:
            raise exception.DBError(e)
        return stats

    def get_transactions_in_range(self, low, high):
        try:
            coinbase = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                items={"transactions": 1, "_id": 0},
                n=high - low,
                skip=low)
        except Exception as e:
            raise exception.DBError(e)
        return coinbase

    def count_accounts(self):
        return self.mongo_cli.count('address_info')

    def count_txs(self):
        return self.mongo_cli.count('transaction_info')

    def get_total_tx_num(self):
        try:
            total_num = self.mongo_cli.count(FLAGS.transaction_info)
        except Exception as e:
            raise exception.DBError(e)
        return total_num

    def get_total_addr_num(self):
        try:
            total_num = self.mongo_cli.count(FLAGS.address_info)
        except Exception as e:
            raise exception.DBError(e)
        return total_num

    def get_total_btm(self, height):
        init_btm = 140700041250000000
        init_award = 41250000000
        epoch_length = 840000
        epoch = height // epoch_length

        total_num = 0
        for n in range(epoch + 1):
            award = init_award / (n + 1)
            total_num += award * (height - n * epoch_length)

        total_num += init_btm
        return total_num


if __name__ == '__main__':
    FLAGS(sys.argv)
    db = DbProxy()
    print db.get_recent_height()
    print db.count_accounts()
    print db.count_txs()

