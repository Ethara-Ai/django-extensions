import urllib

from django import forms
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import Truncator


class ForeignKeySearchInput(ForeignKeyRawIdWidget):
    """
    Widget for displaying ForeignKeys in an autocomplete search input
    instead in a <select> box.
    """

    # Set in subclass to render the widget with a different template
    widget_template = None
    # Set this to the patch of the search view
    search_path = None

    @property
    def media(self):
        pass

    def label_for_value(self, value):
        pass

    def __init__(self, rel, search_fields, attrs=None):
        self.search_fields = search_fields
        super().__init__(rel, site, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        pass
