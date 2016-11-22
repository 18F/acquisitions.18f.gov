from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta


# Create your models here.
class IAA(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        blank=False,
        null=False,
    )
    client = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    signed_on = models.DateField(
        blank=True,
        null=True,
    )
    expires_on = models.DateField(
        blank=True,
        null=True,
    )
    dollars = models.IntegerField(
        blank=True,
        null=True,
    )
    color_of_money = models.CharField(
        choices=(
            ('No-Year Money', 'No-Year Money'),
            ('1-Year Money', '1-Year Money'),
            ('2-Year Money', '2-Year Money'),
        ),
        max_length=100,
        blank=True,
        null=True,
    ),
    authority = models.CharField(
        choices=(
            ('ASF', 'Alternating Services Fund'),
            ('Economy', 'Economy Act'),
        ),
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{0} | {1}".format(self.client, self.id)

    def is_signed(self):
        return self.signed_on != null

    def clean(self):
        if self.signed_on > date.today():
            raise ValidationError({
                'signed_on': 'Date may not be in the future.'
            })


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    iaa = models.ForeignKey(
        IAA,
        on_delete=models.SET_NULL,
        blank=False,
        # TODO: should null=False?
        null=True,
    )
    project_type = models.CharField(
        choices=(
            ('Internal Buy', 'Internal Buy'),
            ('External Buy', 'External Buy'),
            ('Consulting', 'Consulting'),
        ),
        max_length=100,
        blank=False,
        null=False,
    )
    dollars = models.IntegerField(
        blank=True,
        null=True,
    )
    public = models.BooleanField(
        default=False,
    )
    # TODO: should active status be determined by IAA status?
    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return "/projects/{0}/".format(self.id)

    def is_private(self):
        return not self.public

    def clean(self):
        if self.dollars:
            if self.dollars > self.iaa.dollars:
                raise ValidationError({
                    'dollars': 'Value can\'t exceed value of authorizing IAA'
                })

    class Meta:
        permissions = (
            ('view_private', 'Can view non-public projects'),
        )


class Buy(models.Model):
    PROCUREMENT_METHOD_CHOICES = (
        ('Agile BPA', 'Agile BPA'),
        ('Micro-Purchase', 'Micro-Purchase'),
    )

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    project = models.ForeignKey(
        Project,
        related_name='buys',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    dollars = models.PositiveIntegerField(
        blank=False,
        null=True
    )
    public = models.BooleanField(
        default=False,
    )
    base_period_length = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    option_periods = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
    )
    option_period_length = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    procurement_method = models.CharField(
        max_length=200,
        choices=PROCUREMENT_METHOD_CHOICES,
        default="To Be Determined",
        blank=False,
        null=False,
    )

    def __str__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return "/buys/{0}/".format(self.id)

    def is_private(self):
        return not self.public

    def _get_time_from_string(self, length):
        amount, units = length.split(' ')
        amount = int(amount)
        if units == 'days':
            duration = timedelta(days=amount)
        elif units == 'weeks':
            duration = timedelta(weeks=amount)
        else:
            raise ValueError('Couldn\'t parse input length')
        return duration

    def period_of_performance(self):
        # TODO: Come back and see if this makes sense
        # The goal of this is to turn our string-based period of performance
        # into something that can be manipulated and displayed in different
        # ways. But for now, the strings are what's needed for templating
        # and such.
        base = self._get_time_from_string(self.base_period_length)
        option = self._get_time_from_string(self.option_period_length)
        return base + (self.option_periods * option)

    def clean(self):
        # Check that buy is not public without associated project being public
        if (self.project.public is not True) and (self.public is True):
            raise ValidationError({
                'public': 'May not be public if the associated project is not.'
            })

        # Confirm option period existence if option period length is set
        if (self.option_period_length) and (self.option_periods == 0):
            raise ValidationError({
                'option_period_length': 'The number of option periods must be '
                'greater than 0 to set a length'
            })

        if self.dollars:
            if self.dollars > self.project.dollars:
                raise ValidationError({
                    'dollars': 'Value can\'t exceed value of overall project'
                })
