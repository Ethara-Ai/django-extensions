from django.apps import apps
from django.core.management.base import CommandError, LabelCommand
from django.utils.encoding import force_str

from django_extensions.management.utils import signalcommand


class Command(LabelCommand):
    help = "Outputs the specified model as a form definition to the shell."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass


def describe_form(label, fields):
    """Return a string describing a form based on the model"""
    pass
