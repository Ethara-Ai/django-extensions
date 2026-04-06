import time
import logging
from hashlib import md5

# also see: https://djangosnippets.org/snippets/2242/


class RateLimiterFilter(logging.Filter):
    def filter(self, record):
        pass
