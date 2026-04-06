"""
JSONField automatically serializes most Python terms to JSON data.
Creates a TEXT field with a default value of "{}".  See test_json.py for
more information.

 from django.db import models
 from django_extensions.db.fields import json

 class LOL(models.Model):
     extra = json.JSONField()
"""

import datetime
from decimal import Decimal

import json
from django.conf import settings
from mongoengine.fields import StringField


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        pass


def dumps(value):
    pass


def loads(txt):
    pass


class JSONDict(dict):
    """
    Hack so repr() called by dumpdata will output JSON instead of
    Python formatted data.  This way fixtures will work!
    """

    def __repr__(self):
        return dumps(self)


class JSONField(StringField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly. Main object must be a dict object.
    """

    def __init__(self, *args, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = "{}"
        StringField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        pass

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""
        pass
