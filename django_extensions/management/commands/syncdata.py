"""
SyncData
========

Django command similar to 'loaddata' but also deletes.
After 'syncdata' has run, the database will have the same data as the fixture - anything
missing will of been added, anything different will of been updated,
and anything extra will of been deleted.
"""

import os

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import DEFAULT_DB_ALIAS, connections, transaction
from django.template.defaultfilters import pluralize

from django_extensions.management.utils import signalcommand


def humanize(dirname):
    pass


class SyncDataError(Exception):
    pass


class Command(BaseCommand):
    """syncdata command"""

    help = "Makes the current database have the same data as the fixture(s), no more, no less."  # noqa: E501
    args = "fixture [fixture ...]"

    def add_arguments(self, parser):
        pass

    def remove_objects_not_in(self, objects_to_keep, verbosity):
        """
        Delete all the objects in the database that are not in objects_to_keep.
        - objects_to_keep: A map where the keys are classes, and the values are a
         set of the objects of that class we should keep.
        """
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass

    def syncdata(self, fixture_labels, options):
        pass
