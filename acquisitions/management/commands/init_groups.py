#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from projects.models import Project


class Command(BaseCommand):
    help = 'Initialize groups'

    def handle(self, *args, **options):
        try:
            group = Group.objects.get(name='NDA Signed')
        except Group.DoesNotExist:
            group = Group(
                name='NDA Signed'
            )
            group.save()
        group.permissions = [
            Permission.objects.get(codename='view_private'),
            Permission.objects.get(codename='add_iaa'),
            Permission.objects.get(codename='change_iaa'),
            Permission.objects.get(codename='add_project'),
            Permission.objects.get(codename='change_project')
        ]
        group.save()
