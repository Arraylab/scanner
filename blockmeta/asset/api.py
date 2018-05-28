from flask_restful import Resource, reqparse, abort

from manager import AssetManager
from tools import flags

FLAGS = flags.FLAGS


class AssetAPI(Resource):
    def __init__(self):
        self.manager = AssetManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'page', type=int, help='page number of txs/balances')
        self.parser.add_argument('tag', type=str, help='txs/balaces')

    def get(self, asset_id):
        asset_id.strip().lower()
        args = self.parser.parse_args()
        page = args.get('page')
        tag = args.get('tag')
        page = 1 if page is None or not isinstance(
            page, int) or page <= 0 else page
        tag = 'txs' if tag is None or not isinstance(tag, str) or tag not in [
            'txs', 'balances'] else tag
        result = self.manager.handle_asset(asset_id, page, tag)
        if len(result) == 0:
            abort(404, message="asset not found")
        return result


class AssetListAPI(Resource):
    def __init__(self):
        self.manager = AssetManager()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, help='page number')

    def get(self):
        args = self.parser.parse_args()
        page = args.get('page')
        page = 1 if page is None or not isinstance(
            page, int) or page <= 0 else page
        print '********************************', page
        result = self.manager.list_assets(page)
        return result
