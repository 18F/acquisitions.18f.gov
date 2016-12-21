import copy
from datetime import timedelta
from django.forms import widgets
from django import forms
from django.contrib.postgres.validators import (
    ArrayMaxLengthValidator, ArrayMinLengthValidator,
)
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class DurationMultiWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # Create duration options
        DURATIONS = (
            ('days', 'days'),
            ('weeks', 'weeks'),
        )
        _widgets = (
            widgets.NumberInput(attrs=attrs),
            widgets.Select(attrs=attrs, choices=DURATIONS),
        )
        super(DurationMultiWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(' ')
        else:
            return ''

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        length = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            if length[0] is not '':
                length = '{0} {1}'.format(length[0], length[1])
            else:
                raise ValueError
        except ValueError:
            return None
        else:
            return length
