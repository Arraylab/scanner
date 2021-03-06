# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, abort
from flask import current_app

from blockmeta.redis_cli_conf import cache, cache_key
from blockmeta.utils.bytom import remove_0x
from blockmeta.utils.util import valid_addr
from blockmeta.utils import util
from manager import AddressManager
from tools import flags

FLAGS = flags.FLAGS        


class AddressAPI(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.manager = AddressManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, help='transaction page number')

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self, address):
        try:
            address = remove_0x(address.strip().lower())
            args = self.parser.parse_args()
            page = args.get('page')

            if not isinstance(page, int) or page <= 0:
                page = 1

            if not valid_addr(address):
                abort(400, message="invalid address")
            # TODO: return 404 when wrong
            return self.manager.handle_address(address, page)
        except Exception, e:
            self.logger.error("BlockAPI.get Error: %s" % str(e))
            util.wrap_error_response()
