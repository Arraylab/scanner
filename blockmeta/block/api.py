# -*- coding: utf-8 -*-

from flask import current_app
from flask_restful import Resource, reqparse

from blockmeta.constant import DEFAULT_OFFSET
from blockmeta.utils import util
from manager import BlockManager
from tools import flags

FLAGS = flags.FLAGS


class BlockAPI(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.manager = BlockManager()

        super(BlockAPI, self).__init__()

    def get(self, block_id):
        block_id.lower()
        try:
            result = self.manager.handle_block(block_id)
            return util.wrap_response(result)
        except Exception, e:
            self.logger.error("BlockAPI.get Error: %s" % str(e))
            return util.wrap_error_response('block_error')


class BlockListAPI(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.manager = BlockManager()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, help='page number')

        super(BlockListAPI, self).__init__()

    def get(self):
        try:
            args = self.parser.parse_args()
            page = args.get('page')
            if not isinstance(page, int) or page <= 0:
                page = 1
            start, end = DEFAULT_OFFSET * (page - 1), DEFAULT_OFFSET * page

            result = self.manager.list_blocks(start, end)
            result['no_page'] = 1 if not page else int(page)

            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("BlockListAPI.get Error: %s" % str(e))
            return util.wrap_error_response('block_error')

