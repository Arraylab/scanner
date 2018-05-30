from flask_restful import Resource, reqparse
from blockmeta.redis_cli_conf import cache, cache_key
from blockmeta.utils.bytom import remove_0x
from blockmeta.utils import util
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

    @cache.cached(timeout=60 * 3, key_prefix=cache_key)
    def get(self, asset_id):
        asset_id = remove_0x(asset_id.strip().lower())
        args = self.parser.parse_args()
        page = args.get('page')
        tag = args.get('tag')
        page = 1 if page is None or not isinstance(
            page, int) or page <= 0 else page
        tag = 'txs' if tag is None or not isinstance(tag, str) or tag not in [
            'txs', 'balances'] else tag
        result = self.manager.handle_asset(asset_id, page, tag)
        if len(result) == 0:
            return util.wrap_error_response(status='failure', code='404', message='asset not found')
        return util.wrap_response(status='success', code='200', data=result)


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
        result = self.manager.list_assets(page)
        return util.wrap_response(status='success', code='200', data=result)
