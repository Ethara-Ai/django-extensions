import logging
import os
import re
import socket
import sys
import traceback
import webbrowser
import functools
from pathlib import Path
from typing import List, Set  # NOQA

import django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, SystemCheckError
from django.core.management.color import color_style
from django.core.servers.basehttp import get_internal_wsgi_application
from django.dispatch import Signal
from django.template.autoreload import get_template_directories, reset_loaders
from django.utils.autoreload import file_changed, get_reloader
from django.views import debug as django_views_debug

try:
    if "whitenoise.runserver_nostatic" in settings.INSTALLED_APPS:
        USE_STATICFILES = False
    else:
        from django.contrib.staticfiles.handlers import StaticFilesHandler

        USE_STATICFILES = True
except ImportError:
    USE_STATICFILES = False

try:
    from werkzeug import run_simple
    from werkzeug.debug import DebuggedApplication
    from werkzeug.serving import WSGIRequestHandler as _WSGIRequestHandler
    from werkzeug.serving import make_ssl_devcert
    from werkzeug._internal import _log  # type: ignore
    from werkzeug import _reloader

    HAS_WERKZEUG = True
except ImportError:
    HAS_WERKZEUG = False

try:
    import OpenSSL  # NOQA

    HAS_OPENSSL = True
except ImportError:
    HAS_OPENSSL = False

from django_extensions.management.technical_response import null_technical_500_response
from django_extensions.management.utils import (
    RedirectHandler,
    has_ipdb,
    setup_logger,
    signalcommand,
)
from django_extensions.management.debug_cursor import monkey_patch_cursordebugwrapper


runserver_plus_started = Signal()
naiveip_re = re.compile(
    r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
):)?(?P<port>\d+)$""",
    re.X,
)
# 7-bit C1 ANSI sequences (https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python)
ansi_escape = re.compile(
    r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
""",
    re.VERBOSE,
)
DEFAULT_PORT = "8000"
DEFAULT_POLLER_RELOADER_INTERVAL = getattr(
    settings,
    "RUNSERVER_PLUS_POLLER_RELOADER_INTERVAL",
    getattr(settings, "RUNSERVERPLUS_POLLER_RELOADER_INTERVAL", 1),
)
DEFAULT_POLLER_RELOADER_TYPE = getattr(
    settings,
    "RUNSERVER_PLUS_POLLER_RELOADER_TYPE",
    getattr(settings, "RUNSERVERPLUS_POLLER_RELOADER_TYPE", "auto"),
)

logger = logging.getLogger(__name__)
_error_files = set()  # type: Set[str]


def get_all_template_files() -> Set[str]:
    pass


if HAS_WERKZEUG:
    # Monkey patch the reloader to support adding more files to extra_files
    for name, reloader_loop_klass in _reloader.reloader_loops.items():

        class WrappedReloaderLoop(reloader_loop_klass):  # type: ignore
            def __init__(self, *args, **kwargs):
                self._template_files: Set[str] = get_all_template_files()
                super().__init__(*args, **kwargs)
                self._extra_files = self.extra_files

            @property
            def extra_files(self):
                pass

            @extra_files.setter
            def extra_files(self, extra_files):
                pass

            def trigger_reload(self, filename: str) -> None:
                pass

            def register_file_changed(self, filename):
                pass

        _reloader.reloader_loops[name] = WrappedReloaderLoop


def gen_filenames():
    pass


def check_errors(fn):
    # Inspired by https://github.com/django/django/blob/master/django/utils/autoreload.py
    @functools.wraps(fn)
    pass


class Command(BaseCommand):
    help = "Starts a lightweight Web server for development."

    # Validation is called explicitly each time the server is reloaded.
    requires_system_checks: List[str] = []
    DEFAULT_CRT_EXTENSION = ".crt"
    DEFAULT_KEY_EXTENSION = ".key"

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass

    def get_handler(self, *args, **options):
        """Return the default WSGI handler for the runner."""
        pass

    def get_error_handler(self, exc, **options):
        pass

    def inner_run(self, options):
        pass

    @classmethod
    def determine_ssl_files_paths(cls, options):
        pass

    @classmethod
    def _determine_path_for_file(
        cls, current_file_path, other_file_path, expected_extension
    ):
        pass

    @classmethod
    def _get_directory_basing_on_file_paths(cls, current_file_path, other_file_path):
        pass

    @classmethod
    def _get_directory(cls, file_path):
        pass

    @classmethod
    def _get_file_name(cls, file_path):
        pass

    @classmethod
    def _get_extension(cls, file_path):
        pass


def set_werkzeug_log_color():
    """Try to set color to the werkzeug log."""
    pass
