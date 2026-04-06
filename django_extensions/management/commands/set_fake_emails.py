"""
set_fake_emails.py

    Give all users a new email account. Useful for testing in a
    development environment. As such, this command is only available when
    setting.DEBUG is True.

"""

from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import signalcommand

DEFAULT_FAKE_EMAIL = "%(username)s@example.com"


class Command(BaseCommand):
    help = (
        "DEBUG only: give all users a new email based on their account data "
        '("%s" by default). '
        "Possible parameters are: username, first_name, last_name"
    ) % (DEFAULT_FAKE_EMAIL,)
    requires_system_checks: List[str] = []

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
