# -*- coding: utf-8 -*-
from flask import request
import json
from flask_restful import Resource, reqparse, abort
from blockmeta.utils import util
from manager import OdinManager
from tools import flags

FLAGS = flags.FLAGS


class OdinAPI(Resource):
    ppk = 'ppk:519502.2699'

    def __init__(self):
        self.manager = OdinManager()

    def post(self):
        r_data = request.get_data()
        data = json.loads(r_data)
        try:
            data = data['interest']
            uri = data['uri']
            arguments = uri.split('/')
            if len(arguments) != 3 or arguments[0] != self.ppk:
                raise Exception
            content = arguments[2].split('#')[0]
        except Exception:
            return util.wrap_ordin_response(400, uri)

        print arguments[1]
        print content
        found = self.manager.handle_odin(arguments[1], content)
        try:
            assert(found)
        except Exception:
            return util.wrap_ordin_response(404, uri)

        return util.wrap_ordin_response(200, uri, found)

