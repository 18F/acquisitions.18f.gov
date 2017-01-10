from django import template

register = template.Library()


@register.filter
def has_document(obj, doc):
    return getattr(obj, doc)


@register.filter
def title_format(word):
    return word.replace('_', ' ').capitalize()
