#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from team.factories import TeammateFactory, RoleFactory


class Command(BaseCommand):
    help = 'Create a team'

    def handle(self, *args, **options):
        TeammateFactory.create_batch(5)
