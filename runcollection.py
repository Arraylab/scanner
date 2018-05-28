import sys

from collector import agent
from collector.stats.service import StatusService
from tools import flags
import gevent

FLAGS = flags.FLAGS


def status_service():
    my_service = StatusService()
    my_service.start()


if __name__ == "__main__":
    FLAGS(sys.argv)
    # g = gevent.spawn(status_service)
    my_agent = agent.DataAgent()
    my_agent.sync_forever()

