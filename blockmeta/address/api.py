# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, abort

from blockmeta.utils.util import valid_addr
from manager import AddressManager
from tools import flags

FLAGS = flags.FLAGS        


class AddressAPI(Resource):
    def __init__(self):
        self.manager = AddressManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('p', type=int, help='transaction page number')

    def get(self, address):
        address.lower()
        args = self.parser.parse_args()
        page = args.get('page')
        if not isinstance(page, int) or page <= 0:
            page = 1

        if not valid_addr(address):
            abort(400, message="invalid address")

        return self.manager.handle_address(address, page)
