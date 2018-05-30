# -*- coding: utf-8 -*-

from flask import current_app
from blockmeta.redis_cli_conf import cache, cache_key
from flask_restful import Resource, reqparse
from blockmeta.utils.bytom import remove_0x
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

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self, block_id):
        block_id = remove_0x(block_id.strip().lower())

        result = self.manager.handle_block(block_id)
        if result is None:
            return util.wrap_error_response(status='failure', code='404')
        return util.wrap_response(status='success', code='200', data=result)


class BlockListAPI(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.manager = BlockManager()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, help='page number')

        super(BlockListAPI, self).__init__()

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self):
        try:
            args = self.parser.parse_args()
            page = args.get('page', None) if args is not None else None
            if not isinstance(page, int) or page <= 0:
                page = 1
            start, end = DEFAULT_OFFSET * (page - 1), DEFAULT_OFFSET * page
            result = self.manager.list_blocks(start, end)
            if len(result.get('blocks', [])) == 0:
                return util.wrap_error_response(status='failure', code='404')
            result['no_page'] = 1 if not page else int(page)
            return util.wrap_response(status='success', code='200', data=result)
        except Exception, e:
            return util.wrap_error_response(status='failure', code='404')

