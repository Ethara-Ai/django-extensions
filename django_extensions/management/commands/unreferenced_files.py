import os
from collections import defaultdict

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import models

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Prints a list of all files in MEDIA_ROOT that are not referenced in the database."  # noqa: E501

    @signalcommand
    def handle(self, *args, **options):
        pass
