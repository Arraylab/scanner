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
            asset_info = self.mongo_cli.get_one(table=FLAGS.asset_info, cond={'asset_id': content})
            return self._show_asset(asset_info) if asset_info is not None else {}
        return None

    @staticmethod
    def _show_asset(asset_info):
        asset_info.pop('_id')
        return asset_info

