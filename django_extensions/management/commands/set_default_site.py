import socket

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = "Set parameters of the default django.contrib.sites Site"

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
