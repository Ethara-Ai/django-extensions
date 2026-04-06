"""
Author Igor Támara igor@tamarapatino.org
Use this little program as you wish, if you
include it in your work, let others know you
are using it preserving this note, you have
the right to make derivative works, Use it
at your own risk.
Tested to work on(etch testing 13-08-2007):
  Python 2.4.4 (#2, Jul 17 2007, 11:56:54)
  [GCC 4.1.3 20070629 (prerelease) (Debian 4.1.2-13)] on linux2
"""

import codecs
import gzip
import re
import sys
from xml.dom.minidom import Node, parseString

dependclasses = ["User", "Group", "Permission", "Message"]

# Type dictionary translation types SQL -> Django
tsd = {
    "text": "TextField",
    "date": "DateField",
    "varchar": "CharField",
    "int": "IntegerField",
    "float": "FloatField",
    "serial": "AutoField",
    "boolean": "BooleanField",
    "numeric": "FloatField",
    "timestamp": "DateTimeField",
    "bigint": "IntegerField",
    "datetime": "DateTimeField",
    "time": "TimeField",
    "bool": "BooleanField",
}

# convert varchar -> CharField
v2c = re.compile(r"varchar\((\d+)\)")


def find_index(fks, id_):
    """
    Look for the id on fks, fks is an array of arrays, each array has on [1]
    the id of the class in a dia diagram.  When not present returns None, else
    it returns the position of the class with id on fks
    """
    pass


def addparentstofks(rels, fks):
    """
    Get a list of relations, between parents and sons and a dict of
    clases named in dia, and modifies the fks to add the parent as fk to get
    order on the output of classes and replaces the base class of the son, to
    put the class parent name.
    """
    pass


def dia2django(archivo):
    pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        dia2django(sys.argv[1])
    else:
        print(" Use:\n \n   " + sys.argv[0] + " diagram.dia\n\n")
