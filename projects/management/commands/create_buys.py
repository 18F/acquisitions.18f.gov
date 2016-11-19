#! /usr/bin/env python3
from django.core.management.base import BaseCommand, CommandError
from projects.factories import BuyFactory, AddBuyFactory


class Command(BaseCommand):
    help = 'Create some buys'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a', '--add',
            action='store_true',
            default=False,
            help='Add to existing projects instead of creating new ones'
        )

    def handle(self, *args, **options):
        if options['add']:
            AddBuyFactory.create_batch(5)
        else:
            BuyFactory.create_batch(5)
