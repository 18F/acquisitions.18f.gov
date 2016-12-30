from django import template

register = template.Library()


@register.filter
def has_document(obj, doc):
    return getattr(obj, doc)
