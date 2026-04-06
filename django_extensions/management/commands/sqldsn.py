"""
sqldns.py

Prints Data Source Name on stdout
"""

import sys
import warnings
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style
from django.db import DEFAULT_DB_ALIAS
from django_extensions.settings import SQLITE_ENGINES, POSTGRESQL_ENGINES, MYSQL_ENGINES
from django_extensions.utils.deprecation import RemovedInNextVersionWarning


def _sqlite_name(dbhost, dbport, dbname, dbuser, dbpass):
    pass


def _mysql_keyvalue(dbhost, dbport, dbname, dbuser, dbpass):
    pass


def _mysql_args(dbhost, dbport, dbname, dbuser, dbpass):
    pass


def _postgresql_keyvalue(dbhost, dbport, dbname, dbuser, dbpass):
    pass


def _postgresql_kwargs(dbhost, dbport, dbname, dbuser, dbpass):
    pass


def _postgresql_pgpass(dbhost, dbport, dbname, dbuser, dbpass):
    pass


def _uri(engine):
    def inner(dbhost, dbport, dbname, dbuser, dbpass):
        pass

    return inner


_FORMATTERS = [
    (SQLITE_ENGINES, None, _sqlite_name),
    (SQLITE_ENGINES, "filename", _sqlite_name),
    (SQLITE_ENGINES, "uri", _uri("sqlite")),
    (MYSQL_ENGINES, None, _mysql_keyvalue),
    (MYSQL_ENGINES, "keyvalue", _mysql_keyvalue),
    (MYSQL_ENGINES, "args", _mysql_args),
    (MYSQL_ENGINES, "uri", _uri("mysql")),
    (POSTGRESQL_ENGINES, None, _postgresql_keyvalue),
    (POSTGRESQL_ENGINES, "keyvalue", _postgresql_keyvalue),
    (POSTGRESQL_ENGINES, "kwargs", _postgresql_kwargs),
    (POSTGRESQL_ENGINES, "uri", _uri("postgresql")),
    (POSTGRESQL_ENGINES, "pgpass", _postgresql_pgpass),
]


class Command(BaseCommand):
    help = "Prints DSN on stdout, as specified in settings.py"
    requires_system_checks: List[str] = []
    can_import_settings = True

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass

    def show_dsn(self, database, options):
        pass
