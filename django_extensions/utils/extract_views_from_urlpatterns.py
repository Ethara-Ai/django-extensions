from django.core.exceptions import ViewDoesNotExist
from django.urls import URLPattern, URLResolver


def extract_views_from_urlpatterns(urlpatterns, base="", namespace=None):
    """
    Return a list of views from a list of urlpatterns.

    Each object in the returned list is a three-tuple: (view_func, regex, name)
    """
    pass


def describe_pattern(p):
    pass
