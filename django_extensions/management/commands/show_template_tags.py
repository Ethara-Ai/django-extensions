import inspect
import os
import re


from django.apps import apps
from django.core.management import color
from django.core.management import BaseCommand
from django.utils import termcolors
from django.utils.encoding import smart_str

from django_extensions.compat import load_tag_library
from django_extensions.management.color import _dummy_style_func
from django_extensions.management.utils import signalcommand


def no_style():
    pass


def color_style():
    pass


def format_block(block, nlspaces=0):
    """
    Format the given block of text, trimming leading/trailing
    empty lines and any leading whitespace that is common to all lines.
    The purpose is to let us list a code block as a multiline,
    triple-quoted Python string, taking care of
    indentation concerns.
    https://code.activestate.com/recipes/145672/
    """
    pass


class Command(BaseCommand):
    help = "Displays template tags and filters available in the current project."
    results = ""

    def add_result(self, s, depth=0):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
