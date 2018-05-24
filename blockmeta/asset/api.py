from flask_restful import Resource, reqparse, abort

from manager import AssetManager
from tools import flags

FLAGS = flags.FLAGS


class AssetAPI(Resource):
	def __init__(self):
		self.manager = AssetManager()
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('page', type=int, help='page number of txs/balances')
		self.parser.add_argument('tag', type=str, help='txs/balaces')

	def get(self, asset_id):
		asset_id.strip().lower()
		args = self.parser.parse_args()
		page = args.get('page')
		tag = args.get('tag')
		if not isinstance(page, int) or page <= 0:
			page = 1
		if not isinstance(tag, str) or tag not in ['txs', 'balances']:
			tag = 'txs'
		return self.manager.handle_asset(asset_id, page, tag)
