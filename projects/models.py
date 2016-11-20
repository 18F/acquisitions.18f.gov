from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


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
    public = models.BooleanField(
        default=False,
    )
    # TODO: should active status be determined by IAA status?
    active = models.BooleanField(
        default=True,
    )

    def is_private(self):
        return not self.public

    class Meta:
        permissions = (
            ('view_private', 'Can view non-public projects'),
        )


class Buy(models.Model):
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
    dollars = models.IntegerField(
        blank=False,
        null=True
    )
    public = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    def is_private(self):
        return not self.public

    def clean(self):
        if (not self.project.public == True) and (self.public == True):
            raise ValidationError({
                'public': 'May not be public if the associated project is not.'
            })
