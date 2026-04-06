"""
The Django Admin Generator is a project which can automatically generate
(scaffold) a Django Admin for you. By doing this it will introspect your
models and automatically generate an Admin with properties like:

 - `list_display` for all local fields
 - `list_filter` for foreign keys with few items
 - `raw_id_fields` for foreign keys with a lot of items
 - `search_fields` for name and `slug` fields
 - `prepopulated_fields` for `slug` fields
 - `date_hierarchy` for `created_at`, `updated_at` or `joined_at` fields

The original source and latest version can be found here:
https://github.com/WoLpH/django-admin-generator/
"""

import re

from django.apps import apps
from django.conf import settings
from django.core.management.base import LabelCommand, CommandError
from django.db import models

from django_extensions.management.utils import signalcommand

# Configurable constants
MAX_LINE_WIDTH = getattr(settings, "MAX_LINE_WIDTH", 78)
INDENT_WIDTH = getattr(settings, "INDENT_WIDTH", 4)
LIST_FILTER_THRESHOLD = getattr(settings, "LIST_FILTER_THRESHOLD", 25)
RAW_ID_THRESHOLD = getattr(settings, "RAW_ID_THRESHOLD", 100)

LIST_FILTER = getattr(
    settings,
    "LIST_FILTER",
    (
        models.DateField,
        models.DateTimeField,
        models.ForeignKey,
        models.BooleanField,
    ),
)

SEARCH_FIELD_NAMES = getattr(
    settings,
    "SEARCH_FIELD_NAMES",
    (
        "name",
        "slug",
    ),
)

DATE_HIERARCHY_NAMES = getattr(
    settings,
    "DATE_HIERARCHY_NAMES",
    (
        "joined_at",
        "updated_at",
        "created_at",
    ),
)

PREPOPULATED_FIELD_NAMES = getattr(settings, "PREPOPULATED_FIELD_NAMES", ("slug=name",))

PRINT_IMPORTS = getattr(
    settings,
    "PRINT_IMPORTS",
    """# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import %(models)s
""",
)

PRINT_ADMIN_CLASS = getattr(
    settings,
    "PRINT_ADMIN_CLASS",
    """

@admin.register(%(name)s)
class %(name)sAdmin(admin.ModelAdmin):%(class_)s
""",
)

PRINT_ADMIN_PROPERTY = getattr(
    settings,
    "PRINT_ADMIN_PROPERTY",
    """
    %(key)s = %(value)s""",
)


class UnicodeMixin:
    """
    Mixin class to handle defining the proper __str__/__unicode__
    methods in Python 2 or 3.
    """

    def __str__(self):
        return self.__unicode__()


class AdminApp(UnicodeMixin):
    def __init__(self, app_config, model_res, **options):
        self.app_config = app_config
        self.model_res = model_res
        self.options = options

    def __iter__(self):
        for model in self.app_config.get_models():
            admin_model = AdminModel(model, **self.options)

            for model_re in self.model_res:
                if model_re.search(admin_model.name):
                    break
            else:
                if self.model_res:
                    continue

            yield admin_model

    def __unicode__(self):
        return "".join(self._unicode_generator())

    def _unicode_generator(self):
        pass

    def __repr__(self):
        return "<%s[%s]>" % (
            self.__class__.__name__,
            self.app.name,
        )


class AdminModel(UnicodeMixin):
    PRINTABLE_PROPERTIES = (
        "list_display",
        "list_filter",
        "raw_id_fields",
        "search_fields",
        "prepopulated_fields",
        "date_hierarchy",
    )

    def __init__(
        self,
        model,
        raw_id_threshold=RAW_ID_THRESHOLD,
        list_filter_threshold=LIST_FILTER_THRESHOLD,
        search_field_names=SEARCH_FIELD_NAMES,
        date_hierarchy_names=DATE_HIERARCHY_NAMES,
        prepopulated_field_names=PREPOPULATED_FIELD_NAMES,
        **options,
    ):
        self.model = model
        self.list_display = []
        self.list_filter = []
        self.raw_id_fields = []
        self.search_fields = []
        self.prepopulated_fields = {}
        self.date_hierarchy = None
        self.search_field_names = search_field_names
        self.raw_id_threshold = raw_id_threshold
        self.list_filter_threshold = list_filter_threshold
        self.date_hierarchy_names = date_hierarchy_names
        self.prepopulated_field_names = prepopulated_field_names

    def __repr__(self):
        return "<%s[%s]>" % (
            self.__class__.__name__,
            self.name,
        )

    @property
    def name(self):
        pass

    def _process_many_to_many(self, meta):
        pass

    def _process_fields(self, meta):
        pass

    def _process_foreign_key(self, field):
        pass

    def _process_field(self, field, parent_fields):
        pass

    def __unicode__(self):
        return "".join(self._unicode_generator())

    def _yield_value(self, key, value):
        pass

    def _yield_string(self, key, value, converter=repr):
        pass

    def _yield_dict(self, key, value):
        pass

    def _yield_tuple(self, key, value):
        pass

    def _unicode_generator(self):
        pass

    def _process(self):
        pass


class Command(LabelCommand):
    help = """Generate a `admin.py` file for the given app (models)"""
    # args = "[app_name]"
    can_import_settings = True

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass
