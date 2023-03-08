from django.template import Library

register = Library()


@register.filter
def remove_char(value, arg):
    return value.replace(arg, '')
