import logging
import os
import sys

from django_extensions.management.signals import post_command, pre_command


def _make_writeable(filename):
    """
    Make sure that the file is writable. Useful if our source is
    read-only.
    """
    pass


def setup_logger(logger, stream, filename=None, fmt=None):
    """
    Set up a logger (if no handlers exist) for console output,
    and file 'tee' output if desired.
    """
    pass


class RedirectHandler(logging.Handler):
    """Redirect logging sent to one logger (name) to another."""

    def __init__(self, name, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        self.name = name
        self.logger = logging.getLogger(name)

    def emit(self, record):
        pass


def signalcommand(func):
    """decorator for management command handle defs that sends out a pre/post signal."""
    pass


def has_ipdb():
    pass
