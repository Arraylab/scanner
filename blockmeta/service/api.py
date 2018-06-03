#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse
from flask import current_app
from blockmeta.utils import util
from config import BytomConf
from manager import ServiceManager
from tools import flags


FLAGS = flags.FLAGS


class BytomBaseAPI(Resource):

    def __init__(self):
        self.manager = ServiceManager()

        self.logger = current_app.logger
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('q', type=str, help='query info', ignore=True)
        super(BytomBaseAPI, self).__init__()

class BytomChainAPI(BytomBaseAPI):
    def __init__(self):
        self.apis = BytomConf.CHAIN_APIS
        super(BytomChainAPI, self).__init__()

    def get(self, chain_api):
        try:
            if chain_api is None:
                raise Exception("void query info")
            chain_api = chain_api.lower()  # Case-insensitive, BBE compatible
            if chain_api not in self.apis:
                raise Exception("Not a valid chain API")

            result = self.manager.handle_chain_api(chain_api)
            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("BytomChainAPI.get Error: %s" % str(e))
            return util.wrap_error_response("无效的Chain API参数")
