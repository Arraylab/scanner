# -*- coding: utf-8 -*-
from flask import request
import json
from flask_restful import Resource, reqparse
from blockmeta.utils import util
from manager import OdinManager
from tools import flags

FLAGS = flags.FLAGS


class OdinAPI(Resource):
    ppk = 'ppk:519502.2699'

    def __init__(self):
        self.manager = OdinManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('pttp_interest', type=str, help='pttp interest request')

    def get(self):
        data = self.parser.parse_args()
        data = data.get('pttp_interest')
        data = json.loads(data)
        data = data['interest']

        uri = data['uri']
        arguments = uri.split('#')[0]
        arguments.strip()
        argument_list = [ arg for arg in arguments.split('/') if arg != ""]

        if len(argument_list) < 1 or argument_list[0] != self.ppk:
            return util.wrap_ordin_response(400, uri)
        if len(argument_list) == 1:
            return util.hello_world_response(uri)
        elif len(argument_list) == 2:
            return util.parse_next_response(uri)
        elif len(argument_list) == 3:
            found = self.manager.handle_odin(argument_list[1], argument_list[2])
            if found:
                return util.wrap_ordin_response(200, uri, found)
            else:
                return util.wrap_ordin_response(404, uri)
        else:
            pass
        return None
