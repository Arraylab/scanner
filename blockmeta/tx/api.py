# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.restful import Resource, reqparse

from blockmeta.constant import DEFAULT_OFFSET, DEFAULT_START
from blockmeta.utils import util
from blockmeta.utils.bytom import is_hash_prefix
from manager import TxManager
from tools import flags

FLAGS = flags.FLAGS


class TxAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = TxManager()
        super(TxAPI, self).__init__()

    def get(self, tx_hash):
        tx_hash.lower()
        try:
            if not is_hash_prefix(tx_hash):
                raise Exception("Transaction hash is wrong!")

            # TODO: return 404 if tx corresponding to tx_hash not found
            return self.manager.handle_tx(tx_hash) if tx_hash else {}
        except Exception, e:
            self.logger.error("TxAPI.get Error: %s" % str(e))
            util.wrap_error_response("tx_error")


class TxListAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = TxManager()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('end', type=int, help='block to')
        self.parser.add_argument('start', type=int, help='block from')
        self.parser.add_argument('page', type=int, help='page number')

        super(TxListAPI, self).__init__()

    def get(self):
        try:
            args = self.parser.parse_args()
            start, end = args.get('start'), args.get('end')
            page = args.get('page')

            # return block in range [start, end)
            if not isinstance(start, int):
                if isinstance(page, int):
                    start = DEFAULT_OFFSET * (page-1)
                else:
                    start = DEFAULT_START

            if not isinstance(end, int):
                if isinstance(page, int):
                    end = DEFAULT_OFFSET * page
                else:
                    end = DEFAULT_OFFSET

            result = self.manager.list_txs(start, end)
            result['page'] = 1 if not page else int(page)
            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("TxListAPI.get Error: %s" % str(e))
            return util.wrap_error_response('tx_error')
