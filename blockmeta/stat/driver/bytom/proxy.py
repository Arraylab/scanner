# -*- coding: utf-8 -*-

from blockmeta.db.mongo import MongodbClient
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


if __name__ == '__main__':
    FLAGS(sys.argv)
    db = DbProxy()
    print db.request_node_status()
    print
    print db.get_chain_stats_list()
    print
    print db.get_node_stats_list()
