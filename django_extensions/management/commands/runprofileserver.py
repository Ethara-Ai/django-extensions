"""
runprofileserver.py

    Starts a lightweight Web server with profiling enabled.

Credits for kcachegrind support taken from lsprofcalltree.py go to:
 David Allouche
 Jp Calderone & Itamar Shtull-Trauring
 Johan Dahlin
"""

import sys
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import get_internal_wsgi_application

from django_extensions.management.utils import signalcommand

USE_STATICFILES = "django.contrib.staticfiles" in settings.INSTALLED_APPS


class KCacheGrind:
    def __init__(self, profiler):
        self.data = profiler.getstats()
        self.out_file = None

    def output(self, out_file):
        pass

    def _print_summary(self):
        pass

    def _entry(self, entry):
        pass

    def _subentry(self, lineno, subentry):
        pass


class Command(BaseCommand):
    help = "Starts a lightweight Web server with profiling enabled."
    args = "[optional port number, or ipaddr:port]"

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, addrport="", *args, **options):
        pass
