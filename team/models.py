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
    role = models.ForeignKey(Role)
    photo = models.ImageField(
        upload_to='/team/photos',
        default='/team/photos/default.png'
        )

    def __str__(self):
        return self.name

    def is_teammate(self):
        return True
