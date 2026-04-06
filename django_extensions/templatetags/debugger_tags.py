"""
Make debugging Django templates easier.

Example:

    {% load debugger_tags %}

    {{ object|ipdb }}

"""

from django import template


register = template.Library()


@register.filter
def ipdb(obj):  # pragma: no cover
    """Interactive Python debugger filter."""
    pass


@register.filter
def pdb(obj):
    """Python debugger filter."""
    pass


@register.filter
def wdb(obj):  # pragma: no cover
    """Web debugger filter."""
    pass
