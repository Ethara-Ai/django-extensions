from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.management import BaseCommand
from django.db import transaction

from django_extensions.management.utils import signalcommand


def get_model_to_deduplicate():
    pass


def get_field_names(model):
    pass


def keep_first_or_last_instance():
    pass


def get_generic_fields():
    """Return a list of all GenericForeignKeys in all models."""
    pass


class Command(BaseCommand):
    help = """
        Removes duplicate model instances based on a specified
        model and field name(s).

        Makes sure that any OneToOne, ForeignKey, or ManyToMany relationships
        attached to a deleted model(s) get reattached to the remaining model.

        Based on the following:
        https://djangosnippets.org/snippets/2283/
        https://stackoverflow.com/a/41291137/2532070
        https://gist.github.com/edelvalle/01886b6f79ba0c4dce66
    """

    @signalcommand
    def handle(self, *args, **options):
        pass

    @transaction.atomic()
    def merge_model_instances(self, primary_object, alias_objects):
        """
        Merge several model instances into one, the `primary_object`.
        Use this function to merge model objects and migrate all of the related
        fields from the alias objects the primary object.
        """
        pass
