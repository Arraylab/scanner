from flask_restful import Resource, reqparse

from blockmeta.search.manager import SearchManager
from blockmeta.utils import util
from tools import flags

FLAGS = flags.FLAGS


class SearchAPI(Resource):
    
    def __init__(self):
        self.manager = SearchManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('q', type=str, help='query info', ignore=False)
        super(SearchAPI, self).__init__()

    def post(self):
        args = self.parser.parse_args()
        info = args.get('q')

        found = self.manager.search(info)
        if not found:
            return util.wrap_response(status='fail', data=found, code='404')
        return util.wrap_response(status='success', data=found, code='302')
