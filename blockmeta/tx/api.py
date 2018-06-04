# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource, reqparse

from blockmeta.constant import DEFAULT_OFFSET, DEFAULT_START
from blockmeta.redis_cli_conf import cache, cache_key
from blockmeta.utils import util
from blockmeta.utils.bytom import is_hash_prefix, remove_0x
from manager import TxManager
from tools import flags

FLAGS = flags.FLAGS


class TxAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = TxManager()
        super(TxAPI, self).__init__()

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self, tx_hash):
        tx_hash = remove_0x(tx_hash.strip().lower())
        try:
            if not is_hash_prefix(tx_hash):
                raise Exception("Transaction hash is wrong!")

            # TODO return 404 if tx corresponding to tx_hash not found
            return self.manager.handle_tx(tx_hash) if tx_hash else {}
        except Exception as e:
            self.logger.error("TxAPI.get Error: %s" % str(e))
            util.wrap_error_response()


class TxListAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = TxManager()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('end', type=int, help='block to')
        self.parser.add_argument('start', type=int, help='block from')
        self.parser.add_argument('page', type=int, help='page number')

        super(TxListAPI, self).__init__()

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self):
        try:
            args = self.parser.parse_args()
            start, end = args.get('start'), args.get('end')
            page = args.get('page')

            # return block in range [start, end)
            if not isinstance(start, int):
                if isinstance(page, int):
                    start = DEFAULT_OFFSET * (page - 1)
                else:
                    start = DEFAULT_START

            if not isinstance(end, int):
                if isinstance(page, int):
                    end = DEFAULT_OFFSET * page
                else:
                    end = DEFAULT_OFFSET

            result = self.manager.list_txs(start, end)
            result['page'] = 1 if not page else int(page)
        except Exception as e:
            self.logger.error("TxListAPI.get Error: %s" % str(e))
            return util.wrap_error_response()

        return util.wrap_response(data=result)
