from django import template
from gowl.settings import RAND_VERSION

register = template.Library()


@register.simple_tag
def version():
    return RAND_VERSION
