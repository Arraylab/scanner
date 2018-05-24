from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class AssetManager:
    def __init__(self):
        self.driver = BuiltinDriver()

    def handle_asset(self, asset_id, page=1, tag='txs'):
        return self.driver.request_asset_info(asset_id, page, tag)
