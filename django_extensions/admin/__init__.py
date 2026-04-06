#
# Autocomplete feature for admin panel
#
import operator
from functools import update_wrapper, reduce
from typing import Tuple, Dict, Callable  # NOQA

from django.apps import apps
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _
from django.utils.text import get_text_list
from django.contrib import admin

from django_extensions.admin.widgets import ForeignKeySearchInput


class ForeignKeyAutocompleteAdminMixin:
    """
    Admin class for models using the autocomplete feature.

    There are two additional fields:
       - related_search_fields: defines fields of managed model that
         have to be represented by autocomplete input, together with
         a list of target model fields that are searched for
         input string, e.g.:

         related_search_fields = {
            'author': ('first_name', 'email'),
         }

       - related_string_functions: contains optional functions which
         take target model instance as only argument and return string
         representation. By default __unicode__() method of target
         object is used.

    And also an optional additional field to set the limit on the
    results returned by the autocomplete query. You can set this integer
    value in your settings file using FOREIGNKEY_AUTOCOMPLETE_LIMIT or
    you can set this per ForeignKeyAutocompleteAdmin basis. If any value
    is set the results will not be limited.
    """

    related_search_fields = {}  # type: Dict[str, Tuple[str]]
    related_string_functions = {}  # type: Dict[str, Callable]
    autocomplete_limit = getattr(settings, "FOREIGNKEY_AUTOCOMPLETE_LIMIT", None)

    def get_urls(self):
        pass

    def foreignkey_autocomplete(self, request):
        """
        Search in the fields of the given related model and returns the
        result as a simple string to be used by the jQuery Autocomplete plugin
        """
        pass

    def get_related_filter(self, model, request):
        """
        Given a model class and current request return an optional Q object
        that should be applied as an additional filter for autocomplete query.
        If no additional filtering is needed, this method should return
        None.
        """
        pass

    def get_help_text(self, field_name, model_name):
        pass

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Override the default widget for Foreignkey fields if they are
        specified in the related_search_fields class attribute.
        """
        pass


class ForeignKeyAutocompleteAdmin(ForeignKeyAutocompleteAdminMixin, admin.ModelAdmin):
    pass


class ForeignKeyAutocompleteTabularInline(
    ForeignKeyAutocompleteAdminMixin, admin.TabularInline
):
    pass


class ForeignKeyAutocompleteStackedInline(
    ForeignKeyAutocompleteAdminMixin, admin.StackedInline
):
    pass
