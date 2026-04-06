import argparse
import string
import secrets
from typing import List

from django.core.management.base import BaseCommand
from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Generates a simple new password that can be used for a user password. "
    "Uses Python’s secrets module to generate passwords. Do not use this command to "
    "generate your most secure passwords."

    requires_system_checks: List[str] = []

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
