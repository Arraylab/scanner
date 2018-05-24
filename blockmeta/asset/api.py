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
		print asset_id
		asset_id.strip().lower()
		args = self.parser.parse_args()
		page = args.get('page')
		tag = args.get('tag')

		page = 1 if page is None or not isinstance(page, int) or page <= 0 else page
		tag = 'txs' if tag is None or not isinstance(tag, str) or tag not in ['txs', 'balances'] else page
		result = self.manager.handle_asset(asset_id, page, tag)
		if len(result) == 0:
			abort(404, message="asset not found")
		return result

# class AssetListAPI(Resource):
# 	def __init__(self):
# 		self.manager = AssetManager()
# 		self.parser = reqparse.RequestParser()
# 		self.parser.add_argument('page', type=int, help='page number')
#
# 	def get(self):
# 		try:
# 			args = self.parser.parse_args()
# 			page = args.get('page')
# 			if not isinstance(page, int) or page <= 0:
# 				page = 1
# 			result = self.manager.list_blocks(page)
#
# 			return util.wrap_response(data=result)
# 		except Exception, e:
# 			self.logger.error("BlockListAPI.get Error: %s" % str(e))
# 			return util.wrap_error_response('block_error')
