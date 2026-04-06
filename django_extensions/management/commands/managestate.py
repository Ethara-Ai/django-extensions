import json
from operator import itemgetter
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone

from django_extensions.management.utils import signalcommand

DEFAULT_FILENAME = "managestate.json"
DEFAULT_STATE = "default"


class Command(BaseCommand):
    help = "Manage database state in the convenient way."
    _applied_migrations = None
    migrate_args: dict
    migrate_options: dict
    filename: str
    verbosity: int
    database: str
    conn: BaseDatabaseWrapper

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, action, database, filename, state, *args, **options):
        pass

    def dump(self, state: str):
        """Save applied migrations to a file."""
        pass

    def load(self, state: str):
        """Apply migrations from a file."""
        pass

    def get_migrated_apps(self) -> dict:
        """Installed apps having migrations."""
        pass

    def get_applied_migrations(self) -> dict:
        """Installed apps with last applied migrations."""
        pass

    def is_applied(self, app: str, migration: str) -> bool:
        """Check whether a migration for an app is applied or not."""
        pass

    def read(self) -> dict:
        """Get saved state from the file."""
        pass

    def write(self, data: dict):
        """Write new data to the file using existent one."""
        pass
