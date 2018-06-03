# -*- coding: utf-8 -*-

from blockmeta.db.mongo import MongodbClient
from flask import current_app
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

    def get_block_count(self):
        try:
            state = self.mongo_cli.get(flags.FLAGS.db_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if state is None else state[flags.FLAGS.block_height]


