import ast
import traceback
import warnings
import importlib

from typing import (  # NOQA
    Dict,
    List,
    Tuple,
    Union,
)

from django.apps.config import MODELS_MODULE_NAME
from django.utils.module_loading import import_string
from django_extensions.collision_resolvers import CollisionResolvingRunner
from django_extensions.import_subclasses import SubclassesFinder
from django_extensions.utils.deprecation import RemovedInNextVersionWarning


SHELL_PLUS_DJANGO_IMPORTS = [
    "from django.core.cache import cache",
    "from django.conf import settings",
    "from django.contrib.auth import get_user_model",
    "from django.db import transaction",
    "from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When",  # noqa: E501
    "from django.utils import timezone",
    "from django.urls import reverse",
    "from django.db.models import Exists, OuterRef, Subquery",
]


class ObjectImportError(Exception):
    pass


def get_app_name(mod_name):
    """
    Retrieve application name from models.py module path

    >>> get_app_name('testapp.models.foo')
    'testapp'

    'testapp' instead of 'some.testapp' for compatibility:
    >>> get_app_name('some.testapp.models.foo')
    'testapp'
    >>> get_app_name('some.models.testapp.models.foo')
    'testapp'
    >>> get_app_name('testapp.foo')
    'testapp'
    >>> get_app_name('some.testapp.foo')
    'testapp'
    """
    pass


def import_items(import_directives, style, quiet_load=False):
    """
    Import the items in import_directives and return a list of the imported items

    Each item in import_directives should be one of the following forms
        * a tuple like ('module.submodule', ('classname1', 'classname2')), which indicates a 'from module.submodule import classname1, classname2'
        * a tuple like ('module.submodule', 'classname1'), which indicates a 'from module.submodule import classname1'
        * a tuple like ('module.submodule', '*'), which indicates a 'from module.submodule import *'
        * a simple 'module.submodule' which indicates 'import module.submodule'.

    Returns a dict mapping the names to the imported items
    """  # noqa: E501
    pass


def import_objects(options, style):
    pass
