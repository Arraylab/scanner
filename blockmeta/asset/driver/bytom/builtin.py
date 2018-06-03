# coding=utf-8
import sys
sys.path.append('../')
sys.path.append('../../')
from blockmeta.db.mongo import MongodbClient
from tools import flags

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def request_asset_info(self, asset_id, page=1, tag='txs'):
        asset_object = self.mongo_cli.get_one(
            table=FLAGS.asset_info, cond={
                FLAGS.asset_id: asset_id})
        asset_info = self._show_asset(asset_object, page, tag)
        return asset_info

    @staticmethod
    def max_pages(num):
        return max(1, (num-1)/10+1)

    def list_assets(self, page=1):
        asset_num = self.mongo_cli.get_size(table=FLAGS.asset_info)
        page_max = self.max_pages(asset_num)
        page = min(page, page_max)
        skip = (page - 1) * 10
        asset_objects = self.mongo_cli. get_many(
            table=FLAGS.asset_info,
            cond={},
            n=10,
            sort_key='block_height',
            ascend=False,
            skip=skip)
        assets = [self._show_asset_base_info(
            asset_object) for asset_object in asset_objects]
        result = {
            'asset_num': asset_num,
            'assets': assets,
            'page': page,
            'pages': page_max
        }
        return result

    def _show_asset_base_info(self, asset_object):
        fields = [
            'asset_id',
            'amount',
            'asset_definition',
            'code',
            'issue_by',
            'retire']
        result = {field: asset_object.get(field) for field in fields}
        result['issue_timestamp'] = self._get_tx_timestamp(
            asset_object.get('issue_by'))
        result['update_timestamp'] = self._get_block_timestamp(
            asset_object.get('block_hash'))
        result['tx_num'] = len(asset_object.get('txs'))
        result['holder_num'] = len(asset_object.get('balances'))
        return result

    def _show_asset(self, asset_object, page, tag='txs'):
        if asset_object is None:
            return {}
        result = self._show_asset_base_info(asset_object)
        tag = 'txs' if tag not in ['txs', 'balances'] else tag
        page_max = self.max_pages(len(asset_object.get(tag)))
        page = min(page_max, page)
        result['info'] = self._get_txs_info(
            asset_object.get('txs'),
            page) if tag == 'txs' else self._get_balances_info(
            asset_object.get('balances'),
            page)
        result['page'] = page
        result['pages'] = page_max
        return result

    def _get_txs_info(self, tx_ids, page):
        start = (page - 1) * 10
        end = page * 10
        tx_ids.reverse()
        tx_ids = tx_ids[start:end]
        txs = [
            self.mongo_cli.get_one(
                flags.FLAGS.transaction_info, cond={
                    'id': tx_id}) for tx_id in tx_ids]
        info = [self.normalize_tx(tx) for tx in txs]
        return info

    def _get_balances_info(self, balances, page):
        start = (page - 1) * 10
        end = page * 10
        info = [{'address': k, 'balance': v} for k, v in balances.items()]
        info.sort(key=lambda e: e['balance'], reverse=True)
        return info[start:end]

    def normalize_tx(self, tx):
        fields = [
            'block_hash',
            'block_height',
            'id',
            'inputs',
            'outputs',
            'size',
            'status_fail',
            'time_range',
            'version']
        result = {field: tx.get(field) for field in fields}
        result['timestamp'] = self._get_block_timestamp(tx.get('block_hash'))
        return result

    def _get_block_timestamp(self, index):
        cond = {'height': index} if isinstance(index, int) else {'hash': index}
        timestamp = self.mongo_cli.get_one(
            table=FLAGS.block_info, cond=cond, fields={
                'timestamp': True}).get('timestamp')
        return timestamp

    def _get_tx_timestamp(self, tx_id):
        block_hash = self.mongo_cli.get_one(
            table=FLAGS.transaction_info, cond={
                'id': tx_id}, fields={
                'block_hash': True}) .get('block_hash')
        return self._get_block_timestamp(block_hash)
