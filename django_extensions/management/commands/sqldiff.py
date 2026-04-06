"""
sqldiff.py - Prints the (approximated) difference between models and database

TODO:
 - better support for relations
 - better support for constraints (mainly postgresql?)
 - support for table spaces with postgresql
 - when a table is not managed (meta.managed==False) then only do a one-way
   sqldiff ? show differences from db->table but not the other way around since
   it's not managed.

KNOWN ISSUES:
 - MySQL has by far the most problems with introspection. Please be
   careful when using MySQL with sqldiff.
   - Booleans are reported back as Integers, so there's no way to know if
     there was a real change.
   - Varchar sizes are reported back without unicode support so their size
     may change in comparison to the real length of the varchar.
   - Some of the 'fixes' to counter these problems might create false
     positives or false negatives.
"""

import importlib
import sys
import argparse
from typing import Dict, Union, Callable, Optional  # NOQA
from django.apps import apps
from django.core.management import BaseCommand, CommandError
from django.core.management.base import OutputWrapper
from django.core.management.color import no_style
from django.db import connection, transaction, models
from django.db.models import UniqueConstraint
from django.db.models.fields import AutoField, IntegerField
from django.db.models.options import normalize_together

from django_extensions.management.utils import signalcommand

ORDERING_FIELD: IntegerField = IntegerField("_order", null=True)


def flatten(lst, ltypes=(list, tuple)):
    pass


def all_local_fields(meta):
    pass


