# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.restful import Resource

from blockmeta.redis_cli_conf import cache, cache_key
from blockmeta.utils import util
from manager import RankManager
from tools import flags


FLAGS = flags.FLAGS


class RankAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = RankManager()

        super(RankAPI, self).__init__()

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self):
        try:
            rank_info = self.manager.handle_rank_address()
            return util.wrap_response(data=rank_info)
        except Exception as e:
            self.logger.error("RankAPI.get Error: %s" % str(e))
            return util.wrap_error_response()
