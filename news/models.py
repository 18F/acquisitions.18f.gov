from datetime import datetime
from dateutil.tz import tzlocal
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        null=True,
    )
    authors = models.ManyToManyField(
        User,
        blank=False,
    )
    content = models.TextField(
        blank=False,
        null=False,
    )
    publication_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    draft = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return "{0} | {1}".format(self.title, self.publication_date)

    def get_absolute_url(self):
        return reverse('news:post', args=[self.slug])

    def clean(self):
        if self.draft and self.publication_date is not None:
            raise ValidationError({
                'publication_date': 'Drafts may not have a publication date'
            })
        if not self.draft and self.publication_date is None:
            raise ValidationError({
                'publication_date': 'Please set a publication date'
            })

    class Meta:
        pass
