import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand

from django_extensions.compat import get_template_setting
from django_extensions.management.utils import signalcommand

ANNOTATION_RE = re.compile(
    r"\{?#[\s]*?(TODO|FIXME|BUG|HACK|WARNING|NOTE|XXX)[\s:]?(.+)"
)
ANNOTATION_END_RE = re.compile(r"(.*)#\}(.*)")


class Command(BaseCommand):
    help = "Show all annotations like TODO, FIXME, BUG, HACK, WARNING, NOTE or XXX "
    "in your py and HTML files."
    label = "annotation tag (TODO, FIXME, BUG, HACK, WARNING, NOTE, XXX)"

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        # don't add django internal code
        pass
