"""
      Title: Dumpscript management command
    Project: Hardytools (queryset-refactor version)
     Author: Will Hardy
       Date: June 2008
      Usage: python manage.py dumpscript appname > scripts/scriptname.py
  $Revision: 217 $

Description:
    Generates a Python script that will repopulate the database using objects.
    The advantage of this approach is that it is easy to understand, and more
    flexible than directly populating the database, or using XML.

    * It also allows for new defaults to take effect and only transfers what is
      needed.
    * If a new database schema has a NEW ATTRIBUTE, it is simply not
      populated (using a default value will make the transition smooth :)
    * If a new database schema REMOVES AN ATTRIBUTE, it is simply ignored
      and the data moves across safely (I'm assuming we don't want this
      attribute anymore.
    * Problems may only occur if there is a new model and is now a required
      ForeignKey for an existing model. But this is easy to fix by editing the
      populate script. Half of the job is already done as all ForeignKey
      lookups occur though the locate_object() function in the generated script.

Improvements:
    See TODOs and FIXMEs scattered throughout :-)

"""

import datetime
import sys

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import router
from django.db.models import (
    AutoField,
    BooleanField,
    DateField,
    DateTimeField,
    FileField,
    ForeignKey,
)
from django.db.models.deletion import Collector
from django.utils import timezone
from django.utils.encoding import force_str, smart_str

from django_extensions.management.utils import signalcommand


def orm_item_locator(orm_obj):
    """
    Is called every time an object that will not be exported is required.
    Where orm_obj is the referred object.
    We postpone the lookup to locate_object() which will be run on the generated script
    """
    pass


class Command(BaseCommand):
    help = "Dumps the data as a customised python script."

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, *args, **options):
        pass


def get_models(app_labels):
    """
    Get a list of models for the given app labels, with some exceptions.
    TODO: If a required model is referenced, it should also be included.
    Or at least discovered with a get_or_create() call.
    """
    pass


class Code:
    """
    A snippet of python script.
    This keeps track of import statements and can be output to a string.
    In the future, other features such as custom indentation might be included
    in this class.
    """

    def __init__(self, indent=-1, stdout=None, stderr=None):
        if not stdout:
            stdout = sys.stdout
        if not stderr:
            stderr = sys.stderr

        self.indent = indent
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        """Return a string representation of this script."""
        if self.imports:
            self.stderr.write(repr(self.import_lines))
            return flatten_blocks(
                [""] + self.import_lines + [""] + self.lines, num_indents=self.indent
            )
        else:
            return flatten_blocks(self.lines, num_indents=self.indent)

    def get_import_lines(self):
        """Take the stored imports and converts them to lines"""
        pass

    import_lines = property(get_import_lines)


class ModelCode(Code):
    """Produces a python script that can recreate data for a given model class."""

    def __init__(self, model, context=None, stdout=None, stderr=None, options=None):
        super().__init__(indent=0, stdout=stdout, stderr=stderr)
        self.model = model
        if context is None:
            context = {}
        self.context = context
        self.options = options
        self.instances = []

    def get_imports(self):
        """
        Return a dictionary of import statements, with the variable being
        defined as the key.
        """
        pass

    imports = property(get_imports)

    def get_lines(self):
        """
        Return a list of lists or strings, representing the code body.
        Each list is a block, each string is a statement.
        """
        pass

    lines = property(get_lines)


class InstanceCode(Code):
    """Produces a python script that can recreate data for a given model instance."""

    def __init__(
        self, instance, id, context=None, stdout=None, stderr=None, options=None
    ):
        """We need the instance in question and an id"""

        super().__init__(indent=0, stdout=stdout, stderr=stderr)
        self.imports = {}

        self.options = options
        self.instance = instance
        self.model = self.instance.__class__
        if context is None:
            context = {}
        self.context = context
        self.variable_name = "%s_%s" % (self.instance._meta.db_table, id)
        self.skip_me = None
        self.instantiated = False

        self.waiting_list = list(self.model._meta.fields)

        self.many_to_many_waiting_list = {}
        for field in self.model._meta.many_to_many:
            try:
                if not field.remote_field.through._meta.auto_created:
                    continue
            except AttributeError:
                pass
            self.many_to_many_waiting_list[field] = list(
                getattr(self.instance, field.name).all()
            )

    def get_lines(self, force=False):
        """
        Return a list of lists or strings, representing the code body.
        Each list is a block, each string is a statement.

        force (True or False): if an attribute object cannot be included,
        it is usually skipped to be processed later. With 'force' set, there
        will be no waiting: a get_or_create() call is written instead.
        """
        pass

    lines = property(get_lines)

    def skip(self):
        """
        Determine whether or not this object should be skipped.
        If this model instance is a parent of a single subclassed
        instance, skip it. The subclassed instance will create this
        parent instance for us.

        TODO: Allow the user to force its creation?
        """
        pass

    def instantiate(self):
        """Write lines for instantiation"""
        pass

    def get_waiting_list(self, force=False):
        """Add lines for any waiting fields that can be completed now."""
        pass

    def get_many_to_many_lines(self, force=False):
        """Generate lines that define many to many relations for this instance."""
        pass


class Script(Code):
    """Produces a complete python script that can recreate data for the given apps."""

    def __init__(self, models, context=None, stdout=None, stderr=None, options=None):
        super().__init__(stdout=stdout, stderr=stderr)
        self.imports = {}

        self.models = models
        if context is None:
            context = {}
        self.context = context

        self.context["__available_models"] = set(models)
        self.context["__extra_imports"] = {}

        self.options = options

    def _queue_models(self, models, context):
        """
        Work an an appropriate ordering for the models.
        This isn't essential, but makes the script look nicer because
        more instances can be defined on their first try.
        """
        pass

    def get_lines(self):
        """
        Return a list of lists or strings, representing the code body.
        Each list is a block, each string is a statement.
        """
        pass

    lines = property(get_lines)

    # A user-friendly file header
    FILE_HEADER = """

#!/usr/bin/env python


# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially cast so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones intact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# %s
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper:

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
    from dateutil.tz import tzoffset
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():

""" % " ".join(sys.argv)  # noqa: E501


# HELPER FUNCTIONS
# -------------------------------------------------------------------------------


def flatten_blocks(lines, num_indents=-1):
    """
    Take a list (block) or string (statement) and flattens it into a string
    with indentation.
    """
    pass


def get_attribute_value(item, field, context, force=False, skip_autofield=True):
    """Get a string version of the given attribute's value, like repr() might."""
    pass


def make_clean_dict(the_dict):
    pass


def check_dependencies(model, model_queue, avaliable_models):
    """Check that all the dependencies for this model are already in the queue."""
    pass


# EXCEPTIONS
# -------------------------------------------------------------------------------


class SkipValue(Exception):
    """Value could not be parsed or should simply be skipped."""


class DoLater(Exception):
    """Value could not be parsed or should simply be skipped."""


class StrToCodeChanger:
    def __init__(self, string):
        self.repr = string

    def __repr__(self):
        return self.repr
