# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse
from flask import current_app
from blockmeta.utils import util
from manager import RankManager
from tools import flags


FLAGS = flags.FLAGS


class RankAPI(Resource):

    def __int__(self):
        self.logger = current_app.logger
        self.manager = RankManager()

        super(RankAPI, self).__init__()

    def get(self):
        try:
            rank_info = self.manager.handle_rank_address()
            return util.wrap_response(data=rank_info)
        except Exception, e:
            self.logger.error("BlockAPI.get Error: %s" % str(e))
            return util.wrap_error_response()
