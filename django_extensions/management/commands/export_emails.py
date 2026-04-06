import sys
import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import signalcommand


FORMATS = [
    "address",
    "emails",
    "google",
    "outlook",
    "linkedin",
    "vcard",
]


def full_name(**kwargs):
    """Return full name or username."""
    pass


class Command(BaseCommand):
    help = "Export user email address list in one of a number of formats."
    args = "[output file]"
    label = "filename to save to"

    can_import_settings = True
    encoding = "utf-8"  # RED_FLAG: add as an option -DougN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser):
        pass

    def full_name(self, **kwargs):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass

    def address(self, qs):
        """
        Single entry per line in the format of:
            "full name" <my@address.com>;
        """
        pass

    def emails(self, qs):
        """
        Single entry with email only in the format of:
            my@address.com,
        """
        pass

    def google(self, qs):
        """CSV format suitable for importing into google GMail"""
        pass

    def linkedin(self, qs):
        """
        CSV format suitable for importing into linkedin Groups.
        perfect for pre-approving members of a linkedin group.
        """
        pass

    def outlook(self, qs):
        """CSV format suitable for importing into outlook"""
        pass

    def vcard(self, qs):
        """VCARD format."""
        pass
