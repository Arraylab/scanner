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

    def request(self, attribute, content):
        if attribute == 'asset':
            return self.mongo_cli.get_one(table=FLAGS.asset_info, cond={'asset': content})
        return None
