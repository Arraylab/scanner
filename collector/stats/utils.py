# -*- coding: utf-8 -*-

import numpy as np

def compact_to_big(compact):

    mantissa = compact & 0x007fffffffffffff
    is_negative = (compact & 0x0080000000000000) != 0
    exponent = int(compact >> 56)

    if exponent <= 3:
        mantissa >>= 8 * (3 - exponent)
        bn = np.int64(mantissa)
    else:
        bn = np.int64(mantissa)
        bn <<= 8 * (exponent - 3)

    if is_negative:
        bn = -1 * bn

    return bn


def calc_work(nbit):
    difficultyNum = compact_to_big(nbit)
    if difficultyNum <= 0:
        return 0
    # (1 << 256) / (difficultyNum + 1)
    denominator = difficultyNum + 1
    return (1 << 256) / denominator


if __name__ == '__main__':
    height = 21349
    nbit = 2089670227100065245
    difficult = 1814785054
    nonce = 4434603461217934767

    diff_time = 35

    hashcount = calc_work(nbit)
    print 'hashcount:', hashcount
    hashrate = hashcount / diff_time
    print 'hashrate:', hashrate
    print hex(hashrate)
    print hex(hashrate)[-17: -1]

