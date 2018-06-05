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


class BytomBlockAPI(BytomBaseAPI):

    def __init__(self):
        self.apis = BytomConf.BLOCK_APIS
        super(BytomBlockAPI, self).__init__()

    def get(self, block_api):
        try:
            if block_api is None:
                raise Exception("void query info")

            args = self.parser.parse_args()
            query = args.get('q', self.apis[0])

            if query not in self.apis:
                raise Exception("Not a valid block API")

            result = self.manager.handle_block_api(block_api.lower(), query)
            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("BytomBlockAPI.get Error: %s" % str(e))
            return util.wrap_error_response("无效的Block API参数")


class BytomTxAPI(BytomBaseAPI):

    def __init__(self):
        self.apis = BytomConf.TX_APIS
        super(BytomTxAPI, self).__init__()

    def get(self, tx_api):
        try:
            if tx_api is None:
                raise Exception("void query info")

            args = self.parser.parse_args()
            query = args.get('q', self.apis[0])

            if query not in self.apis:
                raise Exception("Not a valid Tx API")

            result = self.manager.handle_tx_api(tx_api.lower(), query)
            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("BytomTxAPI.get Error: %s" % str(e))
            return util.wrap_error_response("无效的Tx API参数")


class BytomAddressAPI(BytomBaseAPI):

    def __init__(self):
        self.apis = BytomConf.ADDR_APIS
        super(BytomAddressAPI, self).__init__()

    def get(self, addr_api):
        try:
            if addr_api is None:
                raise Exception("void query info")

            args = self.parser.parse_args()
            query = args.get('q', self.apis[0])

            if query not in self.apis:
                raise Exception("Not a valid Address API")

            result = self.manager.handle_address_api(addr_api.lower(), query)
            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("BytomAddressAPI.get Error: %s" % str(e))
            return util.wrap_error_response("无效的Address API参数")
