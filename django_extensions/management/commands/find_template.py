import sys

from django.core.management.base import LabelCommand
from django.template import TemplateDoesNotExist, loader

from django_extensions.management.utils import signalcommand


class Command(LabelCommand):
    help = "Finds the location of the given template by resolving its path"
    args = "[template_path]"
    label = "template path"

    @signalcommand
    def handle_label(self, template_path, **options):
        pass
