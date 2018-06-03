# -*- coding: utf-8 -*-

from blockmeta.db.mongo import MongodbClient
from tools import flags

FLAGS = flags.FLAGS


class ChainStats:

    def __init__(self):

        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(flags.FLAGS.mongo_bytom)
