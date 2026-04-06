import os
import sys
import importlib
import inspect
import traceback

from argparse import ArgumentTypeError

from django.apps import apps
from django.conf import settings
from django.core.management.base import CommandError

from django_extensions.management.email_notifications import EmailNotificationCommand
from django_extensions.management.utils import signalcommand


class DirPolicyChoices:
    NONE = "none"
    EACH = "each"
    ROOT = "root"


def check_is_directory(value):
    pass


class BadCustomDirectoryException(Exception):
    def __init__(self, value):
        self.message = (
            value + " If --dir-policy is custom than you must set correct directory in "
            "--dir option or in settings.RUNSCRIPT_CHDIR"
        )

    def __str__(self):
        return self.message


class Command(EmailNotificationCommand):
    help = "Runs a script in django context."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_directory = os.getcwd()
        self.last_exit_code = 0

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
