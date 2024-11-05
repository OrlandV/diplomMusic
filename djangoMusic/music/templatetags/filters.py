from django import template

register = template.Library()


@register.filter
def islist(var):
    return isinstance(var, list)
