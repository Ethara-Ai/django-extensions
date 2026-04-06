import logging

from django.apps import apps
from django.core.management.base import BaseCommand

from django_extensions.management.jobs import get_jobs, print_jobs
from django_extensions.management.utils import setup_logger, signalcommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs scheduled maintenance jobs."

    when_options = [
        "minutely",
        "quarter_hourly",
        "hourly",
        "daily",
        "weekly",
        "monthly",
        "yearly",
    ]

    def add_arguments(self, parser):
        pass

    def usage_msg(self):
        pass

    def runjobs(self, when, options):
        pass

    def runjobs_by_signals(self, when, options):
        """Run jobs from the signals"""
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
