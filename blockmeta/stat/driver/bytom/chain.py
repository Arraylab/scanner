# -*- coding: utf-8 -*-

from proxy import DbProxy
from tools import flags
import threading
import time

FLAGS = flags.FLAGS
DEFAULT_ASSET_ID = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
mutex = threading.Lock()


class ChainStats(object):

    def __init__(self):
        self.proxy = DbProxy()

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

    # 指定高度块的hash rate

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
        sum = 0
        for h in range(low, high):
            block = self.proxy.get_block_by_height(h)
            tx_num = len(block['transactions'])
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

    # 最近24小时内出块总数、平均时间、中位数、最大、最小; 交易总数、平均区块费用、平均交易费用、平均hash rate
    def get_chain_status(self):
        ticks = int(time.time())
        recent_height = self.proxy.get_recent_height()
        block = self.proxy.get_block_by_height(recent_height)
        recent_timestamp = block['timestamp']
        print 'recent_timestamp:', recent_timestamp
        block_hash = block['hash']
        if recent_timestamp + 86400 < ticks:
            return []

        close_height = recent_height - 576
        close_time = self.proxy.get_block_by_height(close_height)['timestamp']
        print 'close_time:', close_time
        if ticks - close_time < 86400:
            while ticks - close_time < 86400:
                close_height -= 1
                close_time = self.proxy.get_block_by_height(close_height)['timestamp']
        else:
            while ticks - close_time >= 86400:
                close_height += 1
                close_time = self.proxy.get_block_by_height(close_height)['timestamp']

        # 所有块时间戳
        tps = self.proxy.get_timestamps_in_range(close_height, recent_height)
        timestamps = [t['timestamp'] for t in tps]
        print 'timestamps:', timestamps

        total_block_num = recent_height - close_height
        timestamps.sort()
        print 'timestamps-2:', timestamps
        average_block_time = 86400 / total_block_num

        #  24小时内出块总数、平均时间、中位数、最大、最小
        intervals = self.get_interval(timestamps)
        length = len(intervals)
        median_interval = (intervals[length / 2] + intervals[length / 2 - 1]) / 2 if length % 2 == 0 else intervals[
            (length + 1) / 2]
        tx_num_24 = self.get_tx_num(recent_height, total_block_num) * total_block_num
        block_fee_24 = self.get_block_fee(recent_height, total_block_num)
        hash_rate_24 = self.get_average_hash_rate(recent_height, total_block_num)
        tx_fee_24 = self.get_average_txs_fee_n(recent_height, total_block_num)

        result = {
            "height": recent_height,
            "block_hash": block_hash,
            "timestamp": recent_timestamp,
            "hash_rate": hash_rate_24,
            "block_num": total_block_num,
            "tx_num": tx_num_24,
            "average_block_fee": block_fee_24,
            "average_tx_fee": tx_fee_24,
            "average_block_interval": average_block_time,
            "median_block_interval": median_interval,
            "max_block_interval": intervals[-1],
            "min_block_interval": intervals[0]
        }
        return result
