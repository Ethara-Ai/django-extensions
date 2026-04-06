from django import template

register = template.Library()


class IndentByNode(template.Node):
    def __init__(self, nodelist, indent_level, if_statement):
        self.nodelist = nodelist
        self.indent_level = template.Variable(indent_level)
        if if_statement:
            self.if_statement = template.Variable(if_statement)
        else:
            self.if_statement = None

    def render(self, context):
        pass


@register.tag
def indentby(parser, token):
    """
    Add indentation to text between the tags by the given indentation level.

    {% indentby <indent_level> [if <statement>] %}
    ...
    {% endindentby %}

    Arguments:
      indent_level - Number of spaces to indent text with.
      statement - Only apply indent_level if the boolean statement evalutates to True.
    """
    pass
