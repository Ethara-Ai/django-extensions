import time
import traceback
from contextlib import contextmanager

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.backends import utils

from django_extensions.settings import DEFAULT_PRINT_SQL_TRUNCATE_CHARS


@contextmanager
def monkey_patch_cursordebugwrapper(
    print_sql=None,
    print_sql_location=False,
    truncate=None,
    logger=print,
    confprefix="DJANGO_EXTENSIONS",
):
    pass
