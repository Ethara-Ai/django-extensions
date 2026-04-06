import re

from django.template import Library
from django.utils.encoding import force_str


register = Library()
re_widont = re.compile(r"\s+(\S+\s*)$")
re_widont_html = re.compile(
    r"([^<>\s])\s+([^<>\s]+\s*)(</?(?:address|blockquote|br|dd|div|dt|fieldset|form|h[1-6]|li|noscript|p|td|th)[^>]*>|$)",
    re.IGNORECASE,
)


@register.filter
def widont(value, count=1):
    """
    Add an HTML non-breaking space between the final two words of the string to
    avoid "widowed" words.

    Examples:

    >>> print(widont('Test   me   out'))
    Test   me&nbsp;out

    >>> print("'",widont('It works with trailing spaces too  '), "'")
    ' It works with trailing spaces&nbsp;too   '

    >>> print(widont('NoEffect'))
    NoEffect
    """
    pass


@register.filter
def widont_html(value):
    """
    Add an HTML non-breaking space between the final two words at the end of
    (and in sentences just outside of) block level tags to avoid "widowed"
    words.

    Examples:

    >>> print(widont_html('<h2>Here is a simple  example  </h2> <p>Single</p>'))
    <h2>Here is a simple&nbsp;example  </h2> <p>Single</p>

    >>> print(widont_html('<p>test me<br /> out</p><h2>Ok?</h2>Not in a p<p title="test me">and this</p>'))
    <p>test&nbsp;me<br /> out</p><h2>Ok?</h2>Not in a&nbsp;p<p title="test me">and&nbsp;this</p>

    >>> print(widont_html('leading text  <p>test me out</p>  trailing text'))
    leading&nbsp;text  <p>test me&nbsp;out</p>  trailing&nbsp;text
    """  # noqa: E501
    pass


if __name__ == "__main__":

    def _test():
        import doctest

        doctest.testmod()

    _test()