class SQLDiff:
    DATA_TYPES_REVERSE_OVERRIDE = {}  # type: Dict[int, Union[str, Callable]]

    IGNORE_MISSING_TABLES = [
        "django_migrations",
    ]

    DIFF_TYPES = [
        "error",
        "comment",
        "table-missing-in-db",
        "table-missing-in-model",
        "field-missing-in-db",
        "field-missing-in-model",
        "fkey-missing-in-db",
        "fkey-missing-in-model",
        "index-missing-in-db",
        "index-missing-in-model",
        "unique-missing-in-db",
        "unique-missing-in-model",
        "field-type-differ",
        "field-parameter-differ",
        "notnull-differ",
    ]
    DIFF_TEXTS = {
        "error": "error: %(0)s",
        "comment": "comment: %(0)s",
        "table-missing-in-db": "table '%(0)s' missing in database",
        "table-missing-in-model": "table '%(0)s' missing in models",
        "field-missing-in-db": "field '%(1)s' defined in model but missing in database",
        "field-missing-in-model": "field '%(1)s' defined in database but missing in model",  # noqa: E501
        "fkey-missing-in-db": "field '%(1)s' FOREIGN KEY defined in model but missing in database",  # noqa: E501
        "fkey-missing-in-model": "field '%(1)s' FOREIGN KEY defined in database but missing in model",  # noqa: E501
        "index-missing-in-db": "field '%(1)s' INDEX named '%(2)s' defined in model but missing in database",  # noqa: E501
        "index-missing-in-model": "field '%(1)s' INDEX defined in database schema but missing in model",  # noqa: E501
        "unique-missing-in-db": "field '%(1)s' UNIQUE named '%(2)s' defined in model but missing in database",  # noqa: E501
        "unique-missing-in-model": "field '%(1)s' UNIQUE defined in database schema but missing in model",  # noqa: E501
        "field-type-differ": "field '%(1)s' not of same type: db='%(3)s', model='%(2)s'",  # noqa: E501
        "field-parameter-differ": "field '%(1)s' parameters differ: db='%(3)s', model='%(2)s'",  # noqa: E501
        "notnull-differ": "field '%(1)s' null constraint should be '%(2)s' in the database",  # noqa: E501
    }

    SQL_FIELD_MISSING_IN_DB = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("ADD COLUMN"),
            style.SQL_FIELD(qn(args[1])),
            " ".join(
                style.SQL_COLTYPE(a) if i == 0 else style.SQL_KEYWORD(a)
                for i, a in enumerate(args[2:])
            ),
        )
    )
    SQL_FIELD_MISSING_IN_MODEL = lambda self, style, qn, args: (
        "%s %s\n\t%s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("DROP COLUMN"),
            style.SQL_FIELD(qn(args[1])),
        )
    )
    SQL_FKEY_MISSING_IN_DB = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s %s %s (%s)%s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("ADD COLUMN"),
            style.SQL_FIELD(qn(args[1])),
            " ".join(
                style.SQL_COLTYPE(a) if i == 0 else style.SQL_KEYWORD(a)
                for i, a in enumerate(args[4:])
            ),
            style.SQL_KEYWORD("REFERENCES"),
            style.SQL_TABLE(qn(args[2])),
            style.SQL_FIELD(qn(args[3])),
            connection.ops.deferrable_sql(),
        )
    )
    SQL_INDEX_MISSING_IN_DB = lambda self, style, qn, args: (
        "%s %s\n\t%s %s (%s%s);"
        % (
            style.SQL_KEYWORD("CREATE INDEX"),
            style.SQL_TABLE(qn(args[2])),
            # style.SQL_TABLE(qn("%s" % '_'.join('_'.join(a) if isinstance(a, (list, tuple)) else a for a in args[0:3] if a))),  # noqa: E501
            style.SQL_KEYWORD("ON"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_FIELD(", ".join(qn(e) for e in args[1])),
            style.SQL_KEYWORD(args[3]),
        )
    )
    SQL_INDEX_MISSING_IN_MODEL = lambda self, style, qn, args: (
        "%s %s;"
        % (
            style.SQL_KEYWORD("DROP INDEX"),
            style.SQL_TABLE(qn(args[1])),
        )
    )
    SQL_UNIQUE_MISSING_IN_DB = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s (%s);"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("ADD CONSTRAINT"),
            style.SQL_TABLE(qn(args[2])),
            style.SQL_KEYWORD("UNIQUE"),
            style.SQL_FIELD(", ".join(qn(e) for e in args[1])),
        )
    )
    SQL_UNIQUE_MISSING_IN_MODEL = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("DROP"),
            style.SQL_KEYWORD("CONSTRAINT"),
            style.SQL_TABLE(qn(args[1])),
        )
    )
    SQL_FIELD_TYPE_DIFFER = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("MODIFY"),
            style.SQL_FIELD(qn(args[1])),
            style.SQL_COLTYPE(args[2]),
        )
    )
    SQL_FIELD_PARAMETER_DIFFER = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("MODIFY"),
            style.SQL_FIELD(qn(args[1])),
            style.SQL_COLTYPE(args[2]),
        )
    )
    SQL_NOTNULL_DIFFER = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("MODIFY"),
            style.SQL_FIELD(qn(args[1])),
            style.SQL_KEYWORD(args[2]),
            style.SQL_KEYWORD("NOT NULL"),
        )
    )
    SQL_ERROR = lambda self, style, qn, args: style.NOTICE(
        "-- Error: %s" % style.ERROR(args[0])
    )
    SQL_COMMENT = lambda self, style, qn, args: style.NOTICE(
        "-- Comment: %s" % style.SQL_TABLE(args[0])
    )
    SQL_TABLE_MISSING_IN_DB = lambda self, style, qn, args: style.NOTICE(
        "-- Table missing: %s" % args[0]
    )
    SQL_TABLE_MISSING_IN_MODEL = lambda self, style, qn, args: style.NOTICE(
        "-- Model missing for table: %s" % args[0]
    )

    can_detect_notnull_differ = False
    can_detect_unsigned_differ = False
    unsigned_suffix = None  # type: Optional[str]

    def __init__(self, app_models, options, stdout, stderr):
        self.has_differences = None
        self.app_models = app_models
        self.options = options
        self.dense = options["dense_output"]
        self.stdout = stdout
        self.stderr = stderr

        self.introspection = connection.introspection

        self.differences = []
        self.unknown_db_fields = {}
        self.new_db_fields = set()
        self.null = {}
        self.unsigned = set()

        self.DIFF_SQL = {
            "error": self.SQL_ERROR,
            "comment": self.SQL_COMMENT,
            "table-missing-in-db": self.SQL_TABLE_MISSING_IN_DB,
            "table-missing-in-model": self.SQL_TABLE_MISSING_IN_MODEL,
            "field-missing-in-db": self.SQL_FIELD_MISSING_IN_DB,
            "field-missing-in-model": self.SQL_FIELD_MISSING_IN_MODEL,
            "fkey-missing-in-db": self.SQL_FKEY_MISSING_IN_DB,
            "fkey-missing-in-model": self.SQL_FIELD_MISSING_IN_MODEL,
            "index-missing-in-db": self.SQL_INDEX_MISSING_IN_DB,
            "index-missing-in-model": self.SQL_INDEX_MISSING_IN_MODEL,
            "unique-missing-in-db": self.SQL_UNIQUE_MISSING_IN_DB,
            "unique-missing-in-model": self.SQL_UNIQUE_MISSING_IN_MODEL,
            "field-type-differ": self.SQL_FIELD_TYPE_DIFFER,
            "field-parameter-differ": self.SQL_FIELD_PARAMETER_DIFFER,
            "notnull-differ": self.SQL_NOTNULL_DIFFER,
        }

    def load(self):
        pass

    def load_null(self):
        raise NotImplementedError(
            (
                "load_null functions must be implemented if diff backend has "
                "'can_detect_notnull_differ' set to True"
            )
        )

    def load_unsigned(self):
        raise NotImplementedError(
            (
                "load_unsigned function must be implemented if diff backend has "
                "'can_detect_unsigned_differ' set to True"
            )
        )

    def add_app_model_marker(self, app_label, model_name):
        pass

    def add_difference(self, diff_type, *args):
        pass

    def get_data_types_reverse_override(self):
        # type: () -> Dict[int, Union[str, Callable]]
        pass

    def format_field_names(self, field_names):
        pass

    def sql_to_dict(self, query, param):
        """
        Execute query and return a dict

        sql_to_dict(query, param) -> list of dicts

        code from snippet at https://www.djangosnippets.org/snippets/1383/
        """
        pass

    def get_field_model_type(self, field):
        pass

    def get_field_db_type_kwargs(
        self,
        current_kwargs,
        description,
        field=None,
        table_name=None,
        reverse_type=None,
    ):
        pass

    def get_field_db_type(self, description, field=None, table_name=None):
        # DB-API cursor.description
        #   (name, type_code, display_size, internal_size, precision, scale, null_ok)
        pass

    def get_field_db_type_lookup(self, type_code):
        pass

    def get_field_class(self, class_path):
        pass

    def get_field_db_nullable(self, field, table_name):
        pass

    def strip_parameters(self, field_type):
        pass

    def get_index_together(self, meta):
        pass

    def get_unique_together(self, meta):
        pass

    def expand_together(self, together, meta):
        pass

    def find_unique_missing_in_db(
        self, meta, table_indexes, table_constraints, table_name, skip_list=None
    ):
        pass

    def find_unique_missing_in_model(
        self, meta, table_indexes, table_constraints, table_name
    ):
        pass

    def find_index_missing_in_db(
        self, meta, table_indexes, table_constraints, table_name
    ):
        pass

    def find_index_missing_in_model(
        self, meta, table_indexes, table_constraints, table_name
    ):
        pass

    def find_field_missing_in_model(self, fieldmap, table_description, table_name):
        pass

    def find_field_missing_in_db(self, fieldmap, table_description, table_name):
        pass

    def find_field_type_differ(self, meta, table_description, table_name, func=None):
        pass

    def find_field_parameter_differ(
        self, meta, table_description, table_name, func=None
    ):
        pass

    def find_field_notnull_differ(self, meta, table_description, table_name):
        pass

    def get_constraints(self, cursor, table_name, introspection):
        pass

    def find_differences(self):
        pass

    def print_diff(self, style=no_style()):
        """Print differences to stdout"""
        pass

    def print_diff_text(self, style):
        pass

    def print_diff_sql(self, style):
        pass


