"""
print_settings
==============

Django command similar to 'diffsettings' but shows all active Django settings.
"""

import fnmatch
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Print the active Django settings."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
