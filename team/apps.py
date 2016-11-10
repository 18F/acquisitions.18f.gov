from __future__ import unicode_literals

from django.apps import AppConfig


class TeamConfig(AppConfig):
    name = 'team'

    def ready(self):
        from team import signals
