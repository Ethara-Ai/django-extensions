"""
set_fake_passwords.py

    Reset all user passwords to a common value. Useful for testing in a
    development environment. As such, this command is only available when
    setting.DEBUG is True.

"""

from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import signalcommand

DEFAULT_FAKE_PASSWORD = "password"


class Command(BaseCommand):
    help = 'DEBUG only: sets all user passwords to a common value ("%s" by default)' % (
        DEFAULT_FAKE_PASSWORD,
    )
    requires_system_checks: List[str] = []

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
