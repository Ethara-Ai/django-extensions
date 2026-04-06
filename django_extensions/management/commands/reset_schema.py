"""
Recreates the public schema for current database (PostgreSQL only).
Useful for Docker environments where you need to reset database
schema while there are active connections.
"""

import warnings

from django.core.management import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.db import connections
from django.conf import settings

from django_extensions.settings import POSTGRESQL_ENGINES
from django_extensions.utils.deprecation import RemovedInNextVersionWarning


class Command(BaseCommand):
    """`reset_schema` command implementation."""

    help = "Recreates the public schema for this project."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
