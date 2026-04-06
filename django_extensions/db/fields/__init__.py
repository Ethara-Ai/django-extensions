"""
Django Extensions additional model fields

Some fields might require additional dependencies to be installed.
"""

import re
import string

try:
    import uuid

    HAS_UUID = True
except ImportError:
    HAS_UUID = False

try:
    import shortuuid

    HAS_SHORT_UUID = True
except ImportError:
    HAS_SHORT_UUID = False

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import DateTimeField, CharField, SlugField, Q, UniqueConstraint
from django.db.models.constants import LOOKUP_SEP
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str


MAX_UNIQUE_QUERY_ATTEMPTS = getattr(
    settings, "EXTENSIONS_MAX_UNIQUE_QUERY_ATTEMPTS", 100
)


class UniqueFieldMixin:
    def check_is_bool(self, attrname):
        pass

    @staticmethod
    def _get_fields(model_cls):
        pass

    def get_queryset(self, model_cls, slug_field):
        pass

    def find_unique(self, model_instance, field, iterator, *args):
        # exclude the current model instance from the queryset used in finding
        # next valid hash
        pass


class AutoSlugField(UniqueFieldMixin, SlugField):
    """
    AutoSlugField

    By default, sets editable=False, blank=True.

    Required arguments:

    populate_from
        Specifies which field, list of fields, or model method
        the slug will be populated from.

        populate_from can traverse a ForeignKey relationship
        by using Django ORM syntax:
            populate_from = 'related_model__field'

    Optional arguments:

    separator
        Defines the used separator (default: '-')

    overwrite
        If set to True, overwrites the slug on every save (default: False)

    slugify_function
        Defines the function which will be used to "slugify" a content
        (default: :py:func:`~django.template.defaultfilters.slugify` )

    It is possible to provide custom "slugify" function with
    the ``slugify_function`` function in a model class.

    ``slugify_function`` function in a model class takes priority over
    ``slugify_function`` given as an argument to :py:class:`~AutoSlugField`.

    Example

    .. code-block:: python

        # models.py

        from django.db import models

        from django_extensions.db.fields import AutoSlugField


        class MyModel(models.Model):
            def slugify_function(self, content):
                return content.replace('_', '-').lower()

            title = models.CharField(max_length=42)
            slug = AutoSlugField(populate_from='title')

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

        if not callable(populate_from):
            if not isinstance(populate_from, (list, tuple)):
                populate_from = (populate_from,)

            if not all(isinstance(e, str) for e in populate_from):
                raise TypeError(
                    "'populate_from' must be str or list[str] or tuple[str], found `%s`"
                    % populate_from
                )

        self.slugify_function = kwargs.pop("slugify_function", slugify)
        self.separator = kwargs.pop("separator", "-")
        self.overwrite = kwargs.pop("overwrite", False)
        self.check_is_bool("overwrite")
        self.overwrite_on_add = kwargs.pop("overwrite_on_add", True)
        self.check_is_bool("overwrite_on_add")
        self.allow_duplicates = kwargs.pop("allow_duplicates", False)
        self.check_is_bool("allow_duplicates")
        self.max_unique_query_attempts = kwargs.pop(
            "max_unique_query_attempts", MAX_UNIQUE_QUERY_ATTEMPTS
        )
        super().__init__(*args, **kwargs)

    def _slug_strip(self, value):
        """
        Clean up a slug by removing slug separator characters that occur at
        the beginning or end of a slug.

        If an alternate separator is used, it will also replace any instances
        of the default '-' separator with the new separator.
        """
        pass

    @staticmethod
    def slugify_func(content, slugify_function):
        pass

    def slug_generator(self, original_slug, start):
        pass

    def create_slug(self, model_instance, add):
        pass

    def get_slug_fields(self, model_instance, lookup_value):
        pass

    def pre_save(self, model_instance, add):
        pass

    def get_internal_type(self):
        pass

    def deconstruct(self):
        pass


class RandomCharField(UniqueFieldMixin, CharField):
    """
    RandomCharField

    By default, sets editable=False, blank=True, unique=False.

    Required arguments:

    length
        Specifies the length of the field

    Optional arguments:

    unique
        If set to True, duplicate entries are not allowed (default: False)

    lowercase
        If set to True, lowercase the alpha characters (default: False)

    uppercase
        If set to True, uppercase the alpha characters (default: False)

    include_alpha
        If set to True, include alpha characters (default: True)

    include_digits
        If set to True, include digit characters (default: True)

    include_punctuation
        If set to True, include punctuation characters (default: False)

    keep_default
        If set to True, keeps the default initialization value (default: False)
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("editable", False)

        self.length = kwargs.pop("length", None)
        if self.length is None:
            raise ValueError("missing 'length' argument")
        kwargs["max_length"] = self.length

        self.lowercase = kwargs.pop("lowercase", False)
        self.check_is_bool("lowercase")
        self.uppercase = kwargs.pop("uppercase", False)
        self.check_is_bool("uppercase")
        if self.uppercase and self.lowercase:
            raise ValueError(
                "the 'lowercase' and 'uppercase' arguments are mutually exclusive"
            )
        self.include_digits = kwargs.pop("include_digits", True)
        self.check_is_bool("include_digits")
        self.include_alpha = kwargs.pop("include_alpha", True)
        self.check_is_bool("include_alpha")
        self.include_punctuation = kwargs.pop("include_punctuation", False)
        self.keep_default = kwargs.pop("keep_default", False)
        self.check_is_bool("include_punctuation")
        self.max_unique_query_attempts = kwargs.pop(
            "max_unique_query_attempts", MAX_UNIQUE_QUERY_ATTEMPTS
        )

        # Set unique=False unless it's been set manually.
        if "unique" not in kwargs:
            kwargs["unique"] = False

        super().__init__(*args, **kwargs)

    def random_char_generator(self, chars):
        pass

    def in_unique_together(self, model_instance):
        pass

    def pre_save(self, model_instance, add):
        pass

    def internal_type(self):
        pass

    def deconstruct(self):
        pass


