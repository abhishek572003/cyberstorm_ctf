from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string into a list using the specified delimiter"""
    if value:
        return value.split(arg)
    return []

@register.filter
def index(sequence, position):
    """Get an item from a sequence by index"""
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return None 