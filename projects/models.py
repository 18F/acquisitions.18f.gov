from __future__ import unicode_literals

from django.db import models
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
        default=date.today,
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
    active = models.BooleanField(
        default=True,
    )

    class Meta:
        permissions = (
            ('view_private', 'Can view non-public projects'),
        )
