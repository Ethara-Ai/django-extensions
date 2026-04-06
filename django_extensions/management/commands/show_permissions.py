from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "List all permissions for models. "
        "By default, excludes admin, auth, contenttypes, and sessions apps."
    )

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
