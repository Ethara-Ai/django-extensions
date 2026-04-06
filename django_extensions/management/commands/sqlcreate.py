import socket
import sys
import warnings
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS

from django_extensions.management.utils import signalcommand
from django_extensions.utils.deprecation import RemovedInNextVersionWarning
from django_extensions.settings import SQLITE_ENGINES, POSTGRESQL_ENGINES, MYSQL_ENGINES


class Command(BaseCommand):
    help = """Generates the SQL to create your database for you, as specified in settings.py
The envisioned use case is something like this:

    ./manage.py sqlcreate [--database=<databasename>] | mysql -u <db_administrator> -p
    ./manage.py sqlcreate [--database=<databasename>] | psql -U <db_administrator> -W
    """  # noqa: E501

    requires_system_checks: List[str] = []
    can_import_settings = True

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
