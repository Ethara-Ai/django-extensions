import importlib.util
from itertools import count
import os
import logging
import warnings

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.db.backends.base.creation import TEST_DATABASE_PREFIX

from django_extensions.settings import SQLITE_ENGINES, POSTGRESQL_ENGINES, MYSQL_ENGINES
from django_extensions.management.mysql import parse_mysql_cnf
from django_extensions.management.utils import signalcommand
from django_extensions.utils.deprecation import RemovedInNextVersionWarning


class Command(BaseCommand):
    help = "Drops test database for this project."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        """Drop test database for this project."""
        pass
