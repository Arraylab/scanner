# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, abort
from blockmeta.utils import util
import time
import json
from manager import OdinManager
from tools import flags

FLAGS = flags.FLAGS


class OdinAPI(Resource):
    ppk = 'ppk:519502.2699'

    def __init__(self):
        self.manager = OdinManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('interest', type=json.loads, help='version')

    def get(self):
        args = self.parser.parse_args()
        data = args.get('interest')
        try:
            uri = ['uri']
            arguments = uri.split('/')
            if len(arguments) != 3 or arguments[0] != self.ppk:
                raise Exception
            content = arguments[2].split('#')[0]
        except Exception:
            return util.wrap_ordin_response(400, uri)

        found = self.manager.handle_odin(arguments[1], content)
        try:
            assert(found)
        except Exception:
            return util.wrap_ordin_response(404, uri)

        return util.wrap_ordin_response(200, uri, found)

