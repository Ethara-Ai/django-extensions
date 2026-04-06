import importlib

from django.conf import settings
from django.contrib.auth import load_backend, BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.base import VALID_KEY_CHARS
from django.core.management.base import BaseCommand, CommandError
from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = (
        "print the user information for the provided session key. "
        "this is very helpful when trying to track down the person who "
        "experienced a site crash."
    )

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
