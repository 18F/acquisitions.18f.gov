#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from news.factories import NewsFactory


class Command(BaseCommand):
    help = 'Create some content'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--number',
            action='store',
            default=5,
            help='The amount of content to create'
        )

    def handle(self, *args, **options):
        number = int(options['number'])

        NewsFactory.create_batch(number)
