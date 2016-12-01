#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission, ContentType
from projects.models import Project
from team.models import Teammate


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
        content_type = ContentType.objects.get_for_model(Project)
        group.permissions = [
            Permission.objects.get(
                codename='view_project',
                content_type=content_type,
            ),
        ]
        group.save()

        try:
            group = Group.objects.get(name='Teammates')
        except Group.DoesNotExist:
            group = Group(
                name='Teammates'
            )
            group.save()
        content_type = ContentType.objects.get_for_model(Teammate)
        group.permissions = [
            Permission.objects.get(
                codename='view_private',
                content_type=content_type,
            ),
        ]
        group.save()
