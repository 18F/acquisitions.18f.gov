#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from projects.factories import ProjectFactory


class Command(BaseCommand):
    help = 'Create a team'

    def handle(self, *args, **options):
        ProjectFactory.create_batch(5)
