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
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def search(self, info):
        info.strip().lower()
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

            return None

        except Exception, e:
            self.logger.error("Search.bytom.BuiltinDriver.search Error: %s" % str(e))

    def search_block_by_height(self, height):
        return self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: height})

    def search_block_by_hash(self, block_hash):
        return self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_id: block_hash})

    def search_tx_by_hash(self, tx_hash):
        return self.mongo_cli.get_one(table=FLAGS.transaction_info, cond={FLAGS.tx_id: tx_hash})
