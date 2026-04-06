from io import BytesIO

import csv
import codecs
import importlib

from django.conf import settings


#
# Django compatibility
#
def load_tag_library(libname):
    """
    Load a templatetag library on multiple Django versions.

    Returns None if the library isn't loaded.
    """
    pass


def get_template_setting(template_key, default=None):
    """Read template settings"""
    pass


class UnicodeWriter:
    """
    CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    We are using this custom UnicodeWriter for python versions 2.x
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = BytesIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        pass

    def writerows(self, rows):
        pass
