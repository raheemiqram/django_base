import re

import django
from django import template
from django.template.base import TextNode

register = template.Library()


class FormFieldNode(template.Node):
    """"
    Add the widget type to a BoundField. Until 3.1, Django did not make this available by default.

    Used by `oscar.templatetags.form_tags.annotate_form_field`
    """
    def __init__(self, field_str):
        self.field = template.Variable(field_str)

    def render(self, context):
        field = self.field.resolve(context)
        if not hasattr(field, 'widget_type') and hasattr(field, 'field'):
            field.widget_type = re.sub(r'widget$|input$', '', field.field.widget.__class__.__name__.lower())
        return ''


@register.tag
def annotate_form_field(parser, token):
    """
    Set an attribute on a form field with the widget type

    This means templates can use the widget type to render things differently
    if they want to. Until 3.1, Django did not make this available by default.
    """
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "annotate_form_field tag requires a form field to be passed")
    if django.VERSION < (3, 1):
        return FormFieldNode(args[1])
    return TextNode('')
