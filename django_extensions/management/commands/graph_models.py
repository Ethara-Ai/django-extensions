import sys
import json
import os
import tempfile
import fnmatch
from collections import OrderedDict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template import loader

from django_extensions.management.modelviz import ModelGraph, generate_dot
from django_extensions.management.utils import signalcommand

try:
    import pygraphviz

    HAS_PYGRAPHVIZ = True
except ImportError:
    HAS_PYGRAPHVIZ = False

try:
    try:
        import pydotplus as pydot
    except ImportError:
        import pydot
    HAS_PYDOT = True
except ImportError:
    HAS_PYDOT = False

DEFAULT_APP_STYLE_NAME = ".app-style.json"


def retheme(graph_data: dict, app_style_filename: str):
    pass


class Command(BaseCommand):
    help = "Creates a GraphViz dot file for the specified app names."
    " You can pass multiple app names and they will all be combined into a"
    " single model. Output is usually directed to a dot file."

    can_import_settings = True

    def __init__(self, *args, **kwargs):
        """
        Allow defaults for arguments to be set in settings.GRAPH_MODELS.

        Each argument in self.arguments is a dict where the key is the
        space-separated args and the value is our kwarg dict.

        The default from settings is keyed as the long arg name with '--'
        removed and any '-' replaced by '_'. For example, the default value for
        --disable-fields can be set in settings.GRAPH_MODELS['disable_fields'].
        """
        self.arguments = {
            "--app-style": {
                "action": "store",
                "help": "Path to style json to configure the style per app",
                "dest": "app-style",
                "default": "",
            },
            "--pygraphviz": {
                "action": "store_true",
                "default": False,
                "dest": "pygraphviz",
                "help": "Output graph data as image using PyGraphViz.",
            },
            "--pydot": {
                "action": "store_true",
                "default": False,
                "dest": "pydot",
                "help": "Output graph data as image using PyDot(Plus).",
            },
            "--dot": {
                "action": "store_true",
                "default": False,
                "dest": "dot",
                "help": (
                    "Output graph data as raw DOT (graph description language) "
                    "text data."
                ),
            },
            "--json": {
                "action": "store_true",
                "default": False,
                "dest": "json",
                "help": "Output graph data as JSON",
            },
            "--disable-fields -d": {
                "action": "store_true",
                "default": False,
                "dest": "disable_fields",
                "help": "Do not show the class member fields",
            },
            "--disable-abstract-fields": {
                "action": "store_true",
                "default": False,
                "dest": "disable_abstract_fields",
                "help": "Do not show the class member fields that were inherited",
            },
            "--display-field-choices": {
                "action": "store_true",
                "default": False,
                "dest": "display_field_choices",
                "help": "Display choices instead of field type",
            },
            "--group-models -g": {
                "action": "store_true",
                "default": False,
                "dest": "group_models",
                "help": "Group models together respective to their application",
            },
            "--all-applications -a": {
                "action": "store_true",
                "default": False,
                "dest": "all_applications",
                "help": "Automatically include all applications from INSTALLED_APPS",
            },
            "--output -o": {
                "action": "store",
                "dest": "outputfile",
                "help": (
                    "Render output file. Type of output dependend on file extensions. "
                    "Use png or jpg to render graph to image."
                ),
            },
            "--layout -l": {
                "action": "store",
                "dest": "layout",
                "default": "dot",
                "help": "Layout to be used by GraphViz for visualization. Layouts: "
                "circo dot fdp neato nop nop1 nop2 twopi",
            },
            "--theme -t": {
                "action": "store",
                "dest": "theme",
                "default": "django2018",
                "help": "Theme to use. Supplied are 'original' and 'django2018'. "
                "You can create your own by creating dot templates in "
                "'django_extentions/graph_models/themename/' template directory.",
            },
            "--verbose-names -n": {
                "action": "store_true",
                "default": False,
                "dest": "verbose_names",
                "help": "Use verbose_name of models and fields",
            },
            "--language -L": {
                "action": "store",
                "dest": "language",
                "help": "Specify language used for verbose_name localization",
            },
            "--exclude-columns -x": {
                "action": "store",
                "dest": "exclude_columns",
                "help": "Exclude specific column(s) from the graph. "
                "Can also load exclude list from file.",
            },
            "--exclude-models -X": {
                "action": "store",
                "dest": "exclude_models",
                "help": "Exclude specific model(s) from the graph. Can also load "
                "exclude list from file. Wildcards (*) are allowed.",
            },
            "--include-models -I": {
                "action": "store",
                "dest": "include_models",
                "help": "Restrict the graph to specified models. "
                "Wildcards (*) are allowed.",
            },
            "--inheritance -e": {
                "action": "store_true",
                "default": True,
                "dest": "inheritance",
                "help": "Include inheritance arrows (default)",
            },
            "--no-inheritance -E": {
                "action": "store_false",
                "default": False,
                "dest": "inheritance",
                "help": "Do not include inheritance arrows",
            },
            "--hide-relations-from-fields -R": {
                "action": "store_false",
                "default": True,
                "dest": "relations_as_fields",
                "help": "Do not show relations as fields in the graph.",
            },
            "--relation-fields-only": {
                "action": "store",
                "default": False,
                "dest": "relation_fields_only",
                "help": "Only display fields that are relevant for relations",
            },
            "--disable-sort-fields -S": {
                "action": "store_false",
                "default": True,
                "dest": "sort_fields",
                "help": "Do not sort fields",
            },
            "--hide-edge-labels": {
                "action": "store_true",
                "default": False,
                "dest": "hide_edge_labels",
                "help": "Do not show relations labels in the graph.",
            },
            "--arrow-shape": {
                "action": "store",
                "default": "dot",
                "dest": "arrow_shape",
                "choices": [
                    "box",
                    "crow",
                    "curve",
                    "icurve",
                    "diamond",
                    "dot",
                    "inv",
                    "none",
                    "normal",
                    "tee",
                    "vee",
                ],
                "help": "Arrow shape to use for relations. Default is dot. "
                "Available shapes: box, crow, curve, icurve, diamond, dot, inv, "
                "none, normal, tee, vee.",
            },
            "--color-code-deletions": {
                "action": "store_true",
                "default": False,
                "dest": "color_code_deletions",
                "help": "Color the relations according to their on_delete setting, "
                "where it is applicable. The colors are: red (CASCADE), "
                "orange (SET_NULL), green (SET_DEFAULT), yellow (SET), "
                "blue (PROTECT), grey (DO_NOTHING), and purple (RESTRICT).",
            },
            "--rankdir": {
                "action": "store",
                "default": "TB",
                "dest": "rankdir",
                "choices": ["TB", "BT", "LR", "RL"],
                "help": "Set direction of graph layout. Supported directions: "
                "TB, LR, BT and RL. Corresponding to directed graphs drawn from "
                "top to bottom, from left to right, from bottom to top, and from "
                "right to left, respectively. Default is TB.",
            },
            "--ordering": {
                "action": "store",
                "default": None,
                "dest": "ordering",
                "choices": ["in", "out"],
                "help": "Controls how the edges are arranged. Supported orderings: "
                '"in" (incoming relations first), "out" (outgoing relations first). '
                "Default is None.",
            },
        }

        defaults = getattr(settings, "GRAPH_MODELS", None)

        if defaults:
            for argument in self.arguments:
                arg_split = argument.split(" ")
                setting_opt = arg_split[0].lstrip("-").replace("-", "_")
                if setting_opt in defaults:
                    self.arguments[argument]["default"] = defaults[setting_opt]

        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        """Unpack self.arguments for parser.add_arguments."""
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass

    def print_output(self, dotdata, output_file=None):
        """Write model data to file or stdout in DOT (text) format."""
        pass

    def render_output_json(self, graph_data, output_file=None):
        """Write model data to file or stdout in JSON format."""
        pass

    def render_output_pygraphviz(self, dotdata, **kwargs):
        """Render model data as image using pygraphviz."""
        pass

    def render_output_pydot(self, dotdata, **kwargs):
        """Render model data as image using pydot."""
        pass