class GenericSQLDiff(SQLDiff):
    can_detect_notnull_differ = False
    can_detect_unsigned_differ = False

    def load_null(self):
        pass

    def load_unsigned(self):
        pass


class MySQLDiff(SQLDiff):
    can_detect_notnull_differ = True
    can_detect_unsigned_differ = True
    unsigned_suffix = "UNSIGNED"

    def load(self):
        pass

    def format_field_names(self, field_names):
        pass

    def load_null(self):
        pass

    def load_unsigned(self):
        pass

    def load_auto_increment(self):
        pass

    # All the MySQL hacks together create something of a problem
    # Fixing one bug in MySQL creates another issue. So just keep in mind
    # that this is way unreliable for MySQL atm.
    def get_field_db_type(self, description, field=None, table_name=None):
        pass

    def find_index_missing_in_model(
        self, meta, table_indexes, table_constraints, table_name
    ):
        pass

    def find_unique_missing_in_db(
        self, meta, table_indexes, table_constraints, table_name, skip_list=None
    ):
        pass


class SqliteSQLDiff(SQLDiff):
    can_detect_notnull_differ = True
    can_detect_unsigned_differ = False

    def load_null(self):
        pass

    def load_unsigned(self):
        pass

    # Unique does not seem to be implied on Sqlite for Primary_key's
    # if this is more generic among databases this might be useful
    # to add to the superclass's find_unique_missing_in_db method
    def find_unique_missing_in_db(
        self, meta, table_indexes, table_constraints, table_name, skip_list=None
    ):
        pass

    # Finding Indexes by using the get_indexes dictionary doesn't seem to work
    # for sqlite.
    def find_index_missing_in_db(
        self, meta, table_indexes, table_constraints, table_name
    ):
        pass

    def find_index_missing_in_model(
        self, meta, table_indexes, table_constraints, table_name
    ):
        pass

    def get_field_db_type(self, description, field=None, table_name=None):
        pass


