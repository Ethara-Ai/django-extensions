import os
import sys
from typing import List

from django.core.management.base import AppCommand

from django_extensions.management.utils import _make_writeable, signalcommand


class Command(AppCommand):
    help = "Creates a Django template tags directory structure for the given app name "
    "in the apps's directory"

    def add_arguments(self, parser):
        pass

    requires_system_checks: List[str] = []
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = True

    @signalcommand
    def handle_app_config(self, app_config, **options):
        pass


def copy_template(template_name, copy_to, tag_library_name):
    """Copy the specified template directory to the copy_to location"""
    pass
