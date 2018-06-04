import re

from flask import current_app

from blockmeta.db.mongo import MongodbClient
from blockmeta.utils.bytom import remove_0x
from tools import flags

ADDRESS_RE = re.compile('bm[0-9A-Za-z]{40,60}\\Z')
HEIGHT_RE = re.compile('(?:0|[1-9][0-9]*)\\Z')
LEN_64_RE = re.compile('[0-9a-fA-F]{64}\\Z')
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

    def search(self, info):
        # info = info.strip()
        info_copy = info
        info = info.strip().lower()
        try:
            if HEIGHT_RE.match(info):
                return {'type': 'block', 'value': info}

            if ADDRESS_RE.match(info):
                return {'type': 'address', 'value': info}

            hash_value = remove_0x(info)
            if LEN_64_RE.match(hash_value):
                block = self.search_block_by_hash(hash_value)
                if block:
                    return {'type': 'block', 'value': hash_value}
                transaction = self.search_tx_by_hash(hash_value)
                if transaction:
                    return {'type': 'tx', 'value': hash_value}
                asset = self.search_asset_by_id(hash_value)
                if asset:
                    return {'type': 'asset', 'value': hash_value}
            asset_id_list = self.search_asset_by_definition(info_copy)
            if len(asset_id_list) > 0:
                return {'type': 'asset_list', 'value': asset_id_list}
            return None
        except Exception as e:
            self.logger.error(
                "Search.bytom.BuiltinDriver.search Error: %s" %
                str(e))

    def search_block_by_height(self, height):
        return self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: height})

    def search_block_by_hash(self, block_hash):
        return self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_id: block_hash})

    def search_tx_by_hash(self, tx_hash):
        return self.mongo_cli.get_one(table=FLAGS.transaction_info, cond={FLAGS.tx_id: tx_hash})

    def search_asset_by_id(self, asset_id):
        asset_dict = self.mongo_cli.get_one(
            table=FLAGS.asset_info, cond={
                FLAGS.asset_id: asset_id})
        return asset_dict

    def search_asset_by_definition(self, definition):
        asset_list = self.mongo_cli.get_many(
            table=FLAGS.asset_info, cond={
                '$or': [
                    {
                        'asset_definition.name': definition}, {
                        'asset_definition.symbol': definition}]}, items={
                'asset_id': True, '_id': False})
        id_list = [asset.get('asset_id') for asset in asset_list]
        return id_list
