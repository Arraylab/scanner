# -*- coding: utf-8 -*-

from blockmeta.utils import util
from flask import current_app
from flask.ext.restful import Resource
from manager import StatManager


class ChainStatsAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = StatManager()
        super(ChainStatsAPI, self).__init__()

    def get(self):
        try:
            result = self.manager.list_chain_stats()
            return util.wrap_response(data=result)
        except Exception as e:
            self.logger.error("ChainStatsAPI.get Error: %s" % str(e))
            return util.wrap_error_response("tx_error")


class NodeStatsAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = StatManager()
        super(NodeStatsAPI, self).__init__()

    def get(self):
        try:
            result = self.manager.list_node_stats()
            return util.wrap_response(data=result)
        except Exception as e:
            self.logger.error("NodeStatsAPI.get Error: %s" % str(e))
            return util.wrap_error_response('tx_error')
