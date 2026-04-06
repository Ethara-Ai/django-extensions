from collections import defaultdict
import fnmatch
import functools
import re
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import get_template

from django_extensions.compat import get_template_setting
from django_extensions.management.color import color_style, no_style
from django_extensions.management.utils import signalcommand
from django_extensions.utils.extract_views_from_urlpatterns import (
    extract_views_from_urlpatterns,
)


class Command(BaseCommand):
    args = ""
    help = "Verify named URLs in templates"
    ignores = set(
        [
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

    def collect_templates(self, options):
        pass

    def collect_views(self, options):
        pass

    def process_template(self, filepath):
        pass
