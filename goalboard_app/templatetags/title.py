from django import template

register = template.Library()


@register.simple_tag
def title(page_title=None):
    return f'{page_title} | Goalboard' if page_title else 'Goalboard'
