from django.apps import apps as django_apps
from django.contrib.auth.management import create_permissions
from django.contrib.auth.management import _get_all_permissions  # type: ignore
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    help = (
        "reloads permissions for specified apps, or all apps if no args are specified"
    )

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
