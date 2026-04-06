import difflib
import os
import inspect
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.loader import AmbiguityError, MigrationLoader

REPLACES_REGEX = re.compile(r"^\s+replaces\s*=\s*\[[^\]]+\]\s*?$", flags=re.MULTILINE)
PYC = ".pyc"


def py_from_pyc(pyc_fn):
    pass


class Command(BaseCommand):
    help = (
        "Deletes left over migrations that have been replaced by a "
        "squashed migration and converts squashed migration into a normal "
        "migration. Modifies your source tree! Use with care!"
    )

    def add_arguments(self, parser):
        pass

    def handle(self, **options):
        pass

    def confirm(self):
        pass

    def find_migration(self, loader, app_label, name):
        pass
