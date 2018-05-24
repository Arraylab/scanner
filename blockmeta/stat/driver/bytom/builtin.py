# -*- coding: utf-8 -*-

from blockmeta.db.mongo import MongodbClient
from tools import flags, exception
import sys

FLAGS = flags.FLAGS


class BuiltinDriver:
    def __init__(self):
        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

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

    def request_chain_status(self):
        try:
            stats = self.mongo_cli.get_many(
                table=FLAGS.chain_status,
                n=1,
                sort_key=FLAGS.timestamp,
                ascend=False
            )
        except Exception as e:
            raise exception.DBError(e)
        return stats


if __name__ == '__main__':
    FLAGS(sys.argv)
    b = BuiltinDriver()
    print b.request_chain_status()
    print b.request_node_status()
