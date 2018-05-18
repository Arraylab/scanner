# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
import gevent
import logging
import json
import threading
import os
import platform
import requests
import socket
import time


mutex = threading.Lock()
LOG = logging.getLogger('node')

TOTAL_GEVENT_TIMEOUT = 60
READ_ADDR_TIMEOUT = 5
LOCK_CONN_TIMEOUT = 2
NODE_STATS_TIMEOUT = 5


class NodeStats:

    def __init__(self, hosts):
        self.hosts = hosts
        self.online_num = 0
        self.online_node = []
        self.time_consume = 0
        self.timestamp = time.time()
        self.positons = []

    def analyze_conn(self, host, timeout):
        if node_conn(host, timeout) == 0:
            mutex.acquire(LOCK_CONN_TIMEOUT)
            self.online_num += 1
            self.online_node.append(host)
            mutex.release()
            print 'Connected: ', host

    def node_stats(self, timeout):
        time_start = time.time()
        jobs = [gevent.spawn(self.analyze_conn, h, timeout)
                for h in self.hosts]
        gevent.joinall(jobs, timeout=TOTAL_GEVENT_TIMEOUT)
        time_end = time.time()
        self.time_consume = time_end - time_start

    def node_position(self):

        def get_position(h):
            ip, _ = h
            info = ip_info(ip)
            if info is not None:
                mutex.acquire(LOCK_CONN_TIMEOUT)
                self.positons.append(info)
                mutex.release()

        jobs = [gevent.spawn(get_position, node) for node in self.online_node]
        gevent.joinall(jobs, timeout=TOTAL_GEVENT_TIMEOUT)


def record_to_file(data, filename):
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists('vnode.json'):
        os.system(r'touch {}'.format(filename))
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


# path: addrbook.json
def read_addr_book(path):
    mutex.acquire(READ_ADDR_TIMEOUT)
    with open(path, 'r') as f:
        data = json.load(f)
    mutex.release()
    if data is None:
        return None
    return data['Addrs']


# (ip, port)
def parse_address(path):
    addrs = read_addr_book(path)
    print addrs
    hosts = []
    for item in addrs:
        ip = item['Addr'].get('IP')
        port = item['Addr'].get('Port')
        if ip is None and port is None:
            return None
        hosts.append((ip, port))
    return hosts


# bytom dir
def data_dir():
    home_dir = os.environ['HOME']
    sysstr = platform.system()
    if sysstr == 'Darwin':
        path = os.path.join(home_dir, "Library", "Bytom")
    elif sysstr == 'Windows':
        path = os.path.join(home_dir, "AppData", "Roaming", "Bytom")
    else:
        path = os.path.join(home_dir, ".bytom")
    return path


def node_conn(host, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    errno = s.connect_ex(host)
    s.close()
    return errno


def ip_info(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip
    r = requests.get(url)
    if r.json()['code'] == 0:
        i = r.json()['data']
        country = i['country']  # 国家
        area = i['area']  # 区域
        region = i['region']  # 地区
        city = i['city']  # 城市
        isp = i['isp']  # 运营商
        print "ip: ", ip
        print u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (
            country, area, region, city, isp)
        return i
    else:
        print "ERRO! ip: %s" % ip
        return None


if __name__ == "__main__":
    filepath = os.path.join(data_dir(), 'addrbook.json')
    hosts = parse_address(filepath)
    stats = NodeStats(hosts)
    stats.node_stats(NODE_STATS_TIMEOUT)
    print 'online node num: ', stats.online_num
    print 'total time: ', stats.time_consume
    for h in stats.online_node:
        ip, _ = h
        ip_info(ip)
