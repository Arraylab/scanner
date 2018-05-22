# -*- coding: utf-8 -*-

from collector.db.mongodriver import MongodbClient
from tools import flags
import sys
import time

FLAGS = flags.FLAGS
DEFAULT_ASSET_ID = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
CONFIRM_NUM = 6


class ChainStats(object):

    def __init__(self):

        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(flags.FLAGS.mongo_bytom)

    def get_recent_height(self):
        state = self.mongo_cli.get(flags.FLAGS.db_status)
        return None if state is None else state[flags.FLAGS.block_height]

    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})

    def get_status(self):
        state = self.mongo_cli.get_one(
                table=FLAGS.chain_status, cond={
                    FLAGS.block_height: 0})
        return None if state is None else state

    # 上一个区块的出块间隔
    def get_last_block_interval(self, height):
        if height <= 0 or height is None:
            return None
        times = []
        for h in range(height-1, height+1):
            block = self.get_block_by_height(h)
            time = block.get(FLAGS.timestamp)
            times.append(time)
        return times[1] - times[0]

    # 指定高度块的难度
    def get_difficulty(self, height):
        if height <= 0 or height is None:
            return None
        block = self.get_block_by_height(h)
        return block.get(FLAGS.difficulty)

    # 指定高度块的hash rate

    # 前N个块的平均hash rate
    # def get_average_hash_rate(self, height, num):
    #     if height - num <= 0 or height <= 0 or num <= 0 or height is None:
    #         return None
    #     sum = 0
    #     for h in range(height-num, height+1):
    #
    #         hash_rate = response['data']['hash_rate']
    #         sum += hash_rate
    #     return sum / num

    # height高度前N个块的平均交易数
    def get_tx_num(self, height, num):
        if height - num <= 0 or height <= 0 or num <= 0:
            return None
        sum = 0
        for h in range(height-num+1, height+1):
            block = self.get_block_by_height(h)
            tx_num = len(block['transactions'])
            sum += tx_num
        return sum / num

    def get_tx_num_between(self, low, high):
        if low <= 0 or high <= 0 or low >= high:
            return None
        sum = 0
        for h in range(low, high):
            block = self.get_block_by_height(h)
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
        sum = 0
        for h in range(height-num, height+1):
            block = self.get_block_by_height(h)
            coinbase = block['transactions'][0]
            fee = coinbase['outputs'][0]['amount'] - self.get_recent_award(height)
            sum += fee
        return sum / num

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
        block = self.get_block_by_height(height)
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
    def chain_status(self):
        ticks = int(time.time())
        recent_height = self.get_recent_height() - CONFIRM_NUM
        block = self.get_block_by_height(recent_height)
        recent_timestamp = block['timestamp']
        block_hash = block['block_hash']
        if recent_timestamp + 86400 < ticks:
            return []
        ti = ticks
        height = recent_height

        # 所有块时间戳
        timestamps = []
        while ticks - ti < 86400:
            height = height - 1
            ti = self.get_block_by_height(height)['timestamp']
            timestamps.append(ti)
        for i in range(1, CONFIRM_NUM+1):
            t = self.get_block_by_height(height-i)['timestamp']
            timestamps.append(t)
        total_num = recent_height - height + CONFIRM_NUM
        timestamps.sort()
        average_block_time = 86400 / total_num

        #  24小时内出块总数、平均时间、中位数、最大、最小
        intervals = self.get_interval(timestamps)
        length = len(intervals)
        median_interval = (intervals[length/2] + intervals[length/2-1]) / 2 if length % 2 == 0 else intervals[(length+1)/2]
        tx_num_24 = self.get_tx_num(recent_height, total_num) * total_num
        block_fee_24 = self.get_block_fee(recent_height, total_num)
        # hash_rate_24 = self.get_average_hash_rate(recent_height, total_num)
        tx_fee_24 = self.get_average_txs_fee_n(recent_height, total_num)

        result = {
            "height": recent_height,
            "block_hash": block_hash,
            "timestamp": recent_timestamp,
            "block_num_24": total_num,
            "tx_num_24": tx_num_24,
            "block_fee_24": block_fee_24,
            "tx_fee_24": tx_fee_24,
            "average_block_interval": average_block_time,
            "median_block_interval": median_interval,
            "max_block_interval": intervals[-1],
            "min_block_interval": intervals[0]
        }
        return result

    # 两区块高度间的chain状态 [low, high)
    def chain_status_between(self, low, high):
        if low <= 0 or high <= 0 or low >= high:
            return None
        recent_block = self.get_block_by_height(high)
        block_hash = recent_block['block_hash']
        recent_timestamp = recent_block['timestamp']
        remote_timestamp = self.get_block_by_height(low)['timestamp']
        total_block_num = high - low
        block_fee = self.get_block_fee(high, total_block_num)
        total_tx_num = 0
        tx_fee = self.get_average_txs_fee_n(high, total_block_num)
        average_block_interval = (recent_timestamp - remote_timestamp) / total_block_num

        timestamps = []
        for h in range(low, high):
            block = self.get_block_by_height(h)
            tx_num = len(block['transactions'])
            total_tx_num += tx_num
            t = block['timestamp']
            timestamps.append(t)
        intervals = self.get_interval(timestamps)
        length = len(intervals)
        if length == 0:
            median_interval = None
            max_interval = None
            min_interval = None
        else:
            median_interval = (intervals[length / 2] + intervals[length / 2 - 1]) / 2 if length % 2 == 0 else intervals[(length + 1) / 2]
            max_interval = intervals[-1]
            min_interval = intervals[0]

        result = {
            "height": high,
            "block_hash": block_hash,
            "timestamp": recent_timestamp,
            "block_num_24": total_block_num,
            "tx_num_24": total_tx_num,
            "block_fee_24": block_fee,
            "tx_fee_24": tx_fee,
            "average_block_interval": average_block_interval,
            "median_block_interval": median_interval,
            "max_block_interval": max_interval,
            "min_block_interval": min_interval
        }
        return result

    # 历史每天的chain状态
    def chain_status_history(self):
        recent_height = self.get_recent_height()
        current_time = int(time.time())
        genesis_time = self.get_block_by_height(0)['timestamp']
        days = (current_time - genesis_time) / 86400

        result = []
        for d in range(days):
            height_point = []
            for h in range(recent_height):
                bl = self.get_block_by_height(h + 1)
                if bl['timestamp'] < genesis_time + d * 86400:
                    continue
                height_point.append(h)

            if len(height_point) == 0:
                break
            for i in range(len(height_point)):
                status = self.chain_status_between(height_point[i], height_point[i + 1])
                result.append(status)
        return result

    # TODO
    def genesis_status(self):
        pass

    # 将历史数据存进db
    def load(self):
        if self.get_status() is None:
            status_history = self.chain_status_history()
            self.mongo_cli.insert(flags.FLAGS.chain_status, status_history)
        else:
            pass

    def save(self):
        status = self.chain_status()
        self.mongo_cli.insert(flags.FLAGS.chain_status, status)



if __name__ == '__main__':
    FLAGS(sys.argv)
    cs = ChainStats()
    h = cs.get_recent_height()
    print h
    print cs.get_last_block_interval(21349)
