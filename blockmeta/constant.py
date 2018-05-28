#common
DEFAULT_START = 0
DEFAULT_OFFSET = 10
DEFAULT_MINER_OFFSET = 30
DEFAULT_LIST = 30
DEFAULT_PERIOD = 30
DEFAULT_RANK_LEN = 100

DISPLAY_LEN = 10
EXPIRE_TIME = 300

MAX_HANDLE = 5
MAX_ADDRESSES = 10
DISPLAY_UNCONFIRMED = 7

MAX_MONTH = 100 * 12
DAY_IN_SEC = 60 * 60 *24
ONE_DAY =  24
LOG_0 = 1e-5
TOP_N = 10

# address api
FILTERS = ['all', 'sent', 'recv', 'unspent', 'unconfirmed', 'confirmed']


FILTER_CONFIRMED ='confirmed'
FILTER_UNCONFIRMED = 'unconfirmed'
FILTER_DEFAULT = 'all'
FILTER_SENT = 'sent'
FILTER_RECEIVED = 'recv'
FILTER_UNSPENT = 'unspent'

SHARDING_SIZE = 1000
EXPIRE_ADDRESS =  30
BTC_IN_SATOSHIS = 100000000


#tx chart
TX_CHARTS = ['opreturn', 'coinbase', 'largetx', 'toprank']
TX_TYPE_DEFAULT = 'opreturn'
TX_TYPE_OPRETURN = 'opreturn'
TX_TYPE_COINBASE = 'coinbase'
TX_TYPE_LARGETX = 'largetx'
TX_TYPE_TOPRANK ='toprank'

PRIORITY_THRESHOLD = 57600000
#driver


#archives
ARCHIVES_FILTERS = ['all', 'bussiness', 'personal', 'miner', 'donation', 'hack', 'gambling', 'other']
DEFAULT_ARCHIVES_FILTER = 'all'
DEFAULT_ARCHIVES_DISPLAY = 30


#graph
EXPIRE_CAPTCHA =  60

#Bitcoin
TX_HASH_LEN = 64
HASHRATE_PER_P = 1024 * 1024 * 1024 * 1024 * 1024



# chain type
BYTOM="bytom"

BYTOM_ASSET_ID = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

# stats
DEFAULT_LIENTEN_PORT = "127.0.0.1:9888"
BASE_URL = "http://" + DEFAULT_LIENTEN_PORT
