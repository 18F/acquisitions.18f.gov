from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teammate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    slack = models.CharField(max_length=100, blank=True, null=True)
    read_only = models.BooleanField(default=False)
    role = models.ForeignKey(Role)

    def __str__(self):
        return self.name

    def is_teammate(self):
        return True

    def is_read_only(self):
        return self.read_only