class PostgresqlSQLDiff(SQLDiff):
    can_detect_notnull_differ = True
    can_detect_unsigned_differ = True

    DATA_TYPES_REVERSE_NAME = {
        "hstore": "django.contrib.postgres.fields.HStoreField",
        "jsonb": "django.contrib.postgres.fields.JSONField",
    }

    # Hopefully in the future we can add constraint checking and other more
    # advanced checks based on this database.
    SQL_LOAD_CONSTRAINTS = """
        SELECT nspname, relname, conname, attname, pg_get_constraintdef(pg_constraint.oid)
        FROM pg_constraint
        INNER JOIN pg_attribute ON pg_constraint.conrelid = pg_attribute.attrelid AND pg_attribute.attnum = any(pg_constraint.conkey)
        INNER JOIN pg_class ON conrelid=pg_class.oid
        INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
        ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END,contype,nspname,relname,conname;
    """  # noqa: E501
    SQL_LOAD_NULL = """
        SELECT nspname, relname, attname, attnotnull
        FROM pg_attribute
        INNER JOIN pg_class ON attrelid=pg_class.oid
        INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace;
    """

    SQL_FIELD_TYPE_DIFFER = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("ALTER"),
            style.SQL_FIELD(qn(args[1])),
            style.SQL_KEYWORD("TYPE"),
            style.SQL_COLTYPE(args[2]),
        )
    )
    SQL_FIELD_PARAMETER_DIFFER = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("ALTER"),
            style.SQL_FIELD(qn(args[1])),
            style.SQL_KEYWORD("TYPE"),
            style.SQL_COLTYPE(args[2]),
        )
    )
    SQL_NOTNULL_DIFFER = lambda self, style, qn, args: (
        "%s %s\n\t%s %s %s %s;"
        % (
            style.SQL_KEYWORD("ALTER TABLE"),
            style.SQL_TABLE(qn(args[0])),
            style.SQL_KEYWORD("ALTER COLUMN"),
            style.SQL_FIELD(qn(args[1])),
            style.SQL_KEYWORD(args[2]),
            style.SQL_KEYWORD("NOT NULL"),
        )
    )

    def load(self):
        pass

    def load_null(self):
        pass

    def load_unsigned(self):
        # PostgreSQL does not support unsigned, so no columns are
        # unsigned. Nothing to do.
        pass

    def load_constraints(self):
        pass

    def get_data_type_arrayfield(self, base_field):
        pass

    def get_data_types_reverse_override(self):
        pass

    def get_constraints(self, cursor, table_name, introspection):
        """
        Find constraints for table

        Backport of django's introspection.get_constraints(...)
        """
        pass

    # def get_field_db_type_kwargs(
    #   self, current_kwargs, description, field=None,
    #   table_name=None, reverse_type=None,
    # ):
    #     kwargs = {}
    #     if field and 'base_field' in current_kwargs:
    #         # find
    #         attname = field.db_column or field.attname
    #         introspect_db_type = self.sql_to_dict(
    #             """SELECT attname, format_type(atttypid, atttypmod) AS type
    #                 FROM   pg_attribute
    #                 WHERE  attrelid = %s::regclass
    #                 AND    attname = %s
    #                 AND    attnum > 0
    #                 AND    NOT attisdropped
    #                 ORDER  BY attnum;
    #             """,
    #             (table_name, attname)
    #         )[0]['type']
    #         # TODO: this gives the concrete type that the database uses, why not use
    #         #       this much earlier in the process to compare to whatever django
    #         #       spits out as the database type ?
    #         max_length = re.search(
    #             "character varying\((\d+)\)\[\]", introspect_db_type
    #         )
    #         if max_length:
    #             kwargs['max_length'] = max_length[1]
    #     return kwargs

    def get_field_db_type(self, description, field=None, table_name=None):
        pass

    def get_field_db_type_lookup(self, type_code):
        pass

    """
    def find_field_type_differ(self, meta, table_description, table_name):
        def callback(field, description, model_type, db_type):
            if field.primary_key and db_type=='integer':
                db_type = 'serial'
            return model_type, db_type
        super().find_field_type_differ(meta, table_description, table_name, callback)
    """


DATABASE_SQLDIFF_CLASSES = {
    "postgis": PostgresqlSQLDiff,
    "postgresql_psycopg2": PostgresqlSQLDiff,
    "postgresql": PostgresqlSQLDiff,
    "mysql": MySQLDiff,
    "sqlite3": SqliteSQLDiff,
    "oracle": GenericSQLDiff,
}


class Command(BaseCommand):
    help = """Prints the (approximated) difference between models and fields in the database for the given app name(s).

It indicates how columns in the database are different from the sql that would
be generated by Django. This command is not a database migration tool. (Though
it can certainly help) It's purpose is to show the current differences as a way
to check/debug ur models compared to the real database tables and columns."""  # noqa: E501

    output_transaction = False

    def add_arguments(self, parser):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exit_code = 1

    @signalcommand
    def handle(self, *args, **options):
        pass

    def execute(self, *args, **options):
        pass

    def run_from_argv(self, argv):
        pass
