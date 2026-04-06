import inspect
import sys
from abc import abstractmethod, ABCMeta
from typing import (  # NOQA
    Dict,
    List,
    Optional,
    Tuple,
)

from django.utils.module_loading import import_string


class BaseCR(metaclass=ABCMeta):
    """
    Abstract base collision resolver. All collision resolvers needs to inherit from this class.
    To write custom collision resolver you need to overwrite resolve_collisions function.
    It receives Dict[str, List[str]], where key is model name and values are full model names
    (full model name means: module + model_name).
    You should return Dict[str, str], where key is model name and value is full model name.
    """  # noqa: E501

    @classmethod
    def get_app_name_and_model(cls, full_model_path):  # type: (str) -> Tuple[str, str]
        pass

    @abstractmethod
    def resolve_collisions(self, namespace):  # type: (Dict[str, List[str]]) -> Dict[str, str]
        pass


class LegacyCR(BaseCR):
    """
    Default collision resolver.

    Model from last application in alphabetical order is selected.
    """

    def resolve_collisions(self, namespace):
        pass


class AppsOrderCR(LegacyCR, metaclass=ABCMeta):
    APP_PRIORITIES = None  # type: List[str]

    def resolve_collisions(self, namespace):
        pass

    def _sort_models_depending_on_priorities(self, models):  # type: (List[str]) -> List[Tuple[int, str]]
        pass


class InstalledAppsOrderCR(AppsOrderCR):
    """
    Collision resolver which selects first model from INSTALLED_APPS.
    You can set your own app priorities list by subclassing him and overwriting APP_PRIORITIES field.
    This collision resolver will select model from first app on this list.
    If both app's are absent on this list, resolver will choose model from first app in alphabetical order.
    """  # noqa: E501

    @property
    def APP_PRIORITIES(self):
        pass


class PathBasedCR(LegacyCR, metaclass=ABCMeta):
    """
    Abstract resolver which transforms full model name into alias.
    To use him you need to overwrite transform_import function
    which should have one parameter. It will be full model name.
    It should return valid alias as str instance.
    """

    @abstractmethod
    def transform_import(self, module_path):  # type: (str) -> str
        pass

    def resolve_collisions(self, namespace):
        pass


class FullPathCR(PathBasedCR):
    """
    Collision resolver which transform full model name to alias by changing dots to underscores.
    He also removes 'models' part of alias, because all models are in models.py files.
    Model from last application in alphabetical order is selected.
    """  # noqa: E501

    def transform_import(self, module_path):
        pass


class AppNameCR(PathBasedCR, metaclass=ABCMeta):
    """
    Abstract collision resolver which transform pair (app name, model_name) to alias by changing dots to underscores.
    You must define MODIFICATION_STRING which should be string to format with two keyword arguments:
    app_name and model_name. For example: "{app_name}_{model_name}".
    Model from last application in alphabetical order is selected.
    """  # noqa: E501

    MODIFICATION_STRING = None  # type: Optional[str]

    def transform_import(self, module_path):
        pass


class AppNamePrefixCR(AppNameCR):
    """
    Collision resolver which transform pair (app name, model_name) to alias "{app_name}_{model_name}".
    Model from last application in alphabetical order is selected.
    Result is different than FullPathCR, when model has app_label other than current app.
    """  # noqa: E501

    MODIFICATION_STRING = "{app_name}_{model_name}"


class AppNameSuffixCR(AppNameCR):
    """
    Collision resolver which transform pair (app name, model_name) to alias "{model_name}_{app_name}"
    Model from last application in alphabetical order is selected.
    """  # noqa: E501

    MODIFICATION_STRING = "{model_name}_{app_name}"


class AppNamePrefixCustomOrderCR(AppNamePrefixCR, InstalledAppsOrderCR):
    """
    Collision resolver which is mixin of AppNamePrefixCR and InstalledAppsOrderCR.
    In case of collisions he sets aliases like AppNamePrefixCR, but sets default model using InstalledAppsOrderCR.
    """  # noqa: E501

    pass


class AppNameSuffixCustomOrderCR(AppNameSuffixCR, InstalledAppsOrderCR):
    """
    Collision resolver which is mixin of AppNameSuffixCR and InstalledAppsOrderCR.
    In case of collisions he sets aliases like AppNameSuffixCR, but sets default model using InstalledAppsOrderCR.
    """  # noqa: E501

    pass


class FullPathCustomOrderCR(FullPathCR, InstalledAppsOrderCR):
    """
    Collision resolver which is mixin of FullPathCR and InstalledAppsOrderCR.
    In case of collisions he sets aliases like FullPathCR, but sets default model using InstalledAppsOrderCR.
    """  # noqa: E501

    pass


class AppLabelCR(PathBasedCR, metaclass=ABCMeta):
    """
    Abstract collision resolver which transform pair (app_label, model_name) to alias.
    You must define MODIFICATION_STRING which should be string to format with two keyword arguments:
    app_label and model_name. For example: "{app_label}_{model_name}".
    This is different from AppNameCR when the app is nested with several level of namespace:
    Gives sites_Site instead of django_contrib_sites_Site
    Model from last application in alphabetical order is selected.
    """  # noqa: E501

    MODIFICATION_STRING = None  # type: Optional[str]

    def transform_import(self, module_path):
        pass


class AppLabelPrefixCR(AppLabelCR):
    """
    Collision resolver which transform pair (app_label, model_name) to alias "{app_label}_{model_name}".
    Model from last application in alphabetical order is selected.
    """  # noqa: E501

    MODIFICATION_STRING = "{app_label}_{model_name}"


class AppLabelSuffixCR(AppLabelCR):
    """
    Collision resolver which transform pair (app_label, model_name) to alias "{model_name}_{app_label}".
    Model from last application in alphabetical order is selected.
    """  # noqa: E501

    MODIFICATION_STRING = "{model_name}_{app_label}"


class CollisionResolvingRunner:
    def __init__(self):
        pass

    def run_collision_resolver(self, models_to_import):
        # type: (Dict[str, List[str]]) -> Dict[str, List[Tuple[str, str]]]
        pass

    @classmethod
    def _get_dictionary_of_names(cls, models_to_import):  # type: (Dict[str, List[str]]) -> (Dict[str, str])
        pass

    @classmethod
    def _assert_is_collision_resolver_result_correct(cls, result):
        pass

    @classmethod
    def _assert_is_collision_resolver_class_correct(cls, collision_resolver_class):
        pass

    @classmethod
    def _get_dictionary_of_modules(cls, dictionary_of_names):
        # type: (Dict[str, str]) -> Dict[str, List[Tuple[str, str]]]
        pass
