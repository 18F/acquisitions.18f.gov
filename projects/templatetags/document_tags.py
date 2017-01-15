from django import template

register = template.Library()


@register.filter
def has_document(obj, doc):
    return getattr(obj, doc)


@register.filter
def title_format(name):
    name = name.replace('_', ' ').title()
    # If length is very short, it's likely to be an acronym
    if len(name) <= 4:
        name = name.upper()
    return name
