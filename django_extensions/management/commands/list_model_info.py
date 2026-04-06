# Author: OmenApps. https://omenapps.com
import inspect

from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django_extensions.management.color import color_style
from django_extensions.management.utils import signalcommand

TAB = "        "
HALFTAB = "    "


class Command(BaseCommand):
    """A simple management command which lists model fields and methods."""

    help = "List out the fields and methods for each model"

    def add_arguments(self, parser):
        pass

    def list_model_info(self, options):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
