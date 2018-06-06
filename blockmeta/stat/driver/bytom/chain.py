# -*- coding: utf-8 -*-

from tools import flags
from blockmeta.db.dbproxy import MongoProxy
from blockmeta.utils.bytom import get_total_btm
import threading


FLAGS = flags.FLAGS
DEFAULT_ASSET_ID = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
mutex = threading.Lock()
STATS_NUMBER = 600


class ChainStats(object):

    def __init__(self):
        self.proxy = MongoProxy()

    # 上一个区块的出块间隔
    def get_last_block_interval(self, height):
        if height <= 0 or height is None:
            return None
        times = []
        for h in range(height-1, height+1):
            block = self.proxy.get_block_by_height(h)
            time = block.get(FLAGS.timestamp)
            times.append(time)
        return times[1] - times[0]

    # 指定高度块的难度
    def get_difficulty(self, height):
        if height <= 0 or height is None:
            return None
        block = self.proxy.get_block_by_height(height)
        return block.get(FLAGS.difficulty)

    # 前N个块的平均hash rate
    def get_average_hash_rate(self, height, num):
        if height - num <= 0 or height <= 0 or num <= 0 or height is None:
            return None
        hash_rates = self.proxy.get_hash_rate_in_range(height-num, height+1)
        sum = 0
        for hr in hash_rates:
            sum += hr['hash_rate']
        return sum / num

    # height高度前N个块的平均交易数
    def get_tx_num(self, height, num):
        if height - num <= 0 or height <= 0 or num <= 0:
            return None
        ts = self.proxy.get_transactions_in_range(height-num, height+1)
        transactions = [t['transactions'] for t in ts]
        sum = 0
        for txs in transactions:
            tx_num = len(txs)
            sum += tx_num
        return sum / num

    def get_tx_num_between(self, low, high):
        if low <= 0 or high <= 0 or low >= high:
            return None
        ts = self.proxy.get_transactions_in_range(low, high)
        transactions = [t['transactions'] for t in ts]
        sum = 0
        for txs in transactions:
            tx_num = len(txs)
            sum += tx_num
        return sum

    @staticmethod
    def get_recent_award(height):
        if height < 0:
            return None
        s = height / 840000
        return 41250000000 / (s + 1)

    # height高度前N个块的平均每个块费用
    def get_block_fee(self, height, num):
        if height - num <= 0 or height <= 0 or num <= 0:
            return None
        transactions = self.proxy.get_transactions_in_range(height-num, height+1)
        coinbases = [t['transactions'][0] for t in transactions]
        fees = [c['outputs'][0]['amount'] for c in coinbases]
        award = 0
        for h in range(height-num, height+1):
            award += self.get_recent_award(height)
        return (sum(fees) - award) / num

    @staticmethod
    def cal_tx_fee(tx):
        total_in = 0
        total_out = 0
        for txin in tx['inputs']:
            btm_in = txin['amount'] if txin['asset_id'] == DEFAULT_ASSET_ID else 0
            total_in += btm_in
        for txout in tx['outputs']:
            btm_out = txout['amount'] if txout['asset_id'] == DEFAULT_ASSET_ID else 0
            total_out += btm_out
        return total_in - total_out

    # 交易平均手续费（x neu/byte)
    def get_average_txs_fee(self, height):
        block = self.proxy.get_block_by_height(height)
        total_size = 0
        total_fee = 0
        for tx in block['transactions'][1:]:
            total_size += tx['size']
            total_fee += self.cal_tx_fee(tx)
        return 0 if total_size == 0 else total_fee / total_size

    # N个块的交易平均手续费, num表示某一高度height往前的N个块
    def get_average_txs_fee_n(self, height, num):
        if height - num <= 0 or num <= 0:
            return 0
        total_fee = 0
        for h in range(height-num, height + 1):
            f = self.get_average_txs_fee(h)
            total_fee += f
        return total_fee / num

    @staticmethod
    def get_interval(timestamps):
        if not isinstance(timestamps, list):
            return None
        intervals = []
        for i in range(len(timestamps) - 1):
            interval = timestamps[i + 1] - timestamps[i]
            intervals.append(interval)
        intervals.sort()
        return intervals

    def get_real_time_data(self):
        height = self.proxy.get_recent_height()
        block_hash = self.proxy.get_block_hash_by_height(height).get('hash')
        difficulty = self.proxy.get_difficulty_by_height(height)

        time_map = self.proxy.get_timestamps_in_range(height-STATS_NUMBER, height)
        timestamps = [t['timestamp'] for t in time_map]
        time_lapse = timestamps[-1] - timestamps[0]

        intervals = self.get_interval(timestamps)
        if intervals is None:
            return None

        avg_interval = time_lapse / (STATS_NUMBER - 1)
        max_interval = intervals[-1]
        min_interval = intervals[0]
        med_interval = intervals[STATS_NUMBER / 2]

        tx_num = self.get_tx_num_between(height-STATS_NUMBER, height)
        tps = '%.2f' % (float(tx_num) / time_lapse)

        total_tx_num = self.proxy.get_total_tx_num()
        total_addr_num = self.proxy.get_total_addr_num()
        total_btm_num = get_total_btm(height)

        avg_block_fee = self.get_block_fee(height, STATS_NUMBER)
        avg_tx_fee = avg_block_fee * STATS_NUMBER / (tx_num - STATS_NUMBER)

        result = {
            "height": height,
            "block_hash": block_hash,
            "difficulty": difficulty,
            "interval_avg": avg_interval,
            "interval_min": min_interval,
            "interval_max": max_interval,
            "interval_med": med_interval,
            "total_tx_num": total_tx_num,
            "total_addr_num": total_addr_num,
            "total_btm_num": total_btm_num,
            "block_fee_avg": avg_block_fee,
            "tx_fee_avg": avg_tx_fee,
            "tps_avg": tps
        }
        return result

