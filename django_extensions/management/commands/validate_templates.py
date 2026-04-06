import os
import fnmatch

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style
from django.template.loader import get_template

from django_extensions.compat import get_template_setting
from django_extensions.management.utils import signalcommand


#
# TODO: Render the template with fake request object ?
#


class Command(BaseCommand):
    args = ""
    help = "Validate templates on syntax and compile errors"
    ignores = set(
        [
            ".DS_Store",
            "*.swp",
            "*~",
        ]
    )

    def add_arguments(self, parser):
        pass

    def ignore_filename(self, filename):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
