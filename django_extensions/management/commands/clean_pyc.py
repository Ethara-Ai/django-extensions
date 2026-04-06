import fnmatch
import os
from os.path import join as _j
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Removes all python bytecode compiled files from the project."

    requires_system_checks: List[str] = []

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