class CreationDateTimeField(DateTimeField):
    """
    CreationDateTimeField

    By default, sets editable=False, blank=True, auto_now_add=True
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("auto_now_add", True)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        pass

    def deconstruct(self):
        pass


class ModificationDateTimeField(CreationDateTimeField):
    """
    ModificationDateTimeField

    By default, sets editable=False, blank=True, auto_now=True

    Sets value to now every time the object is saved.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("auto_now", True)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        pass

    def deconstruct(self):
        pass

    def pre_save(self, model_instance, add):
        pass


class UUIDVersionError(Exception):
    pass


class UUIDFieldMixin:
    """
    UUIDFieldMixin

    By default uses UUID version 4 (randomly generated UUID).

    The field support all uuid versions which are natively supported by the uuid python module, except version 2.
    For more information see: https://docs.python.org/lib/module-uuid.html
    """  # noqa: E501

    DEFAULT_MAX_LENGTH = 36

    def __init__(
        self,
        verbose_name=None,
        name=None,
        auto=True,
        version=4,
        node=None,
        clock_seq=None,
        namespace=None,
        uuid_name=None,
        *args,
        **kwargs,
    ):
        if not HAS_UUID:
            raise ImproperlyConfigured(
                "'uuid' module is required for UUIDField. "
                "(Do you have Python 2.5 or higher installed ?)"
            )

        kwargs.setdefault("max_length", self.DEFAULT_MAX_LENGTH)

        if auto:
            self.empty_strings_allowed = False
            kwargs["blank"] = True
            kwargs.setdefault("editable", False)

        self.auto = auto
        self.version = version
        self.node = node
        self.clock_seq = clock_seq
        self.namespace = namespace
        self.uuid_name = uuid_name or name

        super().__init__(verbose_name=verbose_name, *args, **kwargs)

    def create_uuid(self):
        pass

    def pre_save(self, model_instance, add):
        pass

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        pass

    def deconstruct(self):
        pass


class ShortUUIDField(UUIDFieldMixin, CharField):
    """
    ShortUUIDField

    Generates concise (22 characters instead of 36), unambiguous, URL-safe UUIDs.

    Based on `shortuuid`: https://github.com/stochastic-technologies/shortuuid
    """

    DEFAULT_MAX_LENGTH = 22

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not HAS_SHORT_UUID:
            raise ImproperlyConfigured(
                "'shortuuid' module is required for ShortUUIDField. "
                "(Do you have Python 2.5 or higher installed ?)"
            )
        kwargs.setdefault("max_length", self.DEFAULT_MAX_LENGTH)

    def create_uuid(self):
        pass
