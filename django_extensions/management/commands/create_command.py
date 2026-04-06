import os
import sys
import shutil
from typing import List

from django.core.management.base import AppCommand
from django.core.management.color import color_style

from django_extensions.management.utils import _make_writeable, signalcommand


class Command(AppCommand):
    help = "Creates a Django management command directory structure for the given app "
    "name in the app's directory."

    requires_system_checks: List[str] = []
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = True

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle_app_config(self, args, **options):
        pass


def copy_template(template_name, copy_to, **options):
    """Copy the specified template directory to the copy_to location"""
    pass
