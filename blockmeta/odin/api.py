# -*- coding: utf-8 -*-
import json
from utils import responses
from flask_restful import Resource, reqparse
from blockmeta.utils.bytom import remove_0x
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
        try:
            data = self.parser.parse_args()
            data = data.get('pttp_interest')
            data = json.loads(data)
            data = data['interest']

            uri = data['uri']
            uri = uri.strip().lower()
            arguments = uri.split('#')[0]
            argument_list = [arg for arg in arguments.split('/') if arg != ""]
            if len(argument_list) < 1 or argument_list[0] != self.ppk:
                return responses.wrap_ordin_response(400, uri)
            if len(argument_list) == 1:
                return responses.hello_world_response(uri)
            elif len(argument_list) == 2:
                return responses.parse_next_response(uri)
            elif len(argument_list) == 3:
                argument_list[2] = remove_0x(argument_list[2])
                found = self.manager.handle_odin(argument_list[1], argument_list[2])
                if found:
                    return responses.wrap_ordin_response(200, uri, found)
                else:
                    return responses.wrap_ordin_response(404, uri)
            else:
                pass
        except Exception as e:
            raise Exception('OdinAPI ERROR: %s', e)

