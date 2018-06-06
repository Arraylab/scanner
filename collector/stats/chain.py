# -*- coding: utf-8 -*-

from collector.agent.fetcher import Fetcher
from proxy import DbProxy
from tools import flags
import gevent
import threading
import time

FLAGS = flags.FLAGS
DEFAULT_ASSET_ID = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
CONFIRM_NUM = 6
mutex = threading.Lock()


class ChainStats(object):

    def __init__(self):
        self.proxy = DbProxy()
        self.fetcher = Fetcher()

    # 上一个区块的出块间隔
    def get_last_block_interval(self, height):
        if height <= 0 or height is None:
            return None
        times = []
        for h in range(height - 1, height + 1):
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

    # height高度前N个块的平均交易数
    def get_tx_num(self, height, num):
        if height - num <= 0 or height <= 0 or num <= 0:
            return None
        ts = self.proxy.get_transactions_in_range(height - num, height + 1)
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
        transactions = self.proxy.get_transactions_in_range(
            height - num, height + 1)
        coinbases = [t['transactions'][0] for t in transactions]
        fees = [c['outputs'][0]['amount'] for c in coinbases]
        award = 0
        for h in range(height - num, height + 1):
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

    # 交易平均手续费（neu)
    def get_txs_fee(self, height):
        block = self.proxy.get_block_by_height(height)
        total_fee = 0
        for tx in block['transactions'][1:]:
            total_fee += self.cal_tx_fee(tx)
        return total_fee

    # N个块的交易平均手续费, num表示某一高度height往前的N个块
    def get_average_txs_fee_n(self, height, num):
        if height - num <= 0 or num <= 0:
            return 0
        total_fee = 0
        for h in range(height - num, height + 1):
            f = self.get_txs_fee(h)
            total_fee += f
        return total_fee / num

    @staticmethod
    def get_interval(timestamps):
        if not isinstance(timestamps, list):
            return None
        timestamps.sort()
        avg_interval = (timestamps[-1] - timestamps[0]) / (len(timestamps) - 1)
        intervals = []
        for i in range(len(timestamps) - 1):
            interval = timestamps[i + 1] - timestamps[i]
            intervals.append(interval)
        intervals.sort()

        length = len(intervals)
        median_interval = (intervals[length / 2] + intervals[length / 2 - 1]) / \
            2 if length % 2 == 0 else intervals[(length + 1) / 2]
        intervals_map = {
            "interval_avg": avg_interval,
            "interval_max": intervals[-1],
            "interval_min": intervals[0],
            "interval_med": median_interval
        }
        return intervals_map

    def get_total_num(self, height):
        total_btm_num = self.proxy.get_total_btm(height)
        total_addr_num = self.proxy.get_total_addr_num()
        total_tx_num = self.proxy.get_total_tx_num()
        total = {
            "total_btm_num": total_btm_num,
            "total_addr_num": total_addr_num,
            "total_tx_num": total_tx_num
        }
        return total

    # latest 24 hours
    def chain_status(self):
        ticks = int(time.time())
        recent_height = self.proxy.get_recent_height() - CONFIRM_NUM
        block = self.proxy.get_block_by_height(recent_height)
        recent_timestamp = block['timestamp']
        difficulty = block['difficulty']
        block_hash = block['hash']

        if recent_timestamp + 86400 < ticks:
            return []

        close_height = recent_height - 576
        close_time = self.proxy.get_block_by_height(close_height)['timestamp']
        if ticks - close_time < 86400:
            while ticks - close_time < 86400:
                close_height -= 1
                close_time = self.proxy.get_block_by_height(close_height)[
                    'timestamp']
        else:
            while ticks - close_time >= 86400:
                close_height += 1
                close_time = self.proxy.get_block_by_height(close_height)[
                    'timestamp']

        tps = self.proxy.get_timestamps_in_range(close_height, recent_height)
        timestamps = [t['timestamp'] for t in tps]

        for i in range(1, CONFIRM_NUM + 1):
            t = self.proxy.get_block_by_height(close_height - i)['timestamp']
            timestamps.append(t)
        total_block_num = recent_height - close_height + CONFIRM_NUM
        timestamps.sort()

        intervals = self.get_interval(timestamps)
        tx_num_24 = self.get_tx_num(
            recent_height, total_block_num) * total_block_num
        block_fee_24 = self.get_block_fee(recent_height, total_block_num)
        tx_fee_24 = self.get_average_txs_fee_n(recent_height, total_block_num)

        result = {
            "height": recent_height,
            "block_hash": block_hash,
            "difficulty": difficulty,
            "timestamp": recent_timestamp,
            "24_block_num": total_block_num,
            "24_tx_num": tx_num_24,
            "24_block_fee_avg": block_fee_24,
            "24_tx_fee_avg": tx_fee_24,
            "intervals": intervals,
            "total_num": self.get_total_num(recent_height)
        }
        return result

    # 两区块高度间的chain状态 [low, high)
    def chain_status_between(self, low, high):
        if low <= 0 or high <= 0 or low >= high:
            return None
        recent_block = self.proxy.get_block_by_height(high)
        block_hash = recent_block['hash']
        difficulty = recent_block['difficulty']

        recent_timestamp = recent_block['timestamp']
        total_block_num = high - low

        block_fee = self.get_block_fee(high, total_block_num)
        total_tx_num = 0
        tx_fee = self.get_average_txs_fee_n(high, total_block_num)

        timestamps = []
        for h in range(low, high):
            block = self.proxy.get_block_by_height(h)
            tx_num = len(block['transactions'])
            total_tx_num += tx_num
            t = block['timestamp']
            timestamps.append(t)
        intervals = self.get_interval(timestamps)

        result = {
            "height": high,
            "block_hash": block_hash,
            "difficulty": difficulty,
            "timestamp": recent_timestamp,
            "24_block_num": total_block_num,
            "24_tx_num": total_tx_num,
            "24_block_fee_avg": block_fee,
            "24_tx_fee_avg": tx_fee,
            "intervals": intervals,
            "total_num": self.get_total_num(high)
        }
        return result

    def _compute(self, stats_list, low, high):
        s = self.chain_status_between(low, high)
        mutex.acquire(1)
        stats_list.append(s)
        mutex.release()

    def check_syn_height(self):
        chain_height = self.fetcher.request_chain_height()
        db_height = self.proxy.get_recent_height()
        if db_height < chain_height:
            return False
        return True

    # 历史每天的chain状态
    def chain_status_history(self):
        while not self.check_syn_height():
            time.sleep(10)
        recent_height = self.proxy.get_recent_height()
        genesis_time = self.proxy.get_block_by_height(0)['timestamp']

        tps = self.proxy.get_timestamps_in_range(0, recent_height + 1)
        timestamps = sorted([t['timestamp'] for t in tps])

        height_point = []
        point = genesis_time
        for i in range(len(timestamps)):
            if timestamps[i] - point < 86400:
                continue
            height_point.append(i)
            point = timestamps[i]

        result = []
        jobs = [gevent.spawn(self._compute, result, height_point[i],
                             height_point[i + 1]) for i in range(len(height_point) - 1)]
        gevent.joinall(jobs)
        return result

    def genesis_status(self):
        block = self.proxy.get_block_by_height(0)
        while block is None:
            time.sleep(2)
            block = self.proxy.get_block_by_height(0)
        tx_num = len(block['transactions'])

        initial_status = {
            "height": 0,
            "block_hash": block['hash'],
            "timestamp": block['timestamp'],
            "24_block_num": 1,
            "24_tx_num": tx_num,
            "24_block_fee_avg": 0,
            "24_tx_fee_avg": 0,
            "intervals": {},
            "total_num": {}
        }
        return initial_status

    # 将历史数据存进db
    def load(self):
        if self.proxy.get_status() is None:
            status_genesis = self.genesis_status()
            status_history = self.chain_status_history()
            status_history.append(status_genesis)
            self.proxy.save_chain_patch(status_history)
        else:
            pass

    def save(self):
        status = self.chain_status()
        self.proxy.save_chain(status)
