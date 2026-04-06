import inspect
import os
import sys
import traceback
import warnings

from django.db import connections
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.datastructures import OrderedSet

from django_extensions.management.shells import import_objects
from django_extensions.management.utils import signalcommand
from django_extensions.management.debug_cursor import monkey_patch_cursordebugwrapper


def use_vi_mode():
    pass


def shell_runner(flags, name, help=None):
    """
    Decorates methods with information about the application they are starting

    :param flags: The flags used to start this runner via the ArgumentParser.
    :param name: The name of this runner for the help text for the ArgumentParser.
    :param help: The optional help for the ArgumentParser if the dynamically generated help is not sufficient.
    """  # noqa: E501

    def decorator(fn):
        pass

    return decorator


class Command(BaseCommand):
    help = "Like the 'shell' command but autoloads the models of all installed Django apps."  # noqa: E501
    extra_args = None
    tests_mode = False

    def __init__(self):
        super().__init__()
        self.runners = [
            member
            for name, member in inspect.getmembers(self)
            if hasattr(member, "runner_flags")
        ]

    def add_arguments(self, parser):
        pass

    def run_from_argv(self, argv):
        pass

    def get_ipython_arguments(self, options):
        pass

    def get_notebook_arguments(self, options):
        pass

    def get_imported_objects(self, options):
        pass

    @shell_runner(flags=["--kernel"], name="IPython Kernel")
    def get_kernel(self, options):
        pass

    def load_base_kernel_spec(self, app):
        """Finds and returns the base Python kernelspec to extend from."""
        pass

    def generate_kernel_specs(self, app, ipython_arguments):
        """Generate an IPython >= 3.0 kernelspec that loads django extensions"""
        pass

    def run_notebookapp(self, app_init, options, use_kernel_specs=True, history=True):
        pass

    @shell_runner(flags=["--notebook"], name="IPython Notebook")
    def get_notebook(self, options):
        pass

    @shell_runner(flags=["--lab"], name="JupyterLab Notebook")
    def get_jupyterlab(self, options):
        pass

    @shell_runner(flags=["--plain"], name="plain Python")
    def get_plain(self, options):
        # Using normal Python shell
        pass

    @shell_runner(flags=["--bpython"], name="BPython")
    def get_bpython(self, options):
        pass

    @shell_runner(flags=["--ipython"], name="IPython")
    def get_ipython(self, options):
        pass

    @shell_runner(flags=["--ptpython"], name="PTPython")
    def get_ptpython(self, options):
        pass

    @shell_runner(flags=["--ptipython"], name="PT-IPython")
    def get_ptipython(self, options):
        pass

    @shell_runner(flags=["--idle"], name="Idle")
    def get_idle(self, options):
        pass

    def set_application_name(self, options):
        """
        Set the application_name on PostgreSQL connection

        Use the fallback_application_name to let the user override
        it with PGAPPNAME env variable

        https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS
        """  # noqa: E501
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
