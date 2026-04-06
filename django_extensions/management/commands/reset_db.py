"""
reset_db command

originally from https://www.djangosnippets.org/snippets/828/ by dnordberg
"""

import importlib.util
import os
import logging
import warnings

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS

from django_extensions.settings import SQLITE_ENGINES, POSTGRESQL_ENGINES, MYSQL_ENGINES
from django_extensions.management.mysql import parse_mysql_cnf
from django_extensions.management.utils import signalcommand
from django_extensions.utils.deprecation import RemovedInNextVersionWarning


class Command(BaseCommand):
    help = "Resets the database for this project."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        """
        Reset the database for this project.

        Note: Transaction wrappers are in reverse as a work around for
        autocommit, anybody know how to do this the right way?
        """
        pass
