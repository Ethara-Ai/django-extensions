import logging

from django.core.management.base import BaseCommand

from django_extensions.management.jobs import get_job, print_jobs
from django_extensions.management.utils import setup_logger, signalcommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run a single maintenance job."
    missing_args_message = "test"

    def add_arguments(self, parser):
        pass

    def runjob(self, app_name, job_name, options):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
