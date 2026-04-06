"""
modelviz.py - DOT file generator for Django Models

Based on:
  Django model to DOT (Graphviz) converter
  by Antonio Cavedoni <antonio@cavedoni.org>
  Adapted to be used with django-extensions
"""

import datetime
import os
import re

from django.apps import apps
from django.db.models import deletion
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    OneToOneField,
    RelatedField,
)
from django.db.models.fields.reverse_related import (
    OneToOneRel,
    ManyToOneRel,
)
from django.contrib.contenttypes.fields import GenericRelation
from django.template import Context, Template, loader
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.translation import activate as activate_language


__version__ = "1.1"
__license__ = "Python"
__author__ = ("Bas van Oostveen <v.oostveen@gmail.com>",)
__contributors__ = [
    "Antonio Cavedoni <https://cavedoni.com/>Stefano J. Attardi <https://attardi.org/>",
    "limodou",
    "Carlo C8E Miron",
    "Andre Campos <cahenan@gmail.com>",
    "Justin Findlay <jfindlay@gmail.com>",
    "Alexander Houben <alexander@houben.ch>",
    "Joern Hees <gitdev@joernhees.de>",
    "Kevin Cherepski <cherepski@gmail.com>",
    "Jose Tomas Tocino <theom3ga@gmail.com>",
    "Adam Dobrawy <naczelnik@jawnosc.tk>",
    "Mikkel Munch Mortensen <https://www.detfalskested.dk/>",
    "Andrzej Bistram <andrzej.bistram@gmail.com>",
    "Daniel Lipsitt <danlipsitt@gmail.com>",
    "Florian Anceau <flow.gunso@gmail.com>",
]


ON_DELETE_COLORS = {
    deletion.CASCADE: "red",
    deletion.PROTECT: "blue",
    deletion.SET_NULL: "orange",
    deletion.SET_DEFAULT: "green",
    deletion.SET: "yellow",
    deletion.DO_NOTHING: "grey",
    deletion.RESTRICT: "purple",
}


def parse_file_or_list(arg):
    pass


class ModelGraph:
    def __init__(self, app_labels, **kwargs):
        self.graphs = []
        self.cli_options = kwargs.get("cli_options", None)
        self.disable_fields = kwargs.get("disable_fields", False)
        self.disable_abstract_fields = kwargs.get("disable_abstract_fields", False)
        self.include_models = parse_file_or_list(kwargs.get("include_models", ""))
        self.all_applications = kwargs.get("all_applications", False)
        self.use_subgraph = kwargs.get("group_models", False)
        self.verbose_names = kwargs.get("verbose_names", False)
        self.inheritance = kwargs.get("inheritance", True)
        self.relations_as_fields = kwargs.get("relations_as_fields", True)
        self.relation_fields_only = kwargs.get("relation_fields_only", False)
        self.sort_fields = kwargs.get("sort_fields", True)
        self.language = kwargs.get("language", None)
        if self.language is not None:
            activate_language(self.language)
        self.exclude_columns = parse_file_or_list(kwargs.get("exclude_columns", ""))
        self.exclude_models = parse_file_or_list(kwargs.get("exclude_models", ""))
        self.hide_edge_labels = kwargs.get("hide_edge_labels", False)
        self.arrow_shape = kwargs.get("arrow_shape")
        self.color_code_deletions = kwargs.get("color_code_deletions", False)
        if self.all_applications:
            self.app_labels = [app.label for app in apps.get_app_configs()]
        else:
            self.app_labels = app_labels
        self.rankdir = kwargs.get("rankdir")
        self.display_field_choices = kwargs.get("display_field_choices", False)
        self.ordering = kwargs.get("ordering")

    def generate_graph_data(self):
        pass

    def get_graph_data(self, as_json=False):
        pass

    def add_attributes(self, field, abstract_fields):
        pass

    def add_relation(self, field, model, extras="", color=None):
        pass

    def get_abstract_models(self, appmodels):
        pass

    def get_app_context(self, app):
        pass

    def get_appmodel_attributes(self, appmodel):
        pass

    def get_appmodel_abstracts(self, appmodel):
        pass

    def get_appmodel_context(self, appmodel, appmodel_abstracts):
        pass

    def get_bases_abstract_fields(self, c):
        pass

    def get_inheritance_context(self, appmodel, parent):
        pass

    def get_models(self, app):
        pass

    def get_relation_context(self, target_model, field, label, extras):
        pass

    def process_attributes(self, field, model, pk, abstract_fields):
        pass

    def process_apps(self):
        pass

    def process_local_fields(self, field, model, abstract_fields):
        pass

    def process_local_many_to_many(self, field, model):
        pass

    def process_parent(self, parent, appmodel, model):
        pass

    def sort_model_fields(self, model):
        pass

    def use_model(self, model_name):
        """
        Decide whether to use a model, based on the model name and the lists of
        models to exclude and include.
        """
        pass

    def skip_field(self, field):
        pass


def generate_dot(graph_data, template="django_extensions/graph_models/digraph.dot"):
    pass


def generate_graph_data(*args, **kwargs):
    pass


def use_model(model, include_models, exclude_models):
    pass
