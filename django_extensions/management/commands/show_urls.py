import functools
import json
import re

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.color import color_style, no_style
from django_extensions.management.utils import signalcommand
from django_extensions.utils.extract_views_from_urlpatterns import (
    extract_views_from_urlpatterns,
)


FMTR = {
    "dense": "{url}\t{module}\t{url_name}\t{decorator}",
    "table": "{url},{module},{url_name},{decorator}",
    "aligned": "{url},{module},{url_name},{decorator}",
    "verbose": "{url}\n\tController: {module}\n\tURL Name: {url_name}\n\tDecorators: {decorator}\n",  # noqa: E501
    "json": "",
    "pretty-json": "",
}


class Command(BaseCommand):
    help = "Displays all of the url matching routes for the project."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
