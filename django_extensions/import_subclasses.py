from importlib import import_module
from inspect import (
    getmembers,
    isclass,
)
from pkgutil import walk_packages
from typing import (  # NOQA
    Dict,
    List,
    Tuple,
    Union,
)

from django.conf import settings
from django.utils.module_loading import import_string


class SubclassesFinder:
    def __init__(self, base_classes_from_settings):
        self.base_classes = []
        for element in base_classes_from_settings:
            if isinstance(element, str):
                element = import_string(element)
            self.base_classes.append(element)

    def _should_be_imported(self, candidate_to_import):  # type: (Tuple[str, type]) -> bool
        pass

    def collect_subclasses(self):  # type: () -> Dict[str, List[Tuple[str, str]]]
        """
        Collect all subclasses of user-defined base classes from project.
        :return: Dictionary from module name to list of tuples.
        First element of tuple is model name and second is alias.
        Currently we set alias equal to model name,
        but in future functionality of aliasing subclasses can be added.
        """
        pass

    def _collect_classes_from_module(self, module_name):  # type: (str) -> List[Tuple[str, str]]
        pass
