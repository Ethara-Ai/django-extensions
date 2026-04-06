# Based on https://gist.github.com/voldmar/1264102
# and https://gist.github.com/runekaagaard/2eecf0a8367959dc634b7866694daf2c

import gc
import inspect
import weakref
from collections import defaultdict

import django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models.signals import (
    ModelSignal,
    pre_init,
    post_init,
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
    pre_migrate,
    post_migrate,
)
from django.utils.encoding import force_str


MSG = "{module}.{name} #{line}{is_async}"

SIGNAL_NAMES = {
    pre_init: "pre_init",
    post_init: "post_init",
    pre_save: "pre_save",
    post_save: "post_save",
    pre_delete: "pre_delete",
    post_delete: "post_delete",
    m2m_changed: "m2m_changed",
    pre_migrate: "pre_migrate",
    post_migrate: "post_migrate",
}


class Command(BaseCommand):
    help = "List all signals by model and signal type"

    def handle(self, *args, **options):
        pass
