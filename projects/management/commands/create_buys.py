#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from projects.factories import AgileBPAFactory, AddAgileBPAFactory


class Command(BaseCommand):
    help = 'Create some buys'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a', '--add',
            action='store_true',
            default=False,
            help='Add to existing projects instead of creating new ones'
        )
        parser.add_argument(
            '-n', '--number',
            action='store',
            default=5,
            help='The number of buys to create'
        )

    def handle(self, *args, **options):
        number = int(options['number'])

        if options['add']:
            AddAgileBPAFactory.create_batch(number)
        else:
            AgileBPAFactory.create_batch(number)
