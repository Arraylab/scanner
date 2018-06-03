from driver.bytom.builtin import BuiltinDriver
from flask import current_app
from tools import flags

FLAGS = flags.FLAGS


class AssetManager:
    def __init__(self):
        self.logger = current_app.logger
        self.driver = BuiltinDriver()

    def handle_asset(self, asset_id, page=1, tag='txs'):
        self.logger.info('handle asset: %s | %s' % (str(asset_id), tag))
        return self.driver.request_asset_info(asset_id, page, tag)

    def list_assets(self, page=1):
        self.logger.info('list assets, page: %s', str(page))
        return self.driver.list_assets(page)
