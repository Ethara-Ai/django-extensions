# Author: AxiaCore S.A.S. https://axiacore.com
from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import signalcommand


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""

    help = "Fully clear site-wide cache."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, cache, all_caches, *args, **kwargs):
        pass
