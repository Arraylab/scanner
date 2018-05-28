from flask import current_app

from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class SearchManager:
    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def search(self, query):
        try:
            result = self.driver.search(query)
            return result
        except Exception, e:
            self.logger.error("SearchManager.search Error: %s" % str(e))
            raise Exception("search error: %s", e)
