"""
JSONField automatically serializes most Python terms to JSON data.
Creates a TEXT field with a default value of "{}".  See test_json.py for
more information.

 from django.db import models
 from django_extensions.db.fields import json

 class LOL(models.Model):
     extra = json.JSONField()
"""

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import expressions


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


class JSONList(list):
    """
    Hack so repr() called by dumpdata will output JSON instead of
    Python formatted data.  This way fixtures will work!
    """

    def __repr__(self):
        return dumps(self)


class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.  Main thingy must be a dict object.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = kwargs.get("default", dict)
        models.TextField.__init__(self, *args, **kwargs)

    def get_default(self):
        pass

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        pass

    def get_prep_value(self, value):
        pass

    def from_db_value(self, value, expression, connection):  # type: ignore
        pass

    def get_db_prep_save(self, value, connection, **kwargs):
        """Convert our JSON object to a string before we save"""
        pass

    def deconstruct(self):
        pass
