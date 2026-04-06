"""
MongoDB model fields emulating Django Extensions' additional model fields

These fields are essentially identical to existing Extensions fields.
"""

import re
import datetime
from django import forms
from django.db.models.constants import LOOKUP_SEP
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from mongoengine.fields import StringField, DateTimeField

import uuid


class SlugField(StringField):
    description = _("String (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = kwargs.get("max_length", 50)
        # Set db_index=True unless it's been set manually.
        if "db_index" not in kwargs:
            kwargs["db_index"] = True
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        pass

    def formfield(self, **kwargs):
        pass


class AutoSlugField(SlugField):
    """
    AutoSlugField, adapted for MongoDB

    By default, sets editable=False, blank=True.

    Required arguments:

    populate_from
        Specifies which field or list of fields the slug is populated from.

    Optional arguments:

    separator
        Defines the used separator (default: '-')

    overwrite
        If set to True, overwrites the slug on every save (default: False)

    Inspired by SmileyChris' Unique Slugify snippet:
    https://www.djangosnippets.org/snippets/690/
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("editable", False)

        populate_from = kwargs.pop("populate_from", None)
        if populate_from is None:
            raise ValueError("missing 'populate_from' argument")
        else:
            self._populate_from = populate_from

        self.slugify_function = kwargs.pop("slugify_function", slugify)
        self.separator = kwargs.pop("separator", str("-"))
        self.overwrite = kwargs.pop("overwrite", False)
        super().__init__(*args, **kwargs)

    def _slug_strip(self, value):
        """
        Clean up a slug by removing slug separator characters that occur at
        the beginning or end of a slug.

        If an alternate separator is used, it will also replace any instances
        of the default '-' separator with the new separator.
        """
        pass

    def slugify_func(self, content):
        pass

    def create_slug(self, model_instance, add):
        # get fields to populate from and slug field to set
        pass

    def get_slug_fields(self, model_instance, lookup_value):
        pass

    def pre_save(self, model_instance, add):
        pass

    def get_internal_type(self):
        pass


class CreationDateTimeField(DateTimeField):
    """
    CreationDateTimeField

    By default, sets editable=False, blank=True, default=datetime.now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", datetime.datetime.now)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        pass


class ModificationDateTimeField(CreationDateTimeField):
    """
    ModificationDateTimeField

    By default, sets editable=False, blank=True, default=datetime.now

    Sets value to datetime.now() on each save of the model.
    """

    def pre_save(self, model, add):
        pass

    def get_internal_type(self):
        pass


class UUIDVersionError(Exception):
    pass


class UUIDField(StringField):
    """
    UUIDField

    By default uses UUID version 1 (generate from host ID, sequence number and current time)

    The field support all uuid versions which are natively supported by the uuid python module.
    For more information see: https://docs.python.org/lib/module-uuid.html
    """  # noqa: E501

    def __init__(
        self,
        verbose_name=None,
        name=None,
        auto=True,
        version=1,
        node=None,
        clock_seq=None,
        namespace=None,
        **kwargs,
    ):
        kwargs["max_length"] = 36
        self.auto = auto
        self.version = version
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        StringField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        pass

    def contribute_to_class(self, cls, name):
        pass

    def create_uuid(self):
        pass

    def pre_save(self, model_instance, add):
        pass
